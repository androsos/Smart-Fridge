from django import forms

class HomeForm(forms.Form):
	barcode = forms.IntegerField()

#class WishlistForm(forms.Form):

DATE_CHOICES = (('Monday', 'Monday'), 
	('Tuesday', 'Tuesday'), 
	('Wednesday', 'Wednesday'), 
	('Thursday', 'Thursday'), 
	('Friday', 'Friday'), 
	('Saturday', 'Saturday'),
	)
TIME_CHOICES = [('10', '10:00'), 
	('11', '11:00'), 
	('12', '12:00'), 
	('13', '13:00'), 
	('14', '14:00'), 
	('15', '15:00'),
	]

class ScheduleForm(forms.Form):
	#scheduled_day= forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=DATE_CHOICES)
	scheduled_day= forms.CharField(label='Choose day', widget=forms.RadioSelect(choices=DATE_CHOICES))
	scheduled_time= forms.CharField(label='Choose time', widget=forms.RadioSelect(choices=TIME_CHOICES))
