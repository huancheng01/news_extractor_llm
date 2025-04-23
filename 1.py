import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin


url_q = "https://ict.gdqy.edu.cn/xwdt1"


def clean_filename(name):
    """
    清理文件名中的非法字符
    """
    name = re.sub(r'[\/:*?"<>|]', '_', name)  # 替换非法字符为下划线
    name = name.replace('\n', ' ').strip()  # 移除换行符并去除两端空格
    return name


def b_txt(h_url, output_folder, name):
    content = ''
    base_url = 'https://ict.gdqy.edu.cn/'
    z_url = urljoin(base_url, h_url)  # 自动处理 ../ 和相对路径
    print(f"处理文章：{z_url}")
    try:
        resp = requests.get(z_url)
        resp.encoding = 'utf-8'
        data = resp.text
        bs = BeautifulSoup(data, "html.parser")

        # 查找目标内容，增加空值检查
        ul = bs.find('div', attrs={'class': 'v_news_content'})
        if ul is None:
            print(f"警告：未找到目标 ul 标签，URL: {z_url}")
            return

        # 使用正确的属性筛选方式
        pList = ul.find_all(['h2', 'p'], style=re.compile(r'.*text-indent.*|.*line-height.*'))
        if not pList:
            print(f"警告：未找到符合条件的段落标签，URL: {z_url}")
            return

        # 拼接内容
        for p in pList:
            content += p.text + '\n'

        # 清理文件名
        clean_name = clean_filename(name)

        # 保存内容到文件
        with open(output_folder + '/' + clean_name, 'w', encoding='utf-8') as f:
            f.write(content)
        # print(f"已保存内容到: {output_folder}/{clean_name}")

    except Exception as e:
        print(f"错误：处理 URL {z_url} 时出现问题，错误信息: {e}")


def b_url(url, output_folder):
    try:
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        data = resp.text
        bs = BeautifulSoup(data, "html.parser")  # 使用 bs4 分析网页数据

        # 查找文章列表，增加空值检查
        ar_ul = bs.find('ul', attrs={'id': 'list_1'})
        if ar_ul is None:
            print(f"警告：未找到文章列表 ul 标签，URL: {url}")
            return

        articles = ar_ul.find_all('li')  # 在 ul 的基础之上再去获得其下的所有文章
        if not articles:
            print(f"警告：未找到文章列表，URL: {url}")
            return

        # 处理每篇文章
        for li in articles:
            name = li.text.strip() + '.txt'  # 去除多余空格
            h_url = li.a.get('href')
            b_txt(h_url, output_folder, name)

    except Exception as e:
        print(f"错误：处理 URL {url} 时出现问题，错误信息: {e}")


if __name__ == '__main__':
    output_folder = "E:/studycode/py/pythonProject/爬虫/label"

    for i in range(30):
        if i == 0:
            url = url_q + '.htm'
        else:
            url = url_q + '/' + str(30 - i) + '.htm'
        print(f'正在处理第 {i + 1} 页: {url}')
        b_url(url, output_folder)
