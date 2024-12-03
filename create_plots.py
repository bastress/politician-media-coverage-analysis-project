import pandas as pd
import matplotlib.pyplot as plt
import os

# Create the output directory if it doesn't exist
output_dir = "plots"
os.makedirs(output_dir, exist_ok=True)

# Load the data from the CSV file
file_path = "articles_with_sentiment_title_desc.csv"
data = pd.read_csv(file_path)

# Define the mapping for coding titles
coding_title_mapping = {
    'nt': 'Not Trump',
    'polls': 'Polls',
    'oppositions': 'Oppositions',
    'endorsements': 'Endorsements',
    'campaign': 'Campaign',
    'wellbeing': 'Wellbeing',
    'policy': 'Policy',
    'statements': 'Statements'
}

# Helper function to save and style pie charts
def save_pie_chart(data, title, filename, colors=None):
    fig, ax = plt.subplots(figsize=(8, 8), facecolor='white')  # White background
    wedges, texts, autotexts = ax.pie(
        data,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        textprops={'fontsize': 12, 'color': 'black'},
        wedgeprops={'edgecolor': 'white', 'linewidth': 1}
    )
    
    # Add title with enhanced style
    plt.title(title, fontsize=16, weight='bold', color='darkblue', pad=20)
    
    # Enhance legend
    ax.legend(data.index, title='Categories', title_fontsize=12, loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)
    
    # Format percentage labels (slightly bigger)
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(13)
        autotext.set_weight('bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, filename), bbox_inches='tight', dpi=300)  # High resolution
    plt.close()

# Pie chart: Number of rows with each specific coding
coding_counts = data['coding'].value_counts()
save_pie_chart(coding_counts, 'Typology Distribution', 'coding_distribution.png')

# Pie chart: Number of entries with each sentiment
sentiment_counts = data['sentiment'].value_counts()
colors = {'positive': '#4CAF50', 'neutral': '#9E9E9E', 'negative': '#F44336'}  # Custom sleek colors
sentiment_colors = [colors[sentiment] for sentiment in sentiment_counts.index]
save_pie_chart(sentiment_counts, 'Total Sentiment Destribution', 'sentiment_distribution.png', colors=sentiment_colors)

# Pie charts for sentiment distribution within each coding
for coding in data['coding'].unique():
    subset = data[data['coding'] == coding]
    sentiment_counts = subset['sentiment'].value_counts()
    sentiment_colors = [colors[sentiment] for sentiment in sentiment_counts.index]
    
    # Use the mapped title or fall back to the original coding if not found
    title = f"Sentiment Distribution: {coding_title_mapping.get(coding, coding)}"
    filename = f'sentiment_distribution_{coding}.png'.replace(' ', '_')  # Replace spaces with underscores for filenames
    save_pie_chart(sentiment_counts, title, filename, colors=sentiment_colors)