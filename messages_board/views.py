from django.shortcuts import render, reverse, redirect
from .utils.jsons import json_parser
from django.views.generic import View
from .models import Dialogs
from .forms import DialogCreateForm
from django.db.models import Q


class MsgBoardView(View):
    model = Dialogs
    template_name = 'messages_board/messages_board.html'
    form=DialogCreateForm
    def get(self, request, *args, **kwargs):
        qset=self.model.objects.filter(Q(u1=request.user)|Q(u2=request.user))
        objects=qset.all()
        self.form=self.form()
        context={
            'new_dial':self.form,
            'dialogs':objects,
            'u':request.user
        }
        return render(request, self.template_name,context)
    def post(self, request, *args, **kwargs):
        d=request.POST.dict()
        d.update({'u1':request.user})
        self.form=self.form(d=d)
        dial=''
        if self.form.is_valid():
            try:
                dial=self.form.save(commit=True)
            except:
                dial=self.model.objects.filter(Q(u1=dial.u1, u2=dial.u2)|Q(u2=dial.u1, u1=dial.u2))
                return redirect(reverse('detail_dialog', args=dial.id_dial))
            return redirect(reverse('detail_dialog', args=dial.id_dial))
        return redirect(reverse('404'))


def dialog_view(request, *args, **kwargs):
    id_ = kwargs[0]
    host = request.user
    some_messages = []
    if host.is_authenticated():
        host = host.username
        for message in json_parser.iterate_json(str(id_)):
            if type(message) != json_parser.ReturnToPreventErrors:
                some_messages.append(message)
    context={
        'msgs':some_messages,
    }
    return render(request, 'messages_board/dialog.html', context)