
import torch
import pandas as pd
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification


df = pd.read_csv("open_coding_articles.csv")
model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

texts = list(df['description'].values)
results = nlp(texts)

# save sentiment col to csv
sentiments = [result['label'] for result in results]
df['sentiment'] = sentiments
df.to_csv("articles_with_sentiment.csv", index=False)




