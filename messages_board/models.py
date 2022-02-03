from django.db import models
from django.urls import reverse
from . import json_parser


class Dialogs(models.Model):
    id_dial = models.AutoField(primary_key=True)
    u1 = models.ForeignKey('user.CustomUserModel',
                           related_name='%(app_label)s_%(class)s_u1_related',
                           on_delete=models.DO_NOTHING)
    u2 = models.ForeignKey('user.CustomUserModel',
                           related_name='%(app_label)s_%(class)s_u2_related',
                           on_delete=models.DO_NOTHING)
    last_message = models.TextField()

    def change_last(self, newlast):
        self.last_message = newlast

    def get_absolute_url(self):
        return reverse('detail_dialog', args=[str(self.id_dial)])

    def __str__(self):
        formalized = 'FROM:{}\nTO:{}\nLAST MESSAGE:{}'.format(str(self.u1), str(self.u2), str(self.last_message))
        return formalized

    def in_dial(self, user):
        return [self.u1.pk==user.pk, self.u2.pk==user.pk]

    def get_both_users(self):
        return [self.u1, self.u2]

    def delete(self, using=None, keep_parents=True, full=True):
        if full:
            json_parser.delete_json(str(self.id_dial))
        return super().delete(using, keep_parents)

    class Meta:
        unique_together=('u1','u2')
