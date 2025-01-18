import os
import yaml
from typing import Dict, Any
from dotenv import load_dotenv

class Settings:
    """Configuration management for the AI Research Agent."""
    
    def __init__(self, config_path: str = None):
        """
        Initialize settings from config file and environment variables.
        
        Args:
            config_path: Optional path to config YAML file
        """
        # Load environment variables
        load_dotenv()
        
        # Load config file if provided
        self.config = {}
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
                
        # Initialize default settings
        self.initialize_defaults()
        
        # Override with environment variables
        self.override_from_env()
        
    def initialize_defaults(self):
        """Set default configuration values."""
        self.config.setdefault('social_media', {
            'twitter': {
                'enabled': False,
                'rate_limit': 300,
                'batch_size': 100
            },
            'facebook': {
                'enabled': False,
                'rate_limit': 200,
                'batch_size': 50
            },
            'linkedin': {
                'enabled': False,
                'rate_limit': 100,
                'batch_size': 25
            },
            'instagram': {
                'enabled': False,
                'rate_limit': 200,
                'batch_size': 50
            }
        })
        
        self.config.setdefault('web_scraper', {
            'max_depth': 2,
            'max_pages_per_domain': 100,
            'request_delay': 1.0,
            'timeout': 30,
            'user_agents': [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            ]
        })
        
        self.config.setdefault('storage', {
            'data_dir': 'data',
            'raw_dir': 'data/raw',
            'processed_dir': 'data/processed'
        })
        
        self.config.setdefault('logging', {
            'level': 'INFO',
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'file': 'logs/agent.log'
        })
        
    def override_from_env(self):
        """Override settings from environment variables."""
        # Social Media Credentials
        if os.getenv('TWITTER_API_KEY'):
            self.config['social_media']['twitter'].update({
                'enabled': True,
                'api_key': os.getenv('TWITTER_API_KEY'),
                'api_secret': os.getenv('TWITTER_API_SECRET'),
                'access_token': os.getenv('TWITTER_ACCESS_TOKEN'),
                'access_token_secret': os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
            })
            
        if os.getenv('FACEBOOK_ACCESS_TOKEN'):
            self.config['social_media']['facebook'].update({
                'enabled': True,
                'access_token': os.getenv('FACEBOOK_ACCESS_TOKEN')
            })
            
        if os.getenv('LINKEDIN_USERNAME'):
            self.config['social_media']['linkedin'].update({
                'enabled': True,
                'username': os.getenv('LINKEDIN_USERNAME'),
                'password': os.getenv('LINKEDIN_PASSWORD')
            })
            
        if os.getenv('INSTAGRAM_USERNAME'):
            self.config['social_media']['instagram'].update({
                'enabled': True,
                'username': os.getenv('INSTAGRAM_USERNAME'),
                'password': os.getenv('INSTAGRAM_PASSWORD')
            })
            
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Configuration key (dot notation supported)
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
                
        return value
        
    def update(self, key: str, value: Any):
        """
        Update a configuration value.
        
        Args:
            key: Configuration key (dot notation supported)
            value: New value
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            config = config.setdefault(k, {})
            
        config[keys[-1]] = value