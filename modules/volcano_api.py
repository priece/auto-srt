import json
import time
import uuid
import requests
import base64

class VolcanoEngineAPI:
    def __init__(self, app_id, access_key):
        """
        初始化火山引擎API客户端
        
        参数：
        app_id: 火山引擎应用ID
        access_key: 火山引擎访问密钥
        """
        self.app_id = app_id
        self.access_key = access_key
        # API请求URL
        self.submit_url = "https://openspeech-direct.zijieapi.com/api/v3/auc/bigmodel/submit"  # 提交任务URL
        self.query_url = "https://openspeech-direct.zijieapi.com/api/v3/auc/bigmodel/query"     # 查询任务URL
        self.resource_id = "volc.seedasr.auc"       # 资源ID
    
    def submit_transcription_task(self, audio_file_path):
        """
        提交音频文件转录任务到火山引擎API（使用极速版，直接上传base64音频数据）
        
        参数：
        audio_file_path: 本地音频文件路径
        
        返回：
        task_id: 任务ID，用于后续查询
        x_tt_logid: 请求日志ID，用于调试
        """
        # 生成唯一任务ID
        task_id = str(uuid.uuid4())
        
        # 读取音频文件并转换为base64编码
        print(f'正在读取音频文件: {audio_file_path}')
        with open(audio_file_path, 'rb') as f:
            audio_content = f.read()
            base64_audio = base64.b64encode(audio_content).decode('utf-8')
        
        print(f'音频文件大小: {len(audio_content)} 字节，Base64编码后大小: {len(base64_audio)} 字符')
        
        # 构建请求头，包含认证信息
        headers = {
            "X-Api-App-Key": self.app_id,                 # 应用ID
            "X-Api-Access-Key": self.access_key,           # 访问密钥
            "X-Api-Resource-Id": self.resource_id,       # 资源ID
            "X-Api-Request-Id": task_id,                   # 请求ID
            "X-Api-Sequence": "-1",                        # 请求序列号
            "Content-Type": "application/json"            # 指定内容类型为JSON
        }
        
        # 构建请求体（使用极速版API，直接上传base64数据）
        request_body = {
            "user": {
                "uid": "auto_srt_user"  # 用户ID，可自定义
            },
            "audio": {
                "data": base64_audio,                     # 音频文件的base64编码数据
                "format": "mp3",                         # 音频格式，根据实际文件类型调整
                "sample_rate": 16000,                     # 采样率，默认16000
                "channel": 1                              # 声道数，默认单声道
            },
            "request": {
                "model_name": "bigmodel",                   # 使用大模型
                "enable_channel_split": False,                # 启用声道分离
                "enable_ddc": True,                          # 启用深度断句
                "enable_speaker_info": False,                 # 启用说话人识别
                "enable_punc": True,                         # 启用标点符号
                "enable_itn": True                           # 启用数字转换
            }
        }
        
        print(f'正在提交转录任务，任务ID: {task_id}')
        # 发送POST请求提交任务
        response = requests.post(self.submit_url, data=json.dumps(request_body), headers=headers)
        
        # 打印完整响应JSON
        print(f'API响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}')
        
        # 检查响应状态
        if response.headers.get("X-Api-Status-Code") == "20000000":
            print('任务提交成功')
            x_tt_logid = response.headers.get("X-Tt-Logid", "")  # 获取日志ID
            return task_id, x_tt_logid
        else:
            print(f'任务提交失败。响应头: {response.headers}')
            return None, None
    
    def query_transcription_result(self, task_id, x_tt_logid):
        """
        轮询查询转录结果，直到任务完成或失败
        
        参数：
        task_id: 任务ID
        x_tt_logid: 请求日志ID
        
        返回：
        dict: 包含转录结果和token使用量的字典
              - transcription_result: 转录结果的JSON数据
              - token_stats: token使用量统计信息（包含input_tokens, output_tokens, total_tokens）
        """
        # 构建查询请求头
        headers = {
            "X-Api-App-Key": self.app_id,
            "X-Api-Access-Key": self.access_key,
            "X-Api-Resource-Id": self.resource_id,
            "X-Api-Request-Id": task_id,
            "X-Tt-Logid": x_tt_logid  # 固定传递日志ID
        }
        
        # 循环查询直到任务完成
        while True:
            # 发送查询请求
            response = requests.post(self.query_url, json.dumps({}), headers=headers)
            
            # 打印完整响应JSON
            print(f'查询响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}')
            
            # 获取状态码
            code = response.headers.get('X-Api-Status-Code', "")
            
            if code == '20000000':  # 任务已完成
                print('转录完成成功')
                result = response.json()
                
                # 提取token使用量信息（根据火山引擎API的实际响应结构调整）
                token_stats = {
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "total_tokens": 0
                }
                
                # 尝试从不同可能的位置获取token信息
                if 'usage' in result:
                    token_stats['input_tokens'] = result['usage'].get('input_tokens', 0)
                    token_stats['output_tokens'] = result['usage'].get('output_tokens', 0)
                    token_stats['total_tokens'] = result['usage'].get('total_tokens', 0)
                elif 'metadata' in result:
                    token_stats['input_tokens'] = result['metadata'].get('input_tokens', 0)
                    token_stats['output_tokens'] = result['metadata'].get('output_tokens', 0)
                    token_stats['total_tokens'] = result['metadata'].get('total_tokens', 0)
                elif 'stats' in result:
                    token_stats['input_tokens'] = result['stats'].get('input_tokens', 0)
                    token_stats['output_tokens'] = result['stats'].get('output_tokens', 0)
                    token_stats['total_tokens'] = result['stats'].get('total_tokens', 0)
                elif 'result' in result and isinstance(result['result'], dict):
                    # 尝试从result字段中获取
                    result_dict = result['result']
                    token_stats['input_tokens'] = result_dict.get('input_tokens', 0)
                    token_stats['output_tokens'] = result_dict.get('output_tokens', 0)
                    token_stats['total_tokens'] = result_dict.get('total_tokens', 0)
                
                # 返回包含转录结果和token统计的完整信息
                return {
                    "transcription_result": result,
                    "token_stats": token_stats
                }
            elif code != '20000001' and code != '20000002':  # 任务失败
                print(f'转录失败。状态码: {code}')
                print(f'响应: {response.text}')
                return None
            
            # 任务仍在处理中，等待3秒后再次查询
            print('转录中...')
            time.sleep(3)