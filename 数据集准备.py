import os


def parse_labels(label_content):
    # 将标签部分按行分割，并提取成键值对
    label_data = {}
    for line in label_content.strip().split("\n"):
        if "：" in line:
            key, value = line.split("：", 1)
            label_data[key.strip()] = value.strip()
        else:
            print(f"Warning: Unexpected line format: {line}")
    return label_data


def load_txt_files(directory):
    data = []

    for file_name in os.listdir(directory):
        if file_name.endswith(".txt"):
            with open(os.path.join(directory, file_name), "r", encoding="utf-8") as file:
                content = file.read()

                # 将内容分为文本和标签部分
                if "\n\n" in content:
                    text, label_content = content.split("\n\n", 1)
                else:
                    # 如果没有标签部分，认为标签为空
                    text, label_content = content, ""

                # 判断标签是否为 'None'，如果是，设置标签为空字典
                if label_content.strip() == 'None':
                    label_data = {}
                else:
                    # 否则解析标签内容
                    label_data = parse_labels(label_content) if label_content else {}

                label_data["text"] = text.strip()

                # 将文件内容和提取的标签数据添加到数据列表
                data.append(label_data)

    return data


# 使用函数
directory = "E:/studycode/py/pythonProject/爬虫/ce"
data = load_txt_files(directory)
print(data)
# 打印结果
# for entry in data:
#     print(entry)
