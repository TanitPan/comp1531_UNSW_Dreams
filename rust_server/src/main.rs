use std::{
    collections::{HashMap, HashSet},
    fs,
    net::SocketAddr,
    path::Path,
    sync::{Arc, Mutex},
};

use axum::{
    extract::{Query, State},
    http::StatusCode,
    response::IntoResponse,
    routing::{delete, get, post},
    Json, Router,
};
use chrono::Utc;
use serde::{Deserialize, Serialize};
use uuid::Uuid;

const STORE_PATH: &str = "data/store.json";

#[derive(Debug, Clone)]
struct AppState {
    store: Arc<Mutex<Store>>,
}

#[derive(Debug, Default, Serialize, Deserialize)]
struct Store {
    users: HashMap<u64, User>,
    email_to_user: HashMap<String, u64>,
    sessions: HashMap<String, u64>,
    channels: HashMap<u64, Channel>,
    messages: HashMap<u64, Vec<Message>>,
    next_user_id: u64,
    next_channel_id: u64,
    next_message_id: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct User {
    email: String,
    password: String,
    name_first: String,
    name_last: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct Channel {
    name: String,
    is_public: bool,
    members: HashSet<u64>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct Message {
    message_id: u64,
    u_id: u64,
    message: String,
    time_sent: i64,
}

#[derive(Debug, Serialize)]
struct ErrorResponse {
    error: String,
}

#[derive(Debug)]
struct ApiError {
    status: StatusCode,
    message: String,
}

impl ApiError {
    fn bad_request(message: impl Into<String>) -> Self {
        Self {
            status: StatusCode::BAD_REQUEST,
            message: message.into(),
        }
    }

    fn access_error(message: impl Into<String>) -> Self {
        Self {
            status: StatusCode::FORBIDDEN,
            message: message.into(),
        }
    }
}

impl IntoResponse for ApiError {
    fn into_response(self) -> axum::response::Response {
        (
            self.status,
            Json(ErrorResponse {
                error: self.message,
            }),
        )
            .into_response()
    }
}

#[derive(Debug, Deserialize)]
struct RegisterReq {
    email: String,
    password: String,
    name_first: String,
    name_last: String,
}

#[derive(Debug, Serialize)]
struct AuthResp {
    token: String,
    auth_user_id: u64,
}

#[derive(Debug, Deserialize)]
struct LoginReq {
    email: String,
    password: String,
}

#[derive(Debug, Deserialize)]
struct LogoutReq {
    token: String,
}

#[derive(Debug, Serialize)]
struct LogoutResp {
    is_success: bool,
}

#[derive(Debug, Deserialize)]
struct CreateChannelReq {
    token: String,
    name: String,
    is_public: bool,
}

#[derive(Debug, Serialize)]
struct CreateChannelResp {
    channel_id: u64,
}

#[derive(Debug, Deserialize)]
struct JoinChannelReq {
    token: String,
    channel_id: u64,
}

#[derive(Debug, Serialize)]
struct ChannelSummary {
    channel_id: u64,
    name: String,
}

#[derive(Debug, Serialize)]
struct ChannelsListResp {
    channels: Vec<ChannelSummary>,
}

#[derive(Debug, Serialize)]
struct ChannelDetailsResp {
    name: String,
    is_public: bool,
    member_ids: Vec<u64>,
}

#[derive(Debug, Deserialize)]
struct TokenQuery {
    token: String,
}

#[derive(Debug, Deserialize)]
struct ChannelDetailsQuery {
    token: String,
    channel_id: u64,
}

#[derive(Debug, Deserialize)]
struct SendMessageReq {
    token: String,
    channel_id: u64,
    message: String,
}

#[derive(Debug, Serialize)]
struct SendMessageResp {
    message_id: u64,
}

#[derive(Debug, Deserialize)]
struct ChannelMessagesQuery {
    token: String,
    channel_id: u64,
    start: usize,
}

#[derive(Debug, Serialize)]
struct ChannelMessagesResp {
    messages: Vec<Message>,
    start: usize,
    end: isize,
}

#[derive(Debug, Deserialize)]
struct EchoQuery {
    echo: String,
}

#[derive(Debug, Serialize)]
struct EchoResp {
    echo: String,
}

#[tokio::main]
async fn main() {
    let state = AppState {
        store: Arc::new(Mutex::new(load_store())),
    };

    let app = Router::new()
        .route("/", get(root))
        .route("/echo", get(echo))
        .route("/clear/v1", delete(clear))
        .route("/auth/register/v2", post(auth_register))
        .route("/auth/login/v2", post(auth_login))
        .route("/auth/logout/v1", post(auth_logout))
        .route("/channels/create/v2", post(channels_create))
        .route("/channels/list/v2", get(channels_list))
        .route("/channels/listall/v2", get(channels_listall))
        .route("/channel/join/v2", post(channel_join))
        .route("/channel/details/v2", get(channel_details))
        .route("/message/send/v1", post(message_send))
        .route("/channel/messages/v2", get(channel_messages))
        .with_state(state);

    let addr: SocketAddr = "0.0.0.0:8080".parse().unwrap();
    println!("dreams-rs running on {addr}");
    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

async fn root() -> Json<serde_json::Value> {
    Json(serde_json::json!({"status": "ok", "service": "dreams-rs"}))
}

async fn echo(Query(query): Query<EchoQuery>) -> Result<Json<EchoResp>, ApiError> {
    if query.echo == "echo" {
        return Err(ApiError::bad_request("Cannot echo 'echo'"));
    }
    Ok(Json(EchoResp { echo: query.echo }))
}

async fn clear(State(state): State<AppState>) -> StatusCode {
    let mut store = state.store.lock().unwrap();
    *store = Store::default();
    persist_store(&store);
    StatusCode::OK
}

async fn auth_register(
    State(state): State<AppState>,
    Json(req): Json<RegisterReq>,
) -> Result<Json<AuthResp>, ApiError> {
    if req.email.is_empty() || req.password.len() < 6 {
        return Err(ApiError::bad_request("Invalid email or password"));
    }

    let mut store = state.store.lock().unwrap();
    if store.email_to_user.contains_key(&req.email) {
        return Err(ApiError::bad_request("Email already in use"));
    }

    store.next_user_id += 1;
    let user_id = store.next_user_id;
    let token = Uuid::new_v4().to_string();

    store.users.insert(
        user_id,
        User {
            email: req.email.clone(),
            password: req.password,
            name_first: req.name_first,
            name_last: req.name_last,
        },
    );
    store.email_to_user.insert(req.email, user_id);
    store.sessions.insert(token.clone(), user_id);
    persist_store(&store);

    Ok(Json(AuthResp {
        token,
        auth_user_id: user_id,
    }))
}

async fn auth_login(
    State(state): State<AppState>,
    Json(req): Json<LoginReq>,
) -> Result<Json<AuthResp>, ApiError> {
    let mut store = state.store.lock().unwrap();
    let user_id = *store
        .email_to_user
        .get(&req.email)
        .ok_or_else(|| ApiError::bad_request("Email does not exist"))?;

    let user = store
        .users
        .get(&user_id)
        .ok_or_else(|| ApiError::bad_request("User missing"))?;
    if user.password != req.password {
        return Err(ApiError::bad_request("Incorrect password"));
    }

    let token = Uuid::new_v4().to_string();
    store.sessions.insert(token.clone(), user_id);
    persist_store(&store);

    Ok(Json(AuthResp {
        token,
        auth_user_id: user_id,
    }))
}

async fn auth_logout(
    State(state): State<AppState>,
    Json(req): Json<LogoutReq>,
) -> Json<LogoutResp> {
    let mut store = state.store.lock().unwrap();
    let removed = store.sessions.remove(&req.token).is_some();
    persist_store(&store);
    Json(LogoutResp {
        is_success: removed,
    })
}

async fn channels_create(
    State(state): State<AppState>,
    Json(req): Json<CreateChannelReq>,
) -> Result<Json<CreateChannelResp>, ApiError> {
    if req.name.is_empty() || req.name.len() > 20 {
        return Err(ApiError::bad_request("Channel name must be 1..20 chars"));
    }

    let mut store = state.store.lock().unwrap();
    let user_id = auth_user_id(&store, &req.token)?;

    store.next_channel_id += 1;
    let channel_id = store.next_channel_id;

    let mut members = HashSet::new();
    members.insert(user_id);

    store.channels.insert(
        channel_id,
        Channel {
            name: req.name,
            is_public: req.is_public,
            members,
        },
    );
    persist_store(&store);

    Ok(Json(CreateChannelResp { channel_id }))
}

async fn channels_list(
    State(state): State<AppState>,
    Query(query): Query<TokenQuery>,
) -> Result<Json<ChannelsListResp>, ApiError> {
    let store = state.store.lock().unwrap();
    let user_id = auth_user_id(&store, &query.token)?;

    let channels = store
        .channels
        .iter()
        .filter_map(|(channel_id, channel)| {
            if channel.members.contains(&user_id) {
                Some(ChannelSummary {
                    channel_id: *channel_id,
                    name: channel.name.clone(),
                })
            } else {
                None
            }
        })
        .collect();

    Ok(Json(ChannelsListResp { channels }))
}

async fn channels_listall(
    State(state): State<AppState>,
    Query(query): Query<TokenQuery>,
) -> Result<Json<ChannelsListResp>, ApiError> {
    let store = state.store.lock().unwrap();
    auth_user_id(&store, &query.token)?;

    let channels = store
        .channels
        .iter()
        .map(|(channel_id, channel)| ChannelSummary {
            channel_id: *channel_id,
            name: channel.name.clone(),
        })
        .collect();

    Ok(Json(ChannelsListResp { channels }))
}

async fn channel_join(
    State(state): State<AppState>,
    Json(req): Json<JoinChannelReq>,
) -> Result<StatusCode, ApiError> {
    let mut store = state.store.lock().unwrap();
    let user_id = auth_user_id(&store, &req.token)?;

    let channel = store
        .channels
        .get_mut(&req.channel_id)
        .ok_or_else(|| ApiError::bad_request("Channel not found"))?;

    if !channel.is_public {
        return Err(ApiError::access_error("Cannot join private channel"));
    }

    channel.members.insert(user_id);
    persist_store(&store);
    Ok(StatusCode::OK)
}

async fn channel_details(
    State(state): State<AppState>,
    Query(query): Query<ChannelDetailsQuery>,
) -> Result<Json<ChannelDetailsResp>, ApiError> {
    let store = state.store.lock().unwrap();
    let user_id = auth_user_id(&store, &query.token)?;

    let channel = store
        .channels
        .get(&query.channel_id)
        .ok_or_else(|| ApiError::bad_request("Channel not found"))?;

    if !channel.members.contains(&user_id) {
        return Err(ApiError::access_error("User is not a channel member"));
    }

    let mut member_ids: Vec<u64> = channel.members.iter().copied().collect();
    member_ids.sort_unstable();

    Ok(Json(ChannelDetailsResp {
        name: channel.name.clone(),
        is_public: channel.is_public,
        member_ids,
    }))
}

async fn message_send(
    State(state): State<AppState>,
    Json(req): Json<SendMessageReq>,
) -> Result<Json<SendMessageResp>, ApiError> {
    if req.message.is_empty() || req.message.len() > 1000 {
        return Err(ApiError::bad_request("Message must be 1..1000 chars"));
    }

    let mut store = state.store.lock().unwrap();
    let user_id = auth_user_id(&store, &req.token)?;

    let channel = store
        .channels
        .get(&req.channel_id)
        .ok_or_else(|| ApiError::bad_request("Channel not found"))?;
    if !channel.members.contains(&user_id) {
        return Err(ApiError::access_error("User is not a channel member"));
    }

    store.next_message_id += 1;
    let message_id = store.next_message_id;

    let message = Message {
        message_id,
        u_id: user_id,
        message: req.message,
        time_sent: Utc::now().timestamp(),
    };

    store
        .messages
        .entry(req.channel_id)
        .or_default()
        .insert(0, message);
    persist_store(&store);

    Ok(Json(SendMessageResp { message_id }))
}

async fn channel_messages(
    State(state): State<AppState>,
    Query(query): Query<ChannelMessagesQuery>,
) -> Result<Json<ChannelMessagesResp>, ApiError> {
    let store = state.store.lock().unwrap();
    let user_id = auth_user_id(&store, &query.token)?;

    let channel = store
        .channels
        .get(&query.channel_id)
        .ok_or_else(|| ApiError::bad_request("Channel not found"))?;

    if !channel.members.contains(&user_id) {
        return Err(ApiError::access_error("User is not a channel member"));
    }

    let all_messages = store
        .messages
        .get(&query.channel_id)
        .cloned()
        .unwrap_or_default();
    if query.start > all_messages.len() {
        return Err(ApiError::bad_request("Start out of bounds"));
    }

    let end_index = (query.start + 50).min(all_messages.len());
    let end = if end_index == all_messages.len() {
        -1
    } else {
        end_index as isize
    };

    Ok(Json(ChannelMessagesResp {
        messages: all_messages[query.start..end_index].to_vec(),
        start: query.start,
        end,
    }))
}

fn auth_user_id(store: &Store, token: &str) -> Result<u64, ApiError> {
    store
        .sessions
        .get(token)
        .copied()
        .ok_or_else(|| ApiError::access_error("Invalid token"))
}

fn load_store() -> Store {
    match fs::read_to_string(STORE_PATH) {
        Ok(contents) => serde_json::from_str::<Store>(&contents).unwrap_or_default(),
        Err(_) => Store::default(),
    }
}

fn persist_store(store: &Store) {
    if let Some(parent) = Path::new(STORE_PATH).parent() {
        let _ = fs::create_dir_all(parent);
    }

    if let Ok(serialized) = serde_json::to_string_pretty(store) {
        let _ = fs::write(STORE_PATH, serialized);
    }
}
