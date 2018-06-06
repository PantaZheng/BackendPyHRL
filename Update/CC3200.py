from subprocess import Popen

def cc3200_update(loadti_path=None,ccxml_path=None,out_path=None):
    # 默认路劲设置
    if loadti_path is None:
            loadti_path="C:\\ti\\ccsv6\\ccs_base\\scripting\\examples\\loadti\\loadti.bat"
    if ccxml_path is None:
            ccxml_path="C:\\Users\\Raphael\\ti\\CCSTargetConfigurations\\CC3200.ccxml"
    if out_path is None:
            out_path="D:\\Backend_Python_HduRemoteLab\\CC3200\\distance.out"
    p=Popen([loadti_path,"-n","-c",ccxml_path,out_path])
    stdout, stderr = p.communicate()
