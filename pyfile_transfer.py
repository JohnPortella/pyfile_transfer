'''
Created on 10/5/2015

@author: johnPortella
@version: 1.0

'''

import paramiko, os
from ftplib import FTP

#from config_parser import ConfigUtils


class PyFileTransfer(object):
    '''   
    def __init__(self, transfName):
        transfConf = ConfigUtils.read_trasnfer_config(transfName)
        
        #hostname
        self.__hostname = transfConf['host']
        #username
        self.__username = transfConf['user']
        #password
        self.__password = transfConf['password']
        #protocol
        self.__typeProtocol = transfConf['type']
        #so
        if transfConf['so'] == 'unix':
            self.__SEP = '/'
        elif transfConf['so'] == 'win':
            self.__SEP = chr(92)
        #port
        if 'port' in transfConf:
            self.__port = transfConf['port']
        else:
            self.__port = None
            
        #open transfering
        if self.__typeProtocol == 'ftp':
            if self.__port is None:
                self.__port = 21             
            #open
            self.__t = FTP()
            self.__t.connect(self.__hostname, self.__port, self.__timeout)         
            
        elif self.__typeProtocol == 'sftp':    
            if self.__port is None:
                self.__port = 22
            #open
            self.__ssh = paramiko.Transport((self.__hostname, self.__port))
            
        
    def connection(self):
        if self.__typeProtocol == 'ftp':
            self.__t.login(self.__username, self.__password)
        elif self.__typeProtocol == 'sftp':
            self.__ssh.connect(username = self.__username, password = self.__password)            
            self.__t = paramiko.SFTPClient.from_transport(self.__ssh)
            
    '''
    def __init__(self, typeProtocol='ftp', hostname = 'localhost', so='unix', port = None, timeout = None):
        #Protocol
        self.__typeProtocol = typeProtocol
        #host
        self.__hostname = hostname
        #so        
        if so == 'unix':
            self.__SEP = '/'
        elif so == 'win':
            self.__SEP = chr(92)   
        #timeout
        self.__timeout = timeout
        #port
        if port:
            self.__port = port
        #open transfering
        if self.__typeProtocol == 'ftp':
            if not port:
                self.__port = 21             
            #open
            self.__t = FTP()
            self.__t.connect(self.__hostname, self.__port, self.__timeout)         
            
        elif self.__typeProtocol == 'sftp':    
            if not port:
                self.__port = 22
            #open
            self.__ssh = paramiko.Transport((self.__hostname, self.__port))
            #self.__t.set
                                                    
    def connection(self, username, password):
        if self.__typeProtocol == 'ftp':
            self.__t.login(username, password)
        elif self.__typeProtocol == 'sftp':
            self.__ssh.connect(username = username, password = password)            
            self.__t = paramiko.SFTPClient.from_transport(self.__ssh)                                        
            self.__t.sock.settimeout(self.__timeout)
    
    def get(self,  filename, remoteDirectory=None, localDirectory=None):
        if localDirectory is None:
            localDirectory = os.path.dirname(os.path.realpath(__file__))
        
        if self.__typeProtocol == 'ftp':
            pwdAux = self.__t.pwd()            
            if remoteDirectory is not None: 
                self.__t.cwd(remoteDirectory)
            remoteFile = open(os.path.join(localDirectory, filename), 'wb').write
            self.__t.retrbinary("RETR " + filename, remoteFile)            
            self.__t.cwd(pwdAux)    
            remoteFile.close()
        elif self.__typeProtocol == 'sftp':              
            if remoteDirectory is not None:
                self.__t.chdir(remoteDirectory)                
            self.__t.get(filename, os.path.join(localDirectory, filename))
            self.__t.chdir(None)            
            
    def put(self, filename, remoteDirectory=None, localDirectory=None):
        if localDirectory is None:
            localDirectory = os.path.dirname(os.path.realpath(__file__))
                    
        if self.__typeProtocol == 'ftp':
            pwdAux = self.__t.pwd()
            if remoteDirectory is not None:
                self.__t.cwd(remoteDirectory)                
            localFile = open(filename, 'r')
            self.__t.storbinary('RETR %s' % filename, localFile.write)
            self.__t.cwd(pwdAux)
            localFile.close()
        elif self.__typeProtocol == 'sftp':            
            if remoteDirectory is not None:
                self.__t.chdir(remoteDirectory)
            self.__t.put(os.path.join(localDirectory, filename), filename)        
            self.__t.chdir(None)
            
    def disconnect(self):
        if self.__typeProtocol == 'ftp':
            self.__t.quit()       
        elif self.__typeProtocol == 'sftp':
            self.__t.close()
            self.__ssh.close()
          
    def remotePathJoin (self, *paths):        
        
        if len(paths)== 0:
            return None
        if len(paths)== 1:
            return paths[0]
        else:
            path = paths[0]
        
        for i in paths[1:]:
            path += self.__SEP + i  
        
        return path  
       
                         

t = PyFileTransfer('sftp', 'test.rebex.net', 'unix', 22)
t.connection("demo", "password")
t.get("WinFormClient.png", '/pub/example')
t.disconnect()
