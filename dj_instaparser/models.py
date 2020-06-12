from decimal import Decimal

from django.db import models


class InstagramAccount(models.Model):
    name = models.CharField(max_length=256, unique=True)


class Item(models.Model):
    account = models.ForeignKey(InstagramAccount, verbose_name='Аккаунт', on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=255, default='Название')
    description = models.TextField('Описание', blank=True, null=True)
    image_url = models.TextField('Адрес изображения', blank=True, null=True)
    price = models.DecimalField('Цена', decimal_places=2, max_digits=10, default=Decimal('0.00'))

    def __str__(self):
        return self.description
