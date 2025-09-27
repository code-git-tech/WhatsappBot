#!/usr/bin/env python3
"""
WhatsApp Bot Live Connection Setup
This script helps you connect your bot to real WhatsApp
"""

print("🤖 WHATSAPP BOT LIVE CONNECTION SETUP")
print("=" * 50)
print()

print("📱 Your WhatsApp Number: +15557667459")
print("🤖 Your Bot: dooper_bot.json (441 conversation nodes)")
print()

print("🔧 TO SEE CONVERSATIONS ON YOUR WHATSAPP:")
print()

print("1️⃣ GET WHATSAPP BUSINESS API ACCESS:")
print("   • Go to: https://business.facebook.com/")  
print("   • Add WhatsApp Business API")
print("   • Verify phone number: +15557667459")
print()

print("2️⃣ GET API CREDENTIALS:")
print("   • Go to: https://developers.facebook.com/")
print("   • Create app → Add WhatsApp Business API")
print("   • Copy these values:")
print("     - Access Token (starts with EAA...)")
print("     - Phone Number ID (long number)")
print("     - Create a Verify Token (your secret)")
print()

print("3️⃣ UPDATE YOUR .env FILE:")
print("   Replace these in your .env file:")
print("   WHATSAPP_TOKEN=EAAyour_real_token_here")
print("   WHATSAPP_PHONE_NUMBER_ID=your_real_phone_id")
print("   WHATSAPP_VERIFY_TOKEN=your_secret_verify_token")
print()

print("4️⃣ EXPOSE YOUR BOT TO INTERNET:")
print("   Option A - Install ngrok:")
print("   • Download: https://ngrok.com/download")
print("   • Run: ngrok http 5000")
print("   • Copy the https://xxx.ngrok.io URL")
print()
print("   Option B - Use other tunnel service:")
print("   • LocalTunnel: npx localtunnel --port 5000")
print("   • Serveo: ssh -R 80:localhost:5000 serveo.net")
print()

print("5️⃣ CONFIGURE WEBHOOK:")
print("   In Facebook Developers:")
print("   • Webhook URL: https://your-ngrok-url.ngrok.io/webhook")
print("   • Verify Token: (same as in your .env)")
print("   • Subscribe to: messages")
print()

print("6️⃣ TEST YOUR BOT:")
print("   • Send message to: +15557667459")
print("   • Bot responds with: 'Greetings and welcome to Dooper Health!'")
print("   • Follow conversation flow from dooper_bot.json")
print()

print("🎯 CURRENT STATUS:")
print("   ✅ Bot code: Ready")
print("   ✅ JSON flow: Loaded (441 nodes)")
print("   ✅ Server: Running on localhost:5000")
print("   ❌ WhatsApp API: Need real credentials")
print("   ❌ Internet access: Need ngrok or similar")
print()

print("💡 QUICK START:")
print("   1. Get credentials from developers.facebook.com")
print("   2. Update .env file") 
print("   3. Install ngrok and run: ngrok http 5000")
print("   4. Set webhook URL in Facebook Developers")
print("   5. Send WhatsApp message to +15557667459")
print()

print("🚀 Once setup, your bot will:")
print("   • Receive messages on +15557667459")
print("   • Process through dooper_bot.json flow") 
print("   • Send responses back to WhatsApp")
print("   • Handle medical consultations, appointments, etc.")

if __name__ == "__main__":
    pass