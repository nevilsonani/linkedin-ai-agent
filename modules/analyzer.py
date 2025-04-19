import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from database import DBManager
from collections import Counter

class ContentAnalyzer:
    def __init__(self):
        self.db = DBManager()
    
    def get_top_topics(self, n=5):
        df = pd.read_sql('SELECT content FROM posts', self.db.conn)
        if df.empty:
            return []
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        X = vectorizer.fit_transform(df['content'])
        
        kmeans = KMeans(n_clusters=n, random_state=42).fit(X)
        order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
        terms = vectorizer.get_feature_names_out()
        
        topics = []
        for i in range(n):
            topic_terms = [terms[ind] for ind in order_centroids[i, :5]]
            topics.append(', '.join(topic_terms))
        return topics
    
    def get_optimal_times(self):
        df = pd.read_sql('''
            SELECT 
                strftime('%w', post_time) as weekday,
                strftime('%H', post_time) as hour,
                AVG(likes + comments*2 + shares*3) as engagement
            FROM posts 
            GROUP BY weekday, hour
        ''', self.db.conn)
        if df.empty:
            return pd.DataFrame()
        idx = df.groupby('weekday')['engagement'].idxmax()
        return df.loc[idx].sort_values('weekday')
    
    def get_top_hashtags(self, top_n=10):
        df = pd.read_sql('SELECT hashtags FROM posts', self.db.conn)
        if df.empty:
            return []
        all_hashtags = []
        for tags in df['hashtags'].dropna():
            all_hashtags.extend([tag.strip() for tag in tags.split(',') if tag.strip()])
        counter = Counter(all_hashtags)
        return [tag for tag, _ in counter.most_common(top_n)]
