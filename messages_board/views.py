from django.shortcuts import render, reverse, redirect
from . import json_parser
from django.views.generic import View, DeleteView
from django.contrib.auth import get_user_model, get_user
from .forms import DialogCreateForm
from django.db.models import Q
from django.http import QueryDict, HttpResponse
import datetime
from .models import Dialogs
from django.urls import reverse_lazy

class MsgBoardView(View):
    model = Dialogs
    template_name = 'messages_board/messages_board.html'
    form = DialogCreateForm

    def get(self, request, *args, **kwargs):
        qset = self.model.objects.filter(Q(u1=request.user) | Q(u2=request.user))
        objects = qset.all()
        context = {
            'new_dial': self.form,
            'dialogs': objects,
            'u': request.user
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        d = request.POST.dict()
        d.update({'u1': get_user(request)})
        u2 = get_user_model().objects.get_by_natural_key(username=d['u2'])
        d.update({'u2': u2})
        newD = QueryDict('', mutable=True)
        newD.update(d)
        request.POST = newD
        try:
            try:
                obj = self.model.objects.filter(Q(u1=newD['u1'], u2=newD['u2'])|Q(u2=newD['u1'], u1=newD['u2'])).get()
            except:
                obj=self.model.objects.create(u1=newD['u1'], u2=newD['u2'], last_message='')
                obj.save()
            return redirect(obj.get_absolute_url())
        except:
            return redirect(reverse('404'))


class DialogView(View):
    template_name='messages_board/dialog.html'

    def get(self, request, *args, **kwargs):
        id_ = kwargs['pk']
        host = get_user(request)
        some_messages = []
        dial = Dialogs.objects.get(id_dial=id_)
        u2 = None
        # u2 is a user which not u1!
        if host.is_authenticated and dial.in_dial(host).count(False) != 2:
            try:
                u2 = dial.get_both_users()[dial.in_dial(host).index(False)]
            except:
                u2=dial.get_both_users()[0]
            jlib = None
            try:
                open(json_parser.BASE_JSONS + str(id_), 'r')
            except:
                jlib = json_parser.create_new_json(str(json_parser))
            jlib = json_parser.iterate_json(str(id_))
            for message in jlib:
                if type(message) != json_parser.ReturnToPreventErrors:
                    message['u1'] = get_user_model().objects.get(id=int(message['u1']))
                    message['u2'] = get_user_model().objects.get(id=int(message['u2']))
                    some_messages.append(message)

        elif dial.in_dial(host).count(False) == 2:
            return redirect(reverse('403'))
        context = {
            'msgs': some_messages,
            'oppon': u2
        }
        # u2=None if user not authorised (does not matter because redirected on 403)
        # or if u1=u2 then just send host (u1) explicitly
        if u2 is None:
            context.update({'oppon': host})
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        old = request.POST.dict()
        print(old)
        id_ = kwargs['pk']
        u1 = get_user(request)
        dial = Dialogs.objects.get(id_dial=id_)
        u2 = None
        if dial.u1 != u1.pk:
            u2 = dial.u1
        else:
            u2 = dial.u2
        u2 = u2.pk
        dial.last_message = old['message']
        json_parser.json_write(u1=u1.pk, u2=u2, message=dial.last_message, json_path=str(id_), time=str(datetime.datetime.now()))
        dial.save()
        return redirect(dial.get_absolute_url())


class DeleteDialogView(View):
    model = Dialogs

    def get(self, request,**kwargs):
        id_=kwargs['pk']
        user=get_user(request)
        dial=Dialogs.objects.get(id_dial=id_)
        if user.is_authenticated and user in dial.in_dial(user):
            dial.delete(full=True)
            return redirect(reverse('all_messages'))
        else:
            return redirect(reverse('403'))