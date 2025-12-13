# PaperTranslator

一个学术论文标题和摘要批量翻译脚本，输入为 ICCV 2025 论文数据，基于BuggyPaperTranslator修复，支持断点续传，实时进度显示。


## 环境要求

1. Python >= 3.8


## 安装步骤

1. 克隆项目到本地
```bash
git clone https://github.com/hxxs968/PaperTranslator.git
cd PaperTranslator
```

2. 安装依赖包：
```bash
pip install -r requirements_fixed.txt
```

3. 配置环境变量：

创建 `.env` 文件并添加你的Hugging Face Token
```
HF_TOKEN=your_huggingface_token_here
```

## 使用方法

1. 运行翻译脚本：
```bash
python translator_legacy_fixed.py
```

## 文件说明
- translator_legacy.py：原脚本
- translator_legacy_fixed.py 修复后脚本
- requirements.txt：原依赖文件
- requirements_fixed.txt：修复后依赖文件
- iccv2025.csv：输入文件
- result.csv：输出文件
- example_result.csv：输出样例文件
- FIX_LOG.md：修复记录


## 注意事项

- 请确保 API Key 有足够的配额
- 翻译过程中请保持网络连接稳定
- 支持中断后继续翻译
