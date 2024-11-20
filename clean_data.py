import json
import re
import argparse
import os

# Filter out "[Removed]" articles
def remove_removed_articles(articles):
    return [article for article in articles if article.get('title', '').strip().lower() != "[removed]"]

# Function to filter out articles about Trump family members
def filter_articles(articles):
    filtered_articles = []
    
    target_names = ['melania', 'barron', 'ivanka', 'ivana']
    
    for article in articles:
        title = article.get('title', '').lower()
        match = re.search(r'(\w+)\s+trump', title)
        if match:
            name_before_trump = match.group(1).lower()
            if name_before_trump in target_names and title.count('trump') == 1:
                filtered_articles.append(article)
    
    return filtered_articles

# Function to remove duplicate articles (same title and author)
def remove_duplicates(articles):
    seen = set()
    unique_articles = []
    removed_articles = []
    
    for article in articles:
        title = article.get('title', '').strip()
        author = (article.get('author') or '').strip() # Handle "null" authors
        unique_id = (title, author)
        
        if unique_id not in seen:
            seen.add(unique_id)
            unique_articles.append(article)
        else:
            removed_articles.append(article)  # Track removed duplicates
    
    return unique_articles, removed_articles

# Function to extract all unique source names
def extract_sources(articles):
    sources = set()
    
    for article in articles:
        source_name = article.get('source', {}).get('name', '').strip() # Handle missing source
        if source_name:
            sources.add(source_name)
    
    return sorted(sources)

# Process files
def process_json_files(input_files, filtered_output, remaining_output, sources_output, removed_output):
    all_articles = []
    
    # Load and combine all articles from JSON files
    for file in input_files:
        with open(file, 'r') as f:
            data = json.load(f)
            all_articles.extend(data.get('articles', []))

    all_articles = remove_removed_articles(all_articles)
    
    filtered_articles = filter_articles(all_articles)

    unique_articles, removed_articles = remove_duplicates(all_articles)

    remaining_articles = [article for article in unique_articles if article not in filtered_articles]

    source_names = extract_sources(all_articles)

    with open(filtered_output, 'w') as f:
        json.dump(filtered_articles, f, indent=4)

    with open(remaining_output, 'w') as f:
        json.dump(remaining_articles, f, indent=4)

    with open(sources_output, 'w') as f:
        json.dump(source_names, f, indent=4)

    with open(removed_output, 'w') as f:
        json.dump(removed_articles, f, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Process JSON files of articles.")
    parser.add_argument("input_folder", help="Directory containing input JSON files to process.")
    parser.add_argument("--filtered_output", default="filtered_articles.json", help="Output file for filtered articles.")
    parser.add_argument("--remaining_output", default="remaining_articles.json", help="Output file for remaining articles.")
    parser.add_argument("--sources_output", default="source_names.json", help="Output file for source names.")
    parser.add_argument("--removed_output", default="removed_duplicates.json", help="Output file for removed (duplicate) articles.")

    args = parser.parse_args()
    
    input_files = [os.path.join(args.input_folder, f) for f in os.listdir(args.input_folder) if f.endswith('.json')]
    if not input_files:
        print(f"No JSON files found in the folder: {args.input_folder}")
        return

    process_json_files(input_files, args.filtered_output, args.remaining_output, args.sources_output, args.removed_output)

if __name__ == "__main__":
    main()

# to use:
# python clean_data.py data --filtered_output filtered_articles.json --remaining_output remaining_articles.json --sources_output source_names.json --removed_output removed_duplicates.json

