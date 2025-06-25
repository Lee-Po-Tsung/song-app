import streamlit as st
from appGlobal import SONGLIST, JPS, YTIMG, YTURL
from pandas import concat
import pickle
import random

def hello():
    pop = SONGLIST.popSonglist(10)
    st.video(YTURL(pop['ytID'][0]))

def randomSong():
    songID = random.randrange(len(SONGLIST))
    song = SONGLIST.getSong_from_id(songID)
    showSong(song)

def popList():
    pd = SONGLIST.popSonglist(10)
    st.header("熱門音樂", divider=True)
    st.table(concat([pd["ytID"].apply(lambda id: f"![該影片已不在YT]({YTIMG(id)})").rename("縮圖"), pd['songName'].rename("歌名"), pd['view'].rename("瀏覽次數")], axis=1))

def allList():
    pd = SONGLIST.songlist(1, 10)
    st.header("全部音樂", divider=True)
    st.table(concat([pd["ytID"].apply(lambda id: f"![該影片已不在YT]({YTIMG(id)})").rename("縮圖"), pd['songName'].rename("歌名"), pd['view'].rename("瀏覽次數")], axis=1))

def settingPage():
    ...

def showSong(song):
    st.video(YTURL(song.ytID))
    st.divider()
    jps = pickle.loads(JPS.get_file_data(f"{song.songID}.jps"))
    st.dataframe(jps.lyrics.DataFrame)

st.navigation([
    st.Page(hello, title='首頁', icon=':material/house:', default=True),
    st.Page(allList, title='全部音樂', icon='🎵', url_path='song-list'),
    st.Page(popList, title='熱門音樂', icon='🔥', url_path='pop-song-list'),
    st.Page(randomSong, title='隨機歌曲', icon='🔀', url_path='random-song'),
    st.Page(settingPage, title='設定', icon='⚙', url_path='setting')
]).run()

