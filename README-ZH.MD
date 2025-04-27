# 简介

本项目开发了一个简易的日语50音练习程序

它会随机生成平假名/片假名，并要求你输入对应的的片假名/平假名

并实时统计正确率与用时

# 使用方法

## 安装python包

```shell
pip install -r requirements.txt
```

或

```
pip install Flask==3.1.0
```
## 运行

有两种模式，控制台模式和网页模式，二选一运行即可

### 命令行模式

```shell
python src/hiragana_katakana_trainer_terminal.py
```

### 网页模式（推荐）

```shell
python app.py
```
然后浏览网页

localhost:5000
# 截图

![image-20230322161141744](src/app.png)

