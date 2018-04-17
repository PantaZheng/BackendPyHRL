#-*- coding:utf-8 -*-

import os
import paramiko




def transport(ip,docemnt_name):
    slave = paramiko.Transport(ip, 22)
    slave.connect(username='pi', password='52sunsiyi..')
    sftp=paramiko.SFTPClient.from_transport(slave)
    sftp.put(os.path.abspath('.')+"\\Raspi\\"+docemnt_name, "/home/pi/Files/default.py")
    slave.close()

    ssh=paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
    ssh.connect(hostname=ip,port=22,username='pi',password='52sunsiyi..')
    stdin, stdout, stderr =ssh.exec_command("python /home/pi/Files/default.py")
    res, err = stdout.read(), stderr.read()
    result = res if res else err
    ssh.close()

    return result.decode()

