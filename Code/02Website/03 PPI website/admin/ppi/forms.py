from django import forms

depths= [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    ]

class SearchForm(forms.Form):
	searchbox = forms.CharField(label="",max_length=100)
	depth= forms.IntegerField(label="Interaction Depth", widget=forms.Select(choices=depths))