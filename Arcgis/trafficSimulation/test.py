import os
import sys
filePath = os.path.realpath(__file__)
fileDirPath = os.path.split(filePath)[0]
print 'filePath:',filePath
print 'fileDirPath',fileDirPath

c=os.path.join(fileDirPath,'rpc')
print "os.path.join(fileDirPath,'rpc'):",c

print 'sys.path: ',sys.path
sys.path.insert(0, os.path.join(fileDirPath,'rpc') )
print 'sys.path insert rpc :',sys.path,'\n'
print 'sys.path.remove(sys.path[0])'
sys.path.remove(sys.path[0])
print 'sys.path remove path0 :',sys.path

# import the db 
sys.path.insert(0, os.path.join(fileDirPath,'db') )
print 'sys.path insert db'
print sys.path,'\n'
sys.path.remove(sys.path[0])
print 'sys.path remove path0','\n',sys.path
