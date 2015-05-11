'''
Created on 10/5/2015

@author: johnPortella
@version: 1.0

'''

import paramiko, os
from ftplib import FTP


class PyFileTransfer(object):
    
    
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
    
    def get(self,  filename, remoteDirectory=None, localDirectory=None):
        if localDirectory is None:
            localDirectory = os.path.dirname(os.path.realpath(__file__))
        
        if self.__typeProtocol == 'ftp':
            pwdAux = self.__t.pwd()            
            if remoteDirectory is not None: 
                self.__t.cwd(remoteDirectory)
            self.__t.retrbinary("RETR " + filename, open(os.path.join(localDirectory, filename), 'wb').write)            
            self.__t.cwd(pwdAux)    
        elif self.__typeProtocol == 'sftp':                
            if remoteDirectory is not None:
                self.__t.chdir(remoteDirectory)
            self.__t.get(filename, os.path.join(localDirectory, filename))
    
    def disconnect(self):
        if self.__typeProtocol == 'ftp':
            self.__t.quit()       
        elif self.__typeProtocol == 'sftp':
            self.__t.close()
            self.__ssh.close()
                    
t = PyFileTransfer('sftp', 'test.rebex.net', 'unix', 22)
t.connection("demo", "password")
t.get("readme.txt", '/')
t.disconnect() 