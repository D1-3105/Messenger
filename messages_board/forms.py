from django.forms import ModelForm, CharField
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import Dialogs


class DialogCreateForm(ModelForm):
    u2 =CharField()
    last_message=''

    def __init__(self, d=None, **kwargs):
        if d!=None:
            self.u1 = d.pop('u1', None)
            u2=d.pop('u2', None)
            try:
                self.u2=get_user_model().objects.get_by_natural_key(username=u2)
            except:
                self.u2=self.u1
        else:
            self.u1=None
            self.u2=None
            self.last_message=None
        super(DialogCreateForm, self).__init__(kwargs)

    def save(self, commit=True):
        obj = super(DialogCreateForm, self).save(commit=True)
        obj.u1 = self.u1
        obj.u2 = get_user_model().objects.get(username=self.u2)
        if commit:
            obj.save()
        return obj

    def is_valid(self):
        check=[self.u1, self.u2, self.last_message]
        if None not in check:
            return True
        else:
            return False

    def __str__(self):
        formalized={
            'u1':self.u1,
            'u2':self.u2,
            'last_message':self.last_message,
        }
        return formalized

    class Meta:
        model = Dialogs
        fields=('u2',)