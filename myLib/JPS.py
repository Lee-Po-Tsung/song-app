from typing import overload
import os
import pandas as pd
import pickle

class Descript:
    def __init__(self):
        self._value = []
    def addLine(self, v:str):
        self._value.append(v)
    @property
    def markdown(self):
        return "\n".join(self._value)
    @property
    def html(self):
        return "<br>".join(self._value)
    def __getitem__(self, k):
        return self._value[k]

class word:
    def __init__(self, w: str, p: str):
        self._word = w
        self._phoneticSymbol = p

    @property
    def word(self):
        return self._word

    @property
    def phoneticSymbol(self):
        return self._phoneticSymbol

    def __str__(self):
        return f"{{{self.word} : {self.phoneticSymbol}}}"

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter([self.word, self.phoneticSymbol])

class ruby:
    def __init__(self, line: list[str, word]):
        self._line = line  # 存一行歌詞，其中有 str 和 word 物件

    def phoneticSymbol(self):
        """取得整句的讀音"""
        return "".join(i.phoneticSymbol if isinstance(i, word) else i for i in self._line)

    def word(self):
        """取得整句的原文"""
        return "".join(i.word if isinstance(i, word) else i for i in self._line)

    def __repr__(self):
        return str(self._line)

    def __str__(self):
        return self.word()

    def isRuby(self):
        return len([i for i in self._line if isinstance(i, ruby)]) > 0

    def html(self):
        return "".join(f"<ruby><rb>{i.word}</rb><rt>{i.phoneticSymbol}</rt></ruby>" if isinstance(i, word) else i for i in self._line)

    def selfFormat(self, f:str, sep:str=""):
        """需包含兩個"{}" 例:"{}:{}", "單字:{w}, 注音:{p}" """
        try:
            return sep.join(f.format({'w':i.word, 'p':i.phoneticSymbol}) if isinstance(i, word) else i for i in self._line)
        except:
            return sep.join(f.format(*i) if isinstance(i, word) else i for i in self._line)

class Lyrics:
    def __init__(self):
        """用初始語言建立 DataFrame"""
        self._df = pd.DataFrame()

    @property
    def DataFrame(self):
        return self._df

    @property
    def supportedLangs(self):
        return self._df.columns.to_list()

    def addLang(self, lang: str, value: list[ruby]):
        """新增其他語言的歌詞"""
        self._df[lang.lower()] = value

    def __iter__(self):
        """支援迭代輸出 DataFrame 內的歌詞"""
        for _, row in self._df.iterrows():
            yield row

    def __len__(self):
        return len(self._df)

class JPS:
    def __init__(self):
        self._lyrics = None
        self._timestamp = None
        self.descript = Descript()
    def tofile(self, filename:str):
        path = os.path.dirname(filename)
        if not os.path.exists(path):
            os.mkdir(path)
        if not filename.endswith(".jps"):
            filename += '.jps'
        with open(filename, 'wb') as file:
            pickle.dump(self, file)
    def updateLyrics(self, value: Lyrics):
        self._lyrics = value
    def updateTimestamp(self, value):
        self._timestamp = value
    @property
    def lyrics(self):
        return self._lyrics
    @property
    def timestamp(self):
        return self._timestamp