from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from .models import CustomUserModel
from django.forms import DateField, CharField, Form, EmailField,\
    DateInput, PasswordInput, EmailInput, TextInput


class CustomUserCreationForm(UserCreationForm):
    username=CharField(
        widget=TextInput(attrs={
            'type':'text',
            'class': 'form-control',
            'placeholder': 'Username',
        })
    )
    email=CharField(
        widget=EmailInput(attrs={
            'type':'email',
            'class':'form-control',
            'placeholder':'Email',
        })
    )
    birth_date=DateField(
        widget=DateInput(attrs={
            'type':'date',
            'class':'form-control'
        })
    )
    password1 = CharField(
        widget=PasswordInput(attrs={
            'type':'password',
            'class':'form-control',
            'placeholder':'Password'
        })
    )
    password2 = CharField(
        widget=PasswordInput(attrs={
            'type': 'password',
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )
    class Meta(UserCreationForm.Meta):
        model = CustomUserModel
        fields = UserCreationForm.Meta.fields+('birth_date','email',)

class CustomUserChangeForm(UserChangeForm):
    password = CharField()
    confirm=CharField()
    class Meta(UserChangeForm.Meta):
        model = CustomUserModel
        fields= ('password', 'confirm')
    def is_valid(self):
        if self.data['password'] == self.data['confirm']:
            return super().is_valid()
        return False

class ResetEmailForm(Form):
    username=CharField()
    email=EmailField()
    class Meta:
        model = CustomUserModel
        fields = ('username', 'email')
    def is_valid(self):
        if CustomUserModel.objects.get_by_natural_key(username=self.data['username']).email==self.data['email'] \
                and self.data['email']!=None:
            return super().is_valid()
        return False