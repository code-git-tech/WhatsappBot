#!/usr/bin/env python3
"""
WhatsApp Bot Connection Checker
Run this to verify each step is working
"""
import os
import requests
import json
from dotenv import load_dotenv

def check_bot_connection():
    print("🔍 WHATSAPP BOT CONNECTION CHECKER")
    print("=" * 50)
    
    # Load environment
    load_dotenv()
    
    # Check 1: Environment Variables
    print("\n1️⃣ CHECKING ENVIRONMENT VARIABLES:")
    token = os.getenv("WHATSAPP_TOKEN")
    phone_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    verify_token = os.getenv("WHATSAPP_VERIFY_TOKEN")
    
    if token and token.startswith("EAA"):
        print("   ✅ Access Token: Present and valid format")
    else:
        print("   ❌ Access Token: Missing or invalid")
        print("      Get from: https://developers.facebook.com/")
    
    if phone_id and len(phone_id) > 10:
        print("   ✅ Phone Number ID: Present")
    else:
        print("   ❌ Phone Number ID: Missing")
        print("      Get from Facebook Developers WhatsApp section")
    
    if verify_token and verify_token != "test_verify_token":
        print("   ✅ Verify Token: Set")
    else:
        print("   ⚠️  Verify Token: Using default")
    
    # Check 2: Bot Server
    print("\n2️⃣ CHECKING BOT SERVER:")
    try:
        response = requests.get("http://127.0.0.1:5000", timeout=5)
        print("   ✅ Bot server is running on port 5000")
    except:
        print("   ❌ Bot server not running")
        print("      Start with: python app.py")
    
    # Check 3: Webhook Endpoint
    print("\n3️⃣ CHECKING WEBHOOK ENDPOINT:")
    try:
        test_verification = {
            "hub.mode": "subscribe",
            "hub.verify_token": verify_token,
            "hub.challenge": "test123"
        }
        response = requests.get("http://127.0.0.1:5000/", params=test_verification, timeout=5)
        if response.status_code == 200:
            print("   ✅ Webhook verification works")
        else:
            print(f"   ❌ Webhook verification failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Webhook test failed: {e}")
    
    # Check 4: ngrok status
    print("\n4️⃣ CHECKING INTERNET EXPOSURE:")
    print("   Run this in separate terminal:")
    print("   .\ngrok http 5000")
    print("   Then copy the https://xxx.ngrok.io URL")
    
    # Check 5: WhatsApp API Test
    print("\n5️⃣ TESTING WHATSAPP API:")
    if token and phone_id and token.startswith("EAA"):
        url = f"https://graph.facebook.com/v16.0/{phone_id}/messages"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        # Don't actually send, just test auth
        test_payload = {
            "messaging_product": "whatsapp",
            "to": "1234567890",  # dummy number
            "type": "text",
            "text": {"body": "test"}
        }
        try:
            response = requests.post(url, headers=headers, json=test_payload)
            if response.status_code == 400:  # Expected for dummy number
                print("   ✅ WhatsApp API credentials valid")
            elif response.status_code == 401:
                print("   ❌ WhatsApp API token invalid")
            else:
                print(f"   ⚠️  WhatsApp API response: {response.status_code}")
        except Exception as e:
            print(f"   ❌ WhatsApp API test failed: {e}")
    else:
        print("   ⏭️  Skipped (missing credentials)")
    
    print("\n" + "=" * 50)
    print("🎯 NEXT STEPS:")
    print("1. Fix any ❌ issues above")
    print("2. Set up ngrok tunnel")
    print("3. Configure Facebook webhook with ngrok URL")
    print("4. Test by sending message to +15557667459")
    print("\n📱 Expected result: Bot responds with medical menu")

if __name__ == "__main__":
    check_bot_connection()