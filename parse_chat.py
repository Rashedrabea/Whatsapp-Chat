import re
from datetime import datetime

def parse_chat(file_path):
    """Parse WhatsApp chat file and return list of messages"""
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    chat_data = []
    # Pattern for WhatsApp messages: [Date], [Time] - [Sender]: [Message]
    message_pattern = re.compile(r"(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}\s?[APM]{2}) - ([^:]+?): (.+)")
    
    for line in lines:
        line = line.replace("\u202f", " ")  # Fix special spaces that appear in WhatsApp exports
        match = message_pattern.match(line)
        if match:
            date_str, time_str, sender, message = match.groups()
            try:
                timestamp = datetime.strptime(date_str + ", " + time_str, "%m/%d/%y, %I:%M %p")
                chat_data.append({
                    "timestamp": timestamp, 
                    "sender": sender.strip(), 
                    "message": message.strip()
                })
            except ValueError:
                # Skip messages that don't match expected time format
                continue
    
    return chat_data


# Run the parser when executed directly
if __name__ == "__main__":
    try:
        chat_data = parse_chat("chat.txt")
        
        # Debug: Print statistics
        print(f"\n✅ Successfully parsed {len(chat_data)} messages\n")
        print("📜 First 5 parsed messages:")
        print("-" * 60)
        for i, msg in enumerate(chat_data[:5], 1):
            print(f"\n{i}. {msg['timestamp']}")
            print(f"   From: {msg['sender']}")
            print(f"   Message: {msg['message'][:50]}...")
        
        if len(chat_data) > 0:
            # Get unique users
            users = set(msg['sender'] for msg in chat_data)
            print(f"\n👥 Total unique users: {len(users)}")
            print(f"📊 Total messages: {len(chat_data)}")
            print(f"📅 Date range: {chat_data[0]['timestamp']} to {chat_data[-1]['timestamp']}")
        
    except FileNotFoundError:
        print("❌ Error: chat.txt file not found in the current directory")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
