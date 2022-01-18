from django import forms
from common.mailgun import Mailgun


class ContactForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control col-9', 'placeholder': 'name@example.com'}))

    def send_email(self):
        message = self.cleaned_data['message']
        email = self.cleaned_data['email']
        Mailgun.send_mail(email, message)
