import sys
import csv

from SidiParser import *
from SidParser import *
from GoParser import *

def loadGoTypes():
        global gotypes
        file = open("resources/gameobjects.csv","r")
        data = file.read().split("\n")
        file.close()
        for i in data:
                values = i.split(": ,")
                gotypes[struct.pack("i",int(values[1]))] = values[0]

def loadSectors():
        global dtsectors
        global itsectors
        global slumssectors
        file = open("resources/boundaries.lst","r")
        data = file.read().split("\n")
        file.close()
        
        for i in data:
                values = i.split(", ")
                if values[0]=="DTSECTOR":
                        dtsectors.append(values)
                elif values[0]=="ITSECTOR":
                        itsectors.append(values)
                elif values[0]=="SLUMSSECTOR":
                        slumssectors.append(values)
        
def parseSectors(prefix,sectors):
	
	csvWriter = csv.writer(open("results/staticObjects_" + prefix + ".csv","w"), delimiter=',', quotechar='|', lineterminator='\n');
	#  Backup with Data 
	# csvWriter.writerow(['metr_id','sector_id','path','mxoId','staticId','type','strType','exterior','pos_x','pos_y','pos_z','rotation','quat']);
	csvWriter.writerow(['metr_id','sector_id','mxoId','staticId','type','exterior','pos_x','pos_y','pos_z','rotation','quat']);
        for sector in sectors:

                template ="""
<sector id="SECTORID" path="SECTORPATH">
        <exteriorgos>
        EXTERIORGOLIST
        </exteriorgos>
        <interiorgos>
        INTERIORGOLIST
        </interiorgos>
</sector>
"""
                metrId = 1;
                if(prefix=="slums"):
                    metrId= 1;
                elif(prefix=="dt"):
                    metrId= 2;
                elif(prefix=="it"):
                    metrId= 3;
                # Open CSV File for Writing
                
                sectorid = int(sector[1])
                sectorPath = sector[2].replace("'","")
                sectorBase = sector[3:6]

                sectorBase[0] = float(sectorBase[0])
                sectorBase[1] = float(sectorBase[1])
                sectorBase[2] = float(sectorBase[2])

        

                print "Parsing Slums sector:",sectorid,sectorPath

                sidi = "%s\\%s.sidi" % (basePath,sectorPath)
                sid = "%s\\%s.sid" % (basePath,sectorPath)
                sidgo = "%s\\%s.sidgo" % (basePath,sectorPath)

        
                print "\tParsing sidis"
                sidip.parseSidi(sidi)
                sidiGOS = sidip.returnGos() # gathered SIDI GOS

                print "\tParsing sid"        
                sidp.parseSid(sid)
                sidGOS = sidp.returnGos() # gathered SID GOS

                print "\tParsing sidgo"                
                sidp.parseSid(sidgo)
                sidgoGOS = sidp.returnGos() #gathered SIDGO GOS

                print "\tFormatting sid"
                exteriorGoList =[]
                for exteriorGo in sidGOS:
                    exteriorGoList.append(g.parseGo(gotypes,exteriorGo,sectorBase,sectorid,sectorPath,csvWriter,metrId))
                print "\tFormatting sidgo"
                for exteriorGo in sidgoGOS:
                    exteriorGoList.append(g.parseGo(gotypes,exteriorGo,sectorBase,sectorid,sectorPath,csvWriter,metrId))

                print "\tFormatting sidi"
                interiorGoList = []
                for interiorGo in sidiGOS:
                    interiorGoList.append(g.parseGo(gotypes,interiorGo,sectorBase,sectorid,sectorPath,csvWriter,metrId))

                template = template.replace("SECTORID","%s" % sectorid)
                template = template.replace("SECTORPATH","%s" % sectorPath)
                template = template.replace("EXTERIORGOLIST","%s" % "\n".join(exteriorGoList))
                template = template.replace("INTERIORGOLIST","%s" % "\n".join(interiorGoList))

                file = open("results/%s_%s.xml" % (prefix,sectorid),"w+")
                file.write(template)
                file.close()
                        
        

#define global stuff
gotypes = dict()

dtsectors = []
itsectors = []
slumssectors = []

loadGoTypes()
loadSectors()

#pick the parser instances
g = GoParser()
sidip = SidiParser()
sidp = SidParser()

# base path where extracted world files are
#basePath="D:\\mxo\\Extracted\\resource\\worlds\\final_world"

# On Home
basePath="H:\\games\\The Matrix Online\\extracted\\resource\\worlds\\final_world";

# On Work
#basePath="C:\\Users\\alex\\others\\MatrixOnline\\extracted\\resource\\worlds\\final_world";
# do magic


# init our CSV Writer
#csvWriter = csv.writer(open("results/staticObjects.csv","w"), delimiter=',', quotechar='|', lineterminator='\n');
#csvWriter.writerow(['metr_id','sector_id','path','mxoId','staticId','type','strType','exterior','pos_x','pos_y','pos_z','rotation','quat']);

parseSectors("slums",slumssectors)
parseSectors("it",itsectors)
parseSectors("dt",dtsectors)
