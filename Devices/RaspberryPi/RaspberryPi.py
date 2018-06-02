#-*- coding:utf-8 -*-

import os
import paramiko
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp

def transport(ip, document_name):

    slave = paramiko.Transport(ip, 22)
    slave.connect(username='pi', password='52sunsiyi..')
    sftp=paramiko.SFTPClient.from_transport(slave)
    # 需要修改device
    #sftp.put(os.path.abspath('.') +"\\"+RaspberryPi\\" + document_name, "/home/pi/Files/"+document_name)# 传输文件
    slave.close()
    return document_name+"文件下载到从机成功！"

def start(ip,document_name):
    ssh=paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
    ssh.connect(hostname=ip,port=22,username='pi',password='52sunsiyi..')
    ssh.exec_command("sudo nohup python /home/pi/Files/"+document_name)
    ssh.close()
    return document_name+"文件启动"

def order(ip,function_code,ss,qx):
    master = modbus_tcp.TcpMaster(ip, port=502)
    master.set_timeout(5.0)
    master.execute(1, cst.WRITE_SINGLE_COIL, 1, output_value=True)  # 实验开始置True
    while True:
        label3 = master.execute(1, cst.READ_COILS, 2, 1)[0]  # 获取数据标记
        if label3 == True:  # 数据位已经写入数据
            break
    return master.execute(1, function_code, starting_address=ss, quantity_of_x=qx)# 获取数据

def stop(ip):
    master = modbus_tcp.TcpMaster(ip, port=502)
    master.set_timeout(5.0)
    a=master.execute(1, cst.WRITE_SINGLE_COIL, 0, output_value=False)  # 控制器从机关闭
    return str(a)+"从机关闭"