#-*- coding: utf-8 -*-

from apps.oclib.model import BaseModel

class UserModel(BaseModel):
    pk = 'uid'
    fields = ['uid','data']
    def __init__(self):
        pass

    @classmethod
    def create(cls):
        um = UserModel()
        um.uid = '123456'
        um.data = {'a':1,'b':2}
        return um


def test_user_model():
    user = UserModel.create()
    user.put()
    uid = user.uid
    user1 = UserModel.get(uid)
    print user.uid == user1.uid


class Config(BaseModel):
    pk = 'config_name'
    fields = ['config_name','config_value']
    def __init__(self):
        pass

    @classmethod
    def create(cls,config_name,config_value):
        conf = Config()
        conf.config_name = config_name
        conf.config_value = config_value

def test_Config():
    conf = Config.create("card_config",{'a':0,'b':1})
    conf.put()


