from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from .models import *
from .webcrawler import *
from .proteinrecognition import *

import threading
import time
import datetime

import logging, logging.config
import sys

LOGGING = {
	'version': 1,
	'handlers': {
		'console': {
			'class': 'logging.StreamHandler',
			'stream': sys.stdout,
		}
	},
	'root': {
		'handlers': ['console'],
		'level': 'INFO'
	}
}

logging.config.dictConfig(LOGGING)
logging.info('------------------------------------------------')



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






#logging.info('Hello Console')

def countSeconds():
	
	counter = 0
	while True:
		logging.info(datetime.datetime.today())
		logging.info(counter)
		counter+=1
		time.sleep(1)

def webcrawler():
	
	while True:
		if len(ToCheck.objects.all())>0:
			crawler()
		else:
			logging.info('')
			logging.info('Crawler waiting...')
			logging.info('')
			time.sleep(10)



webcrawlerThread = threading.Thread(target = webcrawler, name = "webcrawlerThread")

webcrawlerThread.daemon = True
webcrawlerThread.start()



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



#logging.info('Hello hello')

def index(request):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			
			logging.info("valid")
			
			query = form.cleaned_data['searchbox']
			
			#query = query.split(" ")[0].lower() #input cleaning
			
			depth = form.cleaned_data['depth'] - 1
			
			logging.info(query)
			
			try:
				queriedProtein = Protein.objects.get(name = query)
				
				
				data = dbdata([],[])
				
				group = 1
				
				data.nodes += [node(queriedProtein.name,group,"https://www.google.com/search?q="+query)]
				
				indexedProteins = [queriedProtein]
				
				message = "Please click on a protein node to get the corresponding article. You can rearrange the network by drag and drop."
				
				generateGraphData(interactionList = queriedProtein.interactions_to.all(), data = data, group =group , level = 0, depth = depth, indexedProteins = indexedProteins)

			except Protein.DoesNotExist:
				logging.info("doesn't exist")
				message = "Sorry, that doesn't look like a protein"

				try:
					
					ToCheck.objects.get(name=query)
					
					logging.info("Protein already in checklist")
					message = "That protein is already in our list to check, try again later."
				
				except ToCheck.DoesNotExist:
						if proteinRecognizer(query):
							logging.info("protein recognized, added to checklist")
							if len(Protein.objects.all()) == 0:
								Protein.objects.create(name=query)
							else:
								ToCheck.objects.create(name=query)
							message = "We don't have that protein in our database, so we've added it to our checklist. Return later to see results."
				data = dbdata([],[])
			
			
			context = {"data":data,"form": form, "message":message}
			return render(request, "ppi/index.html",context)
		else:
			logging.info("form not valid")
			logging.info(form.errors)
			form = SearchForm()
			message = "Sorry, something went wrong with our forms"
			return render(request, "ppi/index.html",{'form': form,'message':message})
	
	else:
		form = SearchForm()
		return render(request, "ppi/index.html",{'form': form})



def about(request):
	form = SearchForm()
	context = {'message': "hello word",'form': form}
	return render(request, "ppi/about.html",context)