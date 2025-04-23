import ollama
import os
import requests
import json





def c_txt(text):
    # 设置提示信息
    prompt = f"""
    请从以下内容中提取以下信息，如果内容中没有获奖相关信息，不对内容进行任何提取，只返回文字"没有获奖信息"：
    1. 比赛项目名称
    2. 参赛学生姓名
    3. 获得的奖项
    4. 指导老师姓名

    需要提取的内容如下：
    {text}
    """
    # 调用 Ollama 模型
    res = ollama.chat(
        model="llama3-cn",
        stream=False,
        messages=[{
            "role": "user",
            "content": prompt
        }],
        options={"temperature": 0}
    )

    result = res.message.content
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

    label_folder = './lable1'

    d_txt(label_folder)