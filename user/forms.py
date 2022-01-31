from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from .models import CustomUserModel
from django.forms import DateInput, CharField, Form, EmailField


class CustomUserCreationForm(UserCreationForm):
    birth_date=DateInput()
    class Meta(UserCreationForm.Meta):
        model = CustomUserModel
        fields = UserCreationForm.Meta.fields+('birth_date',)


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