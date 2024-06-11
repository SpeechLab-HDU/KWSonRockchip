import time

import pyaudio
import wave
import numpy as np


class StreamAudio():

    def callback(self, in_data, frame_count, time_inf, status):
        """
        :brief 非阻塞模式回调函数
        """
        # 记录最近8个chunk的语音
        del self.record_buffer[0]
        self.record_buffer.append(in_data)

        # 将每个chunk写入文件
        self.wf.writeframes(in_data)

        self.embedded_func(in_data)
        return in_data, pyaudio.paContinue

    def __init__(self, embedded_func=None, Format=pyaudio.paInt16, channels=1, rate=16000, chunk=1024, buffer_chunk=8):
        """
        :brief 初始化
        :param embedded_func:绑定的中断服务函数
        :param Format:数据保存格式
        :param channels:录音通道数
        :param rate:录音采样率
        :param chunk:缓冲区块大小
        :param buffer_chunk:记录唤醒前buffer_chunk个chunk的音频
        """
        self.embedded_func = embedded_func
        self.format = Format
        self.chunk = chunk
        self.channels = channels
        self.rate = rate
        self.record_buffer = [b''] * 8  # 录音缓冲区
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=Format,
                                  channels=channels,
                                  rate=rate,
                                  input=True,
                                  frames_per_buffer=chunk,
                                  stream_callback=self.callback)
        # 将运行时的所有音频写入此文件
        self.wf = wave.open('../logs/LongTimeRecord_' + time.ctime(), 'wb')
        self.wf.setnchannels(self.channels)
        self.wf.setsampwidth(self.p.get_sample_size(self.format))
        self.wf.setframerate(self.rate)
        self.stream.start_stream()

    def read(self):
        """
        :brief 读取数据
        :note 阻塞式调用
        :return numpy格式,chunk大小的数据
        """
        RawData = self.stream.read(self.chunk)
        npData = np.frombuffer(RawData, dtype=np.int16)
        return npData

    def stop(self):
        """
        :brief 停止录音
        """
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.wf.close()

    def save_log(self, index, score):
        """
        :brief 记录唤醒音频
        """
        wf = wave.open('../logs/' + time.ctime() + ', index: %d, ' % index + 'scroe: %.4f' % score, 'wb')  # 保存
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.record_buffer))  # 把record_buffer中的音频保存到文件
        wf.close()
