"""
Simple test file to verify the installation
"""

import sys
from datetime import datetime

def test_imports():
    """Test that all required modules are installed"""
    print("\n🧪 Testing imports...\n")
    
    modules = {
        "fastapi": "FastAPI",
        "uvicorn": "Uvicorn",
        "emoji": "Emoji",
        "textblob": "TextBlob",
        "nltk": "NLTK",
        "pandas": "Pandas"
    }
    
    all_installed = True
    for module_name, display_name in modules.items():
        try:
            __import__(module_name)
            print(f"✅ {display_name} is installed")
        except ImportError:
            print(f"❌ {display_name} is NOT installed")
            all_installed = False
    
    return all_installed

def test_parse_chat():
    """Test parsing chat file"""
    print("\n🧪 Testing chat parsing...\n")
    
    try:
        from parse_chat import parse_chat
        
        # Try to parse the chat file
        try:
            chat_data = parse_chat("chat.txt")
            if chat_data:
                print(f"✅ Successfully parsed {len(chat_data)} messages")
                print(f"   Date range: {chat_data[0]['timestamp']} to {chat_data[-1]['timestamp']}")
                
                # Get unique users
                users = set(msg['sender'] for msg in chat_data)
                print(f"   Users: {', '.join(users)}")
                return True
            else:
                print("⚠️ No messages were parsed. Check your chat.txt file.")
                return False
        except FileNotFoundError:
            print("⚠️ chat.txt file not found. Please add your chat export.")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_analysis():
    """Test chat analysis"""
    print("\n🧪 Testing chat analysis...\n")
    
    try:
        from parse_chat import parse_chat
        from analyze_chat import analyze_chat
        
        try:
            chat_data = parse_chat("chat.txt")
            if chat_data:
                print("✅ Running analysis...")
                results = analyze_chat(chat_data)
                print("✅ Analysis completed successfully!")
                return True
            else:
                print("⚠️ No messages to analyze")
                return False
        except FileNotFoundError:
            print("⚠️ chat.txt file not found")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("🧪 WhatsApp Chat Analyzer - Installation Test")
    print("="*60)
    
    # Test imports
    imports_ok = test_imports()
    
    if not imports_ok:
        print("\n⚠️ Some modules are missing. Please run:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Test parsing
    parse_ok = test_parse_chat()
    
    # Test analysis
    if parse_ok:
        analysis_ok = test_analysis()
    
    print("\n" + "="*60)
    print("✅ All tests completed!")
    print("="*60)
    print("\nYou can now run:")
    print("  - python main.py          (Start the API server)")
    print("  - python analyze_chat.py   (Analyze the chat)")
