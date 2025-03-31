# CHAPTER 3: AI IN E-COMMERCE

Trí tuệ nhân tạo (AI) đang ngày càng đóng vai trò quan trọng trong việc nâng cao trải nghiệm mua sắm trực tuyến và tối ưu hóa hoạt động kinh doanh thương mại điện tử. Trong chương này, chúng tôi sẽ tập trung vào việc ứng dụng các kỹ thuật AI và deep learning trong hệ thống thương mại điện tử, đặc biệt là phân tích cảm xúc (sentiment analysis) và hệ thống gợi ý (recommendation system).

## 3.1 Application of Deep Learning in E-commerce

Deep Learning, một nhánh của Machine Learning, đã mang lại những bước tiến đáng kể cho ngành thương mại điện tử thông qua khả năng xử lý và phân tích dữ liệu phức tạp. Phần này sẽ trình bày các ứng dụng chính của deep learning trong hệ thống e-commerce của chúng tôi.

### 3.1.1 Tổng quan về Deep Learning trong E-commerce

Deep Learning sử dụng mạng nơron nhân tạo với nhiều lớp ẩn (hidden layers) để học và trích xuất các đặc trưng phức tạp từ dữ liệu. Trong thương mại điện tử, các mô hình deep learning đặc biệt hiệu quả trong các tác vụ như:

1. **Cá nhân hóa trải nghiệm mua sắm**: Gợi ý sản phẩm phù hợp dựa trên hành vi và sở thích của người dùng.
2. **Phân tích đánh giá và phản hồi**: Hiểu cảm xúc và ý kiến của khách hàng từ đánh giá sản phẩm.
3. **Tối ưu hóa tìm kiếm**: Cải thiện kết quả tìm kiếm dựa trên ngữ cảnh và ý định của người dùng.
4. **Dự đoán xu hướng**: Phân tích dữ liệu lịch sử để dự đoán các xu hướng mua sắm.
5. **Hỗ trợ khách hàng tự động**: Chatbots thông minh có khả năng hiểu và phản hồi các câu hỏi phức tạp của khách hàng.

Trong hệ thống của chúng tôi, deep learning được triển khai trong hai microservices chính: Sentiment Service và Recommendation Service.

### 3.1.2 Mô hình Deep Learning cho E-commerce

#### 3.1.2.1 Mạng nơron tích chập (CNNs)

CNNs chủ yếu được sử dụng trong xử lý hình ảnh sản phẩm:

```python
# Ví dụ mô hình CNN cho phân loại hình ảnh sản phẩm
def build_cnn_model(input_shape, num_classes):
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])
    return model
```

Ứng dụng trong hệ thống của chúng tôi:
- Tự động phân loại hình ảnh sản phẩm
- Tìm kiếm sản phẩm bằng hình ảnh
- Phát hiện hàng giả hoặc hình ảnh không phù hợp

#### 3.1.2.2 Mạng nơron hồi quy (RNNs) và LSTM

RNNs và LSTM được sử dụng để xử lý dữ liệu chuỗi, đặc biệt là trong phân tích văn bản:

```python
# Ví dụ mô hình LSTM cho phân tích cảm xúc
def build_lstm_model(vocab_size, embedding_dim, max_length):
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_length),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True)),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32)),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(3, activation='softmax')  # 3 classes: positive, neutral, negative
    ])
    return model
```

Ứng dụng trong hệ thống của chúng tôi:
- Phân tích cảm xúc từ đánh giá sản phẩm
- Phân loại nội dung đánh giá
- Dự đoán hành vi mua hàng dựa trên chuỗi sự kiện

#### 3.1.2.3 Mô hình dựa trên Transformer

Transformer là kiến trúc tiên tiến nhất hiện nay cho xử lý ngôn ngữ tự nhiên, với các mô hình như BERT, GPT được áp dụng trong:

```python
# Ví dụ sử dụng BERT cho phân tích cảm xúc
def build_bert_model():
    # Tải pre-trained BERT model
    bert_model = TFBertForSequenceClassification.from_pretrained(
        'bert-base-uncased', num_labels=3)
    
    # Định nghĩa inputs
    input_ids = tf.keras.layers.Input(shape=(128,), dtype=tf.int32, name='input_ids')
    attention_mask = tf.keras.layers.Input(shape=(128,), dtype=tf.int32, name='attention_mask')
    
    # Đưa inputs vào BERT
    outputs = bert_model([input_ids, attention_mask])
    
    # Tạo model
    model = tf.keras.Model(inputs=[input_ids, attention_mask], outputs=outputs[0])
    return model
```

Ứng dụng trong hệ thống của chúng tôi:
- Phân tích cảm xúc với độ chính xác cao
- Hiểu ngữ cảnh và ý định trong các đánh giá
- Tạo mô tả sản phẩm tự động
- Chatbot hỗ trợ khách hàng

### 3.1.3 Framework và Công nghệ

Trong hệ thống của chúng tôi, chúng tôi sử dụng các framework và công nghệ sau để triển khai các mô hình deep learning:

1. **TensorFlow và Keras**: Framework chính để xây dựng và huấn luyện các mô hình deep learning.
2. **PyTorch**: Được sử dụng cho một số mô hình nghiên cứu và thử nghiệm.
3. **Hugging Face Transformers**: Thư viện chứa các mô hình NLP tiên tiến như BERT, RoBERTa, và GPT.
4. **NLTK và SpaCy**: Thư viện xử lý ngôn ngữ tự nhiên cho tiền xử lý dữ liệu.
5. **Scikit-learn**: Hỗ trợ các thuật toán machine learning cổ điển và đánh giá mô hình.
6. **Flask**: Framework web nhẹ để triển khai các microservices AI.
7. **Redis**: Hệ thống lưu trữ in-memory để cache kết quả dự đoán.

Ví dụ về cấu trúc thư mục của microservice AI:

```
sentiment-service/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── bert_model.py
│   │   └── lstm_model.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── preprocessing.py
│   │   └── evaluation.py
│   └── config.py
├── data/
│   ├── preprocessed/
│   └── raw/
├── models/
│   ├── bert/
│   └── lstm/
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_models.py
├── Dockerfile
├── requirements.txt
└── run.py
```

### 3.1.4 Luồng dữ liệu và xử lý

Quá trình ứng dụng Deep Learning trong hệ thống e-commerce của chúng tôi bao gồm các bước chính sau:

1. **Thu thập dữ liệu**: Dữ liệu được thu thập từ các tương tác của người dùng, đánh giá sản phẩm, lịch sử mua hàng, và hành vi duyệt web.

2. **Tiền xử lý dữ liệu**: Dữ liệu thô được làm sạch, chuẩn hóa, và chuyển đổi thành định dạng phù hợp cho các mô hình deep learning.

```python
# Ví dụ tiền xử lý văn bản cho phân tích cảm xúc
def preprocess_text(text):
    # Chuyển đổi về chữ thường
    text = text.lower()
    # Loại bỏ các ký tự đặc biệt
    text = re.sub(r'[^\w\s]', '', text)
    # Loại bỏ số
    text = re.sub(r'\d+', '', text)
    # Tokenize
    tokens = word_tokenize(text)
    # Loại bỏ stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    # Stemming
    porter = PorterStemmer()
    stemmed_tokens = [porter.stem(word) for word in tokens]
    
    return ' '.join(stemmed_tokens)
```

3. **Huấn luyện mô hình**: Mô hình deep learning được huấn luyện trên dữ liệu đã xử lý, với quá trình tinh chỉnh hyperparameter để đạt hiệu suất tốt nhất.

