from abc import ABC, abstractmethod
from typing import Dict, List, Any
from datetime import datetime
from ..utils.logger import setup_logger

class BaseAgent(ABC):
    """Base class for all agents in the system"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = setup_logger(name)
        self.collected_data = []
        
    @abstractmethod
    def collect_data(self, *args, **kwargs) -> List[Dict[str, Any]]:
        """
        Collect data from the source
        
        Returns:
            List[Dict[str, Any]]: Collected data
        """
        pass
    
    @abstractmethod
    def process_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process collected data
        
        Args:
            data: Raw collected data
            
        Returns:
            List[Dict[str, Any]]: Processed data
        """
        pass
    
    def save_data(self, data: List[Dict[str, Any]], filename: str = None) -> None:
        """
        Save collected data to a file
        
        Args:
            data: Data to save
            filename: Optional filename, defaults to timestamp
        """
        if filename is None:
            filename = f"{self.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
        try:
            with open(f"data/{filename}", "w") as f:
                json.dump(data, f, indent=2)
            self.logger.info(f"Data saved to {filename}")
        except Exception as e:
            self.logger.error(f"Error saving data: {str(e)}")