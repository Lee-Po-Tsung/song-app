import pandas as pd
from typing import overload
import ast
from io import StringIO
from math import ceil

class Sheet:
    def __init__(self, csv_path):
        """初始化，讀取 CSV 檔案"""
        self._path = csv_path
        try:
            self._df = pd.read_csv(self._path, converters={'langs': ast.literal_eval})
        except:
            self._df = pd.DataFrame(columns=['songID', 'songName', 'ytID', 'view', 'langs'])
            self.save()

    @overload
    def getdata(self, e: int): ...
    @overload
    def getdata(self, s: int, e: int): ...
    def getdata(self, *args):
        """根據索引範圍獲取資料"""
        match len(args):
            case 0:
                raise TypeError(f"getdata expected at least 1 argument, got 0")
            case 1 | 2:
                return self._df.iloc[slice(*args), :]
        raise TypeError("getdata expected at most 2 arguments, got " + str(len(args)))
    
    def addSong(self, songName: str, ytID: str, langs: list=[]):
        new_song_id = self._df['songID'].max() + 1 if not self._df.empty else 1
        newSong = pd.DataFrame([[new_song_id, songName, ytID, 0, langs]], columns=['songID', 'songName', 'ytID', 'view', 'langs'])
        if not newSong.empty:
            self._df = pd.concat([self._df, newSong], axis=0, ignore_index=True)
        self.save()

    def getSong_from_id(self, song_id: int):
        song = self._df.loc[self._df['songID'] == song_id]
        if song.empty:
            raise ValueError(f"Error: No song found with songID {song_id}")
            
        return song.iloc[0]

    def getSong_from_name(self, song_name: str):
        song = self._df.loc[self._df['songName'] == song_name]
        if song.empty:
            raise ValueError(f"Error: No song found with songID {song_name}")
        return song.iloc[0]
    
    def songViewed(self, id: int):
        self.getSong_from_id(id)['view'] += 1
        self.save()

    def save(self):
        """將當前 DataFrame 存回 CSV 檔案"""
        self._df.to_csv(self._path, index=False)

    def popSonglist(self, size=50):
        return self._df.sort_values("view").iloc[:size].reset_index(drop=True)

    def songlist(self, page, size=50):
        """分頁獲取資料，預設每頁 50 筆"""
        if size < 1 or page < 1:
            raise ValueError("???")
        total_rows = len(self._df)
        if (page - 1) * size > total_rows:
            raise ValueError(f"page number > {ceil(total_rows / size)}")
        return self.getdata((page - 1) * size, page * size)
    
    def filter(self, items:list[str]):
        new = Sheet(StringIO())
        new._df = self._df.filter(items=items)
        return new
    
    def TF(self, series: pd.Series):
        new = Sheet(StringIO())
        new._df = self._df[series]
        return new

    def __len__(self):
        """獲取總行數"""
        return len(self._df)
 