import requests
from bs4 import BeautifulSoup


url_q = "https://ict.gdqy.edu.cn/xwdt1"

def b_txt(h_url,output_folder,name):
    content = ''
    z_url = 'https://ict.gdqy.edu.cn/' + h_url
    resp = requests.get(z_url)
    resp.encoding = 'utf-8'
    data = resp.text
    bs = BeautifulSoup(data,"html.parser")
    # 查找目标内容，增加空值检查
    ul = bs.find('ul', attrs={'class': 'v_news_content'})
    if ul is None:
        print(f"警告：未找到目标 ul 标签，URL: {z_url}")
        return

    # 使用正确的属性筛选方式
    pList = ul.find_all('p', style='text-indent:32px;line-height:150%')
    if not pList:
        print(f"警告：未找到符合条件的段落标签，URL: {z_url}")
        return
    for p in pList:
        content += p.text + '\n'
    with open(output_folder + '/' + name, 'w', encoding='utf-8') as f:
        f.write(content)



def b_url(url,output_folder):
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    data = resp.text
    bs = BeautifulSoup(data,"html.parser")                  #使用bs4分析网页数据
    ar_ul = bs.find('ul',attrs={'id':'list_1'})             #获得所有新闻标签的父标签ul对象
    articles = ar_ul.find_all('li')                         #在ul的基础之上再去获得其下的所有文章
    for li in articles:
        name = li.text + '.txt'
        h_url = li.a.get('href')
        print(h_url)
        b_txt(h_url,output_folder,name)


if __name__ == '__main__':

    output_folder = r"E:\studycode\py\pythonProject\爬虫\label"

    for i in range(30):
        if i == 0:
            url = url_q + '.htm'
        else:
            url = url_q + '/' + str(30-i) + '.htm'
        print(f'正在处理第 {i + 1} 页: {url}')

        b_url(url,output_folder)