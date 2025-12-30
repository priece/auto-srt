import subprocess

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
            
        # 构建FFmpeg命令行参数
        # -i: 输入文件
        # -vn: 禁用视频流（只提取音频）
        # -acodec libmp3lame: 使用MP3编码器
        # -q:a 2: 设置音频质量（0-9，0为最高质量）
        # -ac 1: 将音频转换为单声道
        # -y: 自动覆盖输出文件，避免交互式确认
        command = [
            'ffmpeg',
            '-i', video_path,
            '-vn',
            '-acodec', 'libmp3lame',
            '-q:a', '2',
            '-ac', '1',  # 转换为单声道音频
            '-y',  # 自动覆盖输出文件
            audio_output_path
        ]
        
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