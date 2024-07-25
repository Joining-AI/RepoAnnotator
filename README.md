# 🔧 RepoAnnotator

[![Official Website](https://img.shields.io/badge/Official%20Website-sjtujoining.com-blue?style=for-the-badge&logo=world&logoColor=white)](https://sjtujoining.com)

[![GitHub Repo stars](https://img.shields.io/github/stars/Joining-AI/RepoAnnotator?style=social)](https://github.com/Joining-AI/RepoAnnotator)

## 快速开始

> **步骤 0** - 安装 Python 3.11 或更高版本。[参见此处](https://www.tutorialsteacher.com/python/install-python) 获取详细指南。

<br />

> **步骤 1** - 下载项目

```bash
$ git clone https://github.com/Joining-AI/RepoAnnotator.git
$ cd RepoAnnotator
```

<br />

> **步骤 2** - 安装依赖项

```bash
$ pip install -r requirements.txt
```

<br />

> **步骤 3** - 使用 API 密钥创建 `.env` 文件

在项目根目录下创建 `.env` 文件，并填入以下内容：

```
QWEN_API=
```

将对应的 API 密钥填入等号右侧。

<br />

> **步骤 4** - 指定项目信息并导入类

```python
root_folder = r"D:\Joining\mem0-main\mem0-main"
new_root_folder = r'mem0'
exclude_list=[r'D:\Joining\mem0-main\mem0-main\.github']
from Applications.RepoAnnotator import RepoAnnotator
```
将 `root_folder` 替换为你的项目根目录路径，`new_root_folder` 替换为翻译后文件的目标文件夹路径，`exclude_list` 中填入你想要排除的目录或文件路径。
<br />

> **步骤 5** - 处理项目

```python
RepoAnnotator.run(root_folder, new_root_folder, exclude_list)
```
直接运行 `ipynb` 文件即可。

<br />


## ✉️ 支持 / 联系我们

- [社区讨论区](https://discord.gg/spBgZmm3Xe)
- 我们的邮箱: inuyasha2023ch@gmail.com

## 🛡 免责声明

本项目 "RepoAnnotator "是一个实验性应用程序，按 "现状 "提供，不做任何明示或暗示的保证。我们根据 MIT 许可分享用于学术目的的代码。本文不提供任何学术建议，也不建议在学术或研究论文中使用。

---

<p align="center">
<a href="https://star-history.com/#Joining-AI/RepoAnnotator">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=Joining-AI/RepoAnnotator&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=Joining-AI/RepoAnnotator&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=Joining-AI/RepoAnnotator&type=Date" />
  </picture>
</a>
</p>

---
