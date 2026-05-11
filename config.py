"""
Configuration file for WhatsApp Chat Analyzer
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# API Configuration
API_HOST = "127.0.0.1"
API_PORT = 8000
API_RELOAD = True

# Chat file configuration
CHAT_FILE_PATH = os.path.join(BASE_DIR, "chat.txt")

# Stopwords for word analysis
STOPWORDS = {
    "the", "is", "and", "to", "you", "a", "in", "for", "of", "on", 
    "it", "this", "that", "with", "be", "have", "from", "or", "an", "as",
    "at", "by", "are", "was", "were", "been", "being", "do", "does", "did",
    "will", "would", "should", "could", "may", "might", "must", "can", "has"
}

# Minimum word length to include in analysis
MIN_WORD_LENGTH = 2

# Number of top items to return in analysis
TOP_N = 10

# Date format for WhatsApp exports
WHATSAPP_DATE_FORMAT = "%m/%d/%y, %I:%M %p"
