from typing import Dict, List, Any, Optional
from .base import BaseAgent
import tweepy
import facebook
from linkedin_api import Linkedin
import instaloader
from time import sleep
import json

from datetime import datetime, timedelta
from pathlib import Path
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')

class SocialMediaAgent(BaseAgent):
    """Agent for collecting data from social media platforms"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("SocialMediaAgent")
        self.config = config
        self.clients = self._initialize_clients()
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
    def _initialize_clients(self) -> Dict[str, Any]:
        """Initialize API clients for configured platforms"""
        clients = {}
        
        # Twitter Client
        if 'twitter' in self.config:
            try:
                clients['twitter'] = tweepy.Client(
                    bearer_token=self.config['twitter']['bearer_token'],
                    consumer_key=self.config['twitter']['api_key'],
                    consumer_secret=self.config['twitter']['api_secret'],
                    access_token=self.config['twitter']['access_token'],
                    access_token_secret=self.config['twitter']['access_token_secret']
                )
            except Exception as e:
                self.logger.error(f"Twitter client failed: {str(e)}")
        
        # Facebook Client
        if 'facebook' in self.config:
            try:
                clients['facebook'] = facebook.GraphAPI(
                    access_token=self.config['facebook']['access_token'],
                    version=self.config['facebook'].get('version', '3.1')
                )
            except Exception as e:
                self.logger.error(f"Facebook client failed: {str(e)}")
        
        # LinkedIn Client
        if 'linkedin' in self.config:
            try:
                clients['linkedin'] = Linkedin(
                    self.config['linkedin']['username'],
                    self.config['linkedin']['password']
                )
            except Exception as e:
                self.logger.error(f"LinkedIn client failed: {str(e)}")
        
        # Instagram Client
        if 'instagram' in self.config:
            try:
                loader = instaloader.Instaloader()
                if 'username' in self.config['instagram']:
                    loader.login(
                        self.config['instagram']['username'],
                        self.config['instagram']['password']
                    )
                clients['instagram'] = loader
            except Exception as e:
                self.logger.error(f"Instagram client failed: {str(e)}")
        
        return clients
    
    def collect(self, keywords: List[str], days_back: int = 7, max_items: int = 100) -> Dict[str, List[Dict]]:
        """Collect data from all configured platforms"""
        results = {}
        since_date = datetime.now() - timedelta(days=days_back)
        
        for platform, client in self.clients.items():
            if client is None:
                continue
                
            try:
                if platform == 'twitter':
                    results[platform] = self._collect_twitter(keywords, since_date, max_items)
                elif platform == 'facebook':
                    results[platform] = self._collect_facebook(keywords, since_date, max_items)
                elif platform == 'linkedin':
                    results[platform] = self._collect_linkedin(keywords, max_items)
                elif platform == 'instagram':
                    results[platform] = self._collect_instagram(keywords, max_items)
                
            except Exception as e:
                self.logger.error(f"{platform} collection failed: {str(e)}")
                results[platform] = []
        
        return results
    
    def _collect_twitter(self, keywords: List[str], since_date: datetime, max_items: int) -> List[Dict]:
        """Collect data from Twitter"""
        tweets = []
        for keyword in keywords:
            try:
                response = self.clients['twitter'].search_recent_tweets(
                    query=keyword,
                    max_results=min(max_items, 100),
                    start_time=since_date
                )
                if response.data:
                    for tweet in response.data:
                        tweets.append({
                            'id': tweet.id,
                            'text': tweet.text,
                            'created_at': tweet.created_at.isoformat(),
                            'keyword': keyword,
                            'platform': 'twitter'
                        })
                sleep(1)  # Respect rate limits
            except Exception as e:
                self.logger.error(f"Error collecting tweets for {keyword}: {str(e)}")
        return tweets
    
    def _collect_facebook(self, keywords: List[str], since_date: datetime, max_items: int) -> List[Dict]:
        """Collect data from Facebook"""
        posts = []
        for keyword in keywords:
            try:
                response = self.clients['facebook'].search(
                    type='post',
                    q=keyword,
                    limit=max_items
                )
                for post in response['data']:
                    if datetime.strptime(post['created_time'], '%Y-%m-%dT%H:%M:%S+0000') >= since_date:
                        posts.append({
                            'id': post['id'],
                            'message': post.get('message', ''),
                            'created_time': post['created_time'],
                            'keyword': keyword,
                            'platform': 'facebook'
                        })
                sleep(1)  # Respect rate limits
            except Exception as e:
                self.logger.error(f"Error collecting Facebook posts for {keyword}: {str(e)}")
        return posts
    
    def _collect_linkedin(self, keywords: List[str], max_items: int) -> List[Dict]:
        """Collect data from LinkedIn"""
        posts = []
        for keyword in keywords:
            try:
                results = self.clients['linkedin'].search_posts(keyword, limit=max_items)
                for post in results:
                    posts.append({
                        'urn': post['urn'],
                        'text': post.get('text', ''),
                        'created_time': post.get('created_time', ''),
                        'keyword': keyword,
                        'platform': 'linkedin'
                    })
                sleep(1)  # Respect rate limits
            except Exception as e:
                self.logger.error(f"Error collecting LinkedIn posts for {keyword}: {str(e)}")
        return posts
    
    def _collect_instagram(self, keywords: List[str], max_items: int) -> List[Dict]:
        """Collect data from Instagram"""
        posts = []
        for keyword in keywords:
            try:
                hashtag_posts = self.clients['instagram'].get_hashtag_posts(keyword.replace('#', ''))
                count = 0
                for post in hashtag_posts:
                    if count >= max_items:
                        break
                    posts.append({
                        'id': post.mediaid,
                        'caption': post.caption if post.caption else '',
                        'timestamp': post.date_utc.isoformat(),
                        'keyword': keyword,
                        'platform': 'instagram'
                    })
                    count += 1
                sleep(2)  # Respect rate limits
            except Exception as e:
                self.logger.error(f"Error collecting Instagram posts for {keyword}: {str(e)}")
        return posts
    
    def process(self, raw_data: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Add sentiment analysis and basic metrics"""
        processed = {
            'metadata': {
                'collection_date': datetime.now().isoformat(),
                'platforms': list(raw_data.keys()),
                'total_items': sum(len(posts) for posts in raw_data.values())
            },
            'data': raw_data,
            'analytics': {
                'sentiment': self._calculate_sentiment(raw_data),
                'engagement': self._calculate_engagement(raw_data)
            }
        }
        return processed
    
    def _calculate_sentiment(self, data: Dict[str, List[Dict]]) -> Dict[str, float]:
        """Calculate average sentiment scores"""
        sentiment_scores = {'positive': 0, 'neutral': 0, 'negative': 0, 'compound': 0}
        total_items = 0
        
        for platform, posts in data.items():
            for post in posts:
                text = post.get('text', '') or post.get('message', '') or post.get('caption', '')
                if text:
                    scores = self.sentiment_analyzer.polarity_scores(text)
                    sentiment_scores['positive'] += scores['pos']
                    sentiment_scores['neutral'] += scores['neu']
                    sentiment_scores['negative'] += scores['neg']
                    sentiment_scores['compound'] += scores['compound']
                    total_items += 1
        
        if total_items > 0:
            for key in sentiment_scores:
                sentiment_scores[key] /= total_items
        
        return sentiment_scores
    
    def _calculate_engagement(self, data: Dict[str, List[Dict]]) -> Dict[str, int]:
        """Calculate basic engagement metrics"""
        engagement = {
            'total_posts': sum(len(posts) for posts in data.values()),
            'platform_distribution': {platform: len(posts) for platform, posts in data.items()},
            'keyword_distribution': {}
        }
        
        # Count keyword occurrences
        keyword_counts = {}
        for platform, posts in data.items():
            for post in posts:
                keyword = post['keyword']
                keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
        
        engagement['keyword_distribution'] = keyword_counts
        return engagement
