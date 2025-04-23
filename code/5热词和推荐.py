# encoding:utf-8
# ! python3
# -*- coding: utf-8 -*-

import os
import math
import linecache
import re
import codecs
import time
import jieba
from jieba import analyse
from collections import Counter

import matplotlib.pyplot as plt
from wordcloud import WordCloud




def seg_doc(file_content, stopwords):
    
    seg_list = jieba.cut(file_content)
    
    clean_list = []
    for word in seg_list:
        if word not in stopwords:
            if ord(word[0]) > 127:
                if word != '\t':
                    clean_list.append(word)
    return clean_list


def tf(seg_list):
    tf_idf_value = {}
    for word in seg_list:
        if len(word) > 1 and word != '\r\n':
            if not tf_idf_value.get(word):
                tf_idf_value[word] = [1, 0]
            else:
                tf_idf_value[word][0] += 1
    return tf_idf_value

def idf(tf_idf_value, file_content_dict):
    N = len(file_content_dict) # 文章篇数
    idf = 0

    for word in tf_idf_value:
        df = 0
        for file, content in file_content_dict.items():
            if re.findall(word, content, flags=0):
                df += 1
        if df:
            idf = N / df
        tf_idf_value[word][1] = idf
    return tf_idf_value


def weight(tf_idf_value):
    doc_value = {}
    weight = 0
    for key in tf_idf_value:
        weight = tf_idf_value[key][0] * tf_idf_value[key][1]
        doc_value[key] = weight
    return doc_value


#cos函数的目的是计算两个向量的余弦相似度，在多维空间中的相似性

def cos2(w1_value, w2_value):
    w_mul = 0
    w1_exp = 0
    w2_exp = 0
    cos = 0
    for word in w1_value:
        if word in w2_value:
            w_mul += w1_value[word] * w2_value[word]
            w1_exp += math.pow(w1_value[word], 2)
            w2_exp += math.pow(w2_value[word], 2)
    denominator = math.sqrt(w1_exp) * math.sqrt(w2_exp)
    if denominator:
        cos = w_mul / denominator
    return cos


def hotwords(filePath):
    
    word_freq = Counter()
    # 遍历目录下的所有文件
    for root, dirs, files in os.walk(filePath):
        for file in files:
            # 构造文件的完整路径
            file_path = os.path.join(root, file)
            
            # 读取文件内容（假设文件是文本文件）
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # 使用jieba进行分词
            words = jieba.lcut(content)
            
            words = [ word for word in words if len(word) > 1 ]
            
            word_freq.update(words)
    
    
    text1 = ""
    for (k, v) in word_freq.most_common(12):
        print(k, v)
        text1 = text1 + " " + k
    
    wc = WordCloud(
        background_color="white",  # 设置背景为白色，默认为黑色
        collocations=False, font_path='C:/Windows/Fonts/SimHei.ttf', width=1400, height=1400, margin=2
    ).generate(text1.lower())
    # 为云图去掉坐标轴
    
    plt.axis("off")
    # 画云图，显示
    #plt.show(wc)
    # 保存云图
    wc.to_file("./wordcloud.png")           
    



def load_file_content_dict(filePath):
    file_content_dict = {}

    for root, dirs, files in os.walk(filePath):  # dirs 不能去掉
        for file in files:
            txtPath = os.path.join(root, file)
            if not os.path.isfile(txtPath):
                continue
            #print(txtPath)
            if not txtPath.endswith('txt'):
                continue
            with codecs.open(txtPath, 'r', 'utf-8') as f:
                txt = f.read()
                file_content_dict[txtPath] = txt

    print('load_file_content done, count', len(file_content_dict))
    return file_content_dict

def interet(filePath):
    print("请输入你感兴趣的新闻话题：")
    words = input()

    #加载文件并保存到字典中，字典key为文件名，value为对应的文件内容
    file_content_dict = load_file_content_dict(filePath)
    
    #加载停用词
    stopwords = [line.strip() for line in open('./stop.txt', 'r', encoding='utf-8').readlines()]
    stopwords = set(stopwords)

    query_value = {}
    query_value[words] = 1

    files = os.listdir(filePath)
    sim = {}
    news_name = []

    No = 0
    
    #再次遍历所有文件
    for file_name, file_content in file_content_dict.items():
    
            No += 1
            if No % 10 == 0:
                print('#', No)
            
            seg_list = seg_doc(file_content, stopwords)
            
            #计算tf数值
            tf_value = tf(seg_list)

            #计算idf数值
            tf_idf_value = idf(tf_value, file_content_dict)
            
            doc_value = weight(tf_idf_value)
            
            cos_value = cos2(query_value, doc_value)
            sim[file_name] = cos_value
            

    sim_sort = sorted(sim.items(), key=lambda item: item[1], reverse=True)
    i = 0
    for ns_name in sim_sort:
        if i < 3:
            real_name = re.sub(".txt", "", ns_name[0])
            news_name.append(real_name)
            print(i+1, '、', news_name[i])
        else:
            break
        i += 1

if __name__ == "__main__":
    print('1:展示新闻热词')
    print('2:根据用户兴趣推荐新闻')
    key = input('请输入选择（1/2）：')
    filePath = './data/news_data'
    if key == '1':
        start = time.time()
        #热词呈现
        hotwords(filePath)
        end = time.time()
        print(f'cost time: {end - start}')
    else:
        # 兴趣新闻
        start = time.time()
        interet(filePath)
        end = time.time()
        print(f'cost time: {end - start}')


