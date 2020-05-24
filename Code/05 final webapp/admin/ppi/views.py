from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from .models import *
from .webcrawler import *
from .graphtools import *
from .proteinrecognition import *

import threading
import time
import datetime

import joblib

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







webcrawlerThread = threading.Thread(target = webcrawler, name = "webcrawlerThread")

webcrawlerThread.daemon = True
#webcrawlerThread.start()















logging.info('')
logging.info('Finished all depenencies')
logging.info('')

def index(request):

	
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			
			logging.info("valid")
			
			query = form.cleaned_data['searchbox']
			
			#query = query.lower() #and other input verification
			
			query = query.split(" ")[0]
			
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
						
						proteinRecognitionNetwork = joblib.load("ppi\\model\\proteinRecognitionNetwork.pkl")
						
						if isProtein(proteinRecognitionNetwork,query):
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