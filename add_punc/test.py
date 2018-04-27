#coding: utf-8
import polyglot
from polyglot.text import Text, Word

text = Text("Bonjour, Mesdames.")

text = Text("你好，搜狗")
print("Language Detected: Code={}, Name={}\n".format(text.language.code, text.language.name))



