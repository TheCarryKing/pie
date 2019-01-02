# -*-coding:utf-8-*-
import threading
from baidu_acu_asr.AsrClient import AsrClient
import os
from pyaudio import PyAudio, paInt16


# 产生流（mac上麦克风读取音频流，需要先brew install portaudio）
def record_micro():
    NUM_SAMPLES = 2560  # pyaudio内置缓冲大小
    SAMPLING_RATE = 8000  # 取样频率
    pa = PyAudio()
    stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE, input=True, frames_per_buffer=NUM_SAMPLES)
    # yield stream
    while True:
        yield client.generate_stream_request(stream.read(NUM_SAMPLES))


# 产生流（本地音频流）
def generate_file_stream():
    file_path = "/Users/xiashuai01/Downloads/10s.wav"
    if not os.path.exists(file_path):
        logging.info("%s file is not exist, please check it!", file_path)
        os._exit(-1)
    file = open(file_path, "r")
    content = file.read(2560)
    while len(content) > 0:
        yield client.generate_stream_request(content)
        content = file.read(2560)


def run():
    response = client.get_result("/Users/xiashuai01/Downloads/20181126_213030250_0003450587_19.in.wav")
    # response = client.get_result("/Users/xiashuai01/Downloads/20181126_213030250_0003450587_19.in.wav")
    for res in response:
        print("start_time\tend_time\tresult")
        print(res.start_time + "\t" + res.end_time + "\t" + res.result)


def run_stream():
    # responses = client.get_result_by_stream(generate_file_stream())
    responses = client.get_result_by_stream(record_micro())
    for response in responses:
        # for res in responses:
        print("start_time\tend_time\tresult")
        print(response.start_time + "\t" + response.end_time + "\t" + response.result + "\t" + response.serial_num)


if __name__ == '__main__':
    product_id = "1903"
    enable_flush_data = False
    client = AsrClient("180.76.107.131", "8050", product_id, enable_flush_data)
    # 传送文件
    # run()
    # 传送流
    run_stream()
    # 多线程运行
    # for i in range(100):
    #     print(i)
    #     t = threading.Thread(target=run, args=[])
    #     t.start()



