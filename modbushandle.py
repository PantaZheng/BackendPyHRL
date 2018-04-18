#!/usr/bin/env python
#coding:utf-8

import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp

'''设备-hostip映射表'''
device_host={
    1:"192.168.1.101",
    2:"192.168.1.102",
    3:"192.168.1.103",
    4:"192.168.1.104"
}


def Master(device,function_code,starting_address,quantity_x):
    master = modbus_tcp.TcpMaster(device_host[device], port=502)
    '''slave强制设定为1'''
    return master.execute(1, function_code, starting_address, quantity_x)