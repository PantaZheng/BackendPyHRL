#!/usr/bin/env python
#coding:utf-8

import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp

def Master(device_ip,function_code,starting_address,quantity_x):
    master = modbus_tcp.TcpMaster(device_ip, port=502)
    master.set_timeout(5.0)
    # slave强制设定为1，
    res=master.execute(1, cst[function_code], starting_address, quantity_x)
    return