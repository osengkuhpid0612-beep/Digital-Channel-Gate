#!/usr/bin/env python3
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import os

class DataFetcher:
    def __init__(self, config_path="config/sources.json"):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        self.timestamp = datetime.now().isoformat()
    
    def fetch_news(self):
        articles = []
        for source in self.config.get('news_sources', []):
            if not source.get('enabled'):
                continue
            try:
                resp = requests.get(source['url'], timeout=10)
                resp.encoding = 'utf-8'
                soup = BeautifulSoup(resp.text, 'html.parser')
                
                articles.append({
                    'source': source['name'],
                    'url': source['url'],
                    'category': source['category'],
                    'timestamp': self.timestamp,
                    'status': 'fetched'
                })
            except Exception as e:
                print(f"Error fetching {source['name']}: {e}")
        
        return articles
    
    def fetch_tech(self):
        articles = []
        for source in self.config.get('tech_sources', []):
            if not source.get('enabled'):
                continue
            try:
                resp = requests.get(source['url'], timeout=10)
                resp.encoding = 'utf-8'
                soup = BeautifulSoup(resp.text, 'html.parser')
                
                articles.append({
                    'source': source['name'],
                    'url': source['url'],
                    'category': source['category'],
                    'timestamp': self.timestamp,
                    'status': 'fetched'
                })
            except Exception as e:
                print(f"Error fetching {source['name']}: {e}")
        
        return articles
    
    def save_raw_data(self, data, filename):
        os.makedirs('data/raw', exist_ok=True)
        filepath = f"data/raw/{filename}"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 資料已保存到 {filepath}")

if __name__ == "__main__":
    fetcher = DataFetcher()
    
    print("開始收集新聞...")
    news = fetcher.fetch_news()
    fetcher.save_raw_data(news, f"news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    
    print("開始收集科技資訊...")
    tech = fetcher.fetch_tech()
    fetcher.save_raw_data(tech, f"tech_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    
    print("✅ 資料收集完成")
