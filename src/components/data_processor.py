import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class DataProcessor:
    def __init__(self):
        self.stop_words = set(stopwords.words("english"))

    def clean_text(self, text):
        """Clean and preprocess text data."""
        text = re.sub(r"http\S+", "", text)  # Remove URLs
        text = re.sub(r"[^a-zA-Z\s]", "", text)  # Remove non-alphanumeric characters
        text = text.lower().strip()
        return text

    def tokenize_text(self, text):
        """Tokenize text and remove stopwords."""
        tokens = word_tokenize(text)
        filtered_tokens = [word for word in tokens if word not in self.stop_words]
        return filtered_tokens

    def vectorize_text(self, corpus):
        """Convert text data into TF-IDF vectors."""
        vectorizer = TfidfVectorizer(max_features=500)
        vectors = vectorizer.fit_transform(corpus)
        return vectors, vectorizer.get_feature_names_out()

    def load_data(self, file_path):
        """Load data from a CSV or JSON file."""
        if file_path.endswith(".csv"):
            return pd.read_csv(file_path)
        elif file_path.endswith(".json"):
            return pd.read_json(file_path)
        else:
            raise ValueError("Unsupported file format. Use CSV or JSON.")
