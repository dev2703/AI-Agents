# src/analysis/sentiment.py
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from typing import List, Dict, Any
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download necessary NLTK resources
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class CustomerAnalyzer:
    """Analyze customer feedback using sentiment analysis and topic modeling."""
    
    def __init__(self):
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.stop_words = set(stopwords.words("english"))
        self.lemmatizer = WordNetLemmatizer()
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """
        Analyze the sentiment of a given text using VADER.

        Args:
            text (str): The text to analyze.

        Returns:
            dict: Sentiment scores (positive, negative, neutral, compound).
        """
        if not text or not isinstance(text, str):
            return {
                "positive": 0.0,
                "negative": 0.0,
                "neutral": 0.0,
                "compound": 0.0
            }
        
        clean_text = self._clean_text(text)
        scores = self.sentiment_analyzer.polarity_scores(clean_text)
        return scores
    
    def perform_topic_modeling(self, documents: List[str], num_topics: int = 5) -> List[List[str]]:
        """
        Perform topic modeling using Non-Negative Matrix Factorization (NMF).

        Args:
            documents (list): List of preprocessed text documents.
            num_topics (int): Number of topics to extract.

        Returns:
            list: List of topic keywords for each topic.
        """
        if not documents:
            return []
        
        # Preprocess documents
        processed_docs = [self._clean_text(doc) for doc in documents]
        
        # Vectorize text using TF-IDF
        tfidf_vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
        tfidf_matrix = tfidf_vectorizer.fit_transform(processed_docs)
        
        # Perform NMF
        nmf = NMF(n_components=num_topics, random_state=42)
        nmf.fit(tfidf_matrix)
        
        # Extract top keywords for each topic
        feature_names = tfidf_vectorizer.get_feature_names_out()
        topic_keywords = []
        for topic in nmf.components_:
            top_keywords = [feature_names[i] for i in topic.argsort()[-10:]]
            topic_keywords.append(top_keywords)
        
        return topic_keywords
    
    def identify_pain_points(self, texts: List[str]) -> List[str]:
        """
        Identify potential pain points based on sentiment and keywords.

        Args:
            texts (list): List of text documents.

        Returns:
            list: List of identified pain points.
        """
        pain_points = []
        for text in texts:
            if not text:
                continue
            
            # Analyze sentiment
            sentiment_scores = self.analyze_sentiment(text)
            
            # Check for negative sentiment
            if sentiment_scores['compound'] < -0.05:
                # Identify specific pain points using keywords
                if re.search(r"\b(price|cost|expensive)\b", text, re.IGNORECASE):
                    pain_points.append("High Price")
                elif re.search(r"\b(delivery|shipping|late)\b", text, re.IGNORECASE):
                    pain_points.append("Delivery Issues")
                elif re.search(r"\b(quality|poor|bad)\b", text, re.IGNORECASE):
                    pain_points.append("Poor Quality")
                elif re.search(r"\b(support|service|help)\b", text, re.IGNORECASE):
                    pain_points.append("Customer Support")
                else:
                    pain_points.append("General Dissatisfaction")
        
        return pain_points
    
    def identify_user_struggles(self, texts: List[str]) -> List[str]:
        """
        Identify potential user struggles based on keywords and text analysis.

        Args:
            texts (list): List of text documents.

        Returns:
            list: List of identified user struggles.
        """
        struggles = []
        for text in texts:
            if not text:
                continue
            
            # Check for specific struggle keywords
            if re.search(r"\b(difficult|hard|complicated)\b", text, re.IGNORECASE):
                struggles.append("Difficulty Using Product")
            elif re.search(r"\b(problem|issue|error)\b", text, re.IGNORECASE):
                struggles.append("Technical Issues")
            elif re.search(r"\b(confusing|unclear|understand)\b", text, re.IGNORECASE):
                struggles.append("Confusing Instructions")
            elif re.search(r"\b(slow|lag|freeze)\b", text, re.IGNORECASE):
                struggles.append("Performance Issues")
        
        return struggles
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and preprocess text for analysis.

        Args:
            text (str): The text to clean.

        Returns:
            str: The cleaned text.
        """
        # Remove URLs, special characters, and numbers
        text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
        text = re.sub(r"\@\w+|\#", "", text)
        text = re.sub(r"[^\w\s]", "", text)
        
        # Convert to lowercase
        text = text.lower().strip()
        
        # Tokenize and remove stopwords
        tokens = word_tokenize(text)
        filtered_tokens = [word for word in tokens if word not in self.stop_words]
        
        # Lemmatize tokens
        lemmatized_tokens = [self.lemmatizer.lemmatize(word) for word in filtered_tokens]
        
        return " ".join(lemmatized_tokens)