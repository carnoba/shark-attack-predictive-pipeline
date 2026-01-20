import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os

def generate_visuals(db_name, output_dir='outputs'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    conn = sqlite3.connect(db_name)
    df = pd.read_sql('SELECT * FROM sharks', conn)
    conn.close()
    
    print("Generating visualizations...")
    
    # 1. Heatmap of Attacks by Month and Country
    # Focus on top 10 countries to keep it readable
    top_countries = df['Country'].value_counts().nlargest(10).index
    subset = df[df['Country'].isin(top_countries) & (df['Month'] > 0)]
    
    pivot_df = subset.groupby(['Country', 'Month']).size().unstack(fill_value=0)
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_df, annot=True, fmt="d", cmap="YlOrRd")
    plt.title('Heatmap of Shark Attacks by Month and Country (Top 10)')
    plt.savefig(f'{output_dir}/heatmap_attacks.png')
    plt.close()
    print("Saved heatmap.")
    
    # 2. WordCloud of Shark Species
    # Column is likely 'Species' or 'Species_'
    species_col = 'Species' if 'Species' in df.columns else (
        'Species_' if 'Species_' in df.columns else None
    )
    
    if species_col:
        text = " ".join(df[species_col].dropna().astype(str))
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        
        plt.figure(figsize=(15, 7))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('WordCloud of Shark Species')
        plt.savefig(f'{output_dir}/wordcloud_species.png')
        plt.close()
        print("Saved WordCloud.")
    else:
        print("Species column not found for WordCloud.")

if __name__ == "__main__":
    generate_visuals('master_sharks.db')