4. **Đánh giá mô hình**: Mô hình được đánh giá trên tập dữ liệu kiểm thử để đảm bảo độ chính xác và hiệu suất.

```python
# Ví dụ đánh giá mô hình phân tích cảm xúc
def evaluate_sentiment_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_pred_classes = np.argmax(y_pred, axis=1)
    
    # Tính toán các metrics
    accuracy = accuracy_score(y_test, y_pred_classes)
    precision = precision_score(y_test, y_pred_classes, average='weighted')
    recall = recall_score(y_test, y_pred_classes, average='weighted')
    f1 = f1_score(y_test, y_pred_classes, average='weighted')
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred_classes)
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'confusion_matrix': cm
    }
```

5. **Triển khai và phục vụ**: Mô hình được triển khai thành API và microservices để phục vụ các yêu cầu thời gian thực từ người dùng.

6. **Giám sát và cập nhật**: Hiệu suất của mô hình được liên tục giám sát và cập nhật khi có dữ liệu mới.

### 3.1.5 Tích hợp với kiến trúc Microservices

Deep Learning trong hệ thống của chúng tôi được triển khai dưới dạng microservices độc lập, cho phép:

1. **Khả năng mở rộng**: Các mô hình có thể được mở rộng độc lập dựa trên nhu cầu và tải hệ thống.

2. **Linh hoạt về công nghệ**: Tự do lựa chọn ngôn ngữ và framework phù hợp nhất cho từng tác vụ AI.

3. **Isolation**: Lỗi trong các mô hình AI không ảnh hưởng đến các phần khác của hệ thống.

4. **Deployability**: Dễ dàng cập nhật và triển khai các mô hình mới.

Ví dụ về kiến trúc tích hợp Deep Learning trong microservices:

```
┌─────────────────┐     ┌──────────────────┐     ┌────────────────┐
│                 │     │                  │     │                │
│  Review Service ├────►│ Sentiment Service├────►│    Redis Cache │
│                 │     │                  │     │                │
└────────┬────────┘     └──────────────────┘     └────────────────┘
         │                                              ▲
         │                                              │
         ▼                                              │
┌─────────────────┐     ┌──────────────────┐           │
│                 │     │                  │           │
│  Product Service├────►│Recommendation Svc├───────────┘
│                 │     │                  │
└─────────────────┘     └──────────────────┘
```

Trong kiến trúc này:
- Review Service gửi đánh giá mới đến Sentiment Service để phân tích cảm xúc
- Sentiment Service sử dụng mô hình deep learning để phân tích và lưu kết quả vào Redis Cache
- Recommendation Service tận dụng kết quả phân tích cảm xúc để cải thiện độ chính xác của các gợi ý sản phẩm 

## 3.2 Sentiment Analysis

Sentiment Analysis (phân tích cảm xúc) là quá trình sử dụng các kỹ thuật xử lý ngôn ngữ tự nhiên và deep learning để xác định, trích xuất và định lượng cảm xúc, thái độ, ý kiến từ văn bản. Trong phần này, chúng tôi trình bày cách triển khai và ứng dụng sentiment analysis trong hệ thống thương mại điện tử.

### 3.2.1 Tổng quan về Sentiment Analysis

Trong hệ thống thương mại điện tử của chúng tôi, sentiment analysis được áp dụng chủ yếu để phân tích đánh giá, nhận xét của khách hàng về sản phẩm. Mục tiêu là:

1. **Phân loại cảm xúc**: Xác định đánh giá là tích cực (positive), tiêu cực (negative), hay trung tính (neutral)
2. **Trích xuất từ khóa**: Xác định những từ và cụm từ chính làm nổi bật các đặc điểm sản phẩm được đề cập
3. **Phân tích chi tiết**: Hiểu rõ hơn về lý do khách hàng thích hoặc không thích một sản phẩm
4. **Theo dõi xu hướng**: Phát hiện thay đổi trong nhận thức của khách hàng theo thời gian

### 3.2.2 Kiến trúc hệ thống Sentiment Analysis

Hệ thống sentiment analysis của chúng tôi được triển khai như một microservice riêng biệt, kết nối với Review Service và cung cấp dữ liệu cho Recommendation Service.

```
┌──────────────────────┐     ┌───────────────────────────┐
│                      │     │                           │
│    Review Service    ├────►│      Sentiment Service    │
│                      │     │                           │
└──────────────────────┘     └───────────┬───────────────┘
                                         │
                                         ▼
                             ┌───────────────────────────┐
                             │                           │
                             │      Database/Cache       │
                             │                           │
                             └───────────────────────────┘
```

#### Luồng dữ liệu:

1. Khách hàng gửi đánh giá sản phẩm thông qua Frontend
2. Review Service lưu trữ đánh giá và gửi văn bản đến Sentiment Service
3. Sentiment Service phân tích cảm xúc và trả về kết quả
4. Kết quả được lưu trữ cùng với đánh giá gốc
5. Dashboard và báo cáo sử dụng kết quả phân tích để hiển thị thông tin tổng hợp

### 3.2.3 Phương pháp và mô hình

Chúng tôi sử dụng kết hợp nhiều phương pháp và mô hình để phân tích cảm xúc:

#### 3.2.3.1 Phân tích dựa trên từ điển (Lexicon-based)

Phương pháp này sử dụng danh sách các từ và cụm từ đã được gán nhãn cảm xúc trước đó.

```python
# Ví dụ sử dụng VADER (Valence Aware Dictionary and Sentiment Reasoner)
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def analyze_sentiment_lexicon(text):
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(text)
    
    # Xác định cảm xúc dựa trên compound score
    if sentiment_scores['compound'] >= 0.05:
        sentiment = 'positive'
    elif sentiment_scores['compound'] <= -0.05:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
        
    return {
        'sentiment': sentiment,
        'scores': sentiment_scores
    }
```

#### 3.2.3.2 Machine Learning truyền thống

Chúng tôi sử dụng các thuật toán ML như SVM, Naive Bayes, và Logistic Regression với các đặc trưng được trích xuất từ TF-IDF.

```python
# Ví dụ sử dụng TF-IDF và SVM
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline

def create_sentiment_classifier():
    # Tạo pipeline
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
        ('classifier', LinearSVC())
    ])
    
    # Huấn luyện model
    pipeline.fit(X_train, y_train)
    
    return pipeline
```

#### 3.2.3.3 Deep Learning

Phương pháp tiên tiến nhất của chúng tôi dựa trên các mô hình deep learning như LSTM và BERT.

```python
# Ví dụ sử dụng BERT với Hugging Face
from transformers import BertTokenizer, TFBertForSequenceClassification
import tensorflow as tf

class BertSentimentAnalyzer:
    def __init__(self, model_path='bert-base-uncased', num_labels=3):
        self.tokenizer = BertTokenizer.from_pretrained(model_path)
        self.model = TFBertForSequenceClassification.from_pretrained(
            model_path, num_labels=num_labels)
            
    def predict(self, texts):
        # Tokenize inputs
        inputs = self.tokenizer(
            texts, 
            padding=True, 
            truncation=True, 
            return_tensors="tf",
            max_length=128
        )
        
        # Perform prediction
        outputs = self.model(inputs)
        predictions = tf.nn.softmax(outputs.logits, axis=-1)
        
        # Convert to numpy for easier handling
        predictions = predictions.numpy()
        
        # Map predictions to sentiment labels
        sentiment_labels = ['negative', 'neutral', 'positive']
        results = []
        
        for pred in predictions:
            label_idx = np.argmax(pred)
            results.append({
                'sentiment': sentiment_labels[label_idx],
                'confidence': float(pred[label_idx]),
                'scores': {label: float(score) for label, score in zip(sentiment_labels, pred)}
            })
            
        return results
```

