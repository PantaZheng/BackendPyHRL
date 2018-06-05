from MongoDB import mongodb
from bson import json_util as jsonb
a=jsonb.dumps({"role":1,"name":2,"kkk":1})
print(a)
k=jsonb.loads(a)
print(k["role"])