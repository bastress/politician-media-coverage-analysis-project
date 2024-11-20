import json
import csv

input_file = 'open_coding.json'
output_file = 'open_coding_articles.csv'

with open(input_file, 'r') as file:
    articles = json.load(file)

with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['title', 'description']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    
    for article in articles:
        writer.writerow({
            'title': article['title'],
            'description': article['description']
        })

print(f"Data has been written to {output_file}")
