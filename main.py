import streamlit as st
import time
from datetime import datetime, timedelta
import pygame.mixer

# Initialize pygame mixer for alarm sound
pygame.mixer.init()

def load_alarm_sound():
    try:
        pygame.mixer.music.load("alarm.wav")  # You'll need to provide an alarm sound file
    except:
        st.warning("Alarm sound file not found. Timer will still work but without sound.")

def format_time(seconds):
    return str(timedelta(seconds=seconds))[2:7]  # Format as MM:SS

def main():
    st.title("🍅 Pomodoro Timer")
    
    # Clean, modern styling
    st.markdown("""
        <style>
        .stButton>button {
            width: 100%;
            margin-bottom: 10px;
        }
        .big-text {
            font-size: 4rem;
            font-weight: bold;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    # Session state initialization
    if 'time_remaining' not in st.session_state:
        st.session_state.time_remaining = 0
    if 'running' not in st.session_state:
        st.session_state.running = False
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None

    # Timer duration input
    duration = st.number_input(
        "Focus Duration (minutes)",
        min_value=1,
        max_value=60,
        value=25,
        step=1
    )

    # Timer display
    if st.session_state.time_remaining > 0:
        st.markdown(f'<p class="big-text">{format_time(st.session_state.time_remaining)}</p>', 
                   unsafe_allow_html=True)
    else:
        st.markdown(f'<p class="big-text">{format_time(duration * 60)}</p>', 
                   unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # Start button
    with col1:
        if st.button("Start" if not st.session_state.running else "Pause"):
            if not st.session_state.running:
                st.session_state.running = True
                st.session_state.time_remaining = duration * 60
                st.session_state.start_time = time.time()
                load_alarm_sound()
            else:
                st.session_state.running = False

    # Reset button
    with col2:
        if st.button("Reset"):
            st.session_state.running = False
            st.session_state.time_remaining = duration * 60
            st.session_state.start_time = None

    # Timer logic
    if st.session_state.running:
        elapsed = int(time.time() - st.session_state.start_time)
        st.session_state.time_remaining = max(0, duration * 60 - elapsed)
        
        if st.session_state.time_remaining <= 0:
            st.session_state.running = False
            try:
                pygame.mixer.music.play()
                st.balloons()
            except:
                st.warning("Time's up!")
        
        st.experimental_rerun()

if __name__ == "__main__":
    main()
