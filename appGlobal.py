# from sys import modules
# from os.path import abspath, dirname, join

# MAINFILE = abspath(modules['__main__'].__file__)

# if MAINFILE == join(dirname(__file__), 'streamlit_app.py'):
if True:
    from myLib.JPSZip_api import ZipHandler
    from myLib.sheet import Sheet

    SONG = ZipHandler("data/SONG")
    SONGLIST = Sheet("data/songlist.csv")

YTURL = "https://www.youtube.com/watch?v={}".format

YTIMG_MAX = "https://i.ytimg.com/vi/{}/maxresdefault.jpg".format

YTIMG_HQ = "https://i.ytimg.com/vi/{}/hqdefault.jpg".format

YTIMG_MQ = "https://i.ytimg.com/vi/{}/mqdefault.jpg".format

YTIMG_SD = "https://i.ytimg.com/vi/{}/sddefault.jpg".format

YTIMG = "https://i.ytimg.com/vi/{}/default.jpg".format