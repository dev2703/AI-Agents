from typing import List, Dict, Any
from config.settings import Settings
from utils.logger import Logger
from agents.social_media import SocialMediaAgent
from agents.web_scraper import WebScraperAgent
import argparse
import json
import streamlit as st
from datetime import datetime
from ui import user_interface

class ResearchOrchestrator:
    """Main orchestrator for the AI Research Agent system."""
    
    def __init__(self, config_path: str = None):
        """
        Initialize the orchestrator.
        
        Args:
            config_path: Optional path to config file
        """
        # Initialize settings
        self.settings = Settings(config_path)
        
        # Initialize logger
        self.logger = Logger(
            name="ResearchOrchestrator",
            level=self.settings.get('logging.level', 'INFO'),
            log_file=self.settings.get('logging.file')
        )
        
        # Initialize agents
        self.social_media_agent = SocialMediaAgent(self.settings.get('social_media'))
        self.web_scraper_agent = WebScraperAgent(self.settings.get('web_scraper'))
        
    def run_research(self, 
                    keywords: List[str],
                    websites: List[str] = None,
                    days_back: int = 7,
                    max_items: int = 100) -> Dict[str, Any]:
        """
        Run a complete research operation.
        
        Args:
            keywords: List of keywords to research
            websites: Optional list of websites to scrape
            days_back: Number of days of historical data to collect
            max_items: Maximum items to collect per source
            
        Returns:
            Dictionary containing all collected and processed data
        """
        self.logger.info(f"Starting research for keywords: {keywords}")
        results = {
            "metadata": {
                "keywords": keywords,
                "websites": websites,
                "days_back": days_back,
                "max_items": max_items,
                "timestamp": datetime.now().isoformat()
            },
            "data": {}
        }
        
        # Collect social media data
        try:
            social_media_data = self.social_media_agent.collect(
                keywords=keywords,
                days_back=days_back,
                max_items=max_items
            )
            results["data"]["social_media"] = social_media_data
        except Exception as e:
            self.logger.error(f"Error collecting social media data: {str(e)}")
            
        # Collect web data if websites provided
        if websites:
            try:
                web_data = self.web_scraper_agent.collect(
                    urls=websites,
                    max_pages=max_items
                )
                results["data"]["web"] = web_data
            except Exception as e:
                self.logger.error(f"Error collecting web data: {str(e)}")
                
        # Save results
        self._save_results(results)
        
        return results
        
    def _save_results(self, results: Dict[str, Any]):
        """Save research results to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"research_results_{timestamp}.json"
        
        output_dir = self.settings.get('storage.processed_dir', 'data/processed')
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        output_path = Path(output_dir) / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
            
        self.logger.info(f"Results saved to {output_path}")

def main():
    """Command line interface for the research agent."""
    parser = argparse.ArgumentParser(description='AI Research Agent')
    parser.add_argument('--config', type=str, help='Path to config file')
    parser.add_argument('--keywords', type=str, nargs='+', required=True,
                       help='Keywords to research')
    parser.add_argument('--websites', type=str, nargs='+',
                       help='Websites to scrape')
    parser.add_argument('--days-back', type=int, default=7,
                       help='Number of days of historical data to collect')
    parser.add_argument('--max-items', type=int, default=100,
                       help='Maximum items to collect per source')
                       
    args = parser.parse_args()
    
    # Initialize and run orchestrator
    orchestrator = ResearchOrchestrator(args.config)
    results = orchestrator.run_research(
        keywords=args.keywords,
        websites=args.websites,
        days_back=args.days_back,
        max_items=args.max_items
    )
    st.set_page_config(page_title="AI Research Agent")
    ui.main() 
    
if __name__ == "__main__":
    main()
