# 视频自动字幕生成系统

## 项目概述

这是一个基于Python的视频自动字幕生成系统，通过以下步骤实现字幕创建：
1. 从视频文件中提取音频
2. 调用火山引擎大模型音频转录API
3. 自动生成标准SRT格式字幕文件

## 需求说明

- **输入**：视频文件，路径：`./data/sample.mp4`
- **输出**：字幕文件，保存路径：`./data/sample.srt`
- **实现语言**：Python
- **核心功能**：视频音频提取 + 火山引擎API调用 + SRT字幕生成
- **API凭证**：从`.env`文件读取火山引擎API Key和Access Key

## 技术栈

- **Python 3.x**
- **FFmpeg**：用于视频音频提取
- **Python依赖库**：
  - `python-dotenv`：环境变量管理
  - `requests`：HTTP请求处理
- **火山引擎大模型音频转录API**：用于音频转文本

## 安装步骤

1. **克隆或下载项目**
   ```bash
   cd e:\project_py\auto_srt
   ```

2. **安装Python依赖**
   ```bash
   pip install python-dotenv requests
   ```

3. **安装FFmpeg**
   - Windows：下载FFmpeg并添加到系统PATH
   - macOS：`brew install ffmpeg`
   - Linux：`sudo apt-get install ffmpeg`

## 配置

1. **创建并配置.env文件**
   ```bash
   cp .env.example .env  # 如果有示例文件
   ```
   编辑`.env`文件并填写火山引擎API凭证：
   ```env
   # 火山引擎API凭证
   APP_ID=your_app_id_here
   ACCESS_KEY=your_access_key_here
   ```

2. **准备视频文件**
   将需要生成字幕的视频文件命名为`sample.mp4`，并放置在`./data/`目录下

## 使用方法

### 1. 完整模式（需要FFmpeg和API凭证）

```bash
python auto_srt.py
```

### 2. 模拟模式（不需要FFmpeg和API调用，用于测试）

```bash
python auto_srt.py --mock
# 或
python auto_srt.py -m
```

模拟模式生成示例SRT文件，用于验证字幕格式和流程

## 项目结构

```
auto_srt/
├── auto_srt.py          # 主程序入口，控制整体流程
├── README.md            # 项目文档（英文）
├── README_zh.md         # 项目文档（中文）
├── .env                 # 环境变量配置文件
├── data/                # 数据目录
│   ├── sample.mp4       # 输入视频文件
│   ├── sample.mp3       # 提取的音频文件
│   └── sample.srt       # 生成的字幕文件
├── modules/             # 核心功能模块
│   ├── __init__.py      # 包初始化文件
│   ├── audio_extractor.py  # 音频提取模块
│   ├── volcano_api.py     # 火山引擎API交互模块
│   └── srt_generator.py   # SRT字幕生成模块
└── auc_python/          # 火山引擎API示例代码（可选）
    ├── auc_websocket_demo.py
    └── readme.md
```

## 工作流程

1. **音频提取**：使用FFmpeg从视频中提取音频，保存为MP3格式，并自动转换为单声道
2. **API调用**（使用火山引擎极速版API）：
   - 直接读取本地音频文件并转换为Base64编码
   - 调用火山引擎API提交音频转录任务，直接上传Base64数据
   - 轮询API获取转录结果，直到任务完成
   - 提取转录文本和对应的时间戳信息
3. **SRT生成**：将API响应的转录结果转换为标准SRT格式字幕文件，包含正确的时间戳和文本内容
4. **结果输出**：打印Token使用统计（输入Token、输出Token、总Token），并显示生成的字幕文件路径

## 核心模块说明

### AudioExtractor类
- 检查系统中是否安装FFmpeg
- 使用FFmpeg从视频中提取音频

### VolcanoEngineAPI类
- 处理与火山引擎API的交互
- 提交音频转录任务
- 轮询获取转录结果

### SRTGenerator类
- 将API响应转换为SRT格式
- 生成标准字幕文件

## 注意事项

1. **API调用方式**
   - 当前代码使用火山引擎极速版API，直接上传Base64编码的音频数据，无需云存储
   - 极速版API响应速度快于标准版API，但功能可能有限
   - API调用使用HTTPS协议，确保数据传输安全

2. **时间戳处理**
   - 系统已修复SRT文件中第一句字幕时间戳错误的问题
   - 火山引擎API返回的时间戳单位为毫秒，代码直接使用该时间戳生成SRT格式
   - 时间戳格式：`HH:MM:SS,mmm`（例如：`00:00:00,290`表示0小时0分钟0秒290毫秒）

3. **API凭证**
   - 确保`.env`文件中的APP_ID和ACCESS_KEY有效
   - 凭证可从火山引擎控制台获取
   - 可使用模拟模式（`--mock`或`-m`参数）在没有有效凭证的情况下测试功能

4. **FFmpeg依赖**
   - 完整模式下必须安装FFmpeg
   - 可通过`ffmpeg -version`命令检查是否安装
   - 代码已处理Windows环境下FFmpeg执行后程序卡住的问题

5. **模拟模式**
   - 模拟模式仅用于测试SRT生成功能和程序流程
   - 生成的字幕内容是固定示例，不是真实视频内容
   - 模拟模式会模拟Token使用统计

6. **音频处理**
   - 代码默认将提取的音频转换为**单声道**，避免双声道导致的字幕重复
   - 如果火山引擎API接收双声道音频，会出现两个声道的字幕
   - 可通过修改`modules/audio_extractor.py`中的`-ac`参数调整声道设置

7. **Token使用统计**
   - 程序会打印API调用的Token使用情况
   - 包括：输入Token、输出Token、总Token
   - Token使用量与音频时长和内容复杂度相关

## 示例输出

生成的SRT文件格式示例：
```srt
1
00:00:00,000 --> 00:00:02,000
这是第一句测试字幕。

2
00:00:02,000 --> 00:00:05,000
这是第二句测试字幕，用于演示SRT生成功能。

3
00:00:05,000 --> 00:00:08,000
这是第三句测试字幕，包含多行内容。
```

## 参考文档

- [火山引擎大模型音频转录API文档](https://www.volcengine.com/docs/6561/1354868)
- [FFmpeg官方文档](https://ffmpeg.org/documentation.html)
- [Python base64模块文档](https://docs.python.org/3/library/base64.html)
- [requests库官方文档](https://docs.python-requests.org/en/latest/)

## 更新日志

### [最新版本]
- **修复**：SRT文件中第一句字幕时间戳错误的问题（原错误时间戳如`00:04:50,000 --> 01:28:10,000`）
- **优化**：默认将音频提取为单声道，避免双声道导致的字幕重复
- **改进**：处理了Windows环境下FFmpeg执行后程序卡住的问题
- **新增**：打印Token使用统计（输入Token、输出Token、总Token）
- **升级**：使用火山引擎极速版API，直接上传Base64编码的音频数据，无需云存储
- **重构**：采用模块化设计，将代码分为音频提取、API调用、SRT生成三个核心模块

## 许可证

本项目仅供学习和参考使用。