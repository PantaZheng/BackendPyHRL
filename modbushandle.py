#!/usr/bin/env python
#coding:utf-8

import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp

master = modbus_tcp.TcpMaster("192.168.1.101", port=502)
master.set_timeout(5.0)
master.execute(1,cst.WRITE_SINGLE_COIL,1,output_value=True)# 实验开始置True
while True:
    label3=master.execute(1, cst.READ_COILS, 2, 1)[0]# 获取数据标记
    if label3==True:# 数据位已经写入数据
        res=master.execute(1,cst.READ_HOLDING_REGISTERS,10,2)[0]
        print(str(res)+"mm")
        break
master.execute(1,cst.WRITE_SINGLE_COIL,0,output_value=False)# 控制器关闭