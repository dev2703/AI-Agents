import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from src.orchestration.research_orchestrator import ResearchOrchestrator
from config import load_config

def main():
    st.set_page_config(
        page_title="AI Research Agent",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load production config
    config = load_config()
    
    st.title("Market Research Agent")
    
    with st.sidebar:
        st.header("Research Parameters")
        keywords = st.text_input("Keywords (comma-separated):")
        websites = st.text_input("Websites (comma-separated):")
        days_back = st.slider("Analysis Period (days):", 1, 30, 7)
        max_items = st.number_input("Max Items per Source:", 10, 1000, 100)
    
    if st.button("Start Research"):
        with st.spinner("Running research pipeline..."):
            try:
                orchestrator = ResearchOrchestrator(config)
                keywords_list = [k.strip() for k in keywords.split(",") if k.strip()]
                websites_list = [w.strip() for w in websites.split(",") if w.strip()]
                
                results = orchestrator.run_pipeline(
                    keywords=keywords_list,
                    websites=websites_list,
                    days_back=days_back,
                    max_items=max_items
                )
                
                st.success("Research completed successfully!")
                st.json(results)
                
                # Show visualizations
                self._display_results(results)
                
            except Exception as e:
                st.error(f"Research failed: {str(e)}")
                st.stop()

def _display_results(results: Dict):
    """Render interactive visualizations"""
    tab1, tab2, tab3 = st.tabs(["Sentiment", "Topics", "Engagement"])
    
    with tab1:
        fig = plt.figure(figsize=(10, 6))
        # Add sentiment visualization
        st.pyplot(fig)
    
    with tab2:
        # Topic modeling visualization
        pass
    
    with tab3:
        # Engagement metrics
        pass

if __name__ == "__main__":
    main()