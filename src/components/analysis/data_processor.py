import re
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

class DataProcessor:
    def __init__(self):
        self.stop_words = set(stopwords.words("english"))
        self.lemmatizer = WordNetLemmatizer()

    def clean_text(self, text):
        """
        Clean and preprocess text data.

        Args:
            text (str): The text to clean.

        Returns:
            str: The cleaned text.
        """
        text = re.sub(r"http\S+", "", text)  # Remove URLs
        text = re.sub(r"[^\w\s]", "", text)  # Remove non-alphanumeric characters
        text = re.sub(r'[^\w\s]+', ' ', text)  # Replace multiple spaces with a single space
        text = text.lower().strip()
        return text

    def preprocess_text(self, text):
        """
        Preprocesses text for further analysis.

        Args:
            text (str): The text to preprocess.

        Returns:
            str: The preprocessed text.
        """
        cleaned_text = self.clean_text(text)
        tokens = word_tokenize(cleaned_text)
        filtered_tokens = [word for word in tokens if word not in self.stop_words]
        lemmatized_tokens = [self.lemmatizer.lemmatize(word) for word in filtered_tokens] 
        return " ".join(lemmatized_tokens)

    def tokenize_text(self, text):
        """
        Tokenize text and remove stopwords.

        Args:
            text (str): The text to tokenize.

        Returns:
            list: List of tokens.
        """
        tokens = word_tokenize(text)
        filtered_tokens = [word for word in tokens if word not in self.stop_words]
        return filtered_tokens

    def vectorize_text(self, corpus):
        """
        Convert text data into TF-IDF vectors.

        Args:
            corpus (list): List of text documents.

        Returns:
            tuple: Tuple containing TF-IDF vectors and feature names.
        """
        vectorizer = TfidfVectorizer(max_features=500)
        vectors = vectorizer.fit_transform(corpus)
        return vectors, vectorizer.get_feature_names_out()

    def load_data(self, file_path):
        """
        Load data from a CSV or JSON file.

        Args:
            file_path (str): Path to the file.

        Returns:
            pandas.DataFrame: Loaded data.

        Raises:
            ValueError: If the file format is not supported.
        """
        if file_path.endswith(".csv"):
            return pd.read_csv(file_path)
        elif file_path.endswith(".json"):
            return pd.read_json(file_path)
        else:
            raise ValueError("Unsupported file format. Use CSV or JSON.") 