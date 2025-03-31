import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple, Union
from collections import defaultdict

class SentimentTrendAnalyzer:
    """
    Phân tích xu hướng cảm xúc từ dữ liệu reviews đã được phân tích
    """
    
    def __init__(self, analyzed_reviews: Optional[List[Dict[str, Any]]] = None):
        """
        Khởi tạo analyzer với dữ liệu reviews đã được phân tích cảm xúc
        
        Args:
            analyzed_reviews (List[Dict[str, Any]], optional): Danh sách reviews đã được phân tích
        """
        self.reviews = analyzed_reviews or []
        self.df = None
        
        if self.reviews:
            self._prepare_dataframe()
    
    def load_reviews(self, reviews: List[Dict[str, Any]]):
        """
        Tải reviews đã được phân tích cảm xúc
        
        Args:
            reviews (List[Dict[str, Any]]): Danh sách reviews
        """
        self.reviews = reviews
        self._prepare_dataframe()
    
    def _prepare_dataframe(self):
        """
        Chuyển đổi reviews thành DataFrame để phân tích
        """
        if not self.reviews:
            self.df = pd.DataFrame()
            return
        
        # Chuẩn bị dữ liệu
        data = []
        for review in self.reviews:
            # Kiểm tra review có sentiment info không
            sentiment_info = review.get('sentiment', {})
            if not sentiment_info:
                continue
            
            row = {
                'id': review.get('id', ''),
                'product_id': review.get('product_id', ''),
                'user_id': review.get('user_id', ''),
                'rating': review.get('rating', 0),
                'sentiment': sentiment_info.get('label', 'neutral'),
                'sentiment_score': sentiment_info.get('score', 0.5),
                'created_at': review.get('created_at', '')
            }
            
            data.append(row)
        
        # Tạo DataFrame
        self.df = pd.DataFrame(data)
        
        # Chuyển đổi cột ngày tháng
        if 'created_at' in self.df.columns:
            self.df['created_at'] = pd.to_datetime(self.df['created_at'], errors='coerce')
            
            # Thêm các cột thời gian
            self.df['date'] = self.df['created_at'].dt.date
            self.df['year'] = self.df['created_at'].dt.year
            self.df['month'] = self.df['created_at'].dt.month
            self.df['week'] = self.df['created_at'].dt.isocalendar().week
            self.df['day'] = self.df['created_at'].dt.day
            self.df['hour'] = self.df['created_at'].dt.hour
    
    def get_sentiment_distribution(self) -> Dict[str, int]:
        """
        Tính toán phân phối cảm xúc trong toàn bộ dataset
        
        Returns:
            Dict[str, int]: Dictionary chứa số lượng mỗi loại cảm xúc
        """
        if self.df is None or self.df.empty:
            return {'positive': 0, 'neutral': 0, 'negative': 0}
        
        distribution = self.df['sentiment'].value_counts().to_dict()
        
        # Đảm bảo có đủ các key
        for sentiment in ['positive', 'neutral', 'negative']:
            if sentiment not in distribution:
                distribution[sentiment] = 0
        
        return distribution
    
    def get_sentiment_score_over_time(
        self, 
        time_unit: str = 'day',
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Tính toán điểm cảm xúc trung bình theo thời gian
        
        Args:
            time_unit (str): Đơn vị thời gian ('day', 'week', 'month', 'year')
            start_date (str, optional): Ngày bắt đầu, định dạng 'YYYY-MM-DD'
            end_date (str, optional): Ngày kết thúc, định dạng 'YYYY-MM-DD'
        
        Returns:
            pd.DataFrame: DataFrame chứa điểm cảm xúc theo thời gian
        """
        if self.df is None or self.df.empty or 'created_at' not in self.df.columns:
            return pd.DataFrame()
        
        # Lọc theo khoảng thời gian
        df_filtered = self.df.copy()
        if start_date:
            df_filtered = df_filtered[df_filtered['created_at'] >= pd.to_datetime(start_date)]
        if end_date:
            df_filtered = df_filtered[df_filtered['created_at'] <= pd.to_datetime(end_date)]
        
        # Chuyển đổi cảm xúc thành giá trị số
        df_filtered['sentiment_value'] = df_filtered['sentiment'].map({
            'positive': 1.0, 
            'neutral': 0.5, 
            'negative': 0.0
        })
        
        # Nhóm theo đơn vị thời gian
        if time_unit == 'day':
            grouped = df_filtered.groupby('date')
        elif time_unit == 'week':
            grouped = df_filtered.groupby(['year', 'week'])
        elif time_unit == 'month':
            grouped = df_filtered.groupby(['year', 'month'])
        elif time_unit == 'year':
            grouped = df_filtered.groupby('year')
        else:
            raise ValueError(f"Đơn vị thời gian không hợp lệ: {time_unit}")
        
        # Tính điểm trung bình và số lượng reviews
        result = grouped.agg({
            'sentiment_value': 'mean',
            'id': 'count'
        }).reset_index()
        
        result.rename(columns={
            'sentiment_value': 'avg_sentiment',
            'id': 'review_count'
        }, inplace=True)
        
        return result
    
    def get_sentiment_by_rating(self) -> pd.DataFrame:
        """
        Phân tích mối quan hệ giữa cảm xúc và rating
        
        Returns:
            pd.DataFrame: DataFrame chứa phân phối cảm xúc theo rating
        """
        if self.df is None or self.df.empty or 'rating' not in self.df.columns:
            return pd.DataFrame()
        
        # Nhóm theo rating và sentiment
        grouped = self.df.groupby(['rating', 'sentiment']).size().reset_index(name='count')
        
        # Pivot để có định dạng phù hợp
        pivot_table = grouped.pivot(index='rating', columns='sentiment', values='count').fillna(0)
        
        # Đảm bảo có đủ các cột
        for sentiment in ['positive', 'neutral', 'negative']:
            if sentiment not in pivot_table.columns:
                pivot_table[sentiment] = 0
        
        # Tính tổng số reviews cho mỗi rating
        pivot_table['total'] = pivot_table.sum(axis=1)
        
        # Tính tỷ lệ phần trăm
        for sentiment in ['positive', 'neutral', 'negative']:
            pivot_table[f'{sentiment}_pct'] = pivot_table[sentiment] / pivot_table['total'] * 100
        
        return pivot_table
    
    def compare_products(self, product_ids: List[str]) -> Dict[str, Dict[str, Union[float, int]]]:
        """
        So sánh cảm xúc giữa các sản phẩm
        
        Args:
            product_ids (List[str]): Danh sách ID sản phẩm cần so sánh
        
        Returns:
            Dict[str, Dict[str, Union[float, int]]]: Dictionary chứa thông tin cảm xúc cho mỗi sản phẩm
        """
        if self.df is None or self.df.empty or 'product_id' not in self.df.columns:
            return {}
        
        results = {}
        
        for product_id in product_ids:
            # Lọc reviews của sản phẩm
            product_reviews = self.df[self.df['product_id'] == product_id]
            
            if product_reviews.empty:
                continue
            
            # Tính phân phối cảm xúc
            sentiment_counts = product_reviews['sentiment'].value_counts().to_dict()
            
            # Đảm bảo có đủ các key
            for sentiment in ['positive', 'neutral', 'negative']:
                if sentiment not in sentiment_counts:
                    sentiment_counts[sentiment] = 0
            
            total_reviews = len(product_reviews)
            
            # Tính điểm cảm xúc tổng hợp
            sentiment_score = (
                (sentiment_counts['positive'] * 1.0) + 
                (sentiment_counts['neutral'] * 0.5) + 
                (sentiment_counts['negative'] * 0.0)
            ) / total_reviews if total_reviews > 0 else 0
            
            # Lưu kết quả
            results[product_id] = {
                'total_reviews': total_reviews,
                'sentiment_score': sentiment_score,
                'positive': sentiment_counts['positive'],
                'positive_pct': sentiment_counts['positive'] / total_reviews * 100 if total_reviews > 0 else 0,
                'neutral': sentiment_counts['neutral'],
                'neutral_pct': sentiment_counts['neutral'] / total_reviews * 100 if total_reviews > 0 else 0,
                'negative': sentiment_counts['negative'],
                'negative_pct': sentiment_counts['negative'] / total_reviews * 100 if total_reviews > 0 else 0,
                'avg_rating': product_reviews['rating'].mean() if 'rating' in product_reviews.columns else None
            }
        
        return results
    
    def get_top_products(self, n: int = 5, by: str = 'sentiment_score') -> pd.DataFrame:
        """
        Lấy top sản phẩm theo tiêu chí
        
        Args:
            n (int): Số lượng sản phẩm để trả về
            by (str): Tiêu chí xếp hạng ('sentiment_score', 'positive_count', 'negative_count')
        
        Returns:
            pd.DataFrame: DataFrame chứa top sản phẩm
        """
        if self.df is None or self.df.empty or 'product_id' not in self.df.columns:
            return pd.DataFrame()
        
        # Nhóm theo product_id
        grouped = self.df.groupby('product_id')
        
        # Tính các chỉ số cho mỗi sản phẩm
        product_stats = []
        
        for product_id, group in grouped:
            # Đếm số lượng mỗi loại cảm xúc
            sentiment_counts = group['sentiment'].value_counts().to_dict()
            
            # Đảm bảo có đủ các key
            for sentiment in ['positive', 'neutral', 'negative']:
                if sentiment not in sentiment_counts:
                    sentiment_counts[sentiment] = 0
            
            total_reviews = len(group)
            
            # Tính điểm cảm xúc tổng hợp
            sentiment_score = (
                (sentiment_counts['positive'] * 1.0) + 
                (sentiment_counts['neutral'] * 0.5) + 
                (sentiment_counts['negative'] * 0.0)
            ) / total_reviews
            
            product_stats.append({
                'product_id': product_id,
                'total_reviews': total_reviews,
                'sentiment_score': sentiment_score,
                'positive_count': sentiment_counts['positive'],
                'neutral_count': sentiment_counts['neutral'],
                'negative_count': sentiment_counts['negative'],
                'avg_rating': group['rating'].mean() if 'rating' in group.columns else None
            })
        
        # Chuyển đổi thành DataFrame
        products_df = pd.DataFrame(product_stats)
        
        # Sắp xếp theo tiêu chí
        if by == 'sentiment_score':
            products_df = products_df.sort_values('sentiment_score', ascending=False)
        elif by == 'positive_count':
            products_df = products_df.sort_values('positive_count', ascending=False)
        elif by == 'negative_count':
            products_df = products_df.sort_values('negative_count', ascending=False)
        elif by == 'total_reviews':
            products_df = products_df.sort_values('total_reviews', ascending=False)
        
        # Lấy top n sản phẩm
        return products_df.head(n)
    
    def plot_sentiment_over_time(
        self, 
        time_unit: str = 'day',
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        title: Optional[str] = None,
        save_path: Optional[str] = None
    ):
        """
        Vẽ biểu đồ xu hướng cảm xúc theo thời gian
        
        Args:
            time_unit (str): Đơn vị thời gian ('day', 'week', 'month', 'year')
            start_date (str, optional): Ngày bắt đầu, định dạng 'YYYY-MM-DD'
            end_date (str, optional): Ngày kết thúc, định dạng 'YYYY-MM-DD'
            title (str, optional): Tiêu đề biểu đồ
            save_path (str, optional): Đường dẫn để lưu biểu đồ
        
        Returns:
            matplotlib.figure.Figure: Biểu đồ
        """
        # Lấy dữ liệu
        time_series = self.get_sentiment_score_over_time(time_unit, start_date, end_date)
        
        if time_series.empty:
            print("Không có dữ liệu để vẽ biểu đồ!")
            return None
        
        # Tạo biểu đồ
        fig, ax1 = plt.subplots(figsize=(12, 6))
        
        # Trục x là thời gian
        if time_unit == 'day':
            x = time_series['date']
            x_label = 'Ngày'
        elif time_unit == 'week':
            # Tạo nhãn tuần
            x = time_series.apply(lambda row: f"{row['year']}-W{row['week']}", axis=1)
            x_label = 'Tuần'
        elif time_unit == 'month':
            # Tạo nhãn tháng
            x = time_series.apply(lambda row: f"{row['year']}-{row['month']}", axis=1)
            x_label = 'Tháng'
        elif time_unit == 'year':
            x = time_series['year']
            x_label = 'Năm'
        
        # Vẽ đường điểm cảm xúc
        color = 'tab:blue'
        ax1.set_xlabel(x_label)
        ax1.set_ylabel('Điểm cảm xúc trung bình', color=color)
        ax1.plot(x, time_series['avg_sentiment'], marker='o', linestyle='-', color=color)
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.set_ylim([0, 1])
        
        # Vẽ số lượng reviews trên trục y thứ hai
        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.set_ylabel('Số lượng reviews', color=color)
        ax2.bar(x, time_series['review_count'], alpha=0.3, color=color)
        ax2.tick_params(axis='y', labelcolor=color)
        
        # Xoay nhãn trục x nếu cần
        if time_unit in ['day', 'week', 'month']:
            plt.xticks(rotation=45)
        
        # Tiêu đề
        if title:
            plt.title(title)
        else:
            plt.title(f'Xu hướng cảm xúc theo {x_label.lower()}')
        
        plt.tight_layout()
        
        # Lưu biểu đồ nếu cần
        if save_path:
            plt.savefig(save_path)
        
        return fig
    
    def plot_sentiment_distribution(self, save_path: Optional[str] = None):
        """
        Vẽ biểu đồ phân phối cảm xúc
        
        Args:
            save_path (str, optional): Đường dẫn để lưu biểu đồ
        
        Returns:
            matplotlib.figure.Figure: Biểu đồ
        """
        # Lấy phân phối cảm xúc
        distribution = self.get_sentiment_distribution()
        
        # Tạo biểu đồ
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Biểu đồ cột
        categories = ['Positive', 'Neutral', 'Negative']
        values = [distribution['positive'], distribution['neutral'], distribution['negative']]
        colors = ['green', 'gray', 'red']
        
        ax1.bar(categories, values, color=colors)
        ax1.set_title('Phân phối cảm xúc')
        ax1.set_ylabel('Số lượng reviews')
        
        # Thêm số liệu trên các cột
        for i, v in enumerate(values):
            ax1.text(i, v + 0.1, str(v), ha='center')
        
        # Biểu đồ tròn
        total = sum(values)
        labels = [f'Positive ({values[0]/total*100:.1f}%)', 
                  f'Neutral ({values[1]/total*100:.1f}%)', 
                  f'Negative ({values[2]/total*100:.1f}%)']
        
        ax2.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax2.set_title('Tỷ lệ cảm xúc')
        ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        
        plt.tight_layout()
        
        # Lưu biểu đồ nếu cần
        if save_path:
            plt.savefig(save_path)
        
        return fig
    
    def plot_sentiment_by_rating(self, save_path: Optional[str] = None):
        """
        Vẽ biểu đồ cảm xúc theo rating
        
        Args:
            save_path (str, optional): Đường dẫn để lưu biểu đồ
        
        Returns:
            matplotlib.figure.Figure: Biểu đồ
        """
        # Lấy dữ liệu
        rating_data = self.get_sentiment_by_rating()
        
        if rating_data.empty:
            print("Không có dữ liệu để vẽ biểu đồ!")
            return None
        
        # Tạo biểu đồ
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Biểu đồ cột cho số lượng
        rating_data[['positive', 'neutral', 'negative']].plot(
            kind='bar', stacked=True, color=['green', 'gray', 'red'], ax=ax1
        )
        ax1.set_title('Phân phối cảm xúc theo rating (số lượng)')
        ax1.set_xlabel('Rating')
        ax1.set_ylabel('Số lượng reviews')
        
        # Biểu đồ cột cho tỷ lệ phần trăm
        rating_data[['positive_pct', 'neutral_pct', 'negative_pct']].plot(
            kind='bar', stacked=True, color=['green', 'gray', 'red'], ax=ax2
        )
        ax2.set_title('Phân phối cảm xúc theo rating (phần trăm)')
        ax2.set_xlabel('Rating')
        ax2.set_ylabel('Phần trăm')
        
        plt.tight_layout()
        
        # Lưu biểu đồ nếu cần
        if save_path:
            plt.savefig(save_path)
        
        return fig
    
    def plot_product_comparison(self, product_ids: List[str], save_path: Optional[str] = None):
        """
        Vẽ biểu đồ so sánh cảm xúc giữa các sản phẩm
        
        Args:
            product_ids (List[str]): Danh sách ID sản phẩm cần so sánh
            save_path (str, optional): Đường dẫn để lưu biểu đồ
        
        Returns:
            matplotlib.figure.Figure: Biểu đồ
        """
        # Lấy dữ liệu
        comparison = self.compare_products(product_ids)
        
        if not comparison:
            print("Không có dữ liệu để vẽ biểu đồ!")
            return None
        
        # Tạo DataFrame từ kết quả
        df = pd.DataFrame.from_dict(comparison, orient='index')
        
        # Sắp xếp theo điểm cảm xúc
        df = df.sort_values('sentiment_score', ascending=False)
        
        # Tạo biểu đồ
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Biểu đồ cột cho điểm cảm xúc
        ax1.bar(df.index, df['sentiment_score'], color='blue')
        ax1.set_title('Điểm cảm xúc trung bình theo sản phẩm')
        ax1.set_xlabel('ID sản phẩm')
        ax1.set_ylabel('Điểm cảm xúc (0-1)')
        ax1.set_ylim([0, 1])
        
        # Xoay nhãn trục x
        plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')
        
        # Biểu đồ cột cho phân phối cảm xúc
        df[['positive_pct', 'neutral_pct', 'negative_pct']].plot(
            kind='bar', stacked=True, color=['green', 'gray', 'red'], ax=ax2
        )
        ax2.set_title('Phân phối cảm xúc theo sản phẩm (phần trăm)')
        ax2.set_xlabel('ID sản phẩm')
        ax2.set_ylabel('Phần trăm')
        
        plt.tight_layout()
        
        # Lưu biểu đồ nếu cần
        if save_path:
            plt.savefig(save_path)
        
        return fig 