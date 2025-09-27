#!/usr/bin/env python3
"""
Local WhatsApp Bot Tester
This script simulates WhatsApp interactions without needing webhook setup
"""

import json
import sqlite3
from datetime import datetime

class LocalWhatsAppBot:
    def __init__(self):
        self.db_path = 'bot_state.db'
        self.bot_flow_file = 'dooper_bot.json'
        self.setup_database()
        self.load_bot_flow()
    
    def setup_database(self):
        """Setup SQLite database for conversation state"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            phone_number TEXT PRIMARY KEY,
            current_state TEXT,
            context TEXT,
            last_updated TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def load_bot_flow(self):
        """Load the conversation flow from JSON file"""
        try:
            with open(self.bot_flow_file, 'r', encoding='utf-8') as f:
                self.bot_flow = json.load(f)
            print(f"✅ Loaded bot flow with {len(self.bot_flow)} conversation nodes")
        except Exception as e:
            print(f"❌ Error loading bot flow: {e}")
            self.bot_flow = {}
    
    def get_conversation_state(self, phone_number):
        """Get current conversation state for a phone number"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT current_state, context FROM conversations WHERE phone_number = ?',
            (phone_number,)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0], json.loads(result[1]) if result[1] else {}
        return 'start', {}
    
    def update_conversation_state(self, phone_number, state, context):
        """Update conversation state for a phone number"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            '''INSERT OR REPLACE INTO conversations 
               (phone_number, current_state, context, last_updated) 
               VALUES (?, ?, ?, ?)''',
            (phone_number, state, json.dumps(context), datetime.now())
        )
        
        conn.commit()
        conn.close()
    
    def process_message(self, phone_number, message):
        """Process an incoming message and return bot response"""
        current_state, context = self.get_conversation_state(phone_number)
        
        print(f"\n📱 Processing message from +{phone_number}")
        print(f"💬 User: {message}")
        print(f"🔄 Current State: {current_state}")
        
        # Handle the message based on current conversation flow
        if current_state not in self.bot_flow:
            # Start with welcome message
            current_state = 'start'
        
        node = self.bot_flow.get(current_state, {})
        response_text = node.get('message', 'Hello! I am Dooper Medical Bot. How can I help you today?')
        
        # Get next state based on user input
        next_state = self.determine_next_state(current_state, message, node)
        
        # Update conversation state
        self.update_conversation_state(phone_number, next_state, context)
        
        print(f"🤖 Bot: {response_text}")
        print(f"➡️  Next State: {next_state}")
        
        return response_text, next_state
    
    def determine_next_state(self, current_state, user_message, current_node):
        """Determine the next conversation state based on user input"""
        user_input = user_message.lower().strip()
        
        # Check if current node has operators (next states)
        operators = current_node.get('operators', [])
        
        for operator in operators:
            # Check if user input matches any operator condition
            operator_text = operator.get('text', '').lower()
            operator_value = operator.get('value', '').lower()
            
            # Simple keyword matching
            if (operator_text and operator_text in user_input) or \
               (operator_value and operator_value in user_input):
                return operator.get('next_state', 'start')
        
        # Default fallback based on common inputs
        if any(word in user_input for word in ['hi', 'hello', 'start', 'hey']):
            return 'main_menu'
        elif any(word in user_input for word in ['doctor', 'appointment', 'consultation']):
            return 'book_appointment'
        elif any(word in user_input for word in ['medicine', 'pharmacy', 'drug']):
            return 'order_medicine'
        elif any(word in user_input for word in ['lab', 'test', 'blood']):
            return 'lab_test'
        elif any(word in user_input for word in ['help', 'support']):
            return 'help'
        
        # Stay in current state if no match
        return current_state
    
    def simulate_conversation(self):
        """Interactive conversation simulation"""
        phone_number = "15557667459"
        
        print("🤖 Dooper Medical Bot - Local Simulation")
        print("=" * 50)
        print("Type messages to test the bot. Type 'quit' to exit.")
        print("=" * 50)
        
        while True:
            user_input = input("\n💬 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye! Bot simulation ended.")
                break
            
            if user_input:
                response, next_state = self.process_message(phone_number, user_input)

def main():
    bot = LocalWhatsAppBot()
    bot.simulate_conversation()

if __name__ == "__main__":
    main()