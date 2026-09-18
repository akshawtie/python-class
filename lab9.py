import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_clean_data():
    df = pd.read_csv('lab8data.csv')
    # Impute missing values with the median of their respective columns
    for col in ['Spotify_Streams', 'Apple_Streams']:
        df[col] = df[col].fillna(df[col].median())
    return df

def basic_info(df):
    print("\n--- Basic Information ---")
    print(f"Shape: {df.shape}")
    #print(f"Columns: {df.columns.tolist()}")
    print("\nData Types:\n", df.dtypes)
    print("\nFirst 5 records:\n", df.head())
   # print("\nBasic Statistics (mean, std, percentiles):\n", df.describe())
    print("\nMissing values after cleaning:\n", df.isnull().sum())

def advanced_operations(df):
    print("\n--- Advanced Operations ---")
    
    # 1. Grouping & Aggregation
    genre_streams = df.groupby('Genre')[['Spotify_Streams', 'YouTube_Streams']].mean().reset_index()
    print("\n1. Grouping & Aggregation (Avg Streams by Genre):\n", genre_streams)
    
    # 2. Correlation Analysis
    correlation_matrix = df[['Spotify_Streams', 'Apple_Streams', 'YouTube_Streams', 'Amazon_Streams']].corr()
    print("\n2. Correlation Analysis:\n", correlation_matrix)
    high_spotify = df[df['Spotify_Streams'] > 130]
    print(f"\n3. Filtering Data: Found {len(high_spotify)} tracks with >130M Spotify streams.")
    top_youtube = df.sort_values(by='YouTube_Streams', ascending=False).head(3)
    print("\n4. Sorting (Top 3 YouTube Tracks):\n", top_youtube[['Song', 'Artist', 'YouTube_Streams']])

def visualizations(df):
    df['Total_Streams'] = df[['Spotify_Streams', 'Apple_Streams', 'YouTube_Streams', 'Amazon_Streams']].sum(axis=1)
    artist_group = df.groupby('Artist')[['Spotify_Streams', 'Apple_Streams', 'YouTube_Streams', 'Amazon_Streams', 'Total_Streams']].sum().reset_index()
    top_10_artists = artist_group.sort_values('Total_Streams', ascending=False).head(10)
    # Melt the dataframe to make it suitable for a grouped bar chart in Seaborn
    melted_df = top_10_artists.melt(id_vars='Artist', 
                                    value_vars=['Spotify_Streams', 'Apple_Streams', 'YouTube_Streams', 'Amazon_Streams'],
                                    var_name='Platform', 
                                    value_name='Streams (Millions)')
    # Generate the grouped bar chart
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(14, 7))
    sns.barplot(data=melted_df, x='Artist', y='Streams (Millions)', hue='Platform', palette='magma')
    plt.title('Top 10 Artists by Total Streams: Platform Breakdown', fontsize=16, fontweight='bold')
    plt.xlabel('Artist', fontsize=12)
    plt.ylabel('Streams (Millions)', fontsize=12)
    plt.xticks(rotation=45)
    plt.legend(title='Streaming Platform')
    plt.tight_layout()
    plt.show()

def show_interpretations():
    print("\n--- Data Interpretations ---")
    print("1. Platform Dominance: YouTube consistently drives the highest stream volumes. The dataset median for YouTube is substantially higher than other platforms.")
    print("2. Genre Popularity Discrepancies: Pop music significantly outperforms other genres in total average streams, particularly on YouTube.")
    print("3. High Cross-Platform Correlation: There is an exceptionally strong positive correlation (0.95+) between Spotify and YouTube streams, indicating that a track's success universally scales across platforms.")

def main():
    try:
        df = load_and_clean_data()
    except FileNotFoundError:
        print("Error: lab8data.csv not found in the current directory.")
        return

    while True:
        print("\n=== Data Analysis Dashboard ===")
        print("1. Dataset Info & Preparation")
        print("2. Advanced Operations")
        print("3. Generate Visualizations (Top 10 Artists Bar Chart)")
        print("4. Print Interpretations")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            basic_info(df)
        elif choice == '2':
            advanced_operations(df)
        elif choice == '3':
            visualizations(df)
        elif choice == '4':
            show_interpretations()
        elif choice == '5':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()