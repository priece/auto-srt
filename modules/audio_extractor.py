import subprocess
import os

class AudioExtractor:
    @staticmethod
    def check_ffmpeg():
        """
        检查系统是否安装了FFmpeg
        """
        try:
            # 尝试执行ffmpeg命令，检查版本信息
            # 移除stdout和stderr的重定向，避免Windows下的缓冲问题
            subprocess.run(['ffmpeg', '-version'], check=True)
            return True  # FFmpeg已安装
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False  # FFmpeg未安装
    
    @staticmethod
    def extract_audio(video_path, audio_output_path):
        """
        使用FFmpeg从视频文件中提取音频
        
        参数：
        video_path: 视频文件路径
        audio_output_path: 提取后音频文件的输出路径
        """
        # 首先检查FFmpeg是否已安装
        if not AudioExtractor.check_ffmpeg():
            print("错误: ffmpeg未安装，请先安装ffmpeg。")
            return False
            
        # 根据输出文件扩展名选择编码器
        audio_extension = os.path.splitext(audio_output_path)[1].lower()
        
        # 构建FFmpeg命令行参数基础部分
        command = [
            'ffmpeg',
            '-i', video_path,
            '-vn',
            '-ac', '1',  # 转换为单声道音频
            '-y',  # 自动覆盖输出文件
        ]
        
        # 根据音频格式添加相应的编码器和质量参数
        if audio_extension == '.mp3':
            command.extend(['-acodec', 'libmp3lame', '-q:a', '2'])
        elif audio_extension == '.wav':
            command.extend(['-acodec', 'pcm_s16le'])  # WAV无损格式
        else:
            print(f"不支持的音频格式: {audio_extension}，默认使用MP3格式")
            command.extend(['-acodec', 'libmp3lame', '-q:a', '2'])
        
        # 添加输出文件路径
        command.append(audio_output_path)
        
        print(f"正在从 {video_path} 提取音频到 {audio_output_path}...")
        try:
            # 执行FFmpeg命令，不重定向输出，让FFmpeg直接输出到控制台
            # 移除stdout=subprocess.PIPE和stderr=subprocess.PIPE可以解决Windows下的缓冲问题
            subprocess.run(command, check=True)
            print("音频提取成功完成。")
            return True
        except subprocess.CalledProcessError as e:
            print(f"音频提取错误: {e}")
            return False