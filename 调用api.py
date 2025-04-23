import os

import requests
import json


def get_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """

    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=y0CDJajGkU1HT619wm8ZR1pk&client_secret=zpTnVj5ic3XnyZT9RHArv1iwi5M1snKm"

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


def c_txt(text):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + get_access_token()

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": f"从以下内容中提取比赛项目，参赛学生，获得奖项，指导老师等信息，有多个获奖等级请保留，如果以下内容不是获奖有关内容不进行任何提取直接返回一个None,不要注释：\n{text}"
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.text
    # 解析 JSON 数据
    parsed_data = json.loads(data)
    # 提取 result 字段中的文字
    result = parsed_data.get('result', '')
    # print(result)
    return result

def d_txt(label_folder):
    # 确保提供的路径是一个目录
    if not os.path.isdir(label_folder):
        print(f"{label_folder} 不是有效的目录")
        return

    # 遍历文件夹中的所有文件
    for filename in os.listdir(label_folder):
        file_path = os.path.join(label_folder, filename)

        # 只处理以 .txt 结尾的文件
        if os.path.isfile(file_path) and filename.endswith('.txt'):
            try:
                with open(file_path, 'r+', encoding='utf-8') as file:
                    # 读取文件内容
                    print(f"正在处理文件: {filename}")
                    text = file.read()
                    content = c_txt(text)
                    file.write("\n\n")
                    file.write(content)
                    print("处理完成")
                    # print(text)
                    # print("="*50)  # 用于分隔文件内容
            except Exception as e:
                print(f"无法读取文件 {filename}: {e}")
        else:
            continue


if __name__ == '__main__':

    label_folder = 'E:/studycode/py/pythonProject/爬虫/label'

    d_txt(label_folder)