from django.db import models
from django.urls import reverse


class Dialogs(models.Model):
    id_dial = models.AutoField(primary_key=True)
    u1 = models.ForeignKey('user.CustomUserModel', related_name='sender', on_delete=models.DO_NOTHING)
    u2 = models.ForeignKey('user.CustomUserModel', related_name='receiver', on_delete=models.DO_NOTHING)
    last_message = models.TextField()

    def change_last(self, newlast):
        self.last_message = newlast

    def get_absolute_url(self):
        return reverse('mes_id', args=[str(self.id_dial)])

    def __str__(self):
        formalized = 'FROM:{}\nTO:{}\nLAST MESSAGE:{}'.format(str(self.u1), str(self.u2), str(self.last_message))
        return formalized

    def save(self, *args, **kwargs):
        try:
            return super().save(*args, **kwargs)
        except:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied()
    class Meta:
        unique_together=('u1','u2')
