#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
软件环境：python2.7，Raspbian
硬件环境：树莓派+HC-SR04超声波传感器
* 配置的Mo
"""

import time
import RPi.GPIO as gpio

# 使用BCM编码方式
gpio.setmode(gpio.BCM)

# 定义引脚，使用bcm模式的2、3引脚
gpio_trigger = 2
gpio_echo = 3

gpio.setwarnings(False)  # warnings忽略
gpio.setup(gpio_trigger, gpio.OUT)  # Trigger引脚为输出
gpio.setup(gpio_echo, gpio.IN)  # Echo引脚为输入
time.sleep(2)  # 延迟两秒后开始运行


'''测距函数'''


def dis():
    gpio.output(gpio_trigger, gpio.HIGH)  # 设置trigger为低电平
    time.sleep(0.000015)
    gpio.output(gpio_trigger, gpio.LOW)  # 设置trigger为高电平
    # 等待echo高电平输入开始计时
    while not gpio.input(gpio_echo):
        pass
    start = time.time()
    while gpio.input(gpio.Echo):
        pass
    # 高电平结束停止计时
    stop = time.time()

    elapsed = stop - start  # 计算一共花费多长时间
    distance = elapsed * 34000 / 2  # 计算距离，就是时间乘以声速/2
    print "Distance : %.1fcm" % distance


try:  # 用于捕捉异常
    while True:
        dis()  # 调用测距函数
        time.sleep(0.5)
except KeyboardInterrupt:
    gpio.cleanup()