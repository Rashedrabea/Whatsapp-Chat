import re
from collections import Counter
import emoji

def get_most_used_words(parsed_data, top_n=5):
    """Get the most used words from parsed chat data"""
    word_counts = Counter()
    
    # Common stopwords to filter
    stopwords = {
        "the", "is", "and", "to", "you", "a", "in", "for", "of", "on", 
        "it", "this", "that", "with", "be", "have", "from", "or", "an", "as"
    }
    
    for entry in parsed_data:
        words = re.findall(r'\b\w+\b', entry["message"].lower())
        # Filter stopwords and short words
        words = [w for w in words if w not in stopwords and len(w) > 2]
        word_counts.update(words)

    return word_counts.most_common(top_n)


def get_most_used_emojis(parsed_data, top_n=5):
    """Get the most used emojis from parsed chat data"""
    emoji_counts = Counter()
    
    for entry in parsed_data:
        try:
            # Use emoji.EMOJI_DATA for better compatibility
            emojis = [char for char in entry["message"] if char in emoji.EMOJI_DATA]
            emoji_counts.update(emojis)
        except Exception as e:
            print(f"⚠️ Warning: Error processing emojis - {str(e)}")
            continue

    return emoji_counts.most_common(top_n)


def get_user_stats(parsed_data):
    """Get statistics for each user"""
    user_stats = {}
    
    for entry in parsed_data:
        sender = entry["sender"].strip()
        
        if sender not in user_stats:
            user_stats[sender] = {
                "message_count": 0,
                "word_count": 0,
                "emoji_count": 0,
                "total_chars": 0
            }
        
        message = entry["message"]
        user_stats[sender]["message_count"] += 1
        user_stats[sender]["word_count"] += len(message.split())
        user_stats[sender]["total_chars"] += len(message)
        
        # Count emojis
        try:
            emoji_count = sum(1 for char in message if char in emoji.EMOJI_DATA)
            user_stats[sender]["emoji_count"] += emoji_count
        except:
            pass
    
    return user_stats


def format_analysis_report(analysis_data):
    """Format analysis data into a readable report"""
    report = []
    report.append("\n" + "="*60)
    report.append("📊 WHATSAPP CHAT ANALYSIS REPORT")
    report.append("="*60)
    
    for key, value in analysis_data.items():
        report.append(f"\n{key}:")
        if isinstance(value, dict):
            for k, v in sorted(value.items(), key=lambda x: x[1], reverse=True)[:10]:
                report.append(f"  {k}: {v}")
        elif isinstance(value, list):
            for item in value[:10]:
                report.append(f"  {item}")
        else:
            report.append(f"  {value}")
    
    report.append("\n" + "="*60)
    return "\n".join(report)
