from typing import Dict, List, Any, Optional
from ..agents.base import BaseAgent
import tweepy
import facebook
from linkedin_api import Linkedin
import instaloader
from time import sleep
import json
from datetime import datetime, timedelta

class SocialMediaAgent(BaseAgent):
    """Agent for collecting data from various social media platforms."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.platforms = {}
        self.setup_platforms()
        
    def setup_platforms(self):
        """Initialize connections to different social media platforms."""
        if "twitter" in self.config:
            self.platforms["twitter"] = self._setup_twitter()
        if "facebook" in self.config:
            self.platforms["facebook"] = self._setup_facebook()
        if "linkedin" in self.config:
            self.platforms["linkedin"] = self._setup_linkedin()
        if "instagram" in self.config:
            self.platforms["instagram"] = self._setup_instagram()
            
    def _setup_twitter(self) -> tweepy.Client:
        """Setup Twitter API client."""
        try:
            client = tweepy.Client(
                bearer_token=self.config["twitter"]["bearer_token"],
                consumer_key=self.config["twitter"]["api_key"],
                consumer_secret=self.config["twitter"]["api_secret"],
                access_token=self.config["twitter"]["access_token"],
                access_token_secret=self.config["twitter"]["access_token_secret"]
            )
            self.logger.info("Twitter API client initialized successfully")
            return client
        except Exception as e:
            self.logger.error(f"Failed to initialize Twitter client: {str(e)}")
            return None
            
    def _setup_facebook(self) -> facebook.GraphAPI:
        """Setup Facebook API client."""
        try:
            graph = facebook.GraphAPI(
                access_token=self.config["facebook"]["access_token"],
                version=self.config["facebook"].get("version", "3.1")
            )
            self.logger.info("Facebook API client initialized successfully")
            return graph
        except Exception as e:
            self.logger.error(f"Failed to initialize Facebook client: {str(e)}")
            return None
            
    def _setup_linkedin(self) -> Linkedin:
        """Setup LinkedIn API client."""
        try:
            client = Linkedin(
                self.config["linkedin"]["username"],
                self.config["linkedin"]["password"]
            )
            self.logger.info("LinkedIn API client initialized successfully")
            return client
        except Exception as e:
            self.logger.error(f"Failed to initialize LinkedIn client: {str(e)}")
            return None
            
    def _setup_instagram(self) -> instaloader.Instaloader:
        """Setup Instagram client."""
        try:
            loader = instaloader.Instaloader()
            if "username" in self.config["instagram"]:
                loader.login(
                    self.config["instagram"]["username"],
                    self.config["instagram"]["password"]
                )
            self.logger.info("Instagram client initialized successfully")
            return loader
        except Exception as e:
            self.logger.error(f"Failed to initialize Instagram client: {str(e)}")
            return None
            
    def collect(self, 
                keywords: List[str], 
                days_back: int = 7, 
                max_items: int = 100) -> Dict[str, List[Dict]]:
        """
        Collect data from all configured social media platforms.
        
        Args:
            keywords: List of keywords to search for
            days_back: Number of days of historical data to collect
            max_items: Maximum number of items to collect per platform
            
        Returns:
            Dictionary containing collected data from each platform
        """
        data = {}
        since_date = datetime.now() - timedelta(days=days_back)
        
        for platform, client in self.platforms.items():
            if client is None:
                continue
                
            self.logger.info(f"Collecting data from {platform}")
            try:
                if platform == "twitter":
                    data[platform] = self._collect_twitter(keywords, since_date, max_items)
                elif platform == "facebook":
                    data[platform] = self._collect_facebook(keywords, since_date, max_items)
                elif platform == "linkedin":
                    data[platform] = self._collect_linkedin(keywords, max_items)
                elif platform == "instagram":
                    data[platform] = self._collect_instagram(keywords, max_items)
                    
                self.logger.info(f"Successfully collected {len(data[platform])} items from {platform}")
            except Exception as e:
                self.logger.error(f"Error collecting data from {platform}: {str(e)}")
                data[platform] = []
                
        return data
        
    def _collect_twitter(self, keywords: List[str], since_date: datetime, max_items: int) -> List[Dict]:
        """Collect data from Twitter."""
        tweets = []
        for keyword in keywords:
            try:
                response = self.platforms["twitter"].search_recent_tweets(
                    query=keyword,
                    max_results=min(max_items, 100),
                    start_time=since_date
                )
                if response.data:
                    for tweet in response.data:
                        tweets.append({
                            "id": tweet.id,
                            "text": tweet.text,
                            "created_at": tweet.created_at.isoformat(),
                            "keyword": keyword
                        })
                sleep(1)  # Respect rate limits
            except Exception as e:
                self.logger.error(f"Error collecting tweets for keyword {keyword}: {str(e)}")
                
        return tweets
        
    def _collect_facebook(self, keywords: List[str], since_date: datetime, max_items: int) -> List[Dict]:
        """Collect data from Facebook."""
        posts = []
        for keyword in keywords:
            try:
                response = self.platforms["facebook"].search(
                    type='post',
                    q=keyword,
                    limit=max_items
                )
                for post in response['data']:
                    if datetime.strptime(post['created_time'], '%Y-%m-%dT%H:%M:%S+0000') >= since_date:
                        posts.append({
                            "id": post["id"],
                            "message": post.get("message", ""),
                            "created_time": post["created_time"],
                            "keyword": keyword
                        })
                sleep(1)  # Respect rate limits
            except Exception as e:
                self.logger.error(f"Error collecting Facebook posts for keyword {keyword}: {str(e)}")
                
        return posts

    def _collect_linkedin(self, keywords: List[str], max_items: int) -> List[Dict]:
        """Collect data from LinkedIn."""
        posts = []
        for keyword in keywords:
            try:
                results = self.platforms["linkedin"].search_posts(keyword, limit=max_items)
                for post in results:
                    posts.append({
                        "urn": post["urn"],
                        "text": post.get("text", ""),
                        "created_time": post.get("created_time", ""),
                        "keyword": keyword
                    })
                sleep(1)  # Respect rate limits
            except Exception as e:
                self.logger.error(f"Error collecting LinkedIn posts for keyword {keyword}: {str(e)}")
                
        return posts

    def _collect_instagram(self, keywords: List[str], max_items: int) -> List[Dict]:
        """Collect data from Instagram."""
        posts = []
        for keyword in keywords:
            try:
                hashtag_posts = self.platforms["instagram"].get_hashtag_posts(
                    keyword.replace("#", "")
                )
                count = 0
                for post in hashtag_posts:
                    if count >= max_items:
                        break
                    posts.append({
                        "id": post.mediaid,
                        "caption": post.caption if post.caption else "",
                        "timestamp": post.date_utc.isoformat(),
                        "keyword": keyword
                    })
                    count += 1
                sleep(2)  # Respect rate limits
            except Exception as e:
                self.logger.error(f"Error collecting Instagram posts for keyword {keyword}: {str(e)}")
                
        return posts

    def process(self, data: Dict[str, List[Dict]], *args, **kwargs) -> Dict[str, Any]:
        """
        Process collected social media data.
        
        Args:
            data: Dictionary containing collected data from each platform
            
        Returns:
            Processed data with analytics and insights
        """
        processed_data = {
            "metadata": {
                "collection_date": datetime.now().isoformat(),
                "platforms": list(data.keys()),
                "total_items": sum(len(items) for items in data.values())
            },
            "data": data,
            "analytics": self._generate_analytics(data)
        }
        
        return processed_data
        
    def _generate_analytics(self, data: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Generate analytics from collected data."""
        analytics = {
            "platform_stats": {},
            "keyword_stats": {},
            "temporal_analysis": {}
        }
        
        # Platform statistics
        for platform, items in data.items():
            analytics["platform_stats"][platform] = {
                "total_items": len(items),
                "unique_keywords": len(set(item["keyword"] for item in items))
            }
            
        # Keyword statistics
        all_keywords = [item["keyword"] for items in data.values() for item in items]
        for keyword in set(all_keywords):
            analytics["keyword_stats"][keyword] = {
                "total_mentions": all_keywords.count(keyword),
                "platform_breakdown": {
                    platform: len([item for item in items if item["keyword"] == keyword])
                    for platform, items in data.items()
                }
            }
            
        return analytics