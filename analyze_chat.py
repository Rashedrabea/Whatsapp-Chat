import re
import json
from datetime import datetime, timedelta
from collections import Counter
import emoji
from textblob import TextBlob
import nltk
from nltk.util import ngrams
import random

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


def parse_chat(file_path):
    """Parse chat file and return list of messages"""
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    chat_data = []
    message_pattern = re.compile(r"(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}\s?[APM]{2}) - ([^:]+?): (.+)")
    
    for line in lines:
        line = line.replace("\u202f", " ")  # Fix special spaces
        match = message_pattern.match(line)
        if match:
            date_str, time_str, sender, message = match.groups()
            try:
                timestamp = datetime.strptime(date_str + ", " + time_str, "%m/%d/%y, %I:%M %p")
                chat_data.append({"timestamp": timestamp, "sender": sender, "message": message})
            except ValueError:
                continue
    
    return chat_data


def extract_words(text):
    """Extract meaningful words from text"""
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    words = text.split()
    # Common stopwords in English
    stopwords = {
        "the", "is", "and", "to", "you", "a", "in", "for", "of", "on", 
        "it", "this", "that", "with", "be", "have", "from", "or", "an", "as"
    }
    return [word for word in words if word not in stopwords and len(word) > 2]


def extract_emojis(text):
    """Extract emojis from text safely"""
    try:
        return [char for char in text if char in emoji.EMOJI_DATA]
    except:
        # Fallback if emoji library has issues
        return []


def extract_links(text):
    """Extract URLs from text"""
    return re.findall(r'https?://\S+', text)


