from django import forms


class ReviewForm(forms.Form):
    rating = forms.TextField(label='Rate')
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    content_type_id = forms.IntegerField(widget=forms.HiddenInput)
    next = forms.CharField(widget=forms.HiddenInput)