from django.db import models
from django.urls import reverse


class Dialogs(models.Model):
    id_dial = models.AutoField(primary_key=True)
    u1 = models.ForeignKey('user.CustomUserModel', related_name='sender', on_delete=models.DO_NOTHING, blank=True)
    u2 = models.ForeignKey('user.CustomUserModel', related_name='receiver', on_delete=models.DO_NOTHING, blank=True)
    last_message = models.TextField()

    def change_last(self, newlast):
        self.last_message = newlast

    def get_absolute_url(self):
        return reverse('detail_dialog', args=[str(self.id_dial)])

    def __str__(self):
        formalized = 'FROM:{}\nTO:{}\nLAST MESSAGE:{}'.format(str(self.u1), str(self.u2), str(self.last_message))
        return formalized

    def in_dial(self, user):
        print(self.u1.pk == user.pk, self.u2.pk == user.pk)
        return (self.u1.pk==user.pk)+(self.u2.pk==user.pk)

    class Meta:
        unique_together=('u1','u2')
