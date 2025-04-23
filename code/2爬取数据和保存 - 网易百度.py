
import bs4
import os
import requests
import re
import time
from urllib import request
from bs4 import BeautifulSoup #引入“爬取.py”所需要的所有库




def fetchUrl_WY(url):
    '''
    功能：访问 网易社会url 的网页，获取网页内容并返回
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

def download_WY(title, url, year, month, day):
    '''
    功能：爬取网易社会网站某一URL当日的新闻内容，并保存在指定目录下
    参数：新闻标题，抓取的URL，年，月，日
    '''
    try:
        html = fetchUrl_WY(url)
    except Exception:
        #print(url, ' error')
        return
    bsobj = bs4.BeautifulSoup(html, 'html.parser')
    title = title.replace(':', '')
    title = title.replace('"', '')
    title = title.replace('|', '')
    title = title.replace('/', '')
    title = title.replace('\\', '')
    title = title.replace('*', '')
    title = title.replace('<', '')
    title = title.replace('>', '')
    title = title.replace('?', '')
    title = title.replace('.', '')

    #获取新闻正文内容
    tag = bsobj.find('div', class_='post_body').text
    file_name = r'./data/news_data/' + title + '.txt'
    file = open(file_name, 'w', encoding='utf-8')
    tag = tag.replace(' ', '')
    content = 'URL:' + url + '\n' + tag
    #写入文件
    file.write(content)
    file.close()

def downloads_WY():
    '''
    功能：爬取网易社会网站所有种子URL（URL数组）下的新闻内容，并保存在指定目录下
    参数：无
    '''
    urls = ['http://temp.163.com/special/00804KVA/cm_shehui.js?callback=data_callback',
            'http://temp.163.com/special/00804KVA/cm_shehui_02.js?callback=data_callback',
            'http://temp.163.com/special/00804KVA/cm_shehui_03.js?callback=data_callback']
    '''
    网易新闻的标题及内容是使用js异步加载的，单纯的下载网页源代码是没有标题及内容的
    我们可以在Network的js中找到我们需要的内容
    '''
    for url in urls:
        print('seed', url)
        req = request.urlopen(url)
        res = req.read().decode('gbk')
        pat1 = r'"title":"(.*?)",'
        pat2 = r'"tlink":"(.*?)",'
        m1 = re.findall(pat1, res)
        news_title = []
        for i in m1:
            news_title.append(i)
        m2 = re.findall(pat2, res)
        news_url = []
        for j in m2:
            news_url.append(j)
        for i in range(0, len(news_url)):
            download_WY(news_title[i], news_url[i], year, month, day)

def fetchUrl_BD(url, headers): #爬取百度news所有url
    urlsss = []
    r = requests.get(url, headers=headers).text
    soup = BeautifulSoup(r,'html.parser')
    for i in soup.find_all('h3'):  #文章标题存放在 h3 标签中
        urlsss.append(i.a.get('href'))
    return urlsss

def getContent_BD(urls, headers, year, month, day): #对抓取到的百度新闻连接的内容的操作
    if os.path.exists('./data/news_data/'):
        pass
    else:
        os.mkdir('./data/news_data')

    for q in urls:
        print(q)
        try:
            time.sleep(2)#定时抓取
            r = requests.get(q, headers=headers).text
            soup = BeautifulSoup(r,'html.parser')
            title = soup.find('div', class_="titleFont")#每章的标题
            if os.path.exists('./data/news_data/' +title.get_text().strip() +'.txt'): #检查是否已存在该文件
                continue#内容已经抓取过并存在文件夹中，不必再抓取
            else:
                title_txt = title.get_text()
                title_txt = title_txt.replace(':', '')
                title_txt = title_txt.replace('"', '')
                title_txt = title_txt.replace('|', '')
                title_txt = title_txt.replace('/', '')
                title_txt = title_txt.replace('\\', '')
                title_txt = title_txt.replace('*', '')
                title_txt = title_txt.replace('<', '')
                title_txt = title_txt.replace('>', '')
                title_txt = title_txt.replace('?', '')
                title_txt = title_txt.replace('.', '')
                f = open('./data/news_data/' +title_txt +'.txt','w',encoding='utf-8')
                aaf = 'URL:%s'%q
                f.write(aaf + '\n')
                content_list = soup.find_all('p', class_='contentFont')
                for i in content_list:
                    f.write(i.get_text() + '\n')
                f.close()
        except Exception as result:#处理异常抓取的情况，使程序继续爬取其他网页
            print(q, ' error', result)
            continue


def download_BD():#下载百度新闻的内容以文件形式保存
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
    url = 'https://news.baidu.com/widget?id=AllOtherData&channel=internet&t=1554738238830'
    getContent_BD(fetchUrl_BD(url,headers), headers,year,month,day)

if __name__ == '__main__':
    '''
    主函数：程序入口
    '''
    # 爬取指定日期的新闻
    #对想爬取收集的网站进行选择
    flag_RMRB = input('是否爬取人民日报？是-1 否-0：')
    if flag_RMRB == '1':
        import datetime
        import os
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


    flag_WY = input('是否爬取网易社会新闻？是-1 否-0：')
    if flag_WY == '1':
        downloads_WY()
        print('网易社会抓取完成！')

    flag_BD = input('是否爬取百度新闻？是-1 否-0：')

    if flag_BD == '1':
        download_BD()
        print('百度新闻抓取完成！')

