import streamlit as st
import pandas as pd
import re
import os
import signal
from lab7 import MusicPlayer, Music


# Initialize the music player in session state so it persists across reruns
if 'player' not in st.session_state:
    st.session_state.player = MusicPlayer()

player = st.session_state.player

st.set_page_config(page_title="Music Player", layout="centered")
st.title("🎵 Music Player")


# --- Music Entry Form ---
st.header("Add New Music")
with st.form("add_music_form", clear_on_submit=True):
    title = st.text_input("Song Title")
    artist = st.text_input("Artist Name")
    genre = st.text_input("Genre")
    
    submitted = st.form_submit_button("Add to Library")
    
    if submitted:
        if title and artist and genre:
            if not re.match(r'^[a-zA-Z0-9\s#@]+$', title):
                st.error("Song title can only contain letters, numbers, spaces, '#', and '@'.")
            else:
                player.music_library.append(Music(title, artist, genre))
                player.save_to_csv()
                st.success(f"Successfully added '{title}' to the library!")
        else:
            st.error("Please fill in all fields.")

st.divider()


# --- Song Library ---
st.header("Music Library")
if not player.music_library:
    st.info("Library is empty. Add some songs above!")
else:
    data = [{"Title": m.title, "Artist": m.artist, "Genre": m.genre} for m in player.music_library]
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)


st.divider()
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("Exit Application", use_container_width=True, type="primary"):
        st.success("Application stopped! You can now safely close this browser tab.")
        player.save_to_csv()
        # Kill the streamlit process safely
        os.kill(os.getpid(), signal.SIGTERM)
