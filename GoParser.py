import sys
import struct
import math

class GoParser:


    def getIprfDegrees(self,x,z,x2,z2):
        if (x == x2):
            if(z == z2):
                return 0
            else:
                return 90
        else:
            if(z != z2):
                return 180
            else:
                return -1

    def getGamePosition(self,go,sectorBase):
        
        GO_HALFEXTENDS = go.blob[8:20]
        GO_OFFSETX = struct.unpack("f",GO_HALFEXTENDS[0:4])[0]
        GO_OFFSETY = struct.unpack("f",GO_HALFEXTENDS[4:8])[0]
        GO_OFFSETZ = struct.unpack("f",GO_HALFEXTENDS[8:12])[0]
    
    
        #GO_MIN = go.blob[20:32]
        #GO_MAX = go.blob[32:44]
        #GO_MAX_Y = struct.unpack("f",GO_MAX[4:8])[0]

        #GO_OFFSETY = GO_OFFSETY + GO_MAX_Y/2.0
        
        GO_OFFSETY = GO_OFFSETY + 145.0
		
        GO_MXOPOS = [0.0,0.0,0.0]

        if go.parentOffset == None:
            GO_MXOPOS[0] = sectorBase[0]+GO_OFFSETX
            GO_MXOPOS[1] = sectorBase[1]+GO_OFFSETY
            GO_MXOPOS[2] = sectorBase[2]+GO_OFFSETZ
            return GO_MXOPOS

        #has a parent, which is a IPRF
        if go.parentIprf !=None:
            modX = 1 # modifier for X axis
            modZ = 1 # modified for Z axis

            base = go.parentOffset # first XYZ offset of IPRF
            degrees = self.getIprfDegrees(go.parentOffset[0],go.parentOffset[2],go.parentOffset2[0],go.parentOffset2[2])
            if degrees == 0:
                modX = modZ = 1
            elif degrees == 90:
                modX = 1
                modZ = -1
            elif degrees == 180: #180
                modX = -1
                modZ = -1
            else: #-1, mirrored
                modX = 1
                modZ = 1
                #base = go.parentOffset2

            GO_MXOPOS[0] = sectorBase[0]+base[0] + (modX * GO_OFFSETX)
            GO_MXOPOS[1] = sectorBase[1]+base[1] + GO_OFFSETY
            GO_MXOPOS[2] = sectorBase[2]+base[2] + (modZ * GO_OFFSETZ)

        else: # EPRF children.. oooh The Doors!
            modX = 1 # modifier for X axis
            modZ = 1 # modified for Z axis
            degrees = self.getIprfDegrees(go.parentOffset[0],go.parentOffset[2],go.parentOffset2[0],go.parentOffset2[2])
            if degrees == 0:
                modX = modZ = 1
            elif degrees == 90:
                modX = 1
                modZ = -1
            elif degrees == 180: #180
                modX = -1
                modZ = -1
            else: #-1, mirrored
                modX = -1
                modZ = 1

            base = go.parentOffset # first XYZ offset of IPRF
            GO_MXOPOS[0] = sectorBase[0]+base[0] + (modX * GO_OFFSETX)
            GO_MXOPOS[1] = sectorBase[1]+base[1] + GO_OFFSETY
            GO_MXOPOS[2] = sectorBase[2]+base[2] + (modZ * GO_OFFSETZ)

        #emergency exit for calculations not so well done
        """for i in range(0,len(GO_MXOPOS)):
            if GO_MXOPOS[i]<sectorBase[i] and i!=1: #ignore Y axis
                    print go.blob[0:8].encode('hex')
                    print "Sector base",sectorBase
                    print "Base:",go.parentOffset,go.parentOffset2
                    print "Degrees:",degrees
                    print "Go ofsset :",GO_OFFSETX,GO_OFFSETY,GO_OFFSETZ
                    print "MXO POS",GO_MXOPOS
                    sys.exit(1)"""
      
        return GO_MXOPOS            
        
            
            

    def parseGo(self,gotypes,go,sectorBase,sectorid,sectorPath,csvWriter,metrId):

        GO_TYPE = go.blob[0:4]
        SECTOR_STATICID = go.blob[4:8]
        #halfextends are handler in other part
        GO_QUATERNION = go.blob[20:36]
        # we dont need the "position" and "offset" values

        GO_MXOPOS = self.getGamePosition(go,sectorBase)

        #soo we do some stuff here... nothing fancy

        GO_ROTATION = 0.0
        gook = True
        try:
            GO_ROTATION = math.asin(struct.unpack("f",GO_QUATERNION[4:8])[0]) * 360 / math.pi
            parentDegrees = 0.0                               
            if go.parentOffset != None: #has parent
                parentDegrees = self.getIprfDegrees(go.parentOffset[0],go.parentOffset[2],go.parentOffset2[0],go.parentOffset2[2])
            GO_ROTATION = GO_ROTATION + parentDegrees
        except:
            print GO_QUATERNION[4:8].encode('hex')
            print GO_QUATERNION.encode('hex')
            print struct.unpack("f",GO_QUATERNION[4:8])[0]
            gook = False
                               
        template ="""
            <go mxoid="MXOID" staticid="SECID" type="TYPE" strType="STRTYPE" exterior="EXTERIOR">
                <pos x="POSX" y="POSY" z="POSZ"/>
                <rotation>ROT</rotation>
                <quat>QUAT</quat>
            </go>"""


        GO_MXOID = SECTOR_STATICID[0:2].encode('hex')
        SECTOR_ID = struct.pack("l",sectorid).encode('hex')
        k = SECTOR_ID[1:4]
        k = k+SECTOR_ID[0]
        GO_MXOID = GO_MXOID + k
        

        exterior = True
        if go.parentOffset!=None:
            exterior = False

        # write the final Data to the XML template
        template = template.replace("MXOID",GO_MXOID)
        template = template.replace("SECID",SECTOR_STATICID.encode('hex'))
        try:
            template = template.replace("STRTYPE",gotypes[GO_TYPE])
            STR_GO_TYPE = gotypes[GO_TYPE];
        except:
            template = template.replace("STRTYPE","Unknown(%s)" % GO_TYPE.encode('hex'))
            STR_GO_TYPE = "Unknown(%s)" % GO_TYPE.encode('hex');

        template = template.replace("TYPE",GO_TYPE.encode('hex'))
        template = template.replace("EXTERIOR","%s" % exterior)
        template = template.replace("POSX","%s" % GO_MXOPOS[0])
        template = template.replace("POSY","%s" % GO_MXOPOS[1])
        template = template.replace("POSZ","%s" % GO_MXOPOS[2])
        template = template.replace("ROT","%s" % GO_ROTATION)
        template = template.replace("QUAT",GO_QUATERNION.encode('hex'))
        
        
        csvWriter.writerow([metrId,sectorid,GO_MXOID,SECTOR_STATICID.encode('hex'),GO_TYPE.encode('hex'),"%s" % exterior,"%s" % GO_MXOPOS[0],"%s" % GO_MXOPOS[1],"%s" % GO_MXOPOS[2],"%s" % GO_ROTATION,GO_QUATERNION.encode('hex')]);
        
        if gook == False:
            print template
            print go.blob.encode('hex')
            sys.exit(1)
        
        return template
