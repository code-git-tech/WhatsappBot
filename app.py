# app.py
import os
import json
import sqlite3
import requests
from flask import Flask, request, jsonify, Response
from dotenv import load_dotenv

load_dotenv()
ACCESS_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "verify_token_example")
WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "+15557667459")
BOT_FLOW_FILE = os.getenv("BOT_FLOW_FILE", "dooper_bot.json")

GRAPH_API_VERSION = "v18.0"  # Latest stable version for consistency

DB = "bot_state.db"
BOT_JSON = BOT_FLOW_FILE

# Validate required environment variables
if not ACCESS_TOKEN:
    print("❌ ERROR: WHATSAPP_TOKEN not found in environment variables")
if not PHONE_NUMBER_ID:
    print("❌ ERROR: WHATSAPP_PHONE_NUMBER_ID not found in environment variables")

print(f"🤖 Bot initialized with:")
print(f"   📱 WhatsApp Number: {WHATSAPP_NUMBER}")
print(f"   📋 Bot Flow File: {BOT_JSON}")
print(f"   🔧 Phone Number ID: {PHONE_NUMBER_ID}")
print(f"   🔑 Has Access Token: {'Yes' if ACCESS_TOKEN and ACCESS_TOKEN != 'your_access_token_here' else 'No - Update .env file'}")

app = Flask(__name__)

# ----- DB helpers with fallback -----
# In-memory storage as fallback
memory_storage = {}

def init_db():
    try:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS user_state (
                        user_id TEXT PRIMARY KEY,
                        node_key TEXT,
                        data TEXT
                    )""")
        conn.commit()
        conn.close()
        print("✅ SQLite database initialized successfully")
        return True
    except Exception as e:
        print(f"⚠️ SQLite failed, using in-memory storage: {e}")
        return False

# Global flag to track if SQLite is available
use_sqlite = True

def get_state(user_id):
    global use_sqlite
    
    if use_sqlite:
        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            c.execute("SELECT node_key, data FROM user_state WHERE user_id=?", (user_id,))
            row = c.fetchone()
            conn.close()
            if row:
                node_key, data = row
                return node_key, json.loads(data) if data else {}
            return None, {}
        except Exception as e:
            print(f"⚠️ SQLite error, switching to memory storage: {e}")
            use_sqlite = False
    
    # Fallback to in-memory storage
    if user_id in memory_storage:
        state = memory_storage[user_id]
        return state.get('node_key'), state.get('data', {})
    return None, {}

def set_state(user_id, node_key, data=None):
    global use_sqlite
    
    if use_sqlite:
        try:
            data_json = json.dumps(data or {})
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            c.execute("""INSERT INTO user_state(user_id, node_key, data) VALUES(?,?,?)
                         ON CONFLICT(user_id) DO UPDATE SET node_key=excluded.node_key, data=excluded.data""",
                      (user_id, node_key, data_json))
            conn.commit()
            conn.close()
            return
        except Exception as e:
            print(f"⚠️ SQLite error, switching to memory storage: {e}")
            use_sqlite = False
    
    # Fallback to in-memory storage
    memory_storage[user_id] = {
        'node_key': node_key,
        'data': data or {}
    }

# ----- Load bot flow -----
try:
    with open(BOT_JSON, "r", encoding="utf-8") as f:
        bot_flow = json.load(f)
    print(f"✅ Bot flow loaded successfully from {BOT_JSON}")
except FileNotFoundError:
    print(f"❌ ERROR: Bot flow file {BOT_JSON} not found")
    bot_flow = {"operators": {}}
except json.JSONDecodeError as e:
    print(f"❌ ERROR: Invalid JSON in {BOT_JSON}: {e}")
    bot_flow = {"operators": {}}

# map: node_key -> properties, and also title -> node_key
operators = bot_flow.get("operators", {})
title_to_key = {}
for k, v in operators.items():
    props = v.get("properties", {})
    title = props.get("title", "")
    if title:
        title_to_key[title.lower()] = k

def find_start_node():
    # try 'start' or 'start2' or fallback to first operator
    for t in ("start","start2"):
        if t in title_to_key:
            return title_to_key[t]
    # fallback first operator
    return next(iter(operators.keys()))

def get_node(node_key):
    return operators.get(node_key, {}).get("properties", {})

# ----- Send message via Meta Cloud API -----
def send_whatsapp_text(to, text):
    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    r = requests.post(url, headers=headers, json=payload)
    try:
        r.raise_for_status()
    except Exception as e:
        print("Failed to send message:", r.status_code, r.text)
    return r.json()

# ----- Simple matching: by number or by exact answer text -----
def match_output(node_props, incoming_text):
    outputs = node_props.get("outputs") or {}
    # enumerate outputs to allow numeric choice
    answers = [out.get("answer","") for key,out in outputs.items()]
    # check numeric choice like "1" "2"
    if incoming_text.strip().isdigit():
        idx = int(incoming_text.strip()) - 1
        if 0 <= idx < len(answers):
            return answers[idx]
    # exact case-insensitive match
    for ans in answers:
        if ans and incoming_text.strip().lower() == ans.strip().lower():
            return ans
    # partial match (starts with)
    for ans in answers:
        if ans and ans.lower().startswith(incoming_text.strip().lower()):
            return ans
    return None

# ----- Conversation handler -----
def handle_user_message(user_id, text):
    node_key, data = get_state(user_id)
    if not node_key:
        node_key = find_start_node()
        set_state(user_id, node_key, {})  # initialize
        node = get_node(node_key)
        # send the question and list numbered options if any
        question = node.get("question", "")
        outputs = node.get("outputs") or {}
        if outputs:
            options_text = "\n".join(f"{i+1}. {o.get('answer','')}" for i,o in enumerate(outputs.values()))
            send_whatsapp_text(user_id, f"{question}\n\n{options_text}")
        else:
            send_whatsapp_text(user_id, question)
        return

    node = get_node(node_key)
    # if node expects a form, you should handle sequential fields (left as improvement)
    matched_answer = match_output(node, text)
    if matched_answer:
        # Advance — default: go to followup.nodeName
        followup = node.get("followup") or {}
        next_node_title = followup.get("nodeName", "") or None
        if next_node_title:
            # find node_key by title (user might have titles as "Greeting" etc.)
            next_key = title_to_key.get(next_node_title.lower())
            if next_key:
                set_state(user_id, next_key, data)
                next_node = get_node(next_key)
                q = next_node.get("question","")
                outputs = next_node.get("outputs") or {}
                if outputs:
                    options_text = "\n".join(f"{i+1}. {o.get('answer','')}" for i,o in enumerate(outputs.values()))
                    send_whatsapp_text(user_id, f"{q}\n\n{options_text}")
                else:
                    send_whatsapp_text(user_id, q or "Done.")
                return
        # fallback: try to find a node whose title equals matched_answer
        fallback_key = title_to_key.get(matched_answer.lower())
        if fallback_key:
            set_state(user_id, fallback_key, data)
            next_node = get_node(fallback_key)
            q = next_node.get("question","")
            outputs = next_node.get("outputs") or {}
            if outputs:
                options_text = "\n".join(f"{i+1}. {o.get('answer','')}" for i,o in enumerate(outputs.values()))
                send_whatsapp_text(user_id, f"{q}\n\n{options_text}")
            else:
                send_whatsapp_text(user_id, q or "Done.")
            return

        # if nothing else, acknowledge and stay
        send_whatsapp_text(user_id, f"Got it: {matched_answer}. (No followup configured.)")
        return

    # If no match, re-prompt the same node
    q = node.get("question","Sorry I didn't understand.")
    outputs = node.get("outputs") or {}
    if outputs:
        options_text = "\n".join(f"{i+1}. {o.get('answer','')}" for i,o in enumerate(outputs.values()))
        send_whatsapp_text(user_id, f"Sorry, I didn't get that. {q}\n\n{options_text}")
    else:
        send_whatsapp_text(user_id, "Sorry, I didn't understand. " + q)

# ----- Webhook endpoints -----
@app.route("/", methods=["GET"])  # Health check for Railway
def root_health():
    storage_type = "SQLite" if use_sqlite else "In-Memory"
    return jsonify({
        "status": "ok", 
        "message": "WhatsApp Medical Bot is running",
        "storage": storage_type,
        "bot_flow_loaded": len(operators) > 0
    }), 200

@app.route("/health", methods=["GET"])  # Additional health endpoint
def health_check():
    return "OK", 200

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Meta webhook verification strictly per docs:
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        print(f"🔍 Verification attempt: mode={mode} token_provided={bool(token)} challenge_len={len(challenge) if challenge else 0}")
        if mode == "subscribe" and token == VERIFY_TOKEN and challenge:
            print("✅ Verify token matched. Returning challenge.")
            # Must return raw challenge string with 200 and text/plain
            return Response(challenge, status=200, mimetype='text/plain')
        else:
            if token != VERIFY_TOKEN:
                print(f"❌ Verify token mismatch. Received='{token}' Expected='{VERIFY_TOKEN}'")
            else:
                print("❌ Verification failed: missing or incorrect parameters.")
            # Return 403 as per Meta recommendation when token mismatch
            return Response("Forbidden", status=403, mimetype='text/plain')

    # POST request handling (incoming messages)
    payload = request.get_json(silent=True) or {}
    try:
        entry_list = payload.get("entry", [])
        if entry_list:
            changes = entry_list[0].get("changes", [])
            if changes:
                value = changes[0].get("value", {})
                messages = value.get("messages")
                if messages:
                    msg = messages[0]
                    sender = msg.get("from")
                    text = ""
                    if "text" in msg:
                        text = msg["text"].get("body", "")
                    elif "button" in msg:
                        text = msg["button"].get("text", "")
                    elif "interactive" in msg:
                        interactive = msg["interactive"]
                        text = (interactive.get("button_reply", {}).get("title", "") or
                                interactive.get("list_reply", {}).get("title", ""))
                    print(f"📩 Incoming message from {sender}: {text}")
                    handle_user_message(sender, text)
    except Exception as e:
        print("Webhook processing error:", e)
    return Response("ok", status=200, mimetype='text/plain')

if __name__ == "__main__":
    # Initialize database with error handling
    use_sqlite = init_db()
    
    # Use Railway's dynamic port or default to 5000
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Starting server on port {port}")
    
    try:
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        print(f"❌ Server startup error: {e}")
        # Try alternative port
        print("🔄 Trying alternative port 8000...")
        app.run(host='0.0.0.0', port=8000, debug=False)
