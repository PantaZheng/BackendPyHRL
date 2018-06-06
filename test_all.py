from MongoDB import mongodb
from bson import json_util as jsonb

db=mongodb.LabDB()
print(db.log_get_staff("111"))