import requests
import time

print("🧪 Testing Bot Connection...")
print("🔄 Waiting 2 seconds for tunnel to stabilize...")
time.sleep(2)

# Test if the bot is accessible from internet
ngrok_url = "https://nontransitively-corned-heidi.ngrok-free.dev"

print(f"🌐 Bot URL: {ngrok_url}")

try:
    # Test basic connectivity first
    print("🔗 Testing basic connectivity...")
    response = requests.get(ngrok_url, timeout=10)
    print(f"📊 Basic Response: {response.status_code}")
    
    # Test webhook endpoint
    print("🎯 Testing webhook endpoint...")
    webhook_response = requests.get(f"{ngrok_url}/webhook", timeout=10)
    print(f"✅ Webhook: {webhook_response.status_code} - {webhook_response.text[:100]}")
    
    # Test webhook verification
    print("🔐 Testing webhook verification...")
    verify_url = f"{ngrok_url}/webhook?hub.mode=subscribe&hub.verify_token=my_secure_verify_token_123&hub.challenge=test123"
    verify_response = requests.get(verify_url, timeout=10)
    print(f"✅ Verification: {verify_response.status_code} - {verify_response.text}")
    
    if verify_response.status_code == 200 and verify_response.text == "test123":
        print("\n🎉 SUCCESS! Bot is accessible and webhook verification works!")
        print(f"🌐 Your WhatsApp webhook URL: {ngrok_url}/webhook")
        print("📱 Ready to configure with Facebook!")
    else:
        print(f"\n⚠️ Webhook verification issue: Expected 'test123', got '{verify_response.text}'")
        
except requests.exceptions.ConnectionError as e:
    print(f"❌ Connection Error: {e}")
    print("🔧 Bot server might not be running or ngrok tunnel is down")
except requests.exceptions.Timeout as e:
    print(f"⏱️ Timeout Error: {e}")
    print("🔧 Connection is slow, try again")
except Exception as e:
    print(f"❌ Error: {e}")