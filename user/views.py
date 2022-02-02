from django.shortcuts import render
from django.views.generic import CreateView, FormView
from .forms import CustomUserCreationForm, ResetEmailForm, CustomUserChangeForm
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from .models import CustomUserModel
from django.http.request import QueryDict
from django.core.mail import send_mail

email_from='example@gmail.com'

class SignUpView(CreateView):
    template_name = 'user/sign_up.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')


class ResetViaEmailView(FormView):
    template_name = 'user/reset_via_email.html'
    form_class = ResetEmailForm
    success_url = reverse_lazy('thanks')
    def post(self, request, *args, **kwargs):
        old = request.POST.dict()
        user = CustomUserModel.objects.get_by_natural_key(username=old['username'])
        token = user.token
        old['token'] = token
        newQD = QueryDict('', mutable=True)
        newQD.update(old)
        request.POST = newQD
        send_my_mail('Recover link!', 'user/reset_message.html',
                     email_from, old['email'], old['username'], '{}{}/{}'.format(
                request.build_absolute_uri('/accounts/reset_me/'),old['username'],token))
        return super().post(request, *args, **kwargs)
def send_my_mail(subject, template:str, from_, to, username, url):
    content={
        'username':username,
        'recover_link':url
    }
    html_part=render_to_string(template, content)
    send_mail(subject, '', from_, [to], html_message=html_part)


class ResetPWView(FormView):
    template_name = 'user/reset.html'
    success_url = reverse_lazy('thanks')
    form_class = CustomUserChangeForm
    def get(self, request, *args, **kwargs):
        un=kwargs['username']
        tok=kwargs['token']
        try:
            user=CustomUserModel.objects.get_by_natural_key(un)
            if user.token==tok:
                self.template_name='user/reset.html'
        except:
            self.template_name='403.html'
        return super().get(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        un=kwargs['username']
        pw=request.POST.dict()['password']
        if self.get_form().is_valid():
            user = CustomUserModel.objects.get_by_natural_key(un)
            user.set_password(pw)
            user.change_token()
            user.save()
        return super().post(request, *args, **kwargs)