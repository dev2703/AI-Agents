import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class ResearchDashboard:
    """Generate interactive dashboards for research results"""
    
    def create_dashboard(self, social_data: Dict, web_data: Dict, sentiment: Dict) -> str:
        """Create and display research dashboard"""
        st.title("Research Dashboard")
        
        # Sentiment Analysis
        with st.expander("Sentiment Analysis"):
            self._plot_sentiment(sentiment)
        
        # Engagement Metrics
        with st.expander("Engagement Metrics"):
            self._plot_engagement(social_data.get('analytics', {}).get('engagement', {}))
        
        # Web Data Summary
        if web_data:
            with st.expander("Web Data Summary"):
                self._plot_web_summary(web_data)
        
        return "Dashboard generated successfully"
    
    def _plot_sentiment(self, sentiment: Dict):
        """Plot sentiment analysis results"""
        fig, ax = plt.subplots()
        sns.barplot(
            x=list(sentiment['average_scores'].keys()),
            y=list(sentiment['average_scores'].values()),
            palette="viridis",
            ax=ax
        )
        ax.set_title("Average Sentiment Scores")
        st.pyplot(fig)
    
    def _plot_engagement(self, engagement: Dict):
        """Plot engagement metrics"""
        fig, ax = plt.subplots(1, 2, figsize=(15, 5))
        
        # Platform Distribution
        sns.barplot(
            x=list(engagement['platform_distribution'].keys()),
            y=list(engagement['platform_distribution'].values()),
            palette="magma",
            ax=ax[0]
        )
        ax[0].set_title("Platform Distribution")
        
        # Keyword Distribution
        df_keywords = pd.DataFrame(
            engagement['keyword_distribution'].items(),
            columns=['Keyword', 'Count']
        )
        sns.barplot(
            data=df_keywords.nlargest(10, 'Count'),
            x='Count',
            y='Keyword',
            palette="plasma",
            ax=ax[1]
        )
        ax[1].set_title("Top Keywords")
        
        st.pyplot(fig)
    
    def _plot_web_summary(self, web_data: Dict):
        """Plot web data summary"""
        df_web = pd.DataFrame([
            {
                'website': website,
                'pages': len(pages)
            }
            for website, pages in web_data['data'].items()
        ])
        
        fig, ax = plt.subplots()
        sns.barplot(
            data=df_web.nlargest(10, 'pages'),
            x='pages',
            y='website',
            palette="rocket",
            ax=ax
        )
        ax.set_title("Top Websites by Pages Scraped")
        st.pyplot(fig)
