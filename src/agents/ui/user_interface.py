import streamlit as st
from src.research_orchestrator import ResearchOrchestrator

def main():
    st.title("AI Research Agent")

    # Input fields for user interaction
    keywords = st.text_input("Enter keywords (comma-separated):")
    keywords = keywords.split(",")
    websites = st.text_input("Enter websites (comma-separated):").split(",")
    days_back = st.number_input("Number of days back:", min_value=1, max_value=30, value=7)
    max_items = st.number_input("Maximum items per source:", min_value=1, value=100)

    if st.button("Run Research"):
        orchestrator = ResearchOrchestrator()  # Assuming config is handled appropriately
        results = orchestrator.run_research(keywords=keywords, 
                                           websites=websites, 
                                           days_back=days_back, 
                                           max_items=max_items)

        # Display results (example)
        st.write("Research Results:")
        st.json(results) 

        # Display visualizations (example)
        # Assuming results contain sentiment scores
        sentiments = [item["sentiment"]["compound"] 
                      for sublist in results["data"]["social_media"].values() 
                      for item in sublist]
        orchestrator.data_visualizer.plot_sentiment_distribution(sentiments)
        st.pyplot(plt.gcf())  # Display the plot in Streamlit

if __name__ == "__main__":
    main()