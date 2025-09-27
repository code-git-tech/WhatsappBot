#!/usr/bin/env python3
"""
Message Logger - Shows exactly what JSON you receive when users message your bot
"""

import json
from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verification
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        
        if mode == "subscribe" and token == "1285389302894210":
            print("✅ Webhook verified!")
            return challenge
        else:
            print("❌ Webhook verification failed")
            return "Forbidden", 403

    # POST - Incoming message
    if request.method == 'POST':
        body = request.get_json()
        
        print("\n" + "="*80)
        print("📥 INCOMING MESSAGE JSON:")
        print("="*80)
        print(json.dumps(body, indent=2))
        print("="*80)
        
        # Extract message details
        try:
            entry = body.get('entry', [{}])[0]
            changes = entry.get('changes', [{}])[0]
            value = changes.get('value', {})
            
            if 'messages' in value:
                messages = value['messages']
                contacts = value.get('contacts', [{}])
                
                for message in messages:
                    sender = message.get('from')
                    sender_name = contacts[0].get('profile', {}).get('name', 'Unknown') if contacts else 'Unknown'
                    message_id = message.get('id')
                    timestamp = message.get('timestamp')
                    message_type = message.get('type')
                    
                    print(f"\n📱 MESSAGE DETAILS:")
                    print(f"👤 From: +{sender} ({sender_name})")
                    print(f"🆔 Message ID: {message_id}")
                    print(f"⏰ Time: {timestamp}")
                    print(f"📝 Type: {message_type}")
                    
                    # Extract message content based on type
                    if message_type == 'text':
                        text_body = message.get('text', {}).get('body', '')
                        print(f"💬 Message: '{text_body}'")
                    
                    elif message_type == 'image':
                        image_id = message.get('image', {}).get('id', '')
                        print(f"🖼️ Image ID: {image_id}")
                    
                    elif message_type == 'document':
                        doc_id = message.get('document', {}).get('id', '')
                        filename = message.get('document', {}).get('filename', '')
                        print(f"📄 Document: {filename} (ID: {doc_id})")
                    
                    elif message_type == 'audio':
                        audio_id = message.get('audio', {}).get('id', '')
                        print(f"🎵 Audio ID: {audio_id}")
                    
                    print(f"\n🤖 YOUR BOT SHOULD RESPOND TO: +{sender}")
                    print("-" * 50)
        
        except Exception as e:
            print(f"❌ Error processing message: {e}")
        
        return "OK", 200

if __name__ == '__main__':
    print("🔍 WhatsApp Message Logger Started")
    print("This will show you the exact JSON when users message your bot")
    print("Keep this running and configure webhook to see incoming messages")
    print("-" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)