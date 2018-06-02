from MongoDB import Rebuild

list=Rebuild.slaves_rebuild()

for i in list:
    print(i)