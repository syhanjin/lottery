from pandas import read_excel
import os
from . import prpc

listroot = os.path.join('.', 'html', 'lists')
listjs = os.path.join(listroot, 'list.js')


def load(fp: str):
    # 读取名单
    df = read_excel(fp)
    # 提取学号后两位数字
    df['学号'] = df['学号'].str[-2:]
    # 构建名单文件夹
    if not os.path.exists(listroot):
        os.makedirs(listroot)
    # 构建名单文件
    if not os.path.exists(listjs):
        with open(listjs, 'w') as f:
            f.write('window.name_lists = {}\n')
    # 构建json
    l = '''{\n  "data": [\n'''
    for i, row in df.iterrows():
        l += f'''    {{"number": "{row["学号"]}", "name": "{row["姓名"]}"}},\n'''
    l = l[:-2] + '\n'
    l += '  ]\n}\n'
    # AES-ECB 加密
    l = prpc.encrypt(l).decode('utf-8')
    # 输出到文件
    with open(
        os.path.join(
            listjs
        ), 'a+', encoding='utf-8'
    ) as f:
        fn = fp.rsplit('/', 1)[1]
        f.write(f'''\nwindow.name_lists["{fn}"] = `{l}`''')
