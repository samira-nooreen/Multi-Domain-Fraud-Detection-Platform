"""
Test the AI-powered chatbot with Poe API
"""
from ml_modules.chatbot import MDFDPBot

def test_chatbot():
    print("=" * 70)
    print("MDFDP CHATBOT - AI POWERED TEST")
    print("=" * 70)
    
    # Initialize bot
    bot = MDFDPBot()
    print(f"\n✅ Chatbot initialized")
    print(f"🔑 API Key configured: {bot.api_key[:15]}...")
    print(f"🌐 API URL: {bot.api_url}")
    
    # Test messages
    test_messages = [
        "Hello",
        "How does credit card fraud detection work?",
        "Explain UPI fraud detection",
        "What ML models do you use?",
        "Tell me about fake news detection",
        "Help me with the platform"
    ]
    
    print("\n" + "=" * 70)
    print("TESTING CHATBOT RESPONSES")
    print("=" * 70)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{'─' * 70}")
        print(f"Test {i}/{len(test_messages)}")
        print(f"{'─' * 70}")
        print(f"👤 You: {message}")
        
        response = bot.get_response(message)
        print(f"🤖 Bot: {response}")
        
        # Check if response is from AI or fallback
        if len(response) > 100:
            print(f"✅ Source: AI API (Poe)")
        else:
            print(f"⚡ Source: Rule-based fallback")
    
    print("\n" + "=" * 70)
    print("INTERACTIVE MODE")
    print("=" * 70)
    print("\nTry chatting with the bot! (Type 'quit' to exit)\n")
    
    while True:
        try:
            user_input = input("👤 You: ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if user_input:
                response = bot.get_response(user_input)
                print(f"🤖 Bot: {response}\n")
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")

if __name__ == "__main__":
    test_chatbot()
