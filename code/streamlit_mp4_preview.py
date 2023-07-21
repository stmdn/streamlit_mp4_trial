import streamlit as st
import os
from mutagen.mp3 import MP3
from moviepy.editor import VideoFileClip
from datetime import datetime, time

recordings_folder_name = "./datafiles/"


def list_recording_files():
# Reads the data_folder_name and returns a list of mp4 files found in it.
# Called within tab_session_select before submit button is pressed
  AV_files = []
  
  for file in os.listdir(recordings_folder_name):
    if file.endswith(".mp4") or file.endswith(".mp3"):
      AV_files.append(file)
  
  return AV_files

def get_time_from_string(time_str):
    try:
        timeobj = datetime.strptime(time_str, "%H:%M:%S").time()
        secs_val = timeobj.hour * 3600 + timeobj.minute * 60 + timeobj.second
        return timeobj, secs_val
    except ValueError:
        print("Invalid time format. Please use HH:MM:SS")
        return None, None

tab_AV_select, tab_time_select = \
        st.tabs(["Select Recording",
                 "Select Time Window"
                 ])
submit_AV_select = False
submit_time_select = False
valid_time_selected = False

with tab_AV_select:
  with st.form("Recordings"):
    AV_choices = list_recording_files()
    selected_AV = recordings_folder_name + st.selectbox('Choose a Recording File', options=AV_choices)
    submit_AV_select = st.form_submit_button("Submit")

with tab_time_select:
    with st.form("Time Selection"):
        video_file = open(selected_AV, 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)

        
        if selected_AV.lower().endswith('.mp3'):
            audio = MP3(selected_AV)
            duration = audio.info.length
                
        elif selected_AV.lower().endswith('.mp4'):
            clip = VideoFileClip(selected_AV)
            duration = clip.duration
            clip.close()

        starttime_str = st.text_input("Specify the start time in HH\:MM\:SS format", value="00:00:00")
        #st.write("Duration: ", duration)

        starttime, starttime_secs = get_time_from_string(starttime_str)
        if starttime == None:
           st.write("Invalid time. Please use HH\:MM\:SS")
        elif starttime_secs > round(duration):
           st.write("Error: Specified time is beyond the clip length")
        else:
            valid_time_selected = True
        submit_time_select = st.form_submit_button("Submit")


            
with tab_AV_select:
    if submit_AV_select or submit_time_select:
        st.write("Recording selected: ", selected_AV)            


with tab_time_select:
   if submit_time_select and valid_time_selected:
        st.write("Start time:", starttime)
        