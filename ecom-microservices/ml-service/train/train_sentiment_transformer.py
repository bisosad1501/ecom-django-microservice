import os
import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from transformers import get_linear_schedule_with_warmup
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import joblib
import time
import random
import logging

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Thiết lập seed cho quá trình training
def set_seed(seed_value=42):
    random.seed(seed_value)
    np.random.seed(seed_value)
    torch.manual_seed(seed_value)
    torch.cuda.manual_seed_all(seed_value)

set_seed(42)

# Thư mục lưu mô hình
MODEL_DIR = "ml-service/train/models"
os.makedirs(MODEL_DIR, exist_ok=True)

# Kiểm tra nếu GPU khả dụng
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logger.info(f"Using device: {device}")

# Class Dataset cho BERT
class SentimentDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
        
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = self.labels[idx]
        
        # Tokenize văn bản
        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            return_token_type_ids=False,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )
        
        return {
            'text': text,
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'label': torch.tensor(label, dtype=torch.long)
        }

# Hàm đánh giá mô hình
def evaluate_model(model, data_loader):
    model.eval()
    predictions = []
    actual_labels = []
    
    with torch.no_grad():
        for batch in data_loader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['label'].to(device)
            
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask
            )
            
            _, preds = torch.max(outputs.logits, dim=1)
            
            predictions.extend(preds.cpu().tolist())
            actual_labels.extend(labels.cpu().tolist())
    
    return accuracy_score(actual_labels, predictions), classification_report(
        actual_labels, predictions, target_names=['negative', 'neutral', 'positive'], output_dict=True
    )

# Vẽ biểu đồ kết quả huấn luyện
def plot_training_history(training_stats, filename="transformer_history.png"):
    # Tạo lược đồ huấn luyện
    plt.figure(figsize=(12, 8))
    
    # Vẽ biểu đồ loss
    plt.subplot(2, 1, 1)
    plt.plot([stat['epoch'] for stat in training_stats], [stat['train_loss'] for stat in training_stats], 'b-o', label='Training Loss')
    plt.plot([stat['epoch'] for stat in training_stats], [stat['val_loss'] for stat in training_stats], 'r-o', label='Validation Loss')
    plt.title('Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    # Vẽ biểu đồ accuracy
    plt.subplot(2, 1, 2)
    plt.plot([stat['epoch'] for stat in training_stats], [stat['train_acc'] for stat in training_stats], 'b-o', label='Training Accuracy')
    plt.plot([stat['epoch'] for stat in training_stats], [stat['val_acc'] for stat in training_stats], 'r-o', label='Validation Accuracy')
    plt.title('Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(MODEL_DIR, filename))
    plt.close()

# Hàm huấn luyện mô hình
def train_model(model, train_dataloader, val_dataloader, epochs=4, lr=2e-5):
    # Sử dụng optimizer AdamW
    optimizer = AdamW(model.parameters(), lr=lr, eps=1e-8)
    
    # Tổng số bước huấn luyện
    total_steps = len(train_dataloader) * epochs
    
    # Lịch trình học tập với warmup
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=0,  # Mặc định không sử dụng warmup
        num_training_steps=total_steps
    )
    
    # Lưu thống kê huấn luyện
    training_stats = []
    
    # Bắt đầu huấn luyện
    for epoch in range(1, epochs + 1):
        logger.info(f"Starting epoch {epoch}/{epochs}")
        
        # Training
        model.train()
        total_train_loss = 0
        all_train_preds = []
        all_train_labels = []
        
        for batch in train_dataloader:
            # Chuyển dữ liệu sang GPU
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['label'].to(device)
            
            # Xóa gradient
            model.zero_grad()
            
            # Forward pass
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels
            )
            
            loss = outputs.loss
            total_train_loss += loss.item()
            
            # Backward pass và cập nhật trọng số
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)  # Clipping gradient để tránh exploding gradient
            optimizer.step()
            scheduler.step()
            
            # Lưu dự đoán và nhãn thực tế cho tính accuracy
            _, preds = torch.max(outputs.logits, dim=1)
            all_train_preds.extend(preds.cpu().tolist())
            all_train_labels.extend(labels.cpu().tolist())
        
        # Tính loss và accuracy trung bình
        avg_train_loss = total_train_loss / len(train_dataloader)
        train_accuracy = accuracy_score(all_train_labels, all_train_preds)
        
        logger.info(f"Training loss: {avg_train_loss:.4f}, Accuracy: {train_accuracy:.4f}")
        
        # Validation
        model.eval()
        total_val_loss = 0
        all_val_preds = []
        all_val_labels = []
        
        with torch.no_grad():
            for batch in val_dataloader:
                input_ids = batch['input_ids'].to(device)
                attention_mask = batch['attention_mask'].to(device)
                labels = batch['label'].to(device)
                
                outputs = model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    labels=labels
                )
                
                loss = outputs.loss
                total_val_loss += loss.item()
                
                _, preds = torch.max(outputs.logits, dim=1)
                all_val_preds.extend(preds.cpu().tolist())
                all_val_labels.extend(labels.cpu().tolist())
        
        # Tính loss và accuracy validation
        avg_val_loss = total_val_loss / len(val_dataloader)
        val_accuracy = accuracy_score(all_val_labels, all_val_preds)
        
        logger.info(f"Validation loss: {avg_val_loss:.4f}, Accuracy: {val_accuracy:.4f}")
        
        # Lưu thống kê
        training_stats.append({
            'epoch': epoch,
            'train_loss': avg_train_loss,
            'val_loss': avg_val_loss,
            'train_acc': train_accuracy,
            'val_acc': val_accuracy,
            'learning_rate': scheduler.get_last_lr()[0]
        })
        
        # Lưu mô hình tốt nhất
        if epoch == 1 or val_accuracy > best_val_accuracy:
            best_val_accuracy = val_accuracy
            logger.info(f"Saving best model with validation accuracy: {best_val_accuracy:.4f}")
            torch.save(model.state_dict(), os.path.join(MODEL_DIR, 'bert_sentiment.pt'))
    
    return training_stats

