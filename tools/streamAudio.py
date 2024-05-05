import time

import pyaudio
import wave
import numpy as np


class StreamAudio():

    def callback(self, in_data, frame_count, time_inf, status):
        """
        :brief 非阻塞模式回调函数
        """
        del self.record_buffer[0]
        self.record_buffer.append(in_data)
        self.embeded_func(in_data)
        return in_data, pyaudio.paContinue

    def __init__(self, embeded_func=None, Format=pyaudio.paInt16, channels=1, rate=16000, chunk=1024):
        """
        :brief 初始化
        :param embeded_func:绑定的中断服务函数
        :param Format:数据保存格式
        :param channels:录音通道数
        :param rate:录音采样率
        :param chunk:缓冲区块大小
        """
        self.embeded_func = embeded_func
        self.format = Format
        self.chunk = chunk
        self.channels = channels
        self.rate = rate
        self.record_buffer = [b''] * 8
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=Format,
                                  channels=channels,
                                  rate=rate,
                                  input=True,
                                  frames_per_buffer=chunk,
                                  stream_callback=self.callback)
        self.stream.start_stream()

    def read(self):
        """
        :brief 读取数据
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

    def save_log(self, index, score):
        wf = wave.open('../logs/' + time.ctime() + ', index: %d, ' % index + 'scroe: %.4f' % score, 'wb')  # 保存
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.record_buffer))
        wf.close()
