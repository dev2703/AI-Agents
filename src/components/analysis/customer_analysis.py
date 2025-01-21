from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from .data_processor import DataProcessor

class CustomerAnalyzer:
    def __init__(self):
        self.data_processor = DataProcessor()
        self.sentiment_analyzer = SentimentIntensityAnalyzer()

    def analyze_sentiment(self, text):
        """
        Analyzes the sentiment of a given text using VADER.

        Args:
            text (str): The text to analyze.

        Returns:
            dict: Sentiment scores (positive, negative, neutral, compound).
        """
        clean_text = self.data_processor.clean_text(text)
        scores = self.sentiment_analyzer.polarity_scores(clean_text)
        return scores

    def perform_topic_modeling(self, documents, num_topics=5):
        """
        Performs topic modeling using NMF.

        Args:
            documents (list): List of preprocessed text documents.
            num_topics (int): Number of topics to extract.

        Returns:
            list: List of topic keywords for each topic.
        """
        tfidf_vectorizer = TfidfVectorizer(max_features=500)
        tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
        nmf = NMF(n_components=num_topics)
        nmf_model = nmf.fit(tfidf_matrix)
        topic_words = []
        for topic in nmf_model.components_:
            topic_words.append([tfidf_vectorizer.get_feature_names_out()[i] 
                                for i in topic.argsort()[-10:]])  # Top 10 words for each topic
        return topic_words

    def identify_pain_points(self, texts):
        """
        Identifies potential pain points based on sentiment and keywords.

        Args:
            texts (list): List of text documents.

        Returns:
            list: List of identified pain points.
        """
        pain_points = []
        for text in texts:
            sentiment_scores = self.analyze_sentiment(text)
            if sentiment_scores['compound'] < -0.05:  # Example: Negative sentiment
                pain_points.append("Price")  # Replace with actual pain point identification logic
            # Add more conditions to identify other pain points based on keywords or specific phrases
            # Example:
            # if "delivery" in text and "delay" in text:
            #     pain_points.append("Delivery Delays") 
        return pain_points

    def identify_user_struggles(self, texts):
        """
        Identifies potential user struggles based on keywords and text analysis.

        Args:
            texts (list): List of text documents.

        Returns:
            list: List of identified user struggles.
        """
        struggles = []
        for text in texts:
            # Implement logic to identify user struggles based on keywords, 
            # sentiment, or other relevant factors.
            if "difficult" in text or "problem" in text:
                struggles.append("Difficulty using the product") 
            # Add more conditions to identify other user struggles
        return struggles