# Hàm chính
def main():
    # Load dữ liệu
    logger.info("Loading dataset...")
    DATA_PATH = "ml-service/train/datasets/sentiment_train.csv"
    df = pd.read_csv(DATA_PATH)
    
    # Chuyển nhãn thành số
    sentiment_mapping = {'negative': 0, 'neutral': 1, 'positive': 2}
    df['sentiment_label'] = df['sentiment'].map(sentiment_mapping)
    
    # Phân chia dữ liệu
    X = df['review'].values
    y = df['sentiment_label'].values
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp)
    
    logger.info(f"Training samples: {len(X_train)}")
    logger.info(f"Validation samples: {len(X_val)}")
    logger.info(f"Test samples: {len(X_test)}")
    
    # Khởi tạo tokenizer và mô hình BERT
    logger.info("Loading BERT model and tokenizer...")
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertForSequenceClassification.from_pretrained(
        'bert-base-uncased',
        num_labels=3,  # 3 classes: negative, neutral, positive
        output_attentions=False,
        output_hidden_states=False,
    )
    
    # Đưa mô hình lên GPU
    model = model.to(device)
    
    # Chuẩn bị dữ liệu cho huấn luyện
    batch_size = 16
    
    # Tạo dataset
    train_dataset = SentimentDataset(X_train, y_train, tokenizer)
    val_dataset = SentimentDataset(X_val, y_val, tokenizer)
    test_dataset = SentimentDataset(X_test, y_test, tokenizer)
    
    # Tạo DataLoader
    train_dataloader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
    )
    
    val_dataloader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
    )
    
    test_dataloader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
    )
    
    # Huấn luyện mô hình
    logger.info("Starting model training...")
    global best_val_accuracy
    best_val_accuracy = 0.0
    
    start_time = time.time()
    training_stats = train_model(
        model=model,
        train_dataloader=train_dataloader,
        val_dataloader=val_dataloader,
        epochs=4,  # Có thể điều chỉnh số lượng epochs tùy vào dữ liệu
        lr=2e-5
    )
    
    training_time = time.time() - start_time
    logger.info(f"Training complete in {training_time:.2f} seconds")
    
    # Vẽ biểu đồ huấn luyện
    plot_training_history(training_stats)
    
    # Đánh giá mô hình trên tập test
    logger.info("Evaluating model on test set...")
    
    # Tải mô hình tốt nhất
    model.load_state_dict(torch.load(os.path.join(MODEL_DIR, 'bert_sentiment.pt')))
    
    # Đánh giá
    test_accuracy, test_report = evaluate_model(model, test_dataloader)
    
    logger.info(f"Test Accuracy: {test_accuracy:.4f}")
    logger.info("Classification Report:")
    for label, metrics in test_report.items():
        if isinstance(metrics, dict):
            logger.info(f"{label}: precision={metrics['precision']:.4f}, recall={metrics['recall']:.4f}, f1-score={metrics['f1-score']:.4f}")
    
    # Tạo báo cáo chi tiết
    y_pred = []
    y_true = []
    
    model.eval()
    with torch.no_grad():
        for batch in test_dataloader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['label'].to(device)
            
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            _, preds = torch.max(outputs.logits, dim=1)
            
            y_pred.extend(preds.cpu().tolist())
            y_true.extend(labels.cpu().tolist())
    
    # Ma trận nhầm lẫn
    cm = confusion_matrix(y_true, y_pred)
    logger.info("Confusion Matrix:")
    logger.info(cm)
    
    # Lưu tokenizer
    tokenizer.save_pretrained(os.path.join(MODEL_DIR, 'bert_tokenizer'))
    
    # Lưu mapping nhãn
    joblib.dump(sentiment_mapping, os.path.join(MODEL_DIR, 'sentiment_mapping.pkl'))
    
    logger.info(f"Model and tokenizer saved to {MODEL_DIR}")
    logger.info("Training and evaluation complete!")

if __name__ == "__main__":
    main() 