import streamlit as st
from appGlobal import SONGLIST, SONG, YTIMG, YTURL
from pandas import concat
import json
import random
from streamlit.components.v1 import html

@st.fragment
def hello():
    st.header("歡迎", divider=True)

@st.fragment
def randomSong():
    st.session_state.songID = random.randrange(len(SONGLIST))
    st.switch_page(PAGES["SONGPAGE"])

@st.fragment
def popList():
    pd = SONGLIST.popSonglist(10)
    st.header("熱門音樂", divider=True)
    st.table(concat([pd["ytID"].apply(lambda id: f"![該影片已不在YT]({YTIMG(id)})").rename("縮圖"), pd['songName'].rename("歌名"), pd['view'].rename("瀏覽次數")], axis=1))

@st.fragment
def allList():
    pd = SONGLIST.songlist(st.session_state.currentPage, 10)
    st.header("全部音樂", divider=True)
    st.table(concat([pd["ytID"].apply(lambda id: f"![該影片已不在YT]({YTIMG(id)})").rename("縮圖"), pd['songName'].rename("歌名"), pd['view'].rename("瀏覽次數")], axis=1))

    MaxPage = len(SONGLIST) // 10 + 1

    def changePage():
        st.session_state.update({"currentPage": st.session_state.get("page_selector", 1)})

    cols = st.columns(3, vertical_alignment='bottom', gap="large")
    if cols[0].button("上一頁", disabled=st.session_state.currentPage <= 1, use_container_width=True):
        st.session_state.currentPage -= 1

    cols[1].selectbox(label="頁碼",
                      label_visibility="collapsed", 
                      options=range(1, MaxPage),
                      index=st.session_state.currentPage - 1,
                      width=100, key="page_selector", on_change=changePage, format_func=lambda x: f"{x}")
    
    if cols[2].button("下一頁", disabled=st.session_state.currentPage >= MaxPage, use_container_width=True):
        st.session_state.currentPage += 1    

def searchPage():
    ...

def settingPage():
    ...

@st.fragment
def songPage():
    songID = st.session_state.get("songID", -1)
    if songID == -1:
        st.switch_page(PAGES["HOMEPAGE"])
    else:
        song = SONGLIST.getSong_from_id(songID)
        showSong(song)

def showSong(song):
    st.set_page_config(
        page_title=song.songName,
        page_icon='🎧',
        )
    jps = json.loads(SONG.get_file_data(f"JPS-{song.songID}"))
    st.video(YTURL(song.ytID))
    st.divider()
    if title := jps.get('title', None):
        st.html(f"{title}")
    else:
        st.error("發生錯誤")
    @st.fragment
    def func():
        select = []
        if langs := jps.get("langs", []):
            if langs != []:
                select = st.multiselect("歌詞語言", langs, default=langs[0], max_selections=2)
            else:
                st.write("無歌詞")
        st.divider()
        for lyric in zip(*[jps["lyrics"][lang] for lang in select]):
            st.html(f"<div>{"<br>".join(lyric)}</div>")
    func()
    st.divider()

st.session_state.currentPage = 1

PAGES = {
    "HOMEPAGE": st.Page(hello, title='首頁', icon=':material/house:', default=True),
    "LISTPAGE": st.Page(allList, title='全部音樂', icon='🎵', url_path='song-list'),
    "POPPAGE": st.Page(popList, title='熱門音樂', icon='🔥', url_path='pop-song-list'),
    "SONGPAGE": st.Page(songPage, url_path='song'),
    "RANDPAGE": st.Page(randomSong, title='隨機歌曲', icon='🔀', url_path='random-song'),
    "SEARCHPAGE": st.Page(searchPage, title="搜尋歌曲", icon="🔍", url_path="search-song"),
    "SETTINGPAGE": st.Page(settingPage, title='設定', icon='⚙', url_path='setting')
}

st.navigation([*PAGES.values()], position='top').run()

st.html("""<style>
        ul[data-testid='stSidebarNavItems'] > li:has(span[label='songPage']){display: none;}
        header.stAppHeader  div.rc-overflow > div.rc-overflow-item:has(span[label='songPage']){display: none;}
        </style>""")
