import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

class DataVisualizer:
    def __init__(self):
        pass

    def plot_sentiment_distribution(self, sentiments):
        """
        Plots the distribution of sentiment scores.

        Args:
            sentiments (list): List of sentiment scores (e.g., "positive", "negative", "neutral").
        """
        sns.countplot(x=sentiments, palette="viridis")  # Use a visually appealing color palette
        plt.xlabel("Sentiment")
        plt.ylabel("Count")
        plt.title("Sentiment Distribution")
        plt.show()

    def plot_word_cloud(self, text_data):
        """
        Generates a word cloud from the given text data.

        Args:
            text_data (list): List of text documents.
        """
        text = " ".join(text_data)
        wordcloud = WordCloud(width=800, height=400, background_color="white", colormap="viridis").generate(text) 
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.title("Word Cloud")
        plt.show()

    def plot_topic_distributions(self, topic_distributions, topic_names=None):
        """
        Plots the distribution of documents across different topics.

        Args:
            topic_distributions (list): List of topic distributions for each document.
            topic_names (list): Optional list of topic names.
        """
        if topic_names is None:
            topic_names = [f"Topic {i+1}" for i in range(len(topic_distributions[0]))]
        sns.heatmap(topic_distributions, cmap="viridis", xticklabels=topic_names, annot=True, fmt=".2f") 
        plt.xlabel("Topics")
        plt.ylabel("Documents")
        plt.title("Topic Distributions")
        plt.show()

    def plot_pain_points(self, pain_points):
        """
        Plots the frequency of pain points.

        Args:
            pain_points (list): List of pain points identified in the data.
        """
        pain_point_counts = {point: pain_points.count(point) for point in set(pain_points)}
        plt.figure(figsize=(10, 6))
        plt.bar(pain_point_counts.keys(), pain_point_counts.values(), color="red")  # Highlight pain points with red
        plt.xlabel("Pain Points")
        plt.ylabel("Frequency")
        plt.title("User Pain Points")
        plt.xticks(rotation=45)
        plt.show()

    def plot_user_struggles(self, struggles):
        """
        Plots the frequency of user struggles.

        Args:
            struggles (list): List of user struggles identified in the data.
        """
        struggle_counts = {struggle: struggles.count(struggle) for struggle in set(struggles)}
        plt.figure(figsize=(10, 6))
        plt.bar(struggle_counts.keys(), struggle_counts.values(), color="orange")  # Highlight struggles with orange
        plt.xlabel("User Struggles")
        plt.ylabel("Frequency")
        plt.title("User Struggles")
        plt.xticks(rotation=45)
        plt.show()

    def plot_time_series(self, data, x_column, y_column):
        """
        Plots a time series of the given data.

        Args:
            data (pd.DataFrame): DataFrame containing the data.
            x_column (str): Name of the column for the x-axis (e.g., "date").
            y_column (str): Name of the column for the y-axis (e.g., "count").
        """
        plt.figure(figsize=(10, 6))
        plt.plot(data[x_column], data[y_column])
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.title(f"{y_column} over Time")
        plt.grid(True)
        plt.show()