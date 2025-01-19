import json
import pandas as pd

class OutputHandler:
    def __init__(self):
        pass

    def save_to_csv(self, data, file_path):
        """Save data to a CSV file."""
        data.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}")

    def save_to_json(self, data, file_path):
        """Save data to a JSON file."""
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {file_path}")

    def summarize_findings(self, data):
        """Generate a summary from the research data."""
        summary = {
            "total_entries": len(data),
            "key_insights": data["pain_points"].value_counts().head(5).to_dict(),
        }
        return summary
