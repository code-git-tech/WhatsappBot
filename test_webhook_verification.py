#!/usr/bin/env python3
"""
WhatsApp Webhook Verification Test
This tests if your webhook will work with WhatsApp
"""
import requests
import json

def test_webhook_verification():
    print("🔍 TESTING WHATSAPP WEBHOOK VERIFICATION")
    print("=" * 50)
    
    # Start bot server first
    print("1️⃣ Make sure your bot is running:")
    print("   python app.py")
    print("   (Should show: Running on http://127.0.0.1:5000)")
    print()
    
    # Test webhook verification (what Facebook does)
    print("2️⃣ Testing webhook verification...")
    
    verification_params = {
        "hub.mode": "subscribe",
        "hub.verify_token": "test_verify_token",  # This should match your .env
        "hub.challenge": "test_challenge_123"
    }
    
    try:
        response = requests.get("http://127.0.0.1:5000/", params=verification_params, timeout=5)
        
        if response.status_code == 200:
            print("   ✅ Webhook verification works!")
            print(f"   Challenge response: {response.text}")
        else:
            print(f"   ❌ Verification failed: {response.status_code}")
            print("   Check your WHATSAPP_VERIFY_TOKEN in .env")
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Bot server not running!")
        print("   Start it with: python app.py")
        return
    
    # Test message processing
    print("\n3️⃣ Testing message processing...")
    
    test_message = {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": "test_user",
                        "text": {"body": "Hi"}
                    }]
                }
            }]
        }]
    }
    
    try:
        response = requests.post("http://127.0.0.1:5000/webhook", json=test_message, timeout=10)
        
        if response.status_code == 200:
            print("   ✅ Message processing works!")
            print("   Your bot can handle WhatsApp messages")
        else:
            print(f"   ⚠️ Message processing issue: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Message processing error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 NEXT STEPS TO GET RESPONSES ON +15557667459:")
    print("=" * 50)
    
    print("\n✅ IF TESTS PASSED:")
    print("1. Download ngrok from https://ngrok.com/download")
    print("2. Run: ngrok http 5000")  
    print("3. Copy the https://xxx.ngrok.io URL")
    print("4. Set this URL as webhook in Facebook Developers")
    print("5. Update .env with real WhatsApp API credentials")
    print()
    print("❌ IF TESTS FAILED:")
    print("1. Make sure bot server is running: python app.py")
    print("2. Check .env file has WHATSAPP_VERIFY_TOKEN=test_verify_token")
    print("3. Restart bot server after .env changes")
    
    print("\n📱 AFTER SETUP:")
    print("Messages to +15557667459 will trigger your bot!")
    print("Bot will respond with medical consultation options.")

if __name__ == "__main__":
    test_webhook_verification()