def analyze_chat(chat_data):
    """Analyze chat data and return comprehensive statistics"""
    
    if not chat_data:
        return {"error": "No chat data to analyze"}
    
    word_counter = Counter()
    emoji_counter = Counter()
    user_word_count = {}
    user_emoji_count = {}
    message_counts = Counter()
    message_lengths = {}
    sentiment_scores = {}
    link_counts = Counter()
    question_counts = Counter()
    ignored_messages = Counter()
    chat_energy = {}
    conversation_starters = Counter()
    user_phrases = {}
    response_times = {}

    previous_message = None
    user_timestamps = {}
    
    for idx, msg in enumerate(chat_data):
        text = msg["message"].strip()
        sender = msg["sender"].strip()
        timestamp = msg["timestamp"]

        # Initialize user data
        if sender not in user_timestamps:
            user_timestamps[sender] = []
            user_word_count[sender] = Counter()
            user_emoji_count[sender] = Counter()
            message_counts[sender] = 0
            question_counts[sender] = 0
            sentiment_scores[sender] = []
            user_phrases[sender] = Counter()
            response_times[sender] = []

        # Track timestamps for response time calculation
        user_timestamps[sender].append(timestamp)

        # Word Analysis
        words = extract_words(text)
        word_counter.update(words)
        user_word_count[sender].update(words)

        # Emoji Analysis
        emojis_found = extract_emojis(text)
        emoji_counter.update(emojis_found)
        user_emoji_count[sender].update(emojis_found)

        # Message Length
        message_lengths[sender] = max(message_lengths.get(sender, 0), len(text))

        # Sentiment Analysis
        try:
            polarity = TextBlob(text).sentiment.polarity
            sentiment_scores[sender].append(polarity)
        except:
            sentiment_scores[sender].append(0.5)

        # Links Shared
        links = extract_links(text)
        link_counts.update(links)

        # Questions Asked
        if "?" in text:
            question_counts[sender] += 1

        # Response Time Calculation
        if previous_message and previous_message["sender"] != sender:
            time_diff = (timestamp - previous_message["timestamp"]).total_seconds() / 60
            response_times[sender].append(time_diff)
        
        previous_message = msg

        # Common Phrases (bigrams)
        try:
            words_for_phrases = text.split()
            if len(words_for_phrases) >= 2:
                bigrams = list(ngrams(words_for_phrases, 2))
                user_phrases[sender].update([" ".join(bigram) for bigram in bigrams])
        except:
            pass

        # Message Count
        message_counts[sender] += 1
        
        # Conversation Starters
        if idx == 0 or (previous_message and previous_message["sender"] != sender):
            conversation_starters[sender] += 1

    # Calculate averages
    avg_response_time = {}
    for user, times in response_times.items():
        if times:
            avg_response_time[user] = round(sum(times) / len(times), 2)
        else:
            avg_response_time[user] = 0

    # Calculate average daily chat time
    if chat_data:
        total_duration = (chat_data[-1]["timestamp"] - chat_data[0]["timestamp"]).total_seconds()
        days = max(1, total_duration / (24 * 3600))
        avg_daily_chat_time = round(len(chat_data) / days, 2)
    else:
        avg_daily_chat_time = 0

    # Sentiment Analysis (0-10 scale)
    sentiment_summary = {}
    for user, scores in sentiment_scores.items():
        if scores:
            avg_sentiment = sum(scores) / len(scores)
            sentiment_summary[user] = round((avg_sentiment + 1) * 5, 2)  # Convert -1 to 1 range to 0-10
        else:
            sentiment_summary[user] = 5

    # Chat Energy Score (0-10 scale)
    chat_energy_score = {}
    for user in message_counts.keys():
        energy = (message_counts[user] / max(message_counts.values())) * 5
        energy += sentiment_summary[user] / 2
        chat_energy_score[user] = round(min(10, energy), 2)

    # Print Analysis
    print("\n" + "="*50)
    print("📊 WHATSAPP CHAT ANALYSIS REPORT")
    print("="*50)
    print(f"\n📌 Top 10 words used:")
    for word, count in word_counter.most_common(10):
        print(f"   {word}: {count}")
    
    print(f"\n📌 Top 10 words per user:")
    for user, words in user_word_count.items():
        print(f"   {user}: {words.most_common(5)}")
    
    print(f"\n😊 Top 5 emojis used:")
    for emoji_char, count in emoji_counter.most_common(5):
        print(f"   {emoji_char}: {count}")
    
    print(f"\n⏳ Average response time per user (minutes):")
    for user, time in avg_response_time.items():
        print(f"   {user}: {time} min")
    
    print(f"\n📊 Total messages sent by each user:")
    for user, count in message_counts.most_common():
        print(f"   {user}: {count}")
    
    print(f"\n⌛ Average messages per day: {avg_daily_chat_time}")
    
    print(f"\n📝 Longest message per user:")
    for user, length in sorted(message_lengths.items(), key=lambda x: x[1], reverse=True):
        print(f"   {user}: {length} characters")
    
    print(f"\n🔗 Most common links shared:")
    for link, count in link_counts.most_common(5):
        print(f"   {link}: {count}")
    
    print(f"\n📈 Sentiment analysis per user (0-10):")
    for user, score in sentiment_summary.items():
        print(f"   {user}: {score}")
    
    print(f"\n🔥 Chat energy score per user (0-10):")
    for user, score in chat_energy_score.items():
        print(f"   {user}: {score}")
    
    print(f"\n❓ Questions asked per user:")
    for user, count in question_counts.most_common():
        if count > 0:
            print(f"   {user}: {count}")
    
    print(f"\n� Conversation starters:")
    for user, count in conversation_starters.most_common():
        print(f"   {user}: {count}")
    
    print("\n" + "="*50 + "\n")

    # Return comprehensive data
    return {
        "top_words": word_counter.most_common(10),
        "top_words_per_user": {user: words.most_common(10) for user, words in user_word_count.items()},
        "top_emojis_used": emoji_counter.most_common(5),
        "top_emojis_per_user": {user: emojis.most_common(5) for user, emojis in user_emoji_count.items()},
        "average_response_time": avg_response_time,
        "total_messages_per_user": dict(message_counts),
        "average_daily_messages": avg_daily_chat_time,
        "longest_message_per_user": message_lengths,
        "most_common_links": link_counts.most_common(5),
        "sentiment_analysis": sentiment_summary,
        "chat_energy_score": chat_energy_score,
        "most_common_phrases_per_user": {user: phrases.most_common(5) for user, phrases in user_phrases.items()},
        "questions_asked_per_user": dict(question_counts),
        "conversation_starters": dict(conversation_starters)
    }


# Main execution
if __name__ == "__main__":
    try:
        chat_data = parse_chat("chat.txt")
        if chat_data:
            print(f"\n✅ Successfully parsed {len(chat_data)} messages")
            analyze_chat(chat_data)
        else:
            print("❌ No messages found in chat.txt")
    except FileNotFoundError:
        print("❌ Error: chat.txt file not found")