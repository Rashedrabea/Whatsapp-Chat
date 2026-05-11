# 📊 WhatsApp Chat Analyzer

## 🚀 Overview

WhatsApp Chat Analyzer is a FastAPI-based tool that allows users to upload and analyze WhatsApp chat exports. It provides valuable insights into user interactions, sentiment trends, frequently used words and emojis, response times, and more. The project includes a backend built with FastAPI that processes chat data and returns analytical insights.

## 🎯 Features

- 📂 **Upload WhatsApp Chat Exports** (TXT format)
- 🔍 **Analyze Sentiment** of messages
- ⏳ **Measure Response Times** between users
- 📊 **Find Top Words and Emojis** used
- 📅 **Identify Most Active Days & Hours**
- 📈 **Generate Insights on Conversation Patterns**
- 🌐 **REST API** for easy integration
- 📌 **Top 10 words** used globally
- 📌 **Top 10 words** per user
- 😊 **Top 5 emojis** per user
- ⏳ **Average response time** per user
- 📊 **Total messages** sent by each user
- ⌛ **Average daily** chatting time
- 📝 **Longest message** per user
- 🔗 **Most common links** shared
- 🚀 **Conversation starters** per user
- 📈 **Sentiment analysis** per user
- 🔥 **Chat energy score** (0-10 scale)
- ❓ **Questions asked** per user
- 📌 **Most common phrases** per user

## 🏗 Tech Stack

- **Backend:** FastAPI, Uvicorn
- **Data Processing:** NLTK, TextBlob, Emoji
- **Others:** Pandas, Python 3.8+

## 📂 Project Structure

```
whatsapp-chat-analyzer/
├── main.py              # FastAPI application
├── analyze_chat.py      # Chat analysis logic
├── parse_chat.py        # Chat file parser
├── utils.py             # Utility functions
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── chat.txt             # Sample chat export (add your own)
├── README.md            # This file
└── LICENSE              # MIT License
```

## 🔧 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### 1️⃣ Clone/Download the Repository

```bash
# If using git
git clone https://github.com/yourusername/whatsapp-chat-analyzer.git
cd whatsapp-chat-analyzer

# Or simply download and extract the files
```

### 2️⃣ Create Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Prepare Your Chat Export

1. Open WhatsApp on your phone
2. Go to the chat you want to analyze
3. Tap Options → More → Export Chat → Without Media
4. Save the exported `.txt` file as `chat.txt` in the project folder

### 5️⃣ Run the Application

#### Option A: Start the API Server

```bash
# Windows
python main.py

# macOS/Linux
python3 main.py
```

Server will be available at: `http://127.0.0.1:8000`

#### Option B: Parse and Analyze Locally

```bash
# Windows
python parse_chat.py
python analyze_chat.py

# macOS/Linux
python3 parse_chat.py
python3 analyze_chat.py
```

## 🔗 API Endpoints

### GET `/` - Welcome Message

Returns API information and available endpoints.

```bash
curl http://127.0.0.1:8000/
```

### GET `/health/` - Health Check

Check if the API is running.

```bash
curl http://127.0.0.1:8000/health/
```

### POST `/upload/` - Upload and Analyze Chat

Upload a WhatsApp chat export file for analysis.

```bash
curl -X POST -F "file=@chat.txt" http://127.0.0.1:8000/upload/
```

**Response Example:**

```json
{
  "filename": "chat.txt",
  "status": "success",
  "data": {
    "top_words": [["hello", 45], ["world", 32], ...],
    "top_emojis_used": [["😊", 120], ["❤️", 95], ...],
    "average_response_time": {"User1": 2.5, "User2": 1.8},
    "total_messages_per_user": {"User1": 500, "User2": 480},
    ...
  }
}
```

## � Analysis Output

The analyzer provides:

### Text Statistics

- **Top Words:** Most frequently used words
- **Word Count Per User:** Individual word usage patterns
- **Message Count:** Total messages per user
- **Average Response Time:** Time between responses in minutes

### Emoji Analysis

- **Top Emojis:** Most frequently used emojis globally
- **Top Emojis Per User:** Individual emoji preferences

### Content Analysis

- **Links Shared:** Most common URLs shared
- **Questions Asked:** Questions per user
- **Conversation Starters:** Who initiates conversations
- **Common Phrases:** Frequent two-word combinations

### Sentiment Analysis (0-10 Scale)

- **Sentiment Score:** Overall tone of messages per user
- **Chat Energy:** Activity and engagement level

## 🛠 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:** Make sure to activate your virtual environment and install requirements

```bash
pip install -r requirements.txt
```

### Issue: "chat.txt file not found"

**Solution:** Make sure your chat export file is named exactly `chat.txt` and is in the same folder as the scripts.

### Issue: "No valid messages found"

**Solution:**

- Verify your chat export is in the correct format
- Check that the file isn't empty
- Ensure the date format matches WhatsApp's format

### Issue: CORS errors

**Solution:** CORS is already enabled in `main.py`. If you still have issues, ensure you're accessing the correct API endpoint.

## 📝 Chat Export Format

WhatsApp exports follow this format:

```
1/15/24, 2:30 PM - User1: Hello!
1/15/24, 2:35 PM - User2: Hi there!
1/15/24, 2:40 PM - User1: How are you?
1/15/24, 2:45 PM - User2: I'm doing great! 😊
```

## 🤝 Contributing

Feel free to fork, contribute, or raise issues. PRs are welcome!

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Reporting Issues

If you find a bug or have a suggestion, please open an issue on GitHub.

---

**Created with ❤️ for WhatsApp chat analysis**

Last Updated: May 2026

✨ Happy Chat Analyzing! ✨
