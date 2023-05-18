
from textblob import TextBlob
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from snownlp import SnowNLP

def generate_cloud_map(text, path):

    # 使用Jieba进行分词
    word_list = jieba.cut(text)
    # 将分词结果转化成字符串
    words = ' '.join(word_list)

    # 配置WordCloud对象
    wc = WordCloud(background_color='white', width=800, height=600, max_words=200,
                   font_path='/Users/wjf/Desktop/font/阿里妈妈东方大楷/阿里妈妈东方大楷_Regular.ttf')

    # 生成词云图
    word_cloud = wc.generate(words)

    # 显示词云图
    image = word_cloud.to_image()
    image.save(path)



def emotion_analysis():
  text = "收声音也很小，几乎听不到。网店上个产品，系统奔溃五次，下单不到半个月，降价100，真不错，售后是摆设吗？只会弄个机器人回答？"  # 待分析的中文文本
  s = SnowNLP(text)  # 初始化 SnowNLP 实例

  sentiment_score = s.sentiments  # 获得情感分析得分

  if sentiment_score > 0.5:
      print("这句话是积极的。")
  elif sentiment_score < 0.5:
      print("这句话是消极的。")
  else:
      print("这句话是中性的。")

emotion_analysis()
