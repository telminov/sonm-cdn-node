from django.db import models


# TODO подумать тут
class CMSLog(models.Model):
    ACTION_CHOICES = (
        ('check_delete_assets', 'Проверка удаленных файлов'),
    )

    message = models.CharField(max_length=255, verbose_name='Сообщение')
    action = models.CharField(max_length=255, verbose_name='Событие', choices=ACTION_CHOICES)
    dc = models.DateTimeField(verbose_name='Дата создания', editable=False, auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.action, self.message)

    class Meta:
        verbose_name = 'СMS лог'
        verbose_name_plural = 'СMS логи'
        ordering = ('-dc', )
