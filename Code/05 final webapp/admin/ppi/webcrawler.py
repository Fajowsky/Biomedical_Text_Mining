import random
import copy
import time
import datetime

import joblib

from ppi.models import *


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




from pymed import PubMed

my_email = "norockderipa@yahoo.com"

# Create a PubMed object that GraphQL can use to query
# Note that the parameters are not required but kindly requested by PubMed Central
# https://www.ncbi.nlm.nih.gov/pmc/tools/developers/
pubmed = PubMed(tool="Protein Interaction Text Miner", email=my_email)


class Publication:
	def __init__(self, 
				 pubmed_id, 
				 title,
				 publication_date,
				 abstract,
				 keywords = ""):
		
		self.pubmed_id = pubmed_id
		self.url = "https://www.ncbi.nlm.nih.gov/pubmed/"+pubmed_id.split("\n")[0]
		self.title = title		
		self.publication_date = publication_date
		self.abstract = abstract
		if abstract is not None and abstract is not "":
			self.words = len(abstract.split(" "))  
		else:
			self.words = 0
		self.keywords = keywords
		
		
def queryPubmed(query):   

	nrArticles =500
	print("Pubmed query is",query)
	# Execute the query against the API
	results = pubmed.query(query, max_results=nrArticles)

	# Loop over the retrieved articles
	publications = []
	for article in results:
		#print("we are iterating")
		if hasattr(article, 'keywords'):
			publications +=[Publication(article.pubmed_id,
										article.title,
										article.publication_date,
										article.abstract,
										article.keywords)]
		else:
			publications +=[Publication(article.pubmed_id,
								article.title,
								article.publication_date,
								article.abstract)]
			
	print(len(publications),"publications")
	
	publications = [publication for publication in publications if publication.words is not 0]
	
	print("Extracted",len(publications),"articles with non-empty abstracts")   
	
	
	return publications



def wordSplitter(string, length):
	
	words = string.split(" ")
	
	lists = list((words[0+i:length+i] for i in range(0, len(words), length)))		
		
	sentences = [" ".join(l) for l in lists]		
		
	return sentences


'''instance = proteinRelationPrediction()'''

def findppirelations(isProteinRelation,PROTEINA,PROTEINB):
	
	print()
	print("checking for relations")
	print()
	
	#PPI_Estimator = proteinRelationPrediction()
	
	publications = queryPubmed(str(PROTEINA)+" "+str(PROTEINB))
	
	publications = [publication for publication in publications if PROTEINA in publication.abstract and PROTEINB in publication.abstract]
	
	print("Publications with both proteins",len(publications))
	
	#print("Extracted",len(publications),"articles that have the pair")
	
	interactionArticles = []
	
	for p in publications:
		tempAbstract = p.abstract
		
		tempAbstract = tempAbstract.replace(PROTEINA,"PROTEINA")
		
		tempAbstract = tempAbstract.replace(PROTEINB,"PROTEINB")
		
		#print(tempAbstract)
		#print()
		
		if isProteinRelation(tempAbstract):
			interactionArticles += [p]
	
	#print(len(interactionArticles),"interactions found by network")
	
	if len(interactionArticles)>0:
		
		print(interactionArticles[0].title)
		print()
		print(interactionArticles[0].abstract)
		print()
		print(interactionArticles[0].url)
		print()
		
		pub = interactionArticles[0].title
		abstract = interactionArticles[0].abstract
		link = interactionArticles[0].url
		
		return {"pub":pub,"abstract":abstract,"link":link}
	
	return False


'''
def findppirelations(PROTEINA,PROTEINB):
	
	
	if random.randrange(101)>75:
		pub = "pub" +str(random.randrange(20,4000))
		abstract = "This protein is connected to that protein because etcetera"
		link = "https://www.google.com/search?q="+str(random.randrange(20,4000))
		return {"pub":pub,"abstract":abstract,"link":link}
	
	return 0
'''

def crawler(isProteinRelation):

	print()
	print("Crawler called...")
	print()
	checkList = [p.name for p in ToCheck.objects.all()]


	for A in checkList:
		try:
			PROTEINA = Protein.objects.get(name = A)
		except Protein.DoesNotExist:
			PROTEINA = Protein.objects.create(name=A)#add protein to DB
		
		if len(CurrentCheckList.objects.all())==0:
			for p in Protein.objects.all():
				CurrentCheckList.objects.create(name=p.name)

		againstList = [p.name for p in CurrentCheckList.objects.all()]
		
		for B in againstList:
			if A==B:
				print("Same Protein")
			else:
				article = findppirelations(isProteinRelation,A,B)
				
				if article:

					
					PROTEINB = Protein.objects.get(name = B)
					PROTEINA.interactions.add(PROTEINB, through_defaults={"publication": article["pub"], "abstract":article["abstract"], "link":article["link"]})
			
			CurrentCheckList.objects.get(name = B).delete()#delete PROTEINB FROM CurrentCheckList DB
		ToCheck.objects.get(name = A).delete()#delete PROTEINA FROM ToCheck DB




def updater(isProteinRelation):

	print("updater called")
	print()
	checkList = [p.name for p in Protein.objects.all()]


	for A in checkList:
		

		againstList = [p.name for p in Protein.objects.all()]
		
		for B in againstList:
			
			if Protein.objects.get(name = A) == Protein.objects.get(name = B):
				continue
			
			if Protein.objects.get(name = A) in Protein.objects.get(name = B).interactions.all():
				continue
				
			else:
				#work on thie stuff below

				article = findppirelations(isProteinRelation,A,B)
				
				if article:
					PROTEINA = Protein.objects.get(name = A)
					proteinB = Protein.objects.get(name = B)
					PROTEINA.interactions.add(proteinB, through_defaults={"publication": article["pub"], "abstract":article["abstract"], "link":article["link"]}) #add relation
					#continue
				
				#CurrentCheckList.objects.get(name = B).delete()#delete PROTEINB FROM CurrentCheckList DB



def webcrawler():
	
	start = datetime.datetime.now()
	
	crawler_wait_time_seconds = 10
	
	update_interval_seconds = 24*3600
	
	#PPI NETWORK AND DEPENDENCIES
	
	from keras.preprocessing.sequence import pad_sequences


	PPINetwork = joblib.load("ppi\\model\\PPINetwork.pkl")

	tokenizer = joblib.load("ppi\\model\\tokenizer.pickle")




	def isProteinRelation(text):

		tokenized = tokenizer.texts_to_sequences([text])

		padded_tokenized = pad_sequences(tokenized, maxlen=50)

		manual_bias = 0.49

		return bool(round(PPINetwork.predict([[padded_tokenized[0]]])[0][0]  + manual_bias))
	
	
	while True:
		if len(ToCheck.objects.all())>0:
			crawler(isProteinRelation)
		elif (datetime.datetime.now()-start).seconds>update_interval_seconds:
			updater(isProteinRelation)
			start = datetime.datetime.now()
		else:
			logging.info('')
			logging.info('Crawler waiting...')
			logging.info('')
			time.sleep(crawler_wait_time_seconds)