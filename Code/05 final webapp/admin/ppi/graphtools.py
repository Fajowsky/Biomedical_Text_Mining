from .models import *


#NODES AND GRAPHS FOR D3JS



class node:
	def __init__(self, id, group,url):
		self.id = id #name
		self.group = group #number
		self.url = url #url
	

class link:
	def __init__(self, source, target):
		self.source = source #name
		self.target = target #number
		self.value = 5 #url	

class dbdata:
	def __init__(self, nodes, links):
		self.nodes = nodes
		self.links = links


def generateGraphData(interactionList, data, group, level, depth, indexedProteins):
	#logging.info("Level "+str(level)+" depth "+ str(depth))
	#logging.info(indexedProteins)
	
	if depth == level:
		for i in interactionList:
			
			
			if i.to in indexedProteins:
				data.links +=[link(i.frm,i.to)]
				continue
			
			else:
				#logging.info("   "+str(i))
				
				data.nodes +=[node(i.to,group,i.link)]
				indexedProteins +=[i.to]
				
				data.links +=[link(i.frm,i.to)]
		return
	
	
	for i in interactionList:
		group +=1
		
		
		if i.to in indexedProteins:
			data.links +=[link(i.frm,i.to)]
			continue
		
		else:
			#logging.info("   "+str(i))
			
			data.nodes +=[node(i.to,group,i.link)]
			indexedProteins +=[i.to]
			
			data.links +=[link(i.frm,i.to)]
		
		#logging.info("")
		generateGraphData(i.to.interactions_to.all(),data, group, level+1,depth,indexedProteins)



