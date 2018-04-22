#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
import RPi.GPIO as gpio
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus as modbus
import modbus_tk.modbus_tcp as modbus_tcp
LOGGER = modbus_tk.utils.create_logger(name="console", record_format="%(message)s")

# 测距函数
def dis():
    gpio.output(gpio_trigger, gpio.HIGH)  # 设置trigger为低电平
    time.sleep(0.000015)
    gpio.output(gpio_trigger, gpio.LOW)  # 设置trigger为高电平
    # 等待echo高电平输入开始计时
    while not gpio.input(gpio_echo):
        pass
    start = time.time()
    while gpio.input(gpio_echo):
        pass
    # 高电平结束停止计时
    stop = time.time()

    elapsed = stop - start  # 计算一共花费多长时间
    distance = int(elapsed * 171500)  # 计算距离，就是时间乘以声速/2
    print distance
    return distance    ## 返回单位为mm， 取整


if __name__=="__main__":
    # 引脚设置
    # 使用BCM编码方式
    gpio.setmode(gpio.BCM)
    # 定义引脚，使用bcm模式的2、3引脚
    gpio_trigger = 2
    gpio_echo = 3
    gpio.setwarnings(False)  # warnings忽略
    gpio.setup(gpio_trigger, gpio.OUT)  # Trigger引脚为输出
    gpio.setup(gpio_echo, gpio.IN)  # Echo引脚为输入

    # modbus从机初始设置
    # server里的address需要写的树莓派的IP和需要开放的端口，注意开放相应的端口
    try:
        server = modbus_tcp.TcpServer(port=502)
        server.start()
        slave1 = server.add_slave(1)# 建立树莓派从机1
        slave1.add_block('A', cst.COILS, 0,3)# 添加A区块，起始位置为0，3个线圈开关：控制器、实验、数据
        slave1.set_values('A', 0, [True, False, False]) # 控制器开关开启，实验开关关闭，数据开关关闭
        slave1.add_block('B',cst.HOLDING_REGISTERS,10,100)# 添加B区块，起始位置为10，100个寄存器
    except modbus_tk.modbus.ModbusError, err:
        LOGGER.error("%s- Code=%d" % (err, err.get_exception_code()))
    print "start"

    # 等待连接
    while True:
        coils=slave1.get_values('A',0,3)# 获取三个线圈开关的值
        if coils[0] :# 控制器开关开启，可以开启实验
            if coils[1] :  # 执行实验开关
                slave1.set_values('B', 10, dis())  # 寄存器在位置10存储距离数据
                slave1.set_values('A', 2, True)  # 数据开关打开
                slave1.set_values('A', 1, False)#实验关闭
        else: # 控制器开关关闭
            print "stop"
            server.stop()   # 关闭从机
            gpio.cleanup()  # 清除引脚信息
            break
