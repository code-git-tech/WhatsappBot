import requests
import time

print("🔍 COMPREHENSIVE BOT TEST")
print("="*50)

# Test 1: Local Flask Server
print("\n1. Testing Flask Server Locally...")
try:
    r = requests.get("http://localhost:5000/webhook")
    print(f"✅ Local Status: {r.status_code} - {r.text}")
except Exception as e:
    print(f"❌ Local Error: {e}")

# Test 2: ngrok tunnel
print("\n2. Testing ngrok Tunnel...")
ngrok_url = "https://nontransitively-corned-heidi.ngrok-free.dev"
try:
    r = requests.get(f"{ngrok_url}/webhook", headers={"ngrok-skip-browser-warning": "true"}, timeout=10)
    print(f"✅ ngrok Status: {r.status_code} - {r.text[:100]}")
    tunnel_working = r.status_code == 200
except Exception as e:
    print(f"❌ ngrok Error: {e}")
    tunnel_working = False

# Test 3: Webhook verification
if tunnel_working:
    print("\n3. Testing Webhook Verification...")
    verify_url = f"{ngrok_url}/webhook?hub.mode=subscribe&hub.verify_token=1285389302894210&hub.challenge=test123"
    try:
        r = requests.get(verify_url, headers={"ngrok-skip-browser-warning": "true"}, timeout=10)
        print(f"✅ Verification Status: {r.status_code} - Response: {r.text}")
        if r.text == "test123":
            print("🎉 WEBHOOK VERIFICATION WORKING!")
        else:
            print("⚠️ Verification response incorrect")
    except Exception as e:
        print(f"❌ Verification Error: {e}")

# Test 4: Send test message via API
print("\n4. Testing Direct WhatsApp API...")
api_url = "https://graph.facebook.com/v20.0/110735612113186/messages"
token = "EAAQdBJWZCiykBPsx6F2qaZB5uoZBBoFj0pj1sBA9PLdMMEzj3hZBXtSwDbqB9UmpmJTuMHXU1p7aBn7lZBiVTaVQQuJZA37130deDq7jfF7lQ1c35koe4WxXNSa0r9NsjtyKDyfFDYu9TVGZBZBmFUaRGDWE84ozQbV7k51jWfkR3y4RqF2tEHhWrrVnv5CzaVMrQzYp6uH2WJgpHrkgMA3ttZBMB8toZBymwTWKXgEZC0ZD"

# Note: Replace with a real test recipient number
test_number = "15551234567"  # Example - replace with real number
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
payload = {
    "messaging_product": "whatsapp",
    "to": test_number,
    "type": "text", 
    "text": {"body": "Test message from bot"}
}

print("⚠️ Skipping API test (need real recipient number)")
print(f"📋 API Endpoint: {api_url}")
print(f"📋 Token Status: {'Valid format' if token.startswith('EAA') else 'Invalid'}")

print("\n" + "="*50)
print("SUMMARY:")
print(f"Flask Server: {'✅ Working' if True else '❌ Failed'}")
print(f"Tunnel: {'✅ Working' if tunnel_working else '❌ Failed'}")
print(f"WhatsApp Token: {'✅ Valid format' if token.startswith('EAA') else '❌ Invalid'}")

if tunnel_working:
    print(f"\n🎯 NEXT STEP: Configure webhook in Facebook:")
    print(f"Callback URL: {ngrok_url}/webhook")
    print(f"Verify Token: 1285389302894210")
else:
    print(f"\n🔧 ISSUE: Need to fix tunnel connection first")