"""
Module tiện ích xử lý văn bản cho phân tích cảm xúc
"""

import re
import unicodedata
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from typing import List, Optional

# Đảm bảo stopwords và tokenizer đã được tải
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def preprocess_text(text: str, remove_stopwords: bool = False) -> str:
    """
    Tiền xử lý văn bản
    
    Args:
        text (str): Văn bản cần xử lý
        remove_stopwords (bool): Có loại bỏ stopwords hay không
    
    Returns:
        str: Văn bản đã xử lý
    """
    if not text:
        return ""
    
    # Chuyển về Unicode NFC
    text = unicodedata.normalize('NFC', text)
    
    # Loại bỏ ký tự đặc biệt
    text = re.sub(r'[^\w\s.,!?]', ' ', text)
    
    # Loại bỏ khoảng trắng thừa
    text = re.sub(r'\s+', ' ', text)
    
    # Chuyển về chữ thường
    text = text.lower().strip()
    
    # Loại bỏ stopwords nếu cần
    if remove_stopwords:
        stop_words = set(stopwords.words('english'))
        tokens = word_tokenize(text)
        tokens = [word for word in tokens if word not in stop_words]
        text = ' '.join(tokens)
    
    return text

def tokenize_text(text: str) -> List[str]:
    """
    Tách từ trong văn bản
    
    Args:
        text (str): Văn bản cần tách từ
    
    Returns:
        List[str]: Danh sách các từ
    """
    return word_tokenize(text)

def remove_stopwords(tokens: List[str], language: str = 'english') -> List[str]:
    """
    Loại bỏ stopwords từ danh sách các từ
    
    Args:
        tokens (List[str]): Danh sách các từ
        language (str): Ngôn ngữ của stopwords
    
    Returns:
        List[str]: Danh sách các từ đã loại bỏ stopwords
    """
    stop_words = set(stopwords.words(language))
    return [word for word in tokens if word not in stop_words]

def clean_html(text: str) -> str:
    """
    Loại bỏ các thẻ HTML
    
    Args:
        text (str): Văn bản HTML
    
    Returns:
        str: Văn bản đã loại bỏ HTML
    """
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def extract_text_features(text: str, include_ngrams: bool = False, max_ngram: int = 3) -> List[str]:
    """
    Trích xuất đặc trưng từ văn bản
    
    Args:
        text (str): Văn bản cần trích xuất đặc trưng
        include_ngrams (bool): Có bao gồm n-grams hay không
        max_ngram (int): N-gram tối đa
    
    Returns:
        List[str]: Danh sách các đặc trưng
    """
    # Tiền xử lý
    processed_text = preprocess_text(text, remove_stopwords=True)
    tokens = tokenize_text(processed_text)
    
    # Trích xuất đặc trưng
    features = tokens.copy()
    
    # Thêm n-grams nếu cần
    if include_ngrams and len(tokens) > 1:
        for n in range(2, min(max_ngram + 1, len(tokens) + 1)):
            for i in range(len(tokens) - n + 1):
                ngram = ' '.join(tokens[i:i+n])
                features.append(ngram)
    
    return features