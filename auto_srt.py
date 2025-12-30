# 导入所需模块和类
import os           # 用于文件路径操作
from dotenv import load_dotenv  # 用于加载环境变量

# 从modules包中导入所需类
from modules import AudioExtractor
from modules import VolcanoEngineAPI
from modules import SRTGenerator

# 加载.env文件中的环境变量
load_dotenv()

# 从环境变量中获取火山引擎API凭证
APP_ID = os.getenv('APP_ID')           # 应用ID
ACCESS_KEY = os.getenv('ACCESS_KEY')   # 访问密钥

# 主函数
def main():
    import sys  # 导入sys模块用于处理命令行参数
    
    # 检查是否运行在模拟模式
    # 模拟模式：不调用实际API，使用模拟数据生成SRT
    mock_mode = '--mock' in sys.argv or '-m' in sys.argv
    
    # 检查API凭证是否设置（非模拟模式下）
    if not mock_mode and (not APP_ID or not ACCESS_KEY):
        print("错误: APP_ID和ACCESS_KEY必须在.env文件中设置")
        return
    
    # 定义输入输出文件路径
    video_path = './data/sample.mp4'   # 输入视频文件路径
    audio_path = './data/sample.mp3'   # 提取的音频文件路径
    srt_path = './data/sample.srt'     # 生成的SRT文件路径
    
    if mock_mode:
        print("运行在模拟模式...")
        # 模拟音频提取过程
        print(f"模拟: 从 {video_path} 提取音频到 {audio_path}...")
        print("模拟: 音频提取成功完成。")
        
        # 使用模拟转录结果
        mock_transcription = {
            "segments": [
                {"start": 0.0, "end": 2.0, "text": "这是第一段测试字幕。"},
                {"start": 2.0, "end": 5.0, "text": "这是第二段测试字幕，用于演示SRT生成功能。"},
                {"start": 5.0, "end": 8.0, "text": "这是第三段测试字幕，包含多行内容。"}
            ]
        }
        
        # 模拟token统计信息
        mock_token_stats = {
            "input_tokens": 150,
            "output_tokens": 100,
            "total_tokens": 250
        }
        
        # 生成SRT文件
        SRTGenerator.generate_srt(mock_transcription, srt_path)
        
        # 打印模拟的token使用量信息
        print(f"\n=== Token使用量统计 ===")
        print(f"输入token: {mock_token_stats['input_tokens']}")
        print(f"输出token: {mock_token_stats['output_tokens']}")
        print(f"总token: {mock_token_stats['total_tokens']}")
    else:
        # 步骤1: 从视频中提取音频
        extractor = AudioExtractor()
        if not extractor.extract_audio(video_path, audio_path):
            return  # 音频提取失败，退出程序
        
        # 步骤3: 初始化API客户端并提交转录任务（直接上传本地音频文件）
        api = VolcanoEngineAPI(APP_ID, ACCESS_KEY)
        task_id, x_tt_logid = api.submit_transcription_task(audio_path)
        
        if not task_id:
            print("提交转录任务失败")
            return  # 任务提交失败，退出程序
        
        # 步骤4: 轮询获取转录结果
        result_dict = api.query_transcription_result(task_id, x_tt_logid)
        
        if not result_dict:
            print("获取转录结果失败")
            return
        
        # 提取转录结果和token统计信息
        transcription_result = result_dict['transcription_result']
        token_stats = result_dict['token_stats']
        
        # 步骤5: 生成SRT文件
        SRTGenerator.generate_srt(transcription_result, srt_path)
        
        # 打印token使用量信息
        print(f"\n=== Token使用量统计 ===")
        print(f"输入token: {token_stats['input_tokens']}")
        print(f"输出token: {token_stats['output_tokens']}")
        print(f"总token: {token_stats['total_tokens']}")
    
    # 输出完成信息
    print("\n=== 所有任务成功完成！ ===")
    print(f"视频文件: {video_path}")
    print(f"音频文件: {audio_path}")
    print(f"字幕文件: {srt_path}")
    print(f"\n查看SRT文件: {srt_path}")

# 程序入口点
if __name__ == "__main__":
    main()  # 调用主函数