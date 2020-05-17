import random

from ppi.models import *

def findppirelations(PROTEINA,PROTEINB):
	
	
	if random.randrange(101)>75:
		pub = "pub" +str(random.randrange(20,4000))
		abstract = "This protein is connected to that protein because etcetera"
		link = "https://www.google.com/search?q="+str(random.randrange(20,4000))
		return {"pub":pub,"abstract":abstract,"link":link}
	
	return 0


def crawler():

	checkList = [p.name for p in ToCheck.objects.all()]






	for A in checkList:
		
			
		if len(CurrentCheckList.objects.all())==0:
			for p in Protein.objects.all():
				CurrentCheckList.objects.create(name=p.name)


		againstList = [p.name for p in CurrentCheckList.objects.all()]
		
		for B in againstList:

			
			article = findppirelations(A,B)
			
			if article:
				try:
					PROTEINA = Protein.objects.get(name = A)
				except Protein.DoesNotExist:
					PROTEINA = Protein.objects.create(name=A)#add protein to DB
				
				proteinB = Protein.objects.get(name = B)
				PROTEINA.interactions.add(proteinB, through_defaults={"publication": article["pub"], "abstract":article["abstract"], "link":article["link"]}) #add relation
			
			CurrentCheckList.objects.get(name = B).delete()#delete PROTEINB FROM CurrentCheckList DB
		ToCheck.objects.get(name = A).delete()#delete PROTEINA FROM ToCheck DB