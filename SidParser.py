import os
import sys
import struct
import re

from GoObj import *

pattern = r'.'*0x3c+("\xff"*4)+".."+("\xff"*6)+".."
vpattern = r'..'+"\x00\x00"+'.'*0x38+"\xff"*4+".."+"\xff"*6+".."

class LameFinder:

        def __init__(self):
                self.loadEprf()
                self.loadDoors()
                
        def loadEprf(self):
                file= open("resources/eprf.lst")
                data = file.read().split("\n")
                file.close()

                self.eprfData = []
                for i in data:
                        i = ("000000"+i).decode('hex')
                        self.eprfData.append(i)

        def loadDoors(self):
                file= open("resources/doors.lst")
                data = file.read().split("\n")
                file.close()

                self.doortypes = []
                for i in data:
                        i = i.decode('hex')
                        self.doortypes.append(i)

        def isDoor(self,gotype):
                return gotype in self.doortypes
        

        def findEprfs(self,data):

                info = []
                for eprfId in self.eprfData:
                        offset = 0
                        t = data.count(eprfId)
                        for i in range(0,t):
                                offset = data.find(eprfId,offset)
                                pos = offset+7
                                bx = struct.unpack("h",data[pos:pos+2])[0]
                                by = struct.unpack("h",data[pos+2:pos+4])[0]
                                bz = struct.unpack("h",data[pos+4:pos+6])[0]
                                parentOffset = [bx*10,by*10,bz*10]
                                pos = pos +6
                                bx = struct.unpack("h",data[pos:pos+2])[0]
                                by = struct.unpack("h",data[pos+2:pos+4])[0]
                                bz = struct.unpack("h",data[pos+4:pos+6])[0]
                                parentOffset2 = [bx*10,by*10,bz*10]

                                info.append([offset,parentOffset,parentOffset2])
                                offset = offset+1
                return info


class SidParser:

        def __init__(self):
                self.gos = []
                self.lame = LameFinder()

        def returnGos(self):
                return self.gos
        
        def parseSid(self,fname):
                self.gos = []
                file = open(fname,"rb")
                data = file.read()
                file.close()

                eprfs = []

                if "sidgo" not in fname:
                      eprfs = self.lame.findEprfs(data)

                        

                #use this flag couse python sometimes is not so cool
                results = re.findall(pattern,data,re.DOTALL)
                vresults= re.findall(vpattern,data,re.DOTALL)


                reallist = results
                if len(results)!=len(vresults):
                        print "\t\t\tOne invalid sid go bypassed normal RE. using verified RE"
                        reallist = vresults
                
                for r in reallist:

                        go = GoObj()
                        go.parentIprf = None
                        go.parentOffset = go.parentOffset2 = None
                        go.blob = r

                        if "sidgo" not in fname:
                                isdoor = self.lame.isDoor(r[0:4])
                                if isdoor == True:
                                        #whos your daddy, door?
                                        offset = data.find(r) #unique
                                        diff = len(data) #beat this
                                        cell = None #unknown daddy
                                        for e in eprfs:
                                                newpos = offset-e[0]
                                                if newpos>0 and newpos<diff:
                                                        diff = newpos
                                                        cell = e
                                                        go.parentOffset = e[1]
                                                        go.parentOffset2 = e[2]
                        
                                        
                        self.gos.append(go)

