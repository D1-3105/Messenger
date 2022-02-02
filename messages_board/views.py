from django.shortcuts import render, reverse, redirect
from . import json_parser
from django.views.generic import View
from .models import Dialogs
from django.contrib.auth import get_user_model, get_user
from .forms import DialogCreateForm
from django.db.models import Q
from django.http import QueryDict

class MsgBoardView(View):
    model = Dialogs
    template_name = 'messages_board/messages_board.html'
    form=DialogCreateForm
    def get(self, request, *args, **kwargs):
        qset=self.model.objects.filter(Q(u1=request.user)|Q(u2=request.user))
        objects=qset.all()
        context={
            'new_dial':self.form,
            'dialogs':objects,
            'u':request.user
        }
        return render(request, self.template_name,context)
    def post(self, request, *args, **kwargs):
        d=request.POST.dict()
        d.update({'u1':get_user(request)})
        u2=get_user_model().objects.get_by_natural_key(username=d['u2'])
        d.update({'u2':u2})
        newD=QueryDict('', mutable=True)
        newD.update(d)
        request.POST=newD
        try:
            obj=self.model.objects.get_or_create(u1=newD['u1'], u2=newD['u2'], last_message='')
            return redirect(reverse('detail_dialog'), args=obj.id_dial)
        except:
            return redirect(reverse('404'))


class DialogView(View):
    def get(self, request, *args, **kwargs):
        id_ = kwargs['pk']
        host = request.user
        some_messages = []
        if host.is_authenticated and Dialogs.objects.get(id_dial=id_).in_dial(host)!=0:
            host = host.username
            jlib=None
            try:
                open(json_parser.BASE_JSONS+str(id_), 'r')
            except:
                jlib=json_parser.create_new_json(str(json_parser))
            jlib= json_parser.iterate_json(str(id_))
            for message in jlib:
                if type(message) != json_parser.ReturnToPreventErrors:
                    some_messages.append(message)

        elif Dialogs.objects.get(id_dial=id_).in_dial(host)==0:
            return redirect(reverse('403'))
        context = {
            'msgs': some_messages[::-1],
        }
        return render(request, 'messages_board/dialog.html', context)