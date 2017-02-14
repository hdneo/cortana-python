import os
import sys
import struct
import re

from GoObj import *

pattern = r'.'*0x3c+("\xff"*4)+".."+("\xff"*6)+".."
vpattern = r'..'+"\x00\x00"+'.'*0x38+"\xff"*4+".."+"\xff"*6+".."


class SidParser:

        def __init__(self):
                self.gos = []

        def returnGos(self):
                return self.gos
        
        def parseSid(self,fname):
                self.gos = []
                file = open(fname,"rb")
                data = file.read()
                file.close()
        

                #use this flag couse python sometimes is not so cool
                results = re.findall(pattern,data,re.DOTALL)

                for r in results:
                        go = GoObj()
                        go.parentIprf = None
                        go.parentOffset = go.parentOffset2 = None
                        go.blob = r
                        self.gos.append(go)
