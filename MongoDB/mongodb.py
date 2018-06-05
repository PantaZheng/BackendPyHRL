import pymongo
import csv
import os
from uuid import uuid4

class LabDB:
    """
    必须在程序目录下调用该文件，接口目录设置位于上层
    响应代码：
    200-正常响应
    """
    def __init__(self):
        self.client = pymongo.MongoClient()
        self.db=self.client.db
        self.staff=self.db.staff
        self.slaves=self.db.slaves
        self.log=self.db.log

    def close(self):
        self.client.close()

    #全部依据基础数据重构
    def all_rebuild(self):
        self.client.drop_database(self.db)
        self.staff_rebuild()
        self.slaves_rebuild()
        self.log_rebuild()


    '''staff-----------------------------------------------------------------'''
    def staff_rebuild(self,path=None):
        """
        人员信息重建
        依赖事件：
            path-人员csv文件地址，csv文件必须部署在MongoDB文件夹下，上层输入其
                文件名即可
        """
        if path is None:
            path= "school.csv"
        staff=self.staff
        staff.drop()
        with open("MongoDB\\"+path, encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                id = row[0]
                name = row[1]
                role = row[3]
                if role=="student" or role =="staff":
                    staff.insert_one({"id":id,"password":id,"role":role,
                                      "name":name,"token":uuid4()})
        print("人员数据库初始化为："+str(staff.count()))

    def login_check(self,id,password):
        staff=self.staff
        real_pwd=staff.find_one({"id":id})["password"]
        if real_pwd==password:
            token=uuid4()
            staff.update({"id":id},{"$set":{"token":token}})
            account_set=staff.find_one({"id":id})
            account_set.pop("_id")#删除_id
            account_set.pop("id")#删除id
            account_set.pop("password")#删除pwd
            return account_set

    def modify_password(self,id,token,password):
        staff = self.staff
        if self.token_check(id,token):
            staff.update({"id": id}, {"$set": {"password": password}})
            return 200

    def token_check(self,id,token):
        staff=self.staff
        if token!=staff.find_one({"id":id})["token"]:
            return False
        else:
            return True

    '''slaves----------------------------------------------------------------'''

    def slaves_rebuild(self):
        """
        对从机信息的重建
        依赖事件：
            Devices目录下的从机子文件夹
            子文件夹中的实验文件
            此函数下预设的设备ip表
        `   实验文件地址在server层重构，数据库中不建立文件地址
        """
        #设备映射表
        ipdir = {
            # "Arudino":[".??","192.168.1.101"],
            "CC3200": ["out","192.168.1.102"],
            "RaspberryPi": ["py","192.168.1.103"],
            # "STM32":["192.168.1.104"]
        }

        #抛弃数据库中从机表
        slaves = self.slaves
        slaves.drop()

        #数据建立
        kinds = next(os.walk('Devices'))[1]#获取目录中设备种类
        count=0
        for kind in kinds:
            if kind in ipdir.keys():#设备ip映射表中存在的设备才能继续读取实验文件
                #构建实验文件列表
                experiment_list=[]
                experiments=next(os.walk('Devices\\'+str(kind)))[2]#获取实验文件
                for experiment in experiments:
                    name,extension=experiment.split(".")#切割实验文件名
                    if ipdir[kind][0]==extension and name!="test":#略过用户测试文件
                        experiment_list.append({"name":name})
                #加入设备ip
                for ip in ipdir[kind][1:]:#设定id和IP
                    count += 1
                    slaves.insert({"id":count,"ip":ip,"kind":kind,
                                   "experiments":experiment_list,"state":False})
        print("从机数据库初始化为："+str(slaves.count()))

    def slave_update(self,slave_id):
        slaves = self.slaves
        slave_state=slaves.find_one({"id":slave_id})["state"]
        slaves.update({"id": slave_id}, {"$set": {"state": not slave_state}})

    '''log-------------------------------------------------------------------'''

    # 抛弃日志表
    def log_rebuild(self):
        log = self.log
        log.drop()
        print("日志数据库初始化为:"+str(log.count()))

    #websocket,选哟
    def log_insert(self,staff_id,slave_id,message):

            return


    def log_get_staff(self,token,staff_id,):
        if self.token_check(staff_id,token):

        else

    def log_get_device

    def log_get_alll


