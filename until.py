import hashlib
import os
class until:
    __dir = ''
    __html = ''
    __log = ''
    def __init__(self,project,ymd):
        self.__dir = ''.join([os.getcwd(),os.sep,'data',os.sep,project,os.sep])
        if(False == os.path.exists(self.__dir)):
            os.mkdir(self.__dir)

        self.__html = ''.join([self.__dir,'html',os.sep])
        if(False == os.path.exists(self.__html)):
            os.mkdir(self.__html)

        if(len(ymd) > 0):
            self.__dir = ''.join([self.__dir,ymd,os.sep])
            if(False == os.path.exists(self.__dir)):
                os.mkdir(self.__dir)

            self.__html = ''.join([self.__dir,'html',os.sep])
            if(False == os.path.exists(self.__html)):
                os.mkdir(self.__html)

        self.__log = ''.join([self.__dir,'log.txt'])

    def getDir(self):
        return self.__dir

    def write(self,msg,filename):
        dir = self.__dir + filename
        file = open(dir,'a',encoding='UTF-8')
        file.write(msg)
        file.write('\n')
        file.close()
        return True

    def delete(self,filename):
        dir = self.__dir + filename
        try:
            os.remove(dir)
            return True
        except:
            return False

    def read(self,filename):
        dir = self.__dir + filename
        try:
            file = open(dir,'r',encoding='UTF-8')
            return file.readlines()
        except:
            return ''

    def log(self,key):
        msg = hashlib.md5(key.encode('utf-8')).hexdigest()
        file = open(self.__log,'a',encoding='UTF-8')
        file.write(msg)
        file.write('\n')
        file.close()
        return True

    def hasLog(self,key):
        msg = hashlib.md5(key.encode('utf-8')).hexdigest()
        try:
            file = open(self.__log,'r')
            for line in file.readlines():
                line = line.strip()
                line = str(line)
                if(line == msg):
                    return True
            return False
        except:
            return False

    def error(msg):
        if(False == isinstance(msg, str)):
            msg = str(msg)
        dir = ''.join([os.getcwd(),os.sep,'error.log'])
        file = open(dir,'a',encoding='UTF-8')
        file.write(msg)
        file.write('\n')
        file.close()
        return True