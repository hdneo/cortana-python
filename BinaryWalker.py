import struct

class BinaryWalker:

	def __init__(self):
		self.offset = 0
		
	def setData(self,data):
		self.data = data
		self.offset = 0
	
	def seek(self,nBytes):
		self.offset = self.offset + nBytes
	
	def getInt16(self):
		uint = self.data[self.offset:self.offset+2]
		self.seek(2)
		return struct.unpack("h",uint)[0]
	
	def getInt32(self):
		uint = self.data[self.offset:self.offset+4]
		self.seek(4)
		return struct.unpack("i",uint)[0]
	
	def getFloat(self):
		flt = self.data[self.offset:self.offset+4]
		self.seek(4)
		return struct.unpack("f",flt)[0]
	
	def getDouble(self):
		dbl = self.data[self.offset:self.offset+8]
		self.seek(8)
		return struct.unpack("d",dbl)[0]
		
	def getVector3f(self):
		a = self.getFloat()
		b = self.getFloat()
		c = self.getFloat()
		return [a,b,c]
	
	def getQuat(self):
		a = self.getFloat()
		b = self.getFloat()
		c = self.getFloat()
		d = self.getFloat()
		return [a,b,c,d]
		
	def getBlob(self,nBytes):
		blob = self.data[self.offset:self.offset+nBytes]
		self.seek(nBytes)
		return blob
	