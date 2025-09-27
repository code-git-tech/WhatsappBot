import os, sys, json, requests
from pathlib import Path

try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass

TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
TEST_RECIPIENT = os.getenv("WHATSAPP_TEST_RECIPIENT", "")  # e.g. 15551234567 (no +)

if not TOKEN:
    print("❌ Missing WHATSAPP_TOKEN in .env")
    sys.exit(1)
if not PHONE_NUMBER_ID:
    print("❌ Missing WHATSAPP_PHONE_NUMBER_ID in .env")
    sys.exit(1)
if not TEST_RECIPIENT:
    print("⚠️ Set WHATSAPP_TEST_RECIPIENT=1555XXXXXXX in your .env to avoid typing every time.")
    if len(sys.argv) < 2:
        print("Usage: python send_test_message.py 1555XXXXXXXX [Message text]")
        sys.exit(1)
    TEST_RECIPIENT = sys.argv[1]
    message_text = " ".join(sys.argv[2:]) or "Hello from Dooper Bot test!"
else:
    message_text = " ".join(sys.argv[1:]) or "Hello from Dooper Bot test!"

url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
payload = {
    "messaging_product": "whatsapp",
    "to": TEST_RECIPIENT,
    "type": "text",
    "text": {"body": message_text}
}
print("➡️ Sending message:", json.dumps(payload, indent=2))
resp = requests.post(url, headers=headers, json=payload, timeout=30)
print("📥 Status:", resp.status_code)
try:
    print("📦 Response:", json.dumps(resp.json(), indent=2))
except ValueError:
    print(resp.text)

if resp.status_code == 400 and '131021' in resp.text:
    print("⚠️ Template / session error: Make sure the recipient has sent a message to your number within 24h.")
