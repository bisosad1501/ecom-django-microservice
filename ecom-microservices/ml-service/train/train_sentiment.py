import os
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Embedding, LSTM, SpatialDropout1D, Bidirectional, Input, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import joblib
import pickle
import re
import nltk
from nltk.corpus import stopwords

# 📁 Cấu hình thư mục
MODEL_DIR = "ml-service/train/models"
os.makedirs(MODEL_DIR, exist_ok=True)

# 📥 Tải NLTK resources
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# 🧹 Hàm tiền xử lý văn bản
def preprocess_text(text):
    if isinstance(text, str):
        # Chuyển thành chữ thường
        text = text.lower()
        # Loại bỏ HTML tags
        text = re.sub(r'<.*?>', '', text)
        # Loại bỏ các ký tự đặc biệt và số
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\d+', '', text)
        # Loại bỏ stopwords
        stop_words = set(stopwords.words('english'))
        text = ' '.join([word for word in text.split() if word not in stop_words])
        return text
    return ""

# 📊 Hàm tạo biểu đồ đánh giá mô hình
def plot_training_history(history, filename="model_history.png"):
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='lower right')
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper right')
    
    plt.tight_layout()
    plt.savefig(os.path.join(MODEL_DIR, filename))
    plt.close()

# 📥 Load dữ liệu
print("🔄 Loading dataset...")
DATA_PATH = "ml-service/train/datasets/sentiment_train.csv"
df = pd.read_csv(DATA_PATH)

# 🔄 Tiền xử lý dữ liệu
print("🧹 Preprocessing text data...")
df['processed_review'] = df['review'].apply(preprocess_text)

# Chuyển nhãn thành số
sentiment_mapping = {'negative': 0, 'neutral': 1, 'positive': 2}
df['sentiment_label'] = df['sentiment'].map(sentiment_mapping)

# ✂️ Chia dữ liệu thành train & validation & test
X = df['processed_review']
y = df['sentiment_label']
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp)

# 🔠 Tokenization và Padding
print("🔠 Tokenizing text...")
MAX_WORDS = 10000  # Số lượng từ tối đa trong từ điển
MAX_SEQUENCE_LENGTH = 200  # Độ dài tối đa của mỗi văn bản

tokenizer = Tokenizer(num_words=MAX_WORDS, oov_token="<OOV>")
tokenizer.fit_on_texts(X_train)

# Lưu tokenizer
with open(os.path.join(MODEL_DIR, 'tokenizer.pickle'), 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Chuyển đổi văn bản thành chuỗi số
X_train_seq = tokenizer.texts_to_sequences(X_train)
X_val_seq = tokenizer.texts_to_sequences(X_val)
X_test_seq = tokenizer.texts_to_sequences(X_test)

# Padding chuỗi
X_train_pad = pad_sequences(X_train_seq, maxlen=MAX_SEQUENCE_LENGTH, padding='post')
X_val_pad = pad_sequences(X_val_seq, maxlen=MAX_SEQUENCE_LENGTH, padding='post')
X_test_pad = pad_sequences(X_test_seq, maxlen=MAX_SEQUENCE_LENGTH, padding='post')

# 🏗 Xây dựng mô hình LSTM
print("🏗 Building model...")
EMBEDDING_DIM = 128  # Kích thước vector nhúng
vocab_size = len(tokenizer.word_index) + 1  # Kích thước từ điển

# Định nghĩa kiến trúc mô hình
model = Sequential()
model.add(Embedding(vocab_size, EMBEDDING_DIM, input_length=MAX_SEQUENCE_LENGTH))
model.add(SpatialDropout1D(0.2))
model.add(Bidirectional(LSTM(128, dropout=0.2, recurrent_dropout=0.2)))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(3, activation='softmax'))  # 3 classes: negative, neutral, positive

# Biên dịch mô hình
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Tóm tắt thông tin mô hình
model.summary()

# 🏋️‍♂️ Huấn luyện mô hình
print("🏋️‍♂️ Training model...")
early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
checkpoint = ModelCheckpoint(
    os.path.join(MODEL_DIR, 'best_model.h5'),
    monitor='val_accuracy',
    save_best_only=True,
    mode='max'
)

history = model.fit(
    X_train_pad, y_train,
    validation_data=(X_val_pad, y_val),
    epochs=10,
    batch_size=64,
    callbacks=[early_stopping, checkpoint]
)

# 📊 Vẽ biểu đồ kết quả huấn luyện
plot_training_history(history)

# 🎯 Đánh giá mô hình trên tập test
print("🎯 Evaluating model...")
y_pred_proba = model.predict(X_test_pad)
y_pred = np.argmax(y_pred_proba, axis=1)

print("📊 Classification Report:")
print(classification_report(y_test, y_pred, target_names=['negative', 'neutral', 'positive']))

# Tính toán độ chính xác
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Accuracy: {accuracy:.4f}")

# Tạo ma trận nhầm lẫn
cm = confusion_matrix(y_test, y_pred)
print("📊 Confusion Matrix:")
print(cm)

# 💾 Lưu mô hình
print("💾 Saving model...")
model.save(os.path.join(MODEL_DIR, 'sentiment_lstm.h5'))

# Lưu mapping nhãn
joblib.dump(sentiment_mapping, os.path.join(MODEL_DIR, 'sentiment_mapping.pkl'))

print("✅ Training complete!")
print(f"📁 Model saved to: {os.path.join(MODEL_DIR, 'sentiment_lstm.h5')}")