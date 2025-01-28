from abc import ABC, abstractmethod
from typing import Dict, List, Any
from datetime import datetime
import json
from pathlib import Path
from utils.logger import setup_logger

class BaseAgent(ABC):
    """Base class for all data collection agents"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = setup_logger(name)
        self.collected_data = []
        
    @abstractmethod
    def collect(self, *args, **kwargs) -> Dict[str, List[Dict]]:
        """Collect raw data from sources"""
        pass
    
    @abstractmethod
    def process(self, data: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Process raw data into structured format"""
        pass
    
    def save_data(self, data: Dict, output_dir: str = "data/raw") -> Path:
        """Save collected data to timestamped JSON file"""
        output_path = Path(output_dir) / f"{self.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2)
            self.logger.info(f"Data saved to {output_path}")
            return output_path
        except Exception as e:
            self.logger.error(f"Error saving data: {str(e)}")
            raise