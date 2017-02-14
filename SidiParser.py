import sys
import math

from GoObj import *
from BinaryWalker import *

class SidiParser:

        def __init__(self):
                self.walker = BinaryWalker()
                self.gos = []

        def returnGos(self):
                return self.gos

        def parseSidi(self,filename, bx=0,by=0,bz=0):
                self.gos = []
                binaryData = None
                
                try:
                        print " Parse Sidi File : ", filename
                        file = open(filename,"rb")
                        binaryData = file.read()
                        file.close()
                except:
                        print "Cannot read sidi file",filename
                        sys.exit(1)
                        
                walker = self.walker # save some time typing
                walker.setData(binaryData)
                
                # welcome... to the real world
                walker.seek(0x18)
                IPRF_OFFSET = walker.getInt32()
                print "IPRF_OFFSET : ", IPRF_OFFSET
                
                walker.seek(IPRF_OFFSET+0x4)
                walker.seek(0x8) # skip two information uint32.. not needed
                
                IPRF_COUNT = walker.getInt32()
                
                print "\t\tIPRF:",IPRF_COUNT
                
                # choose the pill to take
                for i in range(0,IPRF_COUNT):
                        #print "\t\t\tIRPF",i
                        IPRF_PACKMAPID = walker.getInt32()
                        
                        deltaX = walker.getInt16()*10
                        deltaY = walker.getInt16()*10
                        deltaZ = walker.getInt16()*10

                        deltaX2 = walker.getInt16()*10
                        deltaY2 = walker.getInt16()*10
                        deltaZ2 = walker.getInt16()*10
                        
                        #print "IPRF %s: " % (i+1),struct.pack("i",IPRF_PACKMAPID).encode('hex')

                        
                        
                        blob = walker.getBlob(0x10) # read the following values (IGNORED FOR NOW)
                        
                        GOS_COUNT = walker.getInt32()
                        
                        #print "GOS INSIDE:", GOS_COUNT
                
                        # congrats on taking the right pill
                        for j in range(0,GOS_COUNT):
                                #print "GO",j
                                GO_BLOB = walker.getBlob(4+4+12+16+12+12+0xe)
                                go = GoObj()
                                go.parentOffset = [deltaX,deltaY,deltaZ]
                                go.parentOffset2 = [deltaX2,deltaY2,deltaZ2]
                                go.blob = GO_BLOB
                                self.gos.append(go)
                                
                        # tank, load the blob-ignoring program (may fail!)
                        
                        nbr = walker.getInt32()
                        walker.seek(nbr * 0x1a)
                        nbr = walker.getInt32()
                        walker.seek(nbr * 0x50)
                        zero = walker.getInt32()
                        assert zero == 0 , "Wasn't 0 but %s" % (struct.pack("i",zero).encode('hex'))
                        nbr = walker.getInt32()
                        walker.seek(nbr * 0x08)
                        nbr = walker.getInt32()
                        walker.seek(nbr * 0x02)
                        
                        
                        #ISHD... ISPI...
                        ## CRISPY CHICKEN part v0.2 ... 
                        nbr = walker.getInt32()
                        for n in range(0,nbr):
                                walker.getBlob(0x4f)
                                rest = walker.getInt32() # rest of the chicken
                                walker.seek(rest + 0x04) # chicken has an extra "FF FF FF FF"
                        
                        nbr = walker.getInt32()
                        walker.seek(nbr * 0x0c)
                        zero = walker.getInt32()
                        if zero != 0:
                                for i in range(0,zero):
                                        walker.seek(0x18)
                                        size = walker.getInt32()
                                        walker.seek(size+4)
                        #assert zero == 0, "Wasn't 0 but %s\n%s" % (struct.pack("i",zero).encode('hex'),hex(walker.offset))
