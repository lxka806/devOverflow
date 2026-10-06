from django import forms


class QuestionForm(forms.Form):
    title = forms.CharField(max_length=200)
    context = forms.CharField(widget=forms.Textarea)


class add_comment(forms.Form):
    context = forms.CharField(widget=forms.Textarea)