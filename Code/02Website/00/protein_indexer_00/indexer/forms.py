from django import forms


class AbstractForm(forms.Form):
	author_name = forms.CharField(label='Author name', max_length=100)
	abstract_text = forms.CharField(widget=forms.Textarea,label='abstract text')
	protein_list = forms.CharField(label='protein list', max_length=100)
	website_address = forms.CharField(label='website address', max_length=100)