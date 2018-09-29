#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
data:18-9-28
'''

from os import path
from wordcloud import WordCloud
import jieba
import sys
reload(sys)
sys.setdefaultencoding('utf8')

d = path.dirname(__file__)

# 打开要进行词云的文件
with open('qq_word.txt', 'r') as f:
    siglist = f.readlines()
    text = "".join(siglist)
	
	#进行分词
    wordlist = jieba.cut(text, cut_all=True)
    word_space_split = " ".join(wordlist)

# 形成一个词云图
wordcloud = WordCloud().generate(word_space_split)

# 把词云图展示出来
# the matplotlib way:
import matplotlib.pyplot as plt

# 设置图片属性
#generate可以对全部文本进行自动分词，但是它对中文支持不好，所以设置中文的字体集
#max_font_size  font_path设置字体集 background_color参数为设置背景颜色,默认颜色为黑色
wordcloud = WordCloud(max_font_size=40,font_path="DroidSansFallbackFull.ttf").generate(word_space_split)
plt.figure()
plt.imshow(wordcloud)
plt.axis("off")
plt.show()