#!/usr/bin/env python3
"""
Test script to send a WhatsApp message using the Business API
This tests our WhatsApp integration without needing webhook setup
"""

import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# WhatsApp API Configuration
WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
WHATSAPP_PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
WHATSAPP_API_URL = f'https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_NUMBER_ID}/messages'

def send_test_message():
    """Send a test message to verify WhatsApp API is working"""
    
    # Test phone number (your number)
    test_phone = "15557667459"  # The number you want to test with
    
    # Message data
    message_data = {
        "messaging_product": "whatsapp",
        "to": test_phone,
        "type": "text",
        "text": {
            "body": "🤖 Hello! This is a test message from your Dooper Medical Bot!\n\n✅ Your WhatsApp Business API is working correctly!\n\nThe bot is ready to handle medical consultations. Send 'Hi' to start a conversation!"
        }
    }
    
    # Headers
    headers = {
        'Authorization': f'Bearer {WHATSAPP_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    try:
        print(f"📤 Sending test message to +{test_phone}...")
        response = requests.post(WHATSAPP_API_URL, json=message_data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            message_id = result.get('messages', [{}])[0].get('id')
            print(f"✅ Message sent successfully!")
            print(f"📱 Message ID: {message_id}")
            print(f"📞 Check your WhatsApp at +{test_phone}")
            return True
        else:
            print(f"❌ Failed to send message")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending message: {str(e)}")
        return False

def check_api_status():
    """Check if our API credentials are valid"""
    
    # Test endpoint to check account info
    test_url = f'https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_NUMBER_ID}'
    headers = {
        'Authorization': f'Bearer {WHATSAPP_TOKEN}'
    }
    
    try:
        print("🔍 Checking WhatsApp Business API status...")
        response = requests.get(test_url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Connection: Working")
            print(f"📱 Phone Number ID: {data.get('id')}")
            print(f"📋 Display Name: {data.get('display_phone_number')}")
            return True
        else:
            print(f"❌ API Check failed")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking API: {str(e)}")
        return False

if __name__ == "__main__":
    print("🤖 Dooper Medical Bot - WhatsApp API Test")
    print("=" * 50)
    
    # Check API status first
    if check_api_status():
        print("\n" + "=" * 50)
        # Send test message
        if send_test_message():
            print("\n🎉 Success! Your WhatsApp integration is working!")
            print("\n📝 Next Steps:")
            print("1. Check your WhatsApp for the test message")
            print("2. The webhook setup can be completed later")
            print("3. For now, you can send messages programmatically")
        else:
            print("\n❌ Message sending failed. Check your credentials.")
    else:
        print("\n❌ API credentials check failed. Please verify your .env file.")
    
    print("\n" + "=" * 50)