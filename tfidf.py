import pandas as pd
import re
import json
import math
from collections import Counter
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# Function to clean text, convert to lowercase, and remove stop words
def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = text.lower()
    words = text.split()
    
    # Extend stop words to include 's'
    custom_stop_words = ENGLISH_STOP_WORDS.union({'s', 't'})  
    stop_words = [word for word in words if word not in custom_stop_words]
    return ' '.join(stop_words)

# Function to read and preprocess the data
def load_and_preprocess_data(input_file):
    df = pd.read_csv(input_file)
    df['title'] = df['title'].apply(clean_text)
    df['description'] = df['description'].apply(clean_text)
    df['text'] = df['title'] + " " + df['description']
    return df

# Function to compute term frequency
def compute_tf(document):
    words = document.split()
    word_counts = Counter(words)
    total_words = len(words)
    tf = {word: count / total_words for word, count in word_counts.items()}
    return tf

# Function to compute inverse document frequency
def compute_idf(documents):
    total_docs = len(documents)
    idf = {}
    all_words = set(word for doc in documents for word in doc.split())
    for word in all_words:
        containing_docs = sum(1 for doc in documents if word in doc.split())
        idf[word] = math.log(total_docs / (1 + containing_docs)) 
    return idf

# Function to calculate TF-IDF for a document
def compute_tfidf(tf, idf):
    return {word: tf[word] * idf[word] for word in tf.keys()}

# Function to calculate top words for each category
def get_top_words_by_category(df):
    categories = df['coding'].unique()
    top_words = {}

    for category in categories:
        category_docs = df[df['coding'] == category]['text'].tolist()
        idf = compute_idf(category_docs)

        tfidf_scores = Counter()
        for doc in category_docs:
            tf = compute_tf(doc)
            tfidf = compute_tfidf(tf, idf)
            tfidf_scores.update(tfidf)

        top_words[category] = tfidf_scores.most_common(10)

    return top_words

# Function to save top words to a JSON file
def save_top_words_to_json(top_words, output_file):
    formatted_top_words = {
        category: {word: score for word, score in words_scores}
        for category, words_scores in top_words.items()
    }
    with open(output_file, 'w') as f:
        json.dump(formatted_top_words, f, indent=4)

# Function to print top words for each category
def print_top_words(top_words):
    for category, words_scores in top_words.items():
        print(f"Top 10 words for category '{category}':")
        for word, score in words_scores:
            print(f"{word}: {score:.4f}")
        print("\n")

# Main function
def main(input_file, output_file):
    df = load_and_preprocess_data(input_file)
    top_words = get_top_words_by_category(df)

    save_top_words_to_json(top_words, output_file)
    print_top_words(top_words)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extract top words by category from a CSV file using manual TF-IDF calculations (excluding stop words)")
    parser.add_argument('input_file', type=str, help="Path to the input CSV file")
    parser.add_argument('output_file', type=str, help="Path to the output JSON file")

    args = parser.parse_args()
    main(args.input_file, args.output_file)




# python tfidf.py annotated_trump_articles.csv topics_tfidf.json




