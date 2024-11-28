import pandas as pd
import re
import json
import math
import argparse
from collections import Counter
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# Function to clean text, convert to lowercase, and remove stop words
def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = text.lower()
    words = text.split()

    custom_stop_words = ENGLISH_STOP_WORDS.union({'s', 't', 'u'}) # s and t left from when we clean apostrophes
    filtered_words = [word for word in words if word not in custom_stop_words]
    return ' '.join(filtered_words)

# Function to read file and combine title and description columns into a single text column
def combine_title_description(input_file):
    df = pd.read_csv(input_file)
    df['title'] = df['title'].apply(clean_text)
    df['description'] = df['description'].apply(clean_text)
    df['text'] = df['title'] + " " + df['description']
    return df

# Function to compute TF
def compute_tf(category_articles):
    tf_per_doc = []
    
    for doc in category_articles:
        words = doc.split()
        total_words = len(words)
        word_counts = Counter(words)
        tf = {word: count / total_words for word, count in word_counts.items()}
        tf_per_doc.append(tf)
    
    # Aggregate TF across all documents in the category
    aggregated_tf = {}
    for tf in tf_per_doc:
        for word, value in tf.items():
            aggregated_tf[word] = aggregated_tf.get(word, 0) + value
    
    # Average TF across documents
    num_docs = len(category_articles)
    averaged_tf = {word: value / num_docs for word, value in aggregated_tf.items()}
    return averaged_tf

# Function to compute IDF
def compute_idf(all_articles):
    N = len(all_articles)
    idf = {}
    all_words = set(word for doc in all_articles for word in doc.split())
    for word in all_words:
        DF = sum(1 for doc in all_articles if word in doc.split())
        idf[word] = math.log(N / (1 + DF))
    return idf

# Function to calculate TF-IDF for a document
def compute_tfidf(tf, idf):
    return {word: tf[word] * idf[word] for word in tf.keys()}

# Function to get TF-IDF (TF over each category, IDF over all articles) and return the top 10
def get_top_words_by_category(df):
    categories = df['coding'].unique()
    top_words = {}

    # idf over all articles
    all_articles = df['text'].tolist()
    idf = compute_idf(all_articles)

    for category in categories:
        category_articles = df[df['coding'] == category]['text'].tolist()
        tf = compute_tf(category_articles) # tf for category articles

        tfidf = compute_tfidf(tf, idf)
        top_ten = Counter(tfidf).most_common(10)

        top_words[category] = top_ten

    return top_words

# Function to save top words to a JSON file
def save_top_words_to_json(top_words, output_file):
    top_words = {
        category: {word: score for word, score in words_scores}
        for category, words_scores in top_words.items()
    }
    with open(output_file, 'w') as f:
        json.dump(top_words, f, indent=4)

# Function to print top words for each category
def print_top_words(top_words):
    for category, words_scores in top_words.items():
        print(f"Top 10 words for category '{category}':")
        for word, score in words_scores:
            print(f"{word}: {score:.4f}")
        print("\n")

# Main function
def main(input_file, output_file):
    df = combine_title_description(input_file)
    top_words = get_top_words_by_category(df)

    save_top_words_to_json(top_words, output_file)
    print_top_words(top_words)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract top words by category from a CSV file using manual TF-IDF calculations (excluding stop words)")
    parser.add_argument('input_file', type=str, help="Path to the input CSV file")
    parser.add_argument('output_file', type=str, help="Path to the output JSON file")

    args = parser.parse_args()
    main(args.input_file, args.output_file)


# python tfidf.py annotated_trump_articles.csv topics_tfidf.json




