from newsapi import NewsApiClient
import json


def fetch_news_articles():
    # Init
    newsapi = NewsApiClient(api_key='')

    # /v2/everything
    all_articles = newsapi.get_everything(q='trump',
                                        searchIn='title',
                                        domains='cnn.com,nytimes.com,foxnews.com,msn.com,usatoday.com,people.com,finance.yahoo.com,nypost.com,forbes.com,dailymail.co.uk,news.google.com,washingtonpost.com,bbc.com,newsweek.com,apnews.com,cbsnews.com,nbcnews.com,cnbc.com,news.yahoo.com,businessinsider.com,theguardian.com,wsj.com,huffpost.com,abcnews.go.com,substack.com,drudgereport.com,reuters.com,buzzfeed.com,independent.co.uk,thehill.com,usnews.com,politico.com,athlonsports.com,breitbart.com,variety.com,sfgate.com,dailydot.co,newsmax.com,axios.com,zerohedge.com,latimes.com,rawstory.com,cbc.ca,ctvnews.ca,globalnews.ca,theglobeandmail.com,cp24.com,thestar.com,nationalpost.com',
                                        from_param='2024-10-19',
                                        to='2024-10-25',
                                        language='en',
                                        sort_by='relevancy',
                                        page=1)

    with open('range1.json', 'w') as json_file:
                json.dump(all_articles, json_file, indent=4)

    # /v2/top-headlines/sources
    sources = newsapi.get_sources()

    with open('sources.json', 'w') as json_file:
                json.dump(sources, json_file, indent=4)

if __name__ == "__main__":
        fetch_news_articles()