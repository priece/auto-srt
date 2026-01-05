# 根据视频生成字幕
- 输入：视频文件，来自 ./data/sample.mp4
- 输出：字幕文件，保存到 ./data/sample.srt
- python实现
- 功能：根据输入的视频文件，先提取音频，再通过火山引擎接口调用，自动生成对应的字幕文件
- 火山引擎代码样例：./auc_python
- 火山引擎文档：https://www.volcengine.com/docs/6561/1354868?lang=zh , 内容为[大模型录音文件识别标准版API]
- 接口中支持audio.url 与 audio.data 二选一方式上传音频，audio.data用的是base64编码
- 需要api key和access key，从 .env文件中配置读取