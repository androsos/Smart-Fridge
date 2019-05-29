from django import forms

class HomeForm(forms.Form):
	barcode = forms.IntegerField()

#class WishlistForm(forms.Form):
