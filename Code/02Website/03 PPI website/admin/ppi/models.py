from django.db import models

class ToCheck(models.Model):
	name = models.CharField(max_length=50)
	
	def __str__(self):
		return self.name

class CurrentCheckList(models.Model):
	name = models.CharField(max_length=50)
	
	def __str__(self):
		return self.name

class Protein(models.Model):

	name = models.CharField(max_length=64)
	interactions = models.ManyToManyField("self", symmetrical=True, through="Interaction")

	def __str__(self):
		return self.name


class Interaction(models.Model):

	frm = models.ForeignKey(
		Protein, on_delete=models.CASCADE, related_name="interactions_to"
	)
	to = models.ForeignKey(
		Protein, on_delete=models.CASCADE, related_name="interactions_from"
	)
	publication = models.CharField(max_length=64)
	
	abstract = models.CharField(max_length=64)
	
	link = models.CharField(max_length=64)

	def __str__(self):
		return f"{self.publication}: {self.frm} <-> {self.to}"
