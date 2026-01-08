# 导入所需模块和类
import os           # 用于文件路径操作
import argparse     # 用于处理命令行参数
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
    import time  # 导入time模块用于统计运行时间
    
    # 记录开始时间
    start_time = time.time()
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='自动生成视频字幕工具')
    parser.add_argument('-a', '--audio-format', choices=['mp3', 'wav'], default='mp3', 
                        help='音频编码格式，支持mp3和wav，默认mp3')
    args = parser.parse_args()
    
    # 检查API凭证是否设置
    if not APP_ID or not ACCESS_KEY:
        print("错误: APP_ID和ACCESS_KEY必须在.env文件中设置")
        end_time = time.time()
        print(f"程序运行时间: {end_time - start_time:.2f}秒")
        return
    
    # 定义输入输出文件路径
    video_path = './data/sample.mp4'   # 输入视频文件路径
    audio_format = args.audio_format   # 根据命令行参数获取音频格式
    audio_path = f'./data/sample.{audio_format}'  # 提取的音频文件路径
    srt_path = './data/sample.srt'     # 生成的SRT文件路径
    
    # 步骤1: 从视频中提取音频
    extractor = AudioExtractor()
    if not extractor.extract_audio(video_path, audio_path):
        end_time = time.time()
        print(f"音频提取失败，程序运行时间: {end_time - start_time:.2f}秒")
        return  # 音频提取失败，退出程序
    
    # 步骤3: 初始化API客户端并提交转录任务（直接上传本地音频文件）
    api = VolcanoEngineAPI(APP_ID, ACCESS_KEY)
    task_id, x_tt_logid = api.submit_transcription_task(audio_path, audio_format)
    
    if not task_id:
        print("提交转录任务失败")
        end_time = time.time()
        print(f"程序运行时间: {end_time - start_time:.2f}秒")
        return  # 任务提交失败，退出程序
    
    # 步骤4: 轮询获取转录结果
    result_dict = api.query_transcription_result(task_id, x_tt_logid)
    
    if not result_dict:
        print("获取转录结果失败")
        end_time = time.time()
        print(f"程序运行时间: {end_time - start_time:.2f}秒")
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
    
    # 计算总耗时
    end_time = time.time()
    total_time = end_time - start_time
    
    # 输出完成信息
    print("\n=== 所有任务成功完成！ ===")
    print(f"视频文件: {video_path}")
    print(f"音频文件: {audio_path}")
    print(f"字幕文件: {srt_path}")
    print(f"总耗时: {total_time:.2f}秒")
    print(f"\n查看SRT文件: {srt_path}")

# 程序入口点
if __name__ == "__main__":
    main()  # 调用主函数