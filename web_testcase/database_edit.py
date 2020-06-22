#! /usr/bin/env python
# -*- coding:utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 <guokunkun@dvt.dvt.com>
#

import configparser
from pymongo import MongoClient


class database:
    def __init__(self, user, passwd):
        # databaseIp = self.getConfig('database','ip')
        # databasePort = self.getConfig('database','port')
        # databaseUsername = self.getConfig('database','username')
        # databaseIp = "172.16.15.29"
        databaseIp = "192.166.168.29"
        port = 27017
        self.authRes = True
        '''
        count = 0
        while True:
            # python 默认连接超时时间是30秒，避免无法连接服务器时被卡住，设置为3ms
            client = MongoClient(databaseIp, port, serverSelectionTimeoutMS=3)

            try:
                self.client.admin.command("ping")
            except:
                print "Mongod connect exception!"
                count = count + 1
            else:
                print "connect mongod ok!"
                break
            if count == 3:
                print "Try 3 times, connect timeout!"
                break
        '''

        # python 默认连接超时时间是30秒，避免无法连接服务器时被卡住，设置为1200ms
        client = MongoClient(databaseIp, port, serverSelectionTimeoutMS=1200)
        # print client

        # 获取数据库version
        db = client.version
        # print  db

        # 认证
        # ret = db.authenticate(user, passwd)
        try:
            ret = db.authenticate(user, passwd)
        except:
            print("Mongod authenticate exception!")
            self.authRes = False
            print("self.authRes is %s" % self.authRes)
        else:
            print("Mongod authenticate success: %s" % ret)

        # 获取集合
        self.coll = db.cmts
        self.cmts = db.cmts
        self.cm = db.cm
        self.olt = db.olt
        self.git = db.git

    # print self.coll

    def getAuthResult(self):
        return self.authRes

    def getCollect(self, item):
        if item == "CCMTS":
            self.coll = self.cmts
        elif item == "CM":
            self.coll = self.cm
        elif item == "OLT":
            self.coll = self.olt
        elif item == "GIT":
            self.coll = self.git
        else:
            self.coll = self.cmts

        return self.coll

    def findData(self, item, str):

        # print ("collect : %s" %item)
        # print ("string : %s" %str)

        self.getCollect(item)
        result = self.coll.find(str)
        # print ("find result is %s"%result)
        return result

    def findCollAllData(self, item):

        # print ("collect : %s" %item)
        # print ("string : %s" %str)

        self.getCollect(item)
        result = self.coll.find()
        # print ("find result is %s"%result)
        return result

    def insertData(self, item, str):
        self.getCollect(item)
        result = self.coll.insert(str)
        return result

    def updateData(self, item, prever, str):
        self.getCollect(item)
        result = self.coll.update_one({"version": prever}, {'$set': str}, upsert=True)
        return result

    def updateGitData(self, item, prever, str):
        self.getCollect(item)
        result = self.coll.update_one({"name": prever}, {'$set': str}, upsert=True)
        return result

    def deleteData(self, item, str):
        self.getCollect(item)
        result = self.coll.remove(str)
        return result

    def deleteDataByVersion(self, ver):
        result = self.coll.remove({"version": ver})
        print(result)
        return result

    def deleteDataByBranch(self, bra):
        result = self.coll.remove({"branch": bra})
        return result

    def getConfig(self, section, key):
        config = configparser.ConfigParser()
        config.read('config.conf')
        return config.get(section, key)