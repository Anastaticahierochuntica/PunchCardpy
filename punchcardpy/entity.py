# -*- coding: UTF-8 -*-

class People:
    """
    学生类
    """
    data = {}
    email = ''
    number = ''
    name = ''
    academy = ''
    clazz = ''
    addressnumber = ''
    address = ''
    status = ''

    def __init__(self, self_information):
        self.data = self_information
        self.email = self_information['email']
        self.number = self_information['number']
        self.name = self_information['name']
        self.academy = self_information['academy']
        self.clazz = self_information['clazz']
        self.addressnumber = self_information['addressnumber']
        self.address = self_information['province'] + self_information['city'] + self_information['country']
        self.status = self_information['status']
