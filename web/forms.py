from django import forms

from web.models import Record


class RecordForm(forms.ModelForm):
    def save(self, *args, **kwargs):
        self.instance.user = self.initial['user']
        return super(RecordForm, self).save(*args, **kwargs)

    class Meta:
        model = Record
        fields = ('title', 'text')


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())