from pandas import read_excel
import os
import datetime
from . import prpc

listroot = os.path.join('.', 'html', 'lists')
listjs = os.path.join(listroot, 'list.js')


def load(fp: str):
    df = read_excel(fp)
    df['学号'] = df['学号'].str[-2:]
    if not os.path.exists(listroot):
        os.makedirs(listroot)
    if not os.path.exists(listjs):
        with open(listjs, 'w') as f:
            f.write('window.name_lists = {}\n')

    l = '''{\n  "data": [\n'''
    for i, row in df.iterrows():
        l += f'''    {{"number": "{row["学号"]}", "name": "{row["姓名"]}"}},\n'''
    l = l[:-2] + '\n'
    l += '  ]\n}\n'
    l = prpc.encrypt(l).decode('utf-8')
    # print(l)
    # return
    with open(
        os.path.join(
            # f'{datetime.datetime.now().__format__("%Y-%m-%d-%H-%M-%S")}.js'
            listjs
        ), 'a+', encoding='utf-8'
    ) as f:
        fn = fp.rsplit('/', 1)[1]
        f.write(f'''\nwindow.name_lists["{fn}"] = `{l}`''')
    # with open(
    #     os.path.join(
    #         # f'{datetime.datetime.now().__format__("%Y-%m-%d-%H-%M-%S")}.js'
    #         listjs
    #     ), 'a+', encoding='utf-8'
    # ) as f:
    #     fn = fp.rsplit('/', 1)[1]
    #     f.write(f'''\nwindow.name_lists["{fn}"] = [\n''')
    #     for i, row in df.iterrows():
    #         f.write(
    #             f'''    {{'number': {row['学号']}, 'name': "{row['姓名']}"}},\n'''
    #         )
