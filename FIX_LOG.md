# FIX_LOG

#### requirements_fixed.txt 

1. 删除错误或不需要的包：

`request` → 删除

`tdqm` → 改为 `tqdm`

`huggingface` → 删除

`tensorflow` → 删除

2. 过旧版本：

`openai==0.27.0` → `openai>=1.0.0`

`python-dotenv==0.1.0` → `python-dotenv>=1.0.0`

3. 添加缺失的包：

`tenacity>=8.2.0`

4. 保留并确保正确版本：

`pandas>=2.0.0`

`tqdm>=4.65.0`

---

#### translator_legacy_fixed.py 

1. 更新 API 接口

2. 将 Token 硬编码改为使用 `python-dotenv` 从环境变量读取

3. 修改模型参数为 `temperature=0.3, max_tokens=2048`

4. 设计专业的学术翻译 Prompt

5. 文件写入方式错误，使用 `pandas` 的 `DataFrame` 统一管理和输出

6. 输入文件名错误，读取 `iccv2025.csv`

7. 睡眠时间设置为 `time.sleep(1)`

8. 翻译标题和摘要

9. 增加异常处理，进度显示，断点续传