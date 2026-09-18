import csv
import os
import re

class Music:
    def __init__(self, title, artist, genre):
        self.title = title
        self.artist = artist
        self.genre = genre
    def __str__(self):
        return f"{self.title} by {self.artist} ({self.genre})"


class MusicPlayer:
    def __init__(self):
        # Array of objects to store musics
        self.music_library = []
        self.queue = []
        self.csv_file = "music_library.csv"
        self.load_from_csv()




    def load_from_csv(self):
        """Loads music from the CSV file if it exists."""
        if os.path.exists(self.csv_file):
            try:
                with open(self.csv_file, 'r', newline='') as f:
                    reader = csv.reader(f)
                    header = next(reader, None) # skip header
                    for row in reader:
                        if len(row) == 3:
                            self.music_library.append(Music(row[0], row[1], row[2]))
            except Exception as e:
                print(f"Error loading from CSV: {e}")


    def save_to_csv(self):
        try:
            with open(self.csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Title", "Artist", "Genre"])
                for music in self.music_library:
                    writer.writerow([music.title, music.artist, music.genre])
            print(f"Data saved to {self.csv_file} successfully.")
        except Exception as e:
            print(f"Error saving to CSV: {e}")





    def add_music_to_library(self):
        print("\n--- Add New Music ---")
        title = input("Enter music title: ").strip()
        artist = input("Enter artist name: ").strip()
        genre = input("Enter genre: ").strip()
        
        if title and artist and genre:
            if not re.match(r'^[a-zA-Z0-9\s#@]+$', title):
                print("Error: Song title can only contain letters, numbers, spaces, '#', and '@'.")
                return
            # Adding object to our array
            self.music_library.append(Music(title, artist, genre))
            print("Music added to library successfully.")
        else:
            print("Error: All fields are required!")




    def display_library(self):
        if not self.music_library:
            print("\nLibrary is empty.")
            return
            
        print("\n--- Music Library ---")
        print(f"{'No.':<5} | {'Title':<20} | {'Artist':<20} | {'Genre':<10}")
        print("-" * 65)
        for i, music in enumerate(self.music_library):
            print(f"{i + 1:<5} | {music.title:<20} | {music.artist:<20} | {music.genre:<10}")




    def enqueue_music(self):
        """Operation to add to the music queue."""
        self.display_library()
        if not self.music_library:
            return
            
        try:
            choice = int(input("\nEnter the number of the music to add to queue: ")) - 1
            if 0 <= choice < len(self.music_library):
                self.queue.append(self.music_library[choice])
                print(f"'{self.music_library[choice].title}' added to queue.")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a valid number.")




    def play_next(self):
        """Operation to play (dequeue) from the music queue."""
        print("\n--- Playing Music ---")
        if not self.queue:
            print("Queue is empty. No music to play.")
        else:
            music = self.queue.pop(0)
            print(f"▶ Now playing: {music.title} by {music.artist}")



    def display_queue(self):
        """Operation to display the current music queue."""
        if not self.queue:
            print("\nQueue is empty.")
            return
            
        print("\n--- Current Queue ---")
        print(f"{'Pos':<5} | {'Title':<20} | {'Artist':<20}")
        print("-" * 55)
        for i, music in enumerate(self.queue):
            print(f"{i + 1:<5} | {music.title:<20} | {music.artist:<20}")



    def run(self):
        """Menu driven interface."""
        while True:
            print("\n" + "="*35)
            print("        MUSIC PLAYER MENU")
            print("="*35)
            print("1. Add Music to Library")
            print("2. Display Library")
            print("3. Add Music to Queue")
            print("4. Play Next in Queue")
            print("5. Display Queue")
            print("6. Exit & Save to CSV")
            print("="*35)
            
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == '1':
                self.add_music_to_library()
            elif choice == '2':
                self.display_library()
            elif choice == '3':
                self.enqueue_music()
            elif choice == '4':
                self.play_next()
            elif choice == '5':
                self.display_queue()
            elif choice == '6':
                self.save_to_csv()
                print("Exiting music player. Goodbye!")
                break
            else:
                print("Invalid choice! Please select between 1 and 6.")



if __name__ == "__main__":
    player = MusicPlayer()
    player.run()
