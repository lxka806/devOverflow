from django import forms


class QuestionForm(forms.Form):
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            "placeholder": "e.g. How do I handle async state in React?",
            "autocomplete": "off",
        }),
    )
    context = forms.CharField(widget=forms.Textarea(attrs={
        "rows": 10,
        "placeholder": "Include what you tried, what you expected, and any relevant code or error messages.",
    }))


class add_comment(forms.Form):
    context = forms.CharField(widget=forms.Textarea(attrs={
        "rows": 4,
        "placeholder": "Share a helpful answer or clarification...",
    }))