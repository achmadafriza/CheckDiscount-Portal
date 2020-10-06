from django import forms

class UpdateTierForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput())
    minimumTransaction = forms.IntegerField(min_value=10000, max_value=20000000)
    maximumTransaction = forms.IntegerField(min_value=10000, max_value=20000000)
    probability = forms.FloatField(min_value=0, max_value=1)
    discount = forms.FloatField(min_value=0, max_value=1)

class DeleteTierForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput())

class CreateTierForm(forms.Form):
    minimumTransaction = forms.IntegerField(min_value=10000, max_value=20000000)
    maximumTransaction = forms.IntegerField(min_value=10000, max_value=20000000)
    probability = forms.FloatField(min_value=0, max_value=1)
    discount = forms.FloatField(min_value=0, max_value=1)