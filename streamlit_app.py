import streamlit as st
import os
import sys

def hello():
    os.system(sys.executable + " --version")

def randomSong():
    ...

def popList():
    ...

def allList():
    ...

def settingPage():
    ...

def showSong(song):
    ...

st.navigation([
    st.Page(hello, title='首頁', icon=':material/house:', default=True),
    st.Page(allList, title='全部音樂', icon='🎵', url_path='song-list'),
    st.Page(popList, title='熱門音樂', icon='🔥', url_path='pop-song-list'),
    st.Page(randomSong, title='隨機歌曲', icon='🔀', url_path='random-song'),
    st.Page(settingPage, title='設定', icon='⚙', url_path='setting')
]).run()

