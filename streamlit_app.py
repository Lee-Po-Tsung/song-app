import streamlit as st
from appGlobal import SONGLIST, SONG, YTIMG, YTURL, Sheet
from pandas import concat, DataFrame
import json
import random
from streamlit.components.v1 import html
from myComponent import table
from math import ceil

# pages

@st.fragment
def hello():
    st.header("歡迎", divider=True)

@st.fragment
def randomSong():
    st.session_state.songID = random.randrange(1, len(SONGLIST))
    st.switch_page(PAGES["SONGPAGE"])

@st.fragment
def popList():
    df = SONGLIST.popSonglist(10)
    st.header("熱門音樂", divider=True)
    showSongList(df)

def allList():
    st.header("全部音樂", divider=True)
    pagedList(SONGLIST)

@st.fragment
def searchPage():
    def inputChange():
        if st.query_params.get("page", None):
            st.query_params.update({"page": 1})
            
    if value := st.text_input("歌名搜尋", on_change=inputChange):
        tmp = SONGLIST.TF(SONGLIST._df["songName"].str.contains(value))
        if len(tmp):
            pagedList(tmp)
        else:
            st.write("無結果")

def settingPage():
    ...

@st.fragment
def songPage():
    songID = -1

    try:
        if songID := st.query_params.get("ID", None):
            songID = int(songID)
        else:
            songID = st.session_state.pop("songID")
    except:
        st.switch_page(PAGES["HOMEPAGE"])
        return
    
    if songID == -1:
        st.switch_page(PAGES["HOMEPAGE"])
    else:
        song = SONGLIST.getSong_from_id(songID)
        showSong(song)

# function

@st.fragment
def pagedList(sheet: Sheet):
    curpage = st.query_params.get("page", "1")
    MaxPage = ceil(len(sheet) / 10)

    if not curpage.isdecimal():
        st.error("你在幹什麼?")
        return
    
    curpage = int(curpage)

    if curpage > MaxPage or curpage < 1:
        st.error("你在幹什麼?")
        return
    
    df = sheet.songlist(curpage, 10)
    showSongList(df)

    def prevPage():
        if curpage > 1:
            st.query_params.update({"page": curpage - 1})

    def nextPage():
        if curpage < MaxPage:
            st.query_params.update({"page": curpage + 1})

    def changePage():
        st.query_params.update({"page": st.session_state.get("page_selector", 1)})

    cols = st.columns(3, vertical_alignment='bottom', gap="large")
    cols[0].button("上一頁", disabled=curpage <= 1, use_container_width=True, on_click=prevPage)
        
    cols[1].selectbox(label="頁碼",
                      label_visibility="collapsed", 
                      options=range(1, MaxPage + 1),
                      index=curpage - 1,
                      width=100, key="page_selector", on_change=changePage, format_func=lambda x: f"{x}")
    
    cols[2].button("下一頁", disabled=curpage >= MaxPage, use_container_width=True, on_click=nextPage)

def showSongList(df: DataFrame):
    index = table(concat([df["ytID"].apply(lambda x: YTIMG(x)).rename("縮圖"), df['songName'].rename("歌名"), df['view'].rename("瀏覽次數")], axis=1),
          tagNames=["img", "p", "p"], 
          attrs=["src", "innerText", "innerText"])
    
    if index != -1:
        st.session_state.songID = df.iloc[index].songID
        st.switch_page(PAGES["SONGPAGE"])

def showSong(song):
    st.set_page_config(
        page_title=song.songName,
        page_icon='🎧',
        )
    st.query_params.update({"ID": song.songID})

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

# main

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
