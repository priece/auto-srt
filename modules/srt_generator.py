class SRTGenerator:
    @staticmethod
    def generate_srt(transcription_result, output_path):
        """
        根据转录结果生成SRT格式字幕文件
        
        参数：
        transcription_result: 音频转录结果（JSON格式）
        output_path: 生成的SRT文件保存路径
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            index = 1  # 字幕序号
            
            # 处理火山引擎API返回的结果格式
            if 'result' in transcription_result:
                # 处理API返回的字幕片段，优先检查utterances字段（火山引擎API实际返回的字段名）
                # 依次尝试utterances、sentences、segments字段
                segments = transcription_result['result'].get('utterances', [])
                if not segments:
                    segments = transcription_result['result'].get('sentences', [])
                    if not segments:
                        segments = transcription_result['result'].get('segments', [])
                
                # 过滤只保留一个声道的内容（默认channel_id为1）
                selected_channel = '1'  # 可以根据需要修改为其他声道
                filtered_segments = []
                
                for segment in segments:
                    # 检查是否有channel_id信息
                    channel_id = segment.get('additions', {}).get('channel_id', '1')
                    
                    # 只保留指定声道的内容
                    if channel_id == selected_channel:
                        filtered_segments.append(segment)
                
                for segment in filtered_segments:
                    # 兼容不同的时间字段名
                    start_time = segment.get('start_time', segment.get('start', 0))  # 开始时间
                    end_time = segment.get('end_time', segment.get('end', 0))        # 结束时间
                    text = segment.get('text', '')                                   # 文本内容
                    
                    # 调试：打印原始时间数据
                    print(f"原始时间数据 - 开始时间: {start_time}, 结束时间: {end_time}, 文本: {text}")
                    
                    # 确保时间单位是毫秒
                    # 检查start_time是否是字符串类型，如果是则转换为数字
                    if isinstance(start_time, str):
                        start_time = float(start_time)
                        end_time = float(end_time)
                    
                    # 火山引擎API返回的时间单位已经是毫秒，不需要转换
                    # 移除错误的时间单位转换逻辑，避免将毫秒误判为秒
                    if isinstance(start_time, float):
                        # 确保时间是整数毫秒
                        start_time = int(start_time)
                        end_time = int(end_time)
                    
                    # 转换为SRT格式时间
                    start_srt = SRTGenerator.format_time(start_time)
                    end_srt = SRTGenerator.format_time(end_time)
                    
                    # 写入SRT条目
                    f.write(f"{index}\n")                    # 序号
                    f.write(f"{start_srt} --> {end_srt}\n")   # 时间范围
                    f.write(f"{text}\n\n")                  # 文本内容
                    index += 1
            else:
                # 处理模拟数据格式（用于测试）
                for segment in transcription_result.get('segments', []):
                    # 模拟数据中时间单位为秒，需转换为毫秒
                    start_time = segment.get('start', 0) * 1000  # 开始时间（毫秒）
                    end_time = segment.get('end', 0) * 1000      # 结束时间（毫秒）
                    text = segment.get('text', '')               # 文本内容
                    
                    # 转换为SRT格式时间
                    start_srt = SRTGenerator.format_time(start_time)
                    end_srt = SRTGenerator.format_time(end_time)
                    
                    # 写入SRT条目
                    f.write(f"{index}\n")
                    f.write(f"{start_srt} --> {end_srt}\n")
                    f.write(f"{text}\n\n")
                    index += 1
            
        print(f"SRT文件已生成: {output_path}")
    
    @staticmethod
    def format_time(ms):
        """
        将毫秒转换为SRT格式时间
        SRT格式：HH:MM:SS,mmm
        
        参数：
        ms: 毫秒数
        
        返回：
        SRT格式的时间字符串
        """
        seconds = ms / 1000              # 转换为秒
        hours = int(seconds // 3600)     # 小时
        minutes = int((seconds % 3600) // 60)  # 分钟
        seconds = int(seconds % 60)      # 秒
        milliseconds = int((ms % 1000))  # 毫秒
        
        # 格式化为SRT时间格式
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"