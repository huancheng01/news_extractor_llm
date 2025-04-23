
import bs4
import os
import requests
import re
import time
from urllib import request
from bs4 import BeautifulSoup #引入“爬取.py”所需要的所有库


def fetchUrl_RMRB(url):
    '''
    功能：访问 人民日报url 的网页，获取网页内容并返回
    参数：目标网页的 url
    返回：目标网页的 html 内容
    '''
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    return r.text

def getPageList_RMRB(year, month, day):
    '''
    功能：获取人民日报当天报纸的各版面的链接列表
    参数：年，月，日
    '''
    url = 'http://paper.people.com.cn/rmrb/html/' + year + '-' + month + '/' + day + '/nbs.D110000renmrb_01.htm'
    #在人民日报版面目录的链接中，“/year-month/day/” 表示日期，后面的 “_01” 表示这是第一版面的链接。
    print(f'种子url地址：{url}')
    html = fetchUrl_RMRB(url)
    bsobj = bs4.BeautifulSoup(html, 'html.parser')
    #print(html)
    bsContainer = bsobj.find('div', attrs={'class': 'swiper-container'})
    #print(bsContainer)
    pageList = bsContainer.find_all('div', attrs={'class': 'swiper-slide'})
    linkList = []
    '''
    根据html分析可知，版面目录存放在一个
    id = “pageList” 的div标签下，class = “right_title1” 或 “right_title2” 的 div 标签中，
    每一个 div 表示一个版面
    '''
    for page in pageList:
        link = page.a["href"]
        url = 'http://paper.people.com.cn/rmrb/html/' + year + '-' + month + '/' + day + '/' + link
        linkList.append(url)
    return linkList

def getTitleList_RMRB(year, month, day, pageUrl):
    '''
    功能：获取报纸某一版面的文章链接列表
    参数：年，月，日，该版面的链接
    '''
    html = fetchUrl_RMRB(pageUrl)
    bsobj = bs4.BeautifulSoup(html, 'html.parser')
    titleList = bsobj.find('div', attrs={'class': 'news'}).ul.find_all('li')
    '''
    使用同样的方法，我们可以知道，文章目录存放在一个id = “titleList” 的div标签下的ul标签中，
    其中每一个li标签表示一篇文章
    '''
    linkList = []

    for title in titleList:
        tempList = title.find_all('a')
        #文章的链接就在li标签下的a标签中
        for temp in tempList:
            link = temp["href"]
            if 'nw.D110000renmrb' in link:#筛选出文章链接抓取，去除版面其他无关内容的链接
                url = 'http://paper.people.com.cn/rmrb/html/' + year + '-' + month + '/' + day + '/' + link
                linkList.append(url)
    return linkList

def getContent_RMRB(html):
    '''
    功能：解析人民日报HTML 网页，获取新闻的文章内容
    参数：html 网页内容
    '''
    bsobj = bs4.BeautifulSoup(html, 'html.parser')
    # 获取文章
    '''
    内容进入文章内容页面之后,由网页分析知正文部分存放在 id = “ozoom” 的 div 标签下的 p 标签里。
    '''
    pList = bsobj.find('div', attrs={'id': 'ozoom'}).find_all('p')
    content = ''
    for p in pList:
        content += p.text + '\n'
    resp = content
    return resp

def saveFile_RMRB(content, path, filename):
    '''
    功能：将文章内容 content 保存到本地文件中
    参数：要保存的内容，路径，文件名
    '''
    # 如果没有该文件夹，则自动生成
    if not os.path.exists(path):
        os.makedirs(path)

    # 保存文件
    with open(path + filename, 'w', encoding='utf-8') as f:
        f.write(content)

def download_RMRB(year, month, day, destdir):
    '''
    功能：爬取《人民日报》网站 某年 某月 某日 的新闻内容，并保存在 指定目录下
    参数：年，月，日，文件保存的根目录
    '''
    
    #第一步，获得对应日期下的所有版面url地址
    pageList = getPageList_RMRB(year, month, day)
    
    #遍历每个版面
    for page in pageList:
        #print('版面：', page)

        try:
            #获取本版面下的文章url地址
            titleList = getTitleList_RMRB(year, month, day, page)
        except:
            print('err page:', page)
            continue

        
        #遍历每个url地址，获得文章实际内容
        for url in titleList:

            #获得文章内容
            try:
                html = fetchUrl_RMRB(url)
            except Exception as err:
                print(err)
                continue
            if len(html) < 100:
                continue
            
            #解析获得文章的标题，并删除非法符号，避免文章标题作为文件名写入时候出错
            bsobj = bs4.BeautifulSoup(html, 'html.parser')
            title = bsobj.h3.text + bsobj.h1.text + bsobj.h2.text

            title_replace_list = [':', ':', '|', '/', '\\', '*', '<', '>', '?', '.', '⑫', ' ']
            for rep in title_replace_list:
                title = title.replace(rep, '')
            
            #抽取文章实体内容
            content = getContent_RMRB(html)
            
            if len(content) < 20:
                print(url)
                continue
            content = url+ '\n' + content

             # 生成保存的文件路径及文件名
            path = destdir + '/'
            fileName = title[:100] + '.txt'
            


            # 保存文件
            saveFile_RMRB(content, path, fileName)



if __name__ == '__main__':
    '''
    主函数：程序入口
    '''
    # 爬取指定日期的新闻
    #对想爬取收集的网站进行选择


    import datetime
    import os
    if not os.path.exists('./data'):
        os.mkdir('./data')
    if not os.path.exists("./data/news_data"):
        os.mkdir("./data/news_data")
        
    newsDate = input('输入爬取的结束日期，如(20200101)：')
    days = int(input('输入爬取的天数：'))
    last_date = datetime.datetime.strptime(newsDate, '%Y%m%d').date()
    for i in range(days):
        crawl_date = (last_date - datetime.timedelta(days = i)).strftime('%Y%m%d')
        year = crawl_date[0:4]
        month = crawl_date[4:6]
        day = crawl_date[6:8]

        print(f'爬取 {crawl_date} 人民日报新闻...')
        download_RMRB(year, month, day, './data/news_data')


    

