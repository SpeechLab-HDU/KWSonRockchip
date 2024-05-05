#!/bin/bash

#找到es8388音频输出设备所在行号
card_line=$(pacmd list-sinks | grep -n "name:.*es8388" | cut -d ':' -f 1)
((card_line--))
#提取es8388音频输出设备索引号
card_index=$(pacmd list-sinks | head -n $card_line | tail -1 | cut -d ':' -f 2)
#切换es8388为默认音频输出设备
pacmd set-default-sink $card_index

#设置为最大音量
pacmd set-sink-volume $card_index 65535

#运行python脚本
/usr/bin/python3 /home/liuhaoqi/PycharmProjects/wekws-main/wekws/stream_kws_ctc_tst.py --config /home/liuhaoqi/PycharmProjects/wekws-main/configs/config.yaml --checkpoint /home/liuhaoqi/PycharmProjects/wekws-main/configs/avg_30.pt --lexicon_file /home/liuhaoqi/PycharmProjects/wekws-main/configs/lexicon.txt --keywords 我要上楼,我要下楼,我要去负一楼,我要去一楼,我要去二楼,我要去三楼,我要去四楼,我要去五楼,电梯关门,电梯开门 --token_file /home/liuhaoqi/PycharmProjects/wekws-main/configs/tokens.txt --threshold 0.0
