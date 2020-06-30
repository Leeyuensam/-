from django.db import models


class User(models.Model):
    username = models.CharField(max_length=32,unique=True)
    password = models.CharField(max_length=32)

    class Meta:
        verbose_name = verbose_name_plural = '用户信息表'

    def __str__(self):
        return self.username
# Create your models here.
