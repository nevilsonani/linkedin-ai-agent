from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from database import DBManager
import time
import datetime

class LinkedInScraper:
    def __init__(self):
        self.db = DBManager()
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=options)
    
    def scrape_profile(self, profile_url):
        self.driver.get(profile_url)
        time.sleep(5)  # Wait for page load
        
        # Scroll to load posts
        for _ in range(3):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        posts = soup.find_all('div', class_='feed-shared-update-v2')
        
        for post in posts:
            try:
                content_span = post.find('span', class_='break-words')
                content = content_span.get_text(strip=True) if content_span else ""
                
                # Engagement extraction (likes, comments, shares)
                likes = 0
                comments = 0
                shares = 0
                
                # Likes count
                likes_span = post.find('span', class_='social-details-social-counts__reactions-count')
                if likes_span and likes_span.text.strip():
                    likes = int(likes_span.text.strip().replace(',', ''))
                
                # Comments count
                comments_span = post.find('span', class_='social-details-social-counts__comments')
                if comments_span and comments_span.text.strip():
                    try:
                        comments = int(comments_span.text.strip().split()[0].replace(',', ''))
                    except:
                        comments = 0
                
                # Shares count (may not always be available)
                shares_span = post.find('span', class_='social-details-social-counts__shares')
                if shares_span and shares_span.text.strip():
                    try:
                        shares = int(shares_span.text.strip().split()[0].replace(',', ''))
                    except:
                        shares = 0
                
                hashtags = [tag.get_text(strip=True) for tag in post.find_all('a', class_='hash-tag')]
                
                self.db.conn.execute('''
                    INSERT INTO posts (content, likes, comments, shares, hashtags, post_time)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (content, likes, comments, shares, ','.join(hashtags), datetime.datetime.now()))
            except Exception as e:
                print(f"Error scraping post: {e}")
        
        self.db.conn.commit()
    
    def close(self):
        self.driver.quit()
