import os
import re
'''
“数据预处理.py”程序 功能1：过滤新闻中除中文外所有字符，便于进行分类中的中文分词 
'''

dst_path = './data/filter_news_data/'
if not os.path.exists(dst_path):
    os.makedirs(dst_path)

src_path = './data/news_data/'
dirs = os.listdir(src_path)
for fn in dirs:                            # 循环读取路径下的新闻文件并筛选输出
    if os.path.splitext(fn)[1] == ".txt":   # 筛选txt文件
        print(fn)
        in_file = open(os.path.join(src_path, fn), 'r', encoding='UTF-8')  # 加载要处理的文件的路径
        out_file = open(os.path.join(dst_path, fn), 'w', encoding='UTF-8')
        for line in in_file:
            line = re.sub(u"([^\u4e00-\u9fa5])", "", line)#只保留汉字字符
            out_file.write(line)
        out_file.close()





