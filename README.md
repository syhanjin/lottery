# lottery

## 使用

请先构建环境并安装依赖

```shell
conda create -n lottery python=3.8 -y
conda activate lottery
pip install -r requirements.txt
```

## [打包](pyinstaller.md)

## 更新日志

### 0.2.4
1. 对随机算法进行了一定修改，如果滚动时间不同，一般不会出现重复
2. 对抽号主窗口添加互斥对象，只能开启一个

### 0.2.3

1. 增加一个小悬浮图标，在任何时候都可以方便打开抽号器

### 0.2.2

### 0.2.1

1. 使用AES-ECB加密本地名单文件，防止有些同学乱改

### 0.1.2

1. 修复末尾数取不到的问题
2. 将学号模式设为默认

### 0.1.1
