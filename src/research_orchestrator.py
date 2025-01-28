from typing import List, Dict, Any
from pathlib import Path
import json
from datetime import datetime
from src.agents.social_media import SocialMediaAgent
from src.agents.web_scraper import WebScraperAgent
from src.analysis.sentiment import SentimentAnalyzer
from src.visualization.dashboards import ResearchDashboard
from src.utils.logger import setup_logger

class ResearchOrchestrator:
    """Main controller for research operations"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = setup_logger("ResearchOrchestrator")
        
        # Initialize agents
        self.social_agent = SocialMediaAgent(config.get('social_media', {}))
        self.web_agent = WebScraperAgent(config.get('web_scraper', {}))
        
        # Initialize analysis and visualization components
        self.analyzer = SentimentAnalyzer()
        self.dashboard = ResearchDashboard()
        
    def run_pipeline(
        self,
        keywords: List[str],
        websites: List[str] = None,
        days_back: int = 7,
        max_items: int = 100
    ) -> Dict[str, Any]:
        """
        Execute complete research pipeline:
        1. Data Collection
        2. Data Processing
        3. Advanced Analysis
        4. Visualization
        5. Save Results
        """
        self.logger.info("Starting research pipeline...")
        
        # Data Collection
        self.logger.info("Collecting social media data...")
        social_data = self.social_agent.collect(
            keywords=keywords,
            days_back=days_back,
            max_items=max_items
        )
        
        web_data = {}
        if websites:
            self.logger.info("Collecting web data...")
            web_data = self.web_agent.collect(
                urls=websites,
                max_items=max_items
            )
        
        # Data Processing
        self.logger.info("Processing social media data...")
        processed_social = self.social_agent.process(social_data)
        
        processed_web = {}
        if web_data:
            self.logger.info("Processing web data...")
            processed_web = self.web_agent.process(web_data)
        
        # Advanced Analysis
        self.logger.info("Performing sentiment analysis...")
        sentiment_report = self.analyzer.generate_report(
            processed_social.get('data', {})
        )
        
        # Generate Outputs
        self.logger.info("Saving results...")
        save_paths = self._save_results(
            social=processed_social,
            web=processed_web,
            sentiment=sentiment_report
        )
        
        # Visualizations
        self.logger.info("Generating dashboard...")
        dashboard_url = self.dashboard.create_dashboard(
            social_data=processed_social,
            web_data=processed_web,
            sentiment=sentiment_report
        )
        
        self.logger.info("Research pipeline completed successfully!")
        
        return {
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'dashboard_url': dashboard_url,
            'data_locations': save_paths
        }
    
    def _save_results(self, **data_categories) -> Dict[str, str]:
        """Save processed data to organized directory structure"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%m%S')
        output_dir = Path(self.config['storage']['processed_dir']) / timestamp
        save_paths = {}
        
        for category, data in data_categories.items():
            if not data:
                continue
                
            category_dir = output_dir / category
            category_dir.mkdir(parents=True, exist_ok=True)
            
            output_path = category_dir / f'{category}_data.json'
            try:
                with open(output_path, 'w') as f:
                    json.dump(data, f, indent=2)
                save_paths[category] = str(output_path)
                self.logger.info(f"Saved {category} data to {output_path}")
            except Exception as e:
                self.logger.error(f"Failed to save {category} data: {str(e)}")
                raise
        
        return save_paths
    
    def _validate_inputs(self, keywords: List[str], websites: List[str]) -> None:
        """Validate research inputs"""
        if not keywords:
            raise ValueError("At least one keyword is required")
        
        if websites:
            for website in websites:
                if not website.startswith(('http://', 'https://')):
                    raise ValueError(f"Invalid website URL: {website}")
    
    def _generate_report(self, social_data: Dict, web_data: Dict) -> Dict[str, Any]:
        """Generate a comprehensive research report"""
        report = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'keywords': social_data.get('metadata', {}).get('keywords', []),
                'websites': web_data.get('metadata', {}).get('websites', []),
                'total_items': {
                    'social_media': social_data.get('metadata', {}).get('total_items', 0),
                    'web': web_data.get('metadata', {}).get('total_pages', 0)
                }
            },
            'analytics': {
                'sentiment': self.analyzer.generate_report(social_data.get('data', {})),
                'engagement': social_data.get('analytics', {}).get('engagement', {})
            }
        }
        return report