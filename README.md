# AI Research Agents

An advanced system for collecting and analyzing data from various sources using AI-powered agents.

**Features**

  - Social media data collection (LinkedIn, Twitter, Instagram, Facebook)
  - Web scraping capabilities for blogs, news sites, and review platforms
  - Automated data processing and analysis with sentiment analysis and topic modeling (enhanced)
  - Flexible trigger system for automation (placeholder)
  - Comprehensive reporting and visualization (enhanced with user interface)

**Installation**

**Prerequisites:**

  - Git: A version control system for tracking code changes. Install it from [https://git-scm.com/downloads](https://git-scm.com/downloads)

**Steps:**

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/yourusername/ai-research-agents.git](https://github.com/yourusername/ai-research-agents.git)
    cd ai-research-agents
    ```

2.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure settings:**

    ```bash
    cp src/config/settings.example.py src/config/settings.py
    # Edit settings.py with your API keys and configuration
    ```

**Usage**

Basic usage example (focusing on data collection):

```python
from src.agents.social_media_agent import SocialMediaAgent
from src.agents.web_scraper_agent import WebScraperAgent

# Initialize agents
social_agent = SocialMediaAgent()
web_agent = WebScraperAgent()

# Collect data
social_data = social_agent.collect_data(platforms=['linkedin', 'twitter'])
web_data = web_agent.scrape_websites(['example.com'])