import pandas as pd
import numpy as np

# Load the data from CSV
df = pd.read_csv('lab8data.csv')


df['Spotify_Streams'] = df['Spotify_Streams'].fillna(df['Spotify_Streams'].mean())
df['Apple_Streams'] = df['Apple_Streams'].fillna(df['Apple_Streams'].mean())

df['Total_Streams'] = df['Spotify_Streams'] + df['Apple_Streams'] + df['YouTube_Streams'] + df['Amazon_Streams']
df['Total_Streams'] = df['Total_Streams'].round(2)

def assign_tier(streams):
    if streams >= 420: return 'Diamond'
    elif streams >= 380: return 'Platinum'
    elif streams >= 350: return 'Gold'
    elif streams >= 300: return 'Silver'
    else: return 'Bronze'

df['Tier'] = df['Total_Streams'].apply(assign_tier)

# Arrays for NumPy tasks
track_ids = np.array([101, 102, 103, 104, 105])
# Using the first 5 rows of streams (Spotify, Apple, YouTube, Amazon) as the 2D array
streams_array_2d = df.loc[:4, ['Spotify_Streams', 'Apple_Streams', 'YouTube_Streams', 'Amazon_Streams']].to_numpy()

while True:
    print("\n==================================================")
    print("         MUSIC PERFORMANCE ANALYZER MENU")
    print("==================================================")
    print("1. Data Cleaning & NumPy Conversion")
    print("2. Calculated Columns (Total Streams & Tier)")
    print("3. Conditional Analysis")
    print("4. Group Analysis")
    print("5. Complexity Analytics")
    print("6. 1D Array Indexing & Slicing")
    print("7. 2D Array Indexing")
    print("8. Slicing & Array Modification")
    print("9. Challenge Questions")
    print("10. Flattening, Reshaping & Conversion")
    print("0. Exit")
    print("==================================================")
    
    choice = input("Enter your choice (0-10): ")

    if choice == '1':
        streams_full_array = df[['Spotify_Streams', 'Apple_Streams', 'YouTube_Streams', 'Amazon_Streams']].to_numpy()
        print("\nArray Shape:", streams_full_array.shape)
        print("Array ndim:", streams_full_array.ndim)
        print("Array dtype:", streams_full_array.dtype)

    elif choice == '2':
        print("\n", df[['Artist', 'Song', 'Total_Streams', 'Tier']])

    elif choice == '3':
        filtered_songs = df[(df['Total_Streams'] >= 380) & (df['YouTube_Streams'] >= 130)]
        print("\n", filtered_songs[['Artist', 'Song', 'Genre', 'Total_Streams', 'Tier']])

    elif choice == '4':
        grouped_df = df.groupby('Genre').agg(
            Avg_Total_Streams=('Total_Streams', 'mean'),
            Max_Total_Streams=('Total_Streams', 'max'),
            Avg_YouTube_Streams=('YouTube_Streams', 'mean'),
            Num_Songs=('Track_ID', 'count')
        ).sort_values(by='Avg_Total_Streams', ascending=False)
        print("\n", grouped_df)

    elif choice == '5':
        top_song = df.loc[df['Total_Streams'].idxmax(), 'Song']
        lowest_youtube = df.loc[df['YouTube_Streams'].idxmin(), 'Song']
        grouped_df = df.groupby('Genre').agg(Avg_Total_Streams=('Total_Streams', 'mean')).sort_values(by='Avg_Total_Streams', ascending=False)
        top_genre = grouped_df.index[0]
        
        print(f"\nHighest Total Streams (Song): {top_song}")
        print(f"Lowest YouTube Streams (Song): {lowest_youtube}")
        print(f"Genre with highest avg streams: {top_genre}")
        
        total_streams_np = df['Total_Streams'].to_numpy()
        print(f"\nMean: {np.mean(total_streams_np):.2f}, Median: {np.median(total_streams_np):.2f}")
        print(f"Std Dev: {np.std(total_streams_np):.2f}, Max: {np.max(total_streams_np):.2f}, Min: {np.min(total_streams_np):.2f}")

    elif choice == '6':
        print("\nFirst, last, middle (positive):", track_ids[0], track_ids[4], track_ids[2])
        print("First, last, middle (negative):", track_ids[-5], track_ids[-1], track_ids[-3])
        print("Index 1 to 3:", track_ids[1:4])
        print("Reversed:", track_ids[::-1])
        print("Alternate:", track_ids[::2])

    elif choice == '7':
        print("\nStream value of ID 103 in YouTube:", streams_array_2d[2, 2])
        print("Fourth track complete stream record:", streams_array_2d[3, :])
        print("All tracks Apple Streams:", streams_array_2d[:, 1])
        print("Top-left 3x2 subarray:\n", streams_array_2d[:3, :2])
        print("Last track's last two stream sources:", streams_array_2d[-1, -2:])

    elif choice == '8':
        slice_3x3 = streams_array_2d[:3, :3]
        original_val = slice_3x3[0, 0]
        slice_3x3[0, 0] = 999
        print("\nOriginal array after modifying view:\n", streams_array_2d)
        
        streams_array_2d[0, 0] = original_val 
        streams_copy = streams_array_2d.copy()
        streams_copy[0, 0] = 999
        
        print("\nOriginal array after modifying copy:\n", streams_array_2d)
        print("Copied array:\n", streams_copy)

    elif choice == '9':
        print("\nStreams >= 100:", streams_array_2d[streams_array_2d >= 100])
        print("Rows where Spotify Streams > 100:\n", streams_array_2d[streams_array_2d[:, 0] > 100])
        
        max_index = np.unravel_index(np.argmax(streams_array_2d, axis=None), streams_array_2d.shape)
        print("Row & Col index of max value:", max_index)
        print("Executing prediction (streams_array_2d[1:5:2, ::-1]):\n", streams_array_2d[1:5:2, ::-1])

    elif choice == '10':
        print("\nFlattened array:", streams_array_2d.flatten())
        print("Reshaped to 4x5:\n", streams_array_2d.reshape(4, 5))
        list_format = streams_array_2d.tolist()
        print("Converted to python list (type check):", type(list_format))

    elif choice == '0':
        print("\nExiting program...")
        break

    else:
        print("\nInvalid choice. Please enter a number between 0 and 10.")