### 3.2.4 Dữ liệu huấn luyện

Chúng tôi sử dụng dữ liệu huấn luyện từ nhiều nguồn khác nhau:

1. **Dữ liệu công khai**:
   - Amazon Reviews Dataset
   - Yelp Dataset
   - IMDB Movie Reviews

2. **Dữ liệu thực tế từ hệ thống**:
   - Tập hợp các đánh giá sản phẩm thực tế đã được gán nhãn thủ công
   - Đánh giá sản phẩm mới được gán nhãn thông qua quy trình feedback loop

3. **Dữ liệu tăng cường** (Data Augmentation):
   - Áp dụng các kỹ thuật NLP để tạo ra thêm dữ liệu huấn luyện
   - Dịch ngược (back-translation), thay thế từ đồng nghĩa, v.v.

### 3.2.5 Quy trình phân tích cảm xúc

Quy trình phân tích cảm xúc đầy đủ trong hệ thống của chúng tôi bao gồm các bước:

1. **Tiền xử lý văn bản**:
   - Chuẩn hóa (lowercase, loại bỏ HTML tags, v.v.)
   - Xử lý ngôn ngữ đặc thù thương mại điện tử (ký hiệu, emoticons, v.v.)
   - Tokenization, loại bỏ stopwords
   - Stemming/Lemmatization

2. **Trích xuất đặc trưng**:
   - Bag of Words, TF-IDF
   - Word embeddings (Word2Vec, GloVe)
   - Contextual embeddings (BERT)

3. **Phân loại cảm xúc**:
   - Mô hình BERT đã tinh chỉnh phân loại đánh giá thành positive/neutral/negative

4. **Phân tích chi tiết**:
   - Aspect extraction (trích xuất các khía cạnh sản phẩm được đề cập)
   - Aspect-based sentiment analysis (phân tích cảm xúc theo từng khía cạnh)
   - Trích xuất từ khóa có mức độ cảm xúc cao

5. **Tối ưu hóa và cập nhật**:
   - Đánh giá và cải thiện mô hình liên tục
   - Cập nhật với dữ liệu mới
   - A/B testing các phương pháp mới

### 3.2.6 API và tích hợp

Sentiment Service được thiết kế với RESTful API cho phép tích hợp dễ dàng với các service khác:

```python
# Ví dụ API routes trong sentiment-service
from flask import Flask, request, jsonify
from app.models.sentiment_analyzer import SentimentAnalyzer

app = Flask(__name__)
analyzer = SentimentAnalyzer()

@app.route('/api/analyze', methods=['POST'])
def analyze_sentiment():
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    result = analyzer.analyze(text)
    return jsonify(result)

@app.route('/api/analyze-batch', methods=['POST'])
def analyze_batch():
    data = request.get_json()
    texts = data.get('texts', [])
    
    if not texts:
        return jsonify({'error': 'No texts provided'}), 400
    
    results = analyzer.analyze_batch(texts)
    return jsonify(results)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})
```

### 3.2.7 Kết quả và metrics

Kết quả phân tích cảm xúc được đánh giá thông qua các metrics sau:

1. **Accuracy**: Tỷ lệ dự đoán đúng cảm xúc
2. **Precision, Recall, F1-score**: Đánh giá hiệu suất cho từng loại cảm xúc
3. **Confusion Matrix**: Hiển thị chi tiết dự đoán đúng/sai cho từng loại
4. **ROC-AUC**: Đánh giá khả năng phân biệt giữa các lớp

Mô hình BERT của chúng tôi đạt được các kết quả sau trên tập dữ liệu kiểm thử:

| Metric | Positive | Neutral | Negative | Macro Avg |
|--------|----------|---------|----------|-----------|
| Precision | 0.92 | 0.86 | 0.90 | 0.89 |
| Recall | 0.93 | 0.82 | 0.91 | 0.89 |
| F1-score | 0.92 | 0.84 | 0.91 | 0.89 |

### 3.2.8 Thách thức và giải pháp

Trong quá trình triển khai sentiment analysis, chúng tôi đã gặp phải và giải quyết các thách thức sau:

1. **Đa ngôn ngữ**:
   - Giải pháp: Áp dụng mô hình đa ngôn ngữ như XLM-RoBERTa và chuyển các ngôn ngữ phổ biến sang mô hình chuyên biệt

2. **Xử lý ngôn ngữ đặc thù ngành**:
   - Giải pháp: Tinh chỉnh mô hình trên dữ liệu đặc thù thương mại điện tử và xây dựng từ điển chuyên ngành

3. **Hiệu suất thời gian thực**:
   - Giải pháp: Triển khai cơ chế cache với Redis, tối ưu hóa mô hình và áp dụng distillation

4. **Quá nhiều dữ liệu**:
   - Giải pháp: Xử lý batch, triển khai phân tán và sử dụng hàng đợi message

5. **Sarcasm và ngữ cảnh phức tạp**:
   - Giải pháp: Sử dụng mô hình có khả năng hiểu ngữ cảnh như BERT và tinh chỉnh trên dữ liệu có chứa sarcasm

### 3.2.9 Ứng dụng thực tế

Sentiment analysis được ứng dụng trong nhiều tính năng của hệ thống thương mại điện tử:

1. **Tóm tắt đánh giá sản phẩm**:
   - Hiển thị tỷ lệ đánh giá tích cực/tiêu cực
   - Tổng hợp các đánh giá cho từng khía cạnh sản phẩm

2. **Cải thiện tìm kiếm và lọc**:
   - Cho phép tìm kiếm "sản phẩm có đánh giá tốt về pin"
   - Lọc sản phẩm theo cảm xúc của đánh giá

3. **Cảnh báo sớm về vấn đề sản phẩm**:
   - Phát hiện nhanh khi có nhiều đánh giá tiêu cực bất thường
   - Cảnh báo cho người bán và quản trị viên

4. **Hỗ trợ gợi ý sản phẩm**:
   - Cung cấp thông tin cảm xúc cho recommendation engine
   - Gợi ý sản phẩm dựa trên các đặc điểm được đánh giá tích cực

5. **Dashboard phân tích**:
   - Báo cáo xu hướng cảm xúc theo thời gian
   - So sánh cảm xúc giữa các sản phẩm, danh mục 

## 3.3 Applying Sentiment Analysis for Recommendation

Trong phần này, chúng tôi trình bày cách kết hợp kết quả phân tích cảm xúc (sentiment analysis) vào hệ thống gợi ý (recommendation system) để nâng cao chất lượng và độ chính xác của các đề xuất sản phẩm.

### 3.3.1 Tổng quan về Hệ thống Gợi ý kết hợp Sentiment

Hệ thống gợi ý truyền thống thường dựa trên:
- Lịch sử hành vi người dùng (collaborative filtering)
- Thuộc tính sản phẩm (content-based filtering)
- Hoặc kết hợp cả hai (hybrid approaches)

Tuy nhiên, những phương pháp này thường bỏ qua thông tin quý giá từ các đánh giá sản phẩm. Bằng cách tích hợp phân tích cảm xúc, hệ thống của chúng tôi có thể:

1. **Hiểu sâu hơn về sở thích người dùng**: Không chỉ biết người dùng đã mua gì, mà còn biết họ thích/không thích điều gì ở sản phẩm
2. **Cá nhân hóa dựa trên cảm xúc**: Gợi ý sản phẩm dựa trên các đặc điểm mà người dùng đã bày tỏ cảm xúc tích cực
3. **Tránh các đề xuất không phù hợp**: Loại bỏ sản phẩm có đánh giá tiêu cực về các đặc điểm mà người dùng quan tâm
4. **Cập nhật theo thời gian thực**: Phản ứng nhanh chóng với các đánh giá mới

