# app.py - WhatsApp Medical Bot
import os
import json
import sqlite3
import requests
from flask import Flask, request, jsonify, Response
from dotenv import load_dotenv
from datetime import datetime

# ----- Load environment variables -----
load_dotenv()

ACCESS_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "verify_token_example")
WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "+15557667459")
BOT_FLOW_FILE = os.getenv("BOT_FLOW_FILE", "dooper_bot.json")
TEST_RECIPIENT = os.getenv("WHATSAPP_TEST_RECIPIENT")

GRAPH_API_VERSION = "v20.0"
DB = "bot_state.db"
BOT_JSON = BOT_FLOW_FILE

# ----- Flask app -----
app = Flask(__name__)

# ----- Validate env -----
if not ACCESS_TOKEN:
    print("❌ ERROR: WHATSAPP_TOKEN not found in environment variables")
if not PHONE_NUMBER_ID:
    print("❌ ERROR: WHATSAPP_PHONE_NUMBER_ID not found in environment variables")

print(f"🤖 Bot initialized with:")
print(f"   📱 WhatsApp Number: {WHATSAPP_NUMBER}")
print(f"   📋 Bot Flow File: {BOT_JSON}")
print(f"   🔧 Phone Number ID: {PHONE_NUMBER_ID}")
print(f"   🔑 Has Access Token: {'Yes' if ACCESS_TOKEN and ACCESS_TOKEN != 'your_access_token_here' else 'No - Update .env file'}")

# ----- In-memory storage fallback -----
memory_storage = {}
memory_message_log = {}

# ----- SQLite DB helpers -----
def init_db():
    try:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS user_state (
                        user_id TEXT PRIMARY KEY,
                        node_key TEXT,
                        data TEXT
                    )""")
        c.execute("""CREATE TABLE IF NOT EXISTS message_log (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT,
                        direction TEXT,
                        message TEXT,
                        ts DATETIME DEFAULT CURRENT_TIMESTAMP
                    )""")
        conn.commit()
        conn.close()
        print("✅ SQLite database initialized successfully")
        return True
    except Exception as e:
        print(f"⚠️ SQLite failed, using in-memory storage: {e}")
        return False

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
    return memory_storage.get(user_id, {}).get('node_key'), memory_storage.get(user_id, {}).get('data', {})

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
    memory_storage[user_id] = {'node_key': node_key, 'data': data or {}}

# ----- Message logging -----
def log_message(user_id: str, direction: str, message: str):
    if not message:
        return
    if use_sqlite:
        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            c.execute("INSERT INTO message_log(user_id,direction,message) VALUES(?,?,?)",
                      (user_id, direction, message))
            conn.commit()
            conn.close()
            return
        except Exception as e:
            print(f"⚠️ SQLite message_log error, switching to memory storage: {e}")
            use_sqlite = False
    arr = memory_message_log.setdefault(user_id, [])
    arr.append({'direction': direction, 'message': message, 'ts': datetime.utcnow().isoformat()+'Z'})

def get_history(user_id: str, limit: int = 100):
    if use_sqlite:
        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            c.execute("SELECT direction, message, ts FROM message_log WHERE user_id=? ORDER BY id DESC LIMIT ?", (user_id, limit))
            rows = c.fetchall()
            conn.close()
            rows.reverse()
            return [{'direction': d, 'message': m, 'ts': ts} for d,m,ts in rows]
        except Exception as e:
            print(f"⚠️ SQLite history fetch error, switching to memory storage: {e}")
            use_sqlite = False
    return memory_message_log.get(user_id, [])[-limit:]

# ----- Load bot flow -----
try:
    with open(BOT_JSON, "r", encoding="utf-8") as f:
        bot_flow = json.load(f)
    print(f"✅ Bot flow loaded successfully from {BOT_JSON}")
except Exception as e:
    print(f"❌ Bot flow load error: {e}")
    bot_flow = {"operators": {}}

operators = bot_flow.get("operators", {})
title_to_key = {}
for k,v in operators.items():
    t = v.get("properties", {}).get("title", "")
    if t: title_to_key[t.lower()] = k

def find_start_node():
    for t in ("start","start2"):
        if t in title_to_key:
            return title_to_key[t]
    return next(iter(operators.keys()), None)

def get_node(node_key):
    return operators.get(node_key, {}).get("properties", {})

# ----- WhatsApp Cloud API sender -----
def send_whatsapp_text(to, text):
    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "messaging_product":"whatsapp",
        "to": to,
        "type":"text",
        "text":{"body": text}
    }
    try:
        log_message(to, 'out', text)
        r = requests.post(url, headers=headers, json=payload, timeout=15)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ WhatsApp API error: {e} | Response: {r.text if 'r' in locals() else 'No response'}")
        return {"error": True, "reason": str(e)}

# ----- Conversation logic -----
def match_output(node_props, incoming_text):
    outputs = node_props.get("outputs") or {}
    answers = [o.get("answer","") for k,o in outputs.items()]
    if incoming_text.strip().isdigit():
        idx = int(incoming_text.strip()) - 1
        if 0 <= idx < len(answers):
            return answers[idx]
    for ans in answers:
        if ans and ans.lower().startswith(incoming_text.strip().lower()):
            return ans
    return None

def handle_user_message(user_id, text):
    log_message(user_id, 'in', text)
    node_key, data = get_state(user_id)
    if not node_key:
        node_key = find_start_node()
        set_state(user_id, node_key, {})
        node = get_node(node_key)
        question = node.get("question","")
        outputs = node.get("outputs") or {}
        if outputs:
            opts = "\n".join(f"{i+1}. {o.get('answer','')}" for i,o in enumerate(outputs.values()))
            send_whatsapp_text(user_id, f"{question}\n\n{opts}")
        else:
            send_whatsapp_text(user_id, question)
        return
    
    node = get_node(node_key)
    matched_answer = match_output(node, text)
    if matched_answer:
        followup = node.get("followup") or {}
        next_title = followup.get("nodeName")
        if next_title:
            next_key = title_to_key.get(next_title.lower())
            if next_key:
                set_state(user_id, next_key, data)
                next_node = get_node(next_key)
                q = next_node.get("question","")
                outputs = next_node.get("outputs") or {}
                if outputs:
                    opts = "\n".join(f"{i+1}. {o.get('answer','')}" for i,o in enumerate(outputs.values()))
                    send_whatsapp_text(user_id, f"{q}\n\n{opts}")
                else:
                    send_whatsapp_text(user_id, q or "Done.")
                return
        
        fallback_key = title_to_key.get(matched_answer.lower())
        if fallback_key:
            set_state(user_id, fallback_key, data)
            next_node = get_node(fallback_key)
            q = next_node.get("question","")
            outputs = next_node.get("outputs") or {}
            if outputs:
                opts = "\n".join(f"{i+1}. {o.get('answer','')}" for i,o in enumerate(outputs.values()))
                send_whatsapp_text(user_id, f"{q}\n\n{opts}")
            else:
                send_whatsapp_text(user_id, q or "Done.")
            return
        
        send_whatsapp_text(user_id, f"Got it: {matched_answer}. (No followup configured.)")
        return
    
    q = node.get("question","Sorry I didn't understand.")
    outputs = node.get("outputs") or {}
    if outputs:
        opts = "\n".join(f"{i+1}. {o.get('answer','')}" for i,o in enumerate(outputs.values()))
        send_whatsapp_text(user_id, f"Sorry, I didn't get that. {q}\n\n{opts}")
    else:
        send_whatsapp_text(user_id, "Sorry, I didn't understand. " + q)

# ----- Flask routes -----
@app.route("/", methods=["GET"])
def root_health():
    storage = "SQLite" if use_sqlite else "In-Memory"
    return jsonify({
        "status": "ok",
        "message": "WhatsApp Medical Bot is running",
        "storage": storage,
        "bot_flow_loaded": len(operators)>0
    }), 200

@app.route("/health", methods=["GET"])
def health_check():
    return "OK", 200

@app.route("/webhook", methods=["GET","POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        print(f"🔍 Verification attempt: mode={mode} token_provided={bool(token)} challenge_len={len(challenge) if challenge else 0}")
        
        if mode=="subscribe" and token==VERIFY_TOKEN and challenge:
            print("✅ Verify token matched. Returning challenge.")
            return Response(challenge, status=200, mimetype='text/plain')
        else:
            if token != VERIFY_TOKEN:
                print(f"❌ Verify token mismatch. Received='{token}' Expected='{VERIFY_TOKEN}'")
            else:
                print("❌ Verification failed: missing or incorrect parameters.")
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
                        text = msg["text"].get("body","")
                    elif "button" in msg:
                        text = msg["button"].get("text","")
                    elif "interactive" in msg:
                        interactive = msg["interactive"]
                        text = (interactive.get("button_reply",{}).get("title","") or
                                interactive.get("list_reply",{}).get("title",""))
                    print(f"📩 Incoming message from {sender}: {text}")
                    handle_user_message(sender, text)
    except Exception as e:
        print("Webhook processing error:", e)
    return Response("ok", status=200, mimetype='text/plain')

@app.route('/history/<user_id>', methods=['GET'])
def history(user_id):
    limit = request.args.get('limit', default=100, type=int)
    hist = get_history(user_id, limit=limit)
    return jsonify({
        'user_id': user_id,
        'count': len(hist),
        'messages': hist
    }), 200

# ----- Initialize SQLite -----
use_sqlite = init_db()

# ----- Run dev server -----
if __name__=="__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Starting Flask development server on port {port}")
    print("⚠️  WARNING: Dev server only. Use Waitress or Gunicorn in production.")
    try:
        app.run(host="0.0.0.0", port=port, debug=True)
    except Exception as e:
        print(f"❌ Server startup error: {e}, trying port 8000...")
        app.run(host="0.0.0.0", port=8000, debug=True)