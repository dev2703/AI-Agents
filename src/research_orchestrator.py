from src.agents.social_media_agent import SocialMediaAgent
from src.agents.web_scraper_agent import WebScraperAgent
from src.analysis.data_processor import DataProcessor
from src.analysis.customer_analysis import CustomerAnalyzer
from src.analysis.data_visualization import DataVisualizer
from src.utils.logger import logger
from config.settings import Settings
import argparse
import json
from datetime import datetime

class ResearchOrchestrator:
    def __init__(self, config_path=None):
        """
        Initialize the orchestrator.

        Args:
            config_path (str): Optional path to the config file.
        """
        self.settings = Settings(config_path)
        self.logger = logger
        self.social_media_agent = SocialMediaAgent(self.settings.get('social_media'))
        self.web_scraper_agent = WebScraperAgent(self.settings.get('web_scraper'))
        self.data_processor = DataProcessor()
        self.customer_analyzer = CustomerAnalyzer()
        self.data_visualizer = DataVisualizer()

    def run_research(self, 
                     keywords: List[str], 
                     websites: List[str] = None, 
                     days_back: int = 7, 
                     max_items: int = 100) -> Dict[str, Any]:
        """
        Run a complete research operation.

        Args:
            keywords: List of keywords to research.
            websites: Optional list of websites to scrape.
            days_back: Number of days of historical data to collect.
            max_items: Maximum items to collect per source.

        Returns:
            Dictionary containing all collected and processed data.
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

        try:
            social_media_data = self.social_media_agent.collect(
                keywords=keywords,
                days_back=days_back,
                max_items=max_items
            )
            results["data"]["social_media"] = social_media_data

            # Sentiment Analysis
            for platform, platform_data in social_media_data.items():
                for item in platform_data:
                    text = item.get("text", "")  # Get the relevant text field
                    sentiment_scores = self.customer_analyzer.analyze_sentiment(text)
                    item["sentiment"] = sentiment_scores

            # Topic Modeling (Example - implement based on your needs)
            # if platform_data:
            #     all_texts = [item.get("text", "") for item in platform_data]
            #     topics = self.customer_analyzer.perform_topic_modeling(all_texts, num_topics=5)
            #     results["data"]["social_media"]["topics"] = topics

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

        # Generate visualizations
        self.data_visualizer.plot_sentiment_distribution([item["sentiment"]["compound"] 
                                                         for sublist in social_media_data.values() 
                                                         for item in sublist])
        # Add more visualizations as needed (e.g., word clouds, topic distributions)

        return results

    def _save_results(self, results: Dict[str, Any]):
        """
        Save research results to file.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"research_results_{timestamp}.json"
        output_dir = self.settings.get('storage.processed_dir', 'data/processed')
        output_path = Path(output_dir) / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        self.logger.info(f"Results saved to {output_path}")