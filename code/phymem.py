# This is the only file you must implement

# This file will be imported from the main code. The PhysicalMemory class
# will be instantiated with the algorithm received from the input. You may edit
# this file as you which

# NOTE: there may be methods you don't need to modify, you must decide what
# you need...

from Queue import Queue

class PhysicalMemory:
	ALGORITHM_AGING_NBITS = 8
	"""How many bits to use for the Aging algorithm"""


	def __init__(self, algorithm):
		assert algorithm in {"fifo", "nru", "aging", "second-chance"}
		self.algorithm = algorithm

		if self.algorithm == "fifo":
			self.allocatedFrames = Queue()
		if self.algorithm == "second-chance":
			self.allocatedFrames = []
			self.access = []
		if self.algorithm == "nru":
			self.allocatedFrames = []
			self.access = []
		if self.algorithm == "aging":
			self.allocatedFrames = []
			self.access = []


	def put(self, frameId):
		"""Allocates this frameId for some page"""
		# Notice that in the physical memory we don't care about the pageId, we only
		# care about the fact we were requested to allocate a certain frameId
		if self.algorithm == "fifo":
			self.allocatedFrames.put(frameId)
		if self.algorithm == "second-chance":
			self.allocatedFrames.append(frameId)
			self.access.append(0)
		if self.algorithm == "nru":
			self.allocatedFrames.append(frameId)
			# [Referenciado, Modificado]
			self.access.append([0,0])
		if self.algorithm == "aging":
			self.allocatedFrames.append(frameId)
			self.access.append([0,0,0,0,0,0,0,0])


	def evict(self):
		"""Deallocates a frame from the physical memory and returns its frameId"""
		# You may assume the physical memory is FULL so we need space!
		# Your code must decide which frame to return, according to the algorithm
		if self.algorithm == "fifo":
			return self.allocatedFrames.get()
			
		if self.algorithm == "second-chance":
			index = 0
			while (True):
				if self.access[index] == 0:
					self.access.pop(index)
					return self.allocatedFrames.pop(index)
				else :
					self.access.pop(index)
					frameId = self.allocatedFrames.pop(index)
					self.put(frameId)
					
		if self.algorithm == "nru":
			# Precedencia 00, 01, 10, 11
			index = 0
			while (index < len(self.access)):
				if (self.access[index] == [0,0]) :
					self.access.pop(index)
					return self.allocatedFrames.pop(index)
				index += 1

			index = 0
			while (index < len(self.access)):
				if (self.access[index] == [0,1]) :
					self.access.pop(index)
					return self.allocatedFrames.pop(index)
				index += 1

			index = 0
			while (index < len(self.access)):
				if (self.access[index] == [1,0]) :
					self.access.pop(index)
					return self.allocatedFrames.pop(index)
				index += 1

			index = 0
			while (index < len(self.access)):
				if (self.access[index] == [1,1]) :
					self.access.pop(index)
					return self.allocatedFrames.pop(index)
				index += 1
				
		if self.algorithm == "aging":
			frameId = 0
			for i in range(0, len(self.allocatedFrames)):
				index = -1
				for j in range(0, len(self.access[i])):
					if self.access[i][j] == 1:
						index1 = j
				if frameId < index:
					frameId = index
			self.access.pop(frameId)
			return self.allocatedFrames.pop(frameId)


	def clock(self):
		"""The amount of time we set for the clock has passed, so this is called"""
		# Clear the reference bits (and/or whatever else you think you must do...)
		if self.algorithm == "nru":
			for i in range(0, len(self.access)):
				self.access[i][0] = 0


	def accesss(self, frameId, isWrite):
		if self.algorithm == "second-chance":
			index = self.allocatedFrames.index(frameId)	
			self.access[index] = 1	
			
		# [Referenciado, Modificado]
		if self.algorithm == "nru":
			index = self.allocatedFrames.index(frameId)
			if (isWrite) :
				self.access[index] = [1, 1]	
			else :		
				self.access[index] = [1, 0]	
				
		if self.algorithm == "aging":
			index = self.allocatedFrames.index(frameId)
			bit = -1
			for i in range(0, len(self.access[index])):
				if self.access[index][i] == 1:
					bit = i
			if bit >= 0 and bit < 7:
				self.access[index][bit] = 0
				self.access[index][bit+1] = 1
			elif bit == -1:
				self.access[index][0] = 1
				
	def algorithm(self):
		print (self.algorithm)
		
# import sys
# sys.path.append("/home/ely/LSO/python")
# from phymem import PhysicalMemory
# p = PhysicalMemory("nru")
