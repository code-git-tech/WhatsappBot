#!/usr/bin/env python3
"""
Quick WhatsApp Bot Test
Tests your bot's webhook endpoint
"""
import requests
import json

def test_bot_webhook():
    print("🔧 TESTING YOUR WHATSAPP BOT CONNECTION")
    print("=" * 50)
    
    bot_url = "http://127.0.0.1:5000"
    
    # Test 1: Check if server is running
    print("1️⃣ Testing if bot server is running...")
    try:
        response = requests.get(f"{bot_url}/", params={
            "hub.mode": "subscribe",
            "hub.verify_token": "test_token",
            "hub.challenge": "test_challenge"
        }, timeout=5)
        print(f"   ✅ Server responding: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Server not accessible: {e}")
        return
    
    # Test 2: Test webhook endpoint
    print("\n2️⃣ Testing webhook endpoint...")
    test_message = {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": "test_user_123",
                        "text": {"body": "Hello"}
                    }]
                }
            }]
        }]
    }
    
    try:
        response = requests.post(f"{bot_url}/webhook", json=test_message, timeout=10)
        if response.status_code == 200:
            print("   ✅ Webhook working! Bot processed test message")
        else:
            print(f"   ⚠️ Webhook responded with: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Webhook error: {e}")
    
    print(f"\n📱 TO SEE CONVERSATIONS IN WHATSAPP APP:")
    print("=" * 50)
    print("Since you've already connected to WhatsApp:")
    print()
    print("🎯 QUICK TEST:")
    print("1. Open WhatsApp on any phone")
    print("2. Send message to: +15557667459") 
    print("3. You should see bot reply with medical menu")
    print()
    print("📱 WHERE TO VIEW CONVERSATIONS:")
    print("• WhatsApp Business app (if you have it installed)")
    print("• WhatsApp Web: https://web.whatsapp.com")
    print("• Meta Business Manager")
    print()
    print("🤖 EXPECTED FIRST REPLY:")
    print("'Greetings and welcome to Dooper Health! I'm here to assist you in efficiently managing your doctor's appointments.'")
    print()
    print("If you're not seeing replies, check:")
    print("• Real access token in .env file")
    print("• Webhook URL configured in Facebook Developers")
    print("• Internet access to your bot (ngrok)")

if __name__ == "__main__":
    test_bot_webhook()