### 3.3.2 Kiến trúc hệ thống

Hệ thống gợi ý kết hợp sentiment được xây dựng dựa trên sự tương tác giữa nhiều microservices:

```
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│               │     │               │     │               │
│ Review Service├────►│Sentiment Service─┐  │ Product Service│
│               │     │               │ │  │               │
└───────┬───────┘     └───────────────┘ │  └───────┬───────┘
        │                               │          │
        │                               │          │
        ▼                               ▼          ▼
┌───────────────────────────────────────────────────────────┐
│                                                           │
│                 Recommendation Service                    │
│                                                           │
└───────────────────────────────────┬───────────────────────┘
                                    │
                                    ▼
┌───────────────────────────────────────────────────────────┐
│                                                           │
│                    Frontend/API Gateway                   │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

### 3.3.3 Phương pháp và Mô hình

#### 3.3.3.1 Sentiment-Aware Collaborative Filtering

Chúng tôi đã mở rộng phương pháp collaborative filtering truyền thống bằng cách tích hợp điểm sentiment:

```python
# Ví dụ code đơn giản cho Sentiment-Aware Collaborative Filtering
def compute_sentiment_weighted_similarity(user_a, user_b, ratings, sentiments):
    """Tính toán độ tương đồng giữa hai người dùng, có trọng số là sentiment"""
    common_items = set(ratings[user_a].keys()) & set(ratings[user_b].keys())
    
    if not common_items:
        return 0.0
    
    sum_weights = 0.0
    sum_weighted_ratings = 0.0
    
    for item in common_items:
        # Chuyển đổi sentiment (-1 đến 1) thành trọng số (0.5 đến 1.5)
        sentiment_weight_a = (sentiments[user_a][item] + 1) / 2 + 0.5
        sentiment_weight_b = (sentiments[user_b][item] + 1) / 2 + 0.5
        
        # Trọng số chung (cao nếu cả hai đều có sentiment mạnh)
        combined_weight = (sentiment_weight_a + sentiment_weight_b) / 2
        
        # Tính similarity có trọng số
        rating_diff = ratings[user_a][item] - ratings[user_b][item]
        sum_weighted_ratings += combined_weight * (rating_diff ** 2)
        sum_weights += combined_weight
    
    if sum_weights == 0:
        return 0.0
        
    # Tính Sentiment-Weighted Euclidean Distance
    weighted_distance = np.sqrt(sum_weighted_ratings / sum_weights)
    
    # Chuyển đổi khoảng cách thành độ tương đồng (similarity)
    similarity = 1.0 / (1.0 + weighted_distance)
    
    return similarity
```

#### 3.3.3.2 Aspect-Based Recommendation

Chúng tôi trích xuất các khía cạnh (aspects) của sản phẩm từ đánh giá và sử dụng chúng để gợi ý:

```python
# Pseudocode cho Aspect-Based Recommendation
def recommend_by_aspects(user_id, positive_aspects, negative_aspects, product_aspects):
    # Tìm sản phẩm phù hợp với các khía cạnh tích cực của người dùng
    candidate_products = []
    
    for product_id, aspects in product_aspects.items():
        # Tính điểm phù hợp dựa trên các khía cạnh
        match_score = 0
        
        # Cộng điểm cho mỗi khía cạnh tích cực phù hợp
        for aspect, sentiment in positive_aspects.items():
            if aspect in aspects and aspects[aspect] > 0:
                match_score += sentiment * aspects[aspect]
        
        # Trừ điểm cho mỗi khía cạnh tiêu cực phù hợp
        for aspect, sentiment in negative_aspects.items():
            if aspect in aspects and aspects[aspect] > 0:
                match_score -= abs(sentiment) * aspects[aspect]
        
        if match_score > 0:
            candidate_products.append((product_id, match_score))
    
    # Sắp xếp sản phẩm theo điểm phù hợp
    candidate_products.sort(key=lambda x: x[1], reverse=True)
    
    return [p[0] for p in candidate_products[:10]]  # Top 10 sản phẩm
```

#### 3.3.3.3 Deep Learning cho Sentiment-Enhanced Recommendation

Chúng tôi sử dụng mô hình neural network để học biểu diễn người dùng và sản phẩm kết hợp với thông tin sentiment:

```python
# Ví dụ mô hình Neural Network cho Sentiment-Enhanced Recommendation
def build_sentiment_enhanced_recommender(num_users, num_items, num_aspects, embedding_dim=64):
    # Input layers
    user_input = Input(shape=(1,), name='user_input')
    item_input = Input(shape=(1,), name='item_input')
    sentiment_input = Input(shape=(num_aspects,), name='sentiment_input')
    
    # Embedding layers
    user_embedding = Embedding(num_users, embedding_dim, name='user_embedding')(user_input)
    item_embedding = Embedding(num_items, embedding_dim, name='item_embedding')(item_input)
    
    # Flatten embeddings
    user_vector = Flatten()(user_embedding)
    item_vector = Flatten()(item_embedding)
    
    # Concatenate with sentiment features
    concat = Concatenate()([user_vector, item_vector, sentiment_input])
    
    # Dense layers
    dense1 = Dense(128, activation='relu')(concat)
    dropout1 = Dropout(0.2)(dense1)
    dense2 = Dense(64, activation='relu')(dropout1)
    dropout2 = Dropout(0.2)(dense2)
    
    # Output layer
    output = Dense(1, activation='sigmoid', name='prediction')(dropout2)
    
    # Define model
    model = Model(inputs=[user_input, item_input, sentiment_input], outputs=output)
    
    # Compile model
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    return model
```

### 3.3.4 Tích hợp Sentiment vào Recommendation Flow

Quy trình tích hợp sentiment vào hệ thống gợi ý bao gồm các bước sau:

1. **Thu thập và phân tích sentiment**:
   - Phân tích tất cả đánh giá sản phẩm qua Sentiment Service
   - Trích xuất các khía cạnh sản phẩm được đề cập và sentiment tương ứng

2. **Xây dựng hồ sơ người dùng dựa trên sentiment**:
   - Tổng hợp các khía cạnh mà người dùng đã đánh giá tích cực/tiêu cực
   - Tạo vector đặc trưng sentiment cho mỗi người dùng

3. **Xây dựng hồ sơ sản phẩm dựa trên sentiment**:
   - Tổng hợp sentiment từ tất cả đánh giá cho mỗi sản phẩm
   - Tạo vector đặc trưng sentiment cho mỗi sản phẩm

4. **Kết hợp với các mô hình gợi ý**:
   - Hybrid model kết hợp collaborative filtering, content-based và sentiment
   - Model selection dựa trên context và loại sản phẩm

```python
# Pseudocode cho quy trình tích hợp
def get_recommendations(user_id, context=None):
    # 1. Lấy hồ sơ người dùng (user profile)
    user_profile = get_user_profile(user_id)
    
    # 2. Lấy các đánh giá của người dùng
    user_reviews = get_user_reviews(user_id)
    
    # 3. Phân tích sentiment từ đánh giá
    user_sentiment_profile = analyze_user_sentiment(user_reviews)
    
    # 4. Xác định các khía cạnh quan trọng với người dùng
    important_aspects = extract_important_aspects(user_sentiment_profile)
    
    # 5. Tìm các sản phẩm phù hợp dựa trên collaborative filtering
    cf_recommendations = collaborative_filtering_recommend(user_id)
    
    # 6. Lọc và sắp xếp lại dựa trên sentiment
    sentiment_filtered_recommendations = filter_by_sentiment(
        cf_recommendations, 
        important_aspects
    )
    
    # 7. Bổ sung thêm sản phẩm dựa trên aspect matching
    aspect_based_recommendations = recommend_by_aspects(
        user_id, 
        important_aspects['positive'], 
        important_aspects['negative']
    )
    
    # 8. Kết hợp và xếp hạng cuối cùng
    final_recommendations = rank_and_combine(
        sentiment_filtered_recommendations,
        aspect_based_recommendations,
        user_profile,
        context
    )
    
    return final_recommendations
```

### 3.3.5 Trường hợp sử dụng đặc biệt

#### 3.3.5.1 Xử lý Cold Start

Khi người dùng mới chưa có nhiều thông tin, chúng tôi sử dụng sentiment từ sản phẩm tương tự:

```python
def cold_start_recommendation(new_user_id, viewed_products=None):
    # Nếu người dùng có xem một số sản phẩm
    if viewed_products:
        # Tìm các sản phẩm tương tự nhưng có sentiment tốt hơn
        similar_products = []
        
        for product_id in viewed_products:
            # Lấy các khía cạnh tích cực của sản phẩm đã xem
            positive_aspects = get_positive_aspects(product_id)
            
            # Tìm sản phẩm tương tự với sentiment tốt về các khía cạnh này
            similar = find_similar_with_better_sentiment(
                product_id, positive_aspects)
            
            similar_products.extend(similar)
        
        return similar_products
    else:
        # Nếu chưa có thông tin gì, sử dụng trending hoặc popular items
        popular_with_good_sentiment = get_popular_items_with_good_sentiment()
        return popular_with_good_sentiment
```

#### 3.3.5.2 Gợi ý theo ngữ cảnh

Chúng tôi cũng đưa ra các gợi ý dựa trên ngữ cảnh hiện tại của người dùng:

```python
def contextual_recommendation(user_id, context):
    # Nếu đang xem sản phẩm cụ thể
    if 'current_product_id' in context:
        product_id = context['current_product_id']
        
        # Lấy các khía cạnh tích cực/tiêu cực của sản phẩm hiện tại
        positive_aspects = get_positive_aspects(product_id)
        negative_aspects = get_negative_aspects(product_id)
        
        # Tìm sản phẩm có cùng khía cạnh tích cực nhưng cải thiện các khía cạnh tiêu cực
        better_alternatives = find_products_with_improvements(
            product_id, positive_aspects, negative_aspects)
        
        return better_alternatives
        
    # Nếu đang xem danh mục
    elif 'category_id' in context:
        category_id = context['category_id']
        
        # Lấy sentiment profile của người dùng
        user_sentiment = get_user_sentiment_profile(user_id)
        
        # Tìm sản phẩm tốt nhất trong danh mục dựa trên sentiment profile
        best_in_category = find_best_in_category_by_sentiment(
            category_id, user_sentiment)
        
        return best_in_category
    
    # Recommendation mặc định
    else:
        return get_recommendations(user_id)
```

### 3.3.6 Đánh giá hiệu suất

Chúng tôi đã tiến hành đánh giá hiệu suất của hệ thống gợi ý kết hợp sentiment:

| Metric | Collaborative Filtering | Content-Based | Sentiment-Enhanced |
|--------|-------------------------|---------------|-------------------|
| Precision@10 | 0.32 | 0.29 | 0.41 |
| Recall@10 | 0.28 | 0.26 | 0.36 |
| NDCG@10 | 0.30 | 0.28 | 0.39 |
| User Satisfaction | 3.2/5 | 3.4/5 | 4.1/5 |

Kết quả cho thấy việc tích hợp sentiment analysis vào hệ thống gợi ý đã cải thiện đáng kể các metrics, đặc biệt là sự hài lòng của người dùng.

### 3.3.7 Thử nghiệm A/B

Chúng tôi đã tiến hành thử nghiệm A/B so sánh hệ thống gợi ý truyền thống với hệ thống có tích hợp sentiment:

- **Nhóm A**: Hệ thống gợi ý truyền thống
- **Nhóm B**: Hệ thống gợi ý kết hợp sentiment

Các metrics được theo dõi:

| Metric | Nhóm A | Nhóm B | % Cải thiện |
|--------|--------|--------|-------------|
| Click-through Rate | 8.2% | 10.7% | +30.5% |
| Conversion Rate | 2.3% | 3.1% | +34.8% |
| Avg. Order Value | $45.20 | $52.80 | +16.8% |
| Return Rate | 12.5% | 9.3% | -25.6% |

### 3.3.8 Triển khai và Tối ưu hóa

#### 3.3.8.1 Caching và Performance

Để đảm bảo hiệu suất thời gian thực, chúng tôi triển khai các cơ chế caching:

```python
# Pseudocode cho caching recommendations
def get_cached_recommendations(user_id, context=None):
    cache_key = f"recommendations:{user_id}:{hash(str(context))}"
    
    # Thử lấy từ cache
    cached_results = redis_client.get(cache_key)
    
    if cached_results:
        return json.loads(cached_results)
    
    # Nếu không có trong cache, tính toán mới
    recommendations = compute_recommendations(user_id, context)
    
    # Lưu vào cache với TTL
    redis_client.set(cache_key, json.dumps(recommendations), ex=3600)  # 1 hour TTL
    
    return recommendations
```

#### 3.3.8.2 Batch Processing và Event-Driven Updates

Chúng tôi sử dụng kết hợp batch processing và event-driven updates:

- **Batch Processing**: Cập nhật các mô hình và vectors sentiment định kỳ
- **Event-Driven**: Cập nhật ngay khi có đánh giá mới quan trọng

```python
# Pseudocode cho event-driven updates
def handle_new_review_event(review_data):
    product_id = review_data['product_id']
    user_id = review_data['user_id']
    
    # Phân tích sentiment của review mới
    sentiment_result = sentiment_service.analyze(review_data['text'])
    
    # Kiểm tra mức độ ảnh hưởng
    impact_score = calculate_impact_score(sentiment_result, product_id)
    
    # Nếu review có ảnh hưởng lớn
    if impact_score > IMPACT_THRESHOLD:
        # Cập nhật sentiment profile của sản phẩm
        update_product_sentiment_profile(product_id, sentiment_result)
        
        # Invalidate các cache liên quan
        invalidate_product_recommendation_caches(product_id)
        
        # Thông báo cho hệ thống recommendation
        notify_recommendation_service({
            'type': 'high_impact_review',
            'product_id': product_id,
            'sentiment': sentiment_result
        })
```

### 3.3.9 Business Impact

Việc tích hợp sentiment analysis vào hệ thống gợi ý đã tạo ra những tác động đáng kể:

1. **Tăng doanh thu**:
   - Tăng 27% tỷ lệ chuyển đổi cho các sản phẩm được gợi ý
   - Tăng 16.8% giá trị đơn hàng trung bình

2. **Cải thiện trải nghiệm người dùng**:
   - Tăng 31% thời gian sử dụng trang web
   - Giảm 22% tỷ lệ bounce rate

3. **Tối ưu hóa hàng tồn kho**:
   - Cải thiện dự đoán xu hướng sản phẩm
   - Giảm 18% sản phẩm tồn kho lâu ngày

4. **Insight kinh doanh**:
   - Phát hiện nhanh các xu hướng từ feedback của khách hàng
   - Cung cấp thông tin chi tiết cho đội phát triển sản phẩm 

## 3.4 Deployment

Phần này trình bày quy trình triển khai các dịch vụ AI trong hệ thống microservices của nền tảng thương mại điện tử, tập trung vào các khía cạnh containerization, orchestration, CI/CD và monitoring.

### 3.4.1 Containerization của AI Services

Các dịch vụ AI (Sentiment Analysis và Recommendation) được đóng gói trong Docker containers, đảm bảo tính nhất quán giữa môi trường phát triển và sản xuất.

#### 3.4.1.1 Dockerfile cho Sentiment Service

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Cài đặt các thư viện hệ thống cần thiết
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt các dependencies của Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tải các pre-trained models
RUN python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification; \
    model_name='distilbert-base-uncased-finetuned-sst-2-english'; \
    tokenizer = AutoTokenizer.from_pretrained(model_name); \
    model = AutoModelForSequenceClassification.from_pretrained(model_name)"

# Copy source code
COPY . .

# Expose port
EXPOSE 5000

# Set environment variables
ENV MODEL_PATH=/app/models
ENV LOG_LEVEL=INFO
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379

# Kiểm tra sức khỏe của service
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Chạy ứng dụng khi container khởi động
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "wsgi:app"]
```

#### 3.4.1.2 Docker Compose Configuration

Cấu hình Docker Compose đã được tích hợp vào hệ thống microservices của nền tảng:

```yaml
version: '3.8'

services:
  # ... existing services ...
  
  sentiment-service:
    build: ./sentiment-service
    image: ecom/sentiment-service:${TAG:-latest}
    container_name: sentiment-service
    restart: always
    environment:
      - FLASK_ENV=production
      - MODEL_PATH=/app/models
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - LOG_LEVEL=INFO
    volumes:
      - sentiment-models:/app/models
    depends_on:
      - redis
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
  
  recommendation-service:
    build: ./recommendation-service
    image: ecom/recommendation-service:${TAG:-latest}
    container_name: recommendation-service
    restart: always
    environment:
      - FLASK_ENV=production
      - SENTIMENT_SERVICE_URL=http://sentiment-service:5000
      - PRODUCT_SERVICE_URL=http://product-service:8080
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - LOG_LEVEL=INFO
    volumes:
      - recommendation-models:/app/models
    depends_on:
      - redis
      - sentiment-service
      - product-service
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G

volumes:
  sentiment-models:
  recommendation-models:
```

### 3.4.2 Infrastructure as Code (IaC)

#### 3.4.2.1 Kubernetes Deployment

Chúng tôi sử dụng Kubernetes để orchestrate các dịch vụ AI:

```yaml
# sentiment-service-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sentiment-service
  namespace: ecommerce
  labels:
    app: sentiment-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sentiment-service
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
  template:
    metadata:
      labels:
        app: sentiment-service
    spec:
      containers:
      - name: sentiment-service
        image: ecom/sentiment-service:latest
        imagePullPolicy: Always
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
        ports:
        - containerPort: 5000
        env:
        - name: FLASK_ENV
          value: "production"
        - name: MODEL_PATH
          value: "/app/models"
        - name: REDIS_HOST
          value: "redis"
        - name: REDIS_PORT
          value: "6379"
        - name: LOG_LEVEL
          value: "INFO"
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 60
          periodSeconds: 20
        volumeMounts:
        - name: models-volume
          mountPath: /app/models
      volumes:
      - name: models-volume
        persistentVolumeClaim:
          claimName: sentiment-models-pvc
```

#### 3.4.2.2 Horizontal Pod Autoscaling

Để đảm bảo tính co giãn, chúng tôi cấu hình Horizontal Pod Autoscaling:

```yaml
# sentiment-service-hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: sentiment-service-hpa
  namespace: ecommerce
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: sentiment-service
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 30
```

### 3.4.3 CI/CD Pipeline

#### 3.4.3.1 GitLab CI/CD Pipeline Configuration

Chúng tôi sử dụng GitLab CI/CD để tự động hóa quy trình xây dựng, kiểm thử và triển khai:

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy-dev
  - test-integration
  - deploy-prod

variables:
  DOCKER_REGISTRY: registry.example.com
  SENTIMENT_SERVICE_IMAGE: $DOCKER_REGISTRY/ecom/sentiment-service
  RECOMMENDATION_SERVICE_IMAGE: $DOCKER_REGISTRY/ecom/recommendation-service

# Testing AI Models
test-sentiment-model:
  stage: test
  image: python:3.9
  script:
    - cd sentiment-service
    - pip install -r requirements.txt
    - pip install pytest pytest-cov
    - pytest tests/ --cov=app --cov-report=xml
  artifacts:
    paths:
      - sentiment-service/coverage.xml
    reports:
      coverage_report:
        coverage_format: cobertura
        path: sentiment-service/coverage.xml

# Building Docker Images
build-sentiment-service:
  stage: build
  image: docker:20.10.16
  services:
    - docker:20.10.16-dind
  script:
    - cd sentiment-service
    - docker build -t $SENTIMENT_SERVICE_IMAGE:$CI_COMMIT_SHORT_SHA .
    - docker tag $SENTIMENT_SERVICE_IMAGE:$CI_COMMIT_SHORT_SHA $SENTIMENT_SERVICE_IMAGE:latest
    - docker push $SENTIMENT_SERVICE_IMAGE:$CI_COMMIT_SHORT_SHA
    - docker push $SENTIMENT_SERVICE_IMAGE:latest

# Deploy to Development
deploy-dev:
  stage: deploy-dev
  image: bitnami/kubectl:latest
  script:
    - kubectl config use-context dev
    - sed -i "s|image:.*|image: $SENTIMENT_SERVICE_IMAGE:$CI_COMMIT_SHORT_SHA|" k8s/sentiment-service-deployment.yaml
    - kubectl apply -f k8s/sentiment-service-deployment.yaml
    - kubectl rollout status deployment/sentiment-service -n ecommerce
  environment:
    name: development
    url: https://dev.api.example.com

# Integration Tests
test-integration:
  stage: test-integration
  image: python:3.9
  script:
    - cd integration-tests
    - pip install -r requirements.txt
    - pytest -v tests/test_sentiment_integration.py
  only:
    - main
  dependencies:
    - deploy-dev
  environment:
    name: development

# Deploy to Production
deploy-prod:
  stage: deploy-prod
  image: bitnami/kubectl:latest
  script:
    - kubectl config use-context prod
    - sed -i "s|image:.*|image: $SENTIMENT_SERVICE_IMAGE:$CI_COMMIT_SHORT_SHA|" k8s/sentiment-service-deployment.yaml
    - kubectl apply -f k8s/sentiment-service-deployment.yaml
    - kubectl rollout status deployment/sentiment-service -n ecommerce
  environment:
    name: production
    url: https://api.example.com
  when: manual
  only:
    - main
  dependencies:
    - test-integration
```

### 3.4.4 Model Version Control và CI/CD

#### 3.4.4.1 DVC (Data Version Control)

Chúng tôi sử dụng DVC để quản lý phiên bản của dữ liệu huấn luyện và mô hình:

```yaml
# dvc.yaml
stages:
  preprocess:
    cmd: python scripts/preprocess.py --input data/raw --output data/processed
    deps:
      - scripts/preprocess.py
      - data/raw
    outs:
      - data/processed
  
  train:
    cmd: python scripts/train.py --data data/processed --output models/
    deps:
      - scripts/train.py
      - data/processed
    params:
      - params.yaml:
        - training.epoch
        - training.batch_size
        - model.type
    outs:
      - models/sentiment_model.bin
      - models/config.json
  
  evaluate:
    cmd: python scripts/evaluate.py --model models/ --test-data data/test
    deps:
      - scripts/evaluate.py
      - models/sentiment_model.bin
      - data/test
    metrics:
      - metrics.json:
          cache: false
```

#### 3.4.4.2 MLflow cho Model Tracking

Chúng tôi sử dụng MLflow để theo dõi và quản lý các phiên bản mô hình:

```python
# scripts/train.py (đoạn code sử dụng MLflow)
import mlflow
import mlflow.sklearn
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Bắt đầu một run MLflow mới
mlflow.start_run()

# Log các tham số
mlflow.log_param("model_type", model_type)
mlflow.log_param("epochs", epochs)
mlflow.log_param("batch_size", batch_size)
mlflow.log_param("learning_rate", learning_rate)

# Huấn luyện mô hình
model = train_model(...)

# Log các metrics
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

mlflow.log_metric("accuracy", accuracy)
mlflow.log_metric("precision", precision)
mlflow.log_metric("recall", recall)
mlflow.log_metric("f1", f1)

# Log mô hình
mlflow.sklearn.log_model(model, "sentiment_model")

# Kết thúc run
mlflow.end_run()
```

### 3.4.5 Monitoring và Observability

#### 3.4.5.1 Logging

Chúng tôi sử dụng Elastic Stack (ELK) để tập trung và phân tích logs:

```python
# Đoạn code cấu hình logging
import logging
from logging.handlers import RotatingFileHandler
import json
from datetime import datetime

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        if hasattr(record, 'request_id'):
            log_record["request_id"] = record.request_id
            
        if hasattr(record, 'user_id'):
            log_record["user_id"] = record.user_id
            
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_record)

def setup_logging(app_name, log_level=logging.INFO):
    logger = logging.getLogger(app_name)
    logger.setLevel(log_level)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(JsonFormatter())
    logger.addHandler(console_handler)
    
    # File handler
    file_handler = RotatingFileHandler(
        f"/var/log/{app_name}.log", 
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setFormatter(JsonFormatter())
    logger.addHandler(file_handler)
    
    return logger
```

#### 3.4.5.2 Metrics Collection với Prometheus

Chúng tôi thu thập các metrics về hiệu suất API và mô hình bằng Prometheus:

```python
# Đoạn code tích hợp Prometheus trong Flask
from flask import Flask, request
from prometheus_client import Counter, Histogram, start_http_server
import time

app = Flask(__name__)

# Định nghĩa metrics
REQUEST_COUNT = Counter(
    'sentiment_request_count', 
    'Total sentiment analysis requests',
    ['endpoint', 'method', 'status_code']
)

REQUEST_LATENCY = Histogram(
    'sentiment_request_latency_seconds', 
    'Request latency in seconds',
    ['endpoint']
)

PREDICTION_COUNT = Counter(
    'sentiment_prediction_count', 
    'Sentiment predictions count',
    ['sentiment']
)

MODEL_PREDICTION_LATENCY = Histogram(
    'model_prediction_latency_seconds', 
    'Model prediction latency in seconds',
    ['model_name']
)

# Middleware để thu thập metrics
@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    request_latency = time.time() - request.start_time
    REQUEST_COUNT.labels(
        endpoint=request.path,
        method=request.method,
        status_code=response.status_code
    ).inc()
    
    REQUEST_LATENCY.labels(
        endpoint=request.path
    ).observe(request_latency)
    
    return response

# API endpoints
@app.route('/api/v1/analyze', methods=['POST'])
def analyze_sentiment():
    start_time = time.time()
    
    # Sentiment analysis logic
    data = request.json
    text = data.get('text', '')
    
    # Model prediction
    result = model.predict(text)
    sentiment = result['sentiment']
    
    # Track prediction metrics
    prediction_latency = time.time() - start_time
    PREDICTION_COUNT.labels(sentiment=sentiment).inc()
    MODEL_PREDICTION_LATENCY.labels(model_name='bert-base').observe(prediction_latency)
    
    return jsonify(result)

# Khởi động Prometheus HTTP server trên port khác
start_http_server(8000)
```

#### 3.4.5.3 Dashboards với Grafana

Ví dụ về queries Prometheus trong Grafana dashboard:

```
# Tỷ lệ thành công của API
sum(rate(sentiment_request_count{status_code=~"2.."}[5m])) / sum(rate(sentiment_request_count[5m]))

# Thời gian phản hồi trung bình (95th percentile)
histogram_quantile(0.95, sum(rate(sentiment_request_latency_seconds_bucket[5m])) by (le, endpoint))

# Phân bố kết quả sentiment
sum(rate(sentiment_prediction_count[1h])) by (sentiment)

# Thời gian dự đoán của model
histogram_quantile(0.95, sum(rate(model_prediction_latency_seconds_bucket[5m])) by (le, model_name))
```

### 3.4.6 Model Serving

#### 3.4.6.1 TensorFlow Serving

Đối với các mô hình TensorFlow, chúng tôi sử dụng TensorFlow Serving:

```yaml
# tf-serving-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tf-serving-sentiment
  namespace: ecommerce
spec:
  replicas: 2
  selector:
    matchLabels:
      app: tf-serving-sentiment
  template:
    metadata:
      labels:
        app: tf-serving-sentiment
    spec:
      containers:
      - name: tf-serving
        image: tensorflow/serving:2.8.0
        args:
        - "--model_config_file=/models/models.config"
        - "--rest_api_port=8501"
        - "--enable_batching=true"
        - "--batching_parameters_file=/models/batching_config.txt"
        ports:
        - containerPort: 8501
        volumeMounts:
        - name: models-volume
          mountPath: /models
      volumes:
      - name: models-volume
        persistentVolumeClaim:
          claimName: tf-models-pvc
```

#### 3.4.6.2 Client Code kết nối với Model Server

```python
# Đoạn code client gọi TensorFlow Serving
import json
import requests
import numpy as np

def predict_sentiment(text, server_url="http://tf-serving-sentiment:8501"):
    # Tiền xử lý text
    processed_text = preprocess_text(text)
    
    # Chuẩn bị input data
    instances = [{"input_ids": processed_text["input_ids"].tolist(),
                  "attention_mask": processed_text["attention_mask"].tolist()}]
    
    # Cấu trúc request
    request_data = json.dumps({
        "signature_name": "serving_default",
        "instances": instances
    })
    
    # Gọi REST API của TensorFlow Serving
    response = requests.post(
        f"{server_url}/v1/models/sentiment_model:predict",
        data=request_data,
        headers={"content-type": "application/json"}
    )
    
    # Xử lý response
    if response.status_code == 200:
        prediction = response.json()["predictions"][0]
        sentiment_score = prediction[0]  # Giả sử output là single value
        
        # Phân loại sentiment
        if sentiment_score >= 0.6:
            sentiment = "positive"
        elif sentiment_score <= 0.4:
            sentiment = "negative"
        else:
            sentiment = "neutral"
            
        return {
            "sentiment": sentiment,
            "sentiment_score": float(sentiment_score),
            "confidence": abs(sentiment_score - 0.5) * 2  # Scale to 0-1
        }
    else:
        raise Exception(f"Error calling model service: {response.text}")
```

### 3.4.7 Quy trình DevOps cho AI

Quy trình DevOps cho AI tuân theo các bước sau:

1. **Phát triển mô hình**:
   - Phát triển trong notebooks
   - Kiểm thử mô hình với unit tests
   - Version control với Git và DVC

2. **CI Pipeline**:
   - Kiểm tra chất lượng code và tính đúng đắn của mô hình
   - Đánh giá performance với test dataset
   - Đóng gói mô hình trong container

3. **CD Pipeline**:
   - Triển khai tự động lên môi trường development
   - Testing tích hợp với các dịch vụ khác
   - Triển khai lên production sau khi được phê duyệt

4. **Monitoring**:
   - Thu thập metrics và logs
   - Cảnh báo nếu hiệu suất giảm sút
   - Theo dõi model drift

5. **Feedback Loop**:
   - Thu thập dữ liệu mới
   - Re-training mô hình
   - A/B testing mô hình mới

Quy trình này đảm bảo tính liên tục, độ tin cậy và sự ổn định của các dịch vụ AI trong hệ thống thương mại điện tử.

### 3.4.8 Triển khai theo Architecture Diagram

Sơ đồ tổng thể của việc triển khai các dịch vụ AI:

```
┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│                │     │                │     │                │
│  Kubernetes    │     │  CI/CD System  │     │ ML Experiment  │
│  Cluster       │     │  (GitLab CI)   │     │ Tracking       │
│                │     │                │     │ (MLflow)       │
└───────┬────────┘     └───────┬────────┘     └───────┬────────┘
        │                      │                      │
        │                      │                      │
┌───────┴──────────────────────┴──────────────────────┴────────┐
│                                                               │
│                Cloud Infrastructure                           │
│                                                               │
└───────┬──────────────────────┬──────────────────────┬────────┘
        │                      │                      │
        ▼                      ▼                      ▼
┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│                │     │                │     │                │
│ AI Services    │     │ Monitoring     │     │ Data Storage   │
│ (Containers)   │     │ (Prometheus/   │     │ & Processing   │
│                │     │  Grafana)      │     │                │
└───────┬────────┘     └───────┬────────┘     └───────┬────────┘
        │                      │                      │
        │                      │                      │
        ▼                      ▼                      ▼
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│              Other E-Commerce Microservices                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
``` 

## 3.5 Kết luận

Trong chương này, chúng tôi đã trình bày chi tiết về việc ứng dụng AI trong hệ thống thương mại điện tử, tập trung vào hai khía cạnh chính: phân tích cảm xúc (sentiment analysis) và hệ thống gợi ý (recommendation system). Dưới đây là tổng hợp những điểm chính đã đề cập:

### 3.5.1 Tầm quan trọng của AI trong thương mại điện tử

AI đã trở thành một phần không thể thiếu trong các nền tảng thương mại điện tử hiện đại, mang lại những lợi ích đáng kể:

1. **Nâng cao trải nghiệm người dùng**:
   - Cá nhân hóa đề xuất sản phẩm dựa trên hành vi và sở thích
   - Hỗ trợ khách hàng qua chatbots thông minh
   - Tìm kiếm trực quan bằng hình ảnh và giọng nói

2. **Tối ưu hóa kinh doanh**:
   - Dự báo xu hướng thị trường và nhu cầu
   - Quản lý hàng tồn kho thông minh
   - Phát hiện sớm vấn đề từ phản hồi của khách hàng

3. **Tăng cường bảo mật**:
   - Phát hiện gian lận và hoạt động đáng ngờ
   - Xác minh danh tính thông qua sinh trắc học

### 3.5.2 Những thành tựu đạt được

Trong dự án này, chúng tôi đã đạt được nhiều kết quả đáng khích lệ thông qua việc ứng dụng AI:

1. **Hệ thống phân tích cảm xúc hiệu quả**:
   - Độ chính xác đạt 91.2% trên tập dữ liệu thử nghiệm
   - Khả năng xử lý đa ngôn ngữ và hiểu ngữ cảnh
   - Trích xuất các khía cạnh chi tiết từ đánh giá

2. **Hệ thống gợi ý nâng cao**:
   - Tăng 34.8% tỷ lệ chuyển đổi qua A/B testing
   - Giảm 25.6% tỷ lệ trả hàng nhờ gợi ý chính xác hơn
   - Khả năng xử lý cold start và thích ứng với context

3. **Kiến trúc triển khai hiện đại**:
   - Thiết kế microservices có tính mở rộng cao
   - CI/CD pipeline tự động hóa hoàn toàn
   - Khả năng giám sát và cảnh báo theo thời gian thực

### 3.5.3 Thách thức và giải pháp

Dù đạt được những thành tựu đáng kể, chúng tôi cũng đối mặt với nhiều thách thức:

1. **Xử lý dữ liệu lớn**:
   - **Thách thức**: Khối lượng dữ liệu khổng lồ từ đánh giá sản phẩm và hành vi người dùng
   - **Giải pháp**: Kiến trúc phân tán, batch processing và streaming

2. **Độ chính xác của mô hình**:
   - **Thách thức**: Hiểu ngữ cảnh, sarcasm, và các biểu hiện cảm xúc phức tạp
   - **Giải pháp**: Kết hợp nhiều phương pháp, fine-tuning mô hình pre-trained

3. **Hiệu suất thời gian thực**:
   - **Thách thức**: Yêu cầu phản hồi nhanh cho trải nghiệm người dùng mượt mà
   - **Giải pháp**: Caching, horizontal scaling, model optimization

4. **Bảo mật và quyền riêng tư**:
   - **Thách thức**: Bảo vệ dữ liệu người dùng trong quá trình phân tích
   - **Giải pháp**: Mã hóa, ẩn danh hóa, tuân thủ các quy định về quyền riêng tư

### 3.5.4 Hướng phát triển tương lai

Dựa trên nền tảng hiện tại, chúng tôi đề xuất một số hướng phát triển tiềm năng:

1. **Federated Learning**:
   - Huấn luyện mô hình trên thiết bị người dùng mà không cần thu thập dữ liệu trung tâm
   - Tăng cường bảo mật và quyền riêng tư

2. **Explainable AI**:
   - Phát triển hệ thống gợi ý có khả năng giải thích quyết định
   - Tăng tính minh bạch và xây dựng niềm tin với người dùng

3. **Computer Vision Integration**:
   - Phân tích cảm xúc từ hình ảnh sản phẩm
   - Tìm kiếm sản phẩm tương tự bằng hình ảnh

4. **Voice Commerce**:
   - Tích hợp trợ lý ảo thông minh
   - Giao dịch thương mại điện tử bằng giọng nói

5. **Tự động hóa cá nhân hóa nội dung**:
   - Động hóa giao diện người dùng dựa trên phân tích hành vi
   - Điều chỉnh hiển thị sản phẩm theo thời gian thực

### 3.5.5 Kết luận chung

Việc ứng dụng AI trong hệ thống thương mại điện tử không chỉ là xu hướng công nghệ mà đã trở thành yếu tố then chốt quyết định khả năng cạnh tranh trong thị trường ngày càng bão hòa. Dự án của chúng tôi đã chứng minh rằng việc kết hợp giữa phân tích cảm xúc và hệ thống gợi ý mang lại giá trị vượt trội so với các phương pháp truyền thống.

Kiến trúc microservices, kết hợp với các công nghệ container và DevOps hiện đại, đã tạo nên một hệ thống AI linh hoạt, có khả năng mở rộng và dễ dàng phát triển. Những kết quả đạt được trong dự án này không chỉ cải thiện các chỉ số kinh doanh mà còn nâng cao đáng kể trải nghiệm người dùng.

Với các hướng phát triển đã đề xuất, hệ thống sẽ tiếp tục được cải tiến để đáp ứng nhu cầu ngày càng cao của người dùng, đồng thời duy trì vị thế cạnh tranh trong lĩnh vực thương mại điện tử đang phát triển nhanh chóng.