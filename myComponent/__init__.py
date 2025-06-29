from streamlit.components.v1 import declare_component
from os import listdir
from os.path import dirname, isdir, abspath, join
from pandas import DataFrame

__all__ = []

PATH = abspath(dirname(__file__))

_component_funcs = {}
for i in listdir(PATH):
    if isdir(join(PATH, i)):
        __all__.append(i)
        _component_funcs.setdefault(i, declare_component(i, path=join(PATH, i)))

def table(df: DataFrame, tagNames: list[str], attrs: list[str], header:None|list[str]=None, key=None):
    if header == None:
        header = df.columns.to_list()
    component_value = _component_funcs["table"](df=df, tagNames=tagNames, attrs=attrs, header=header, key=key, default=-1)
    return component_value