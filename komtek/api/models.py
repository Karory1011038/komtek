from django.db import models

# My models.
from rest_framework import serializers


class Handbook(models.Model):
    uid = models.IntegerField(verbose_name='Идентификатор',default=0)
    name = models.CharField(max_length=250, verbose_name='Наименование')
    short_name = models.CharField(max_length=100, verbose_name='Короткое Наименование')
    description = models.TextField(verbose_name='Описание')
    version = models.CharField(max_length=100, verbose_name='Версия', null=False)
    date = models.DateField(verbose_name='Дата начала действия справочника этой версии', auto_now_add=True)

    class Meta:
        verbose_name = 'Справочник'
        verbose_name_plural = 'Справочники'

    def __str__(self):
        return self.name


class HandbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Handbook
        fields = ('id', 'name', 'short_name', 'description', 'version', 'date')


class Item(models.Model):
    handbook = models.ForeignKey(Handbook, on_delete=models.CASCADE, verbose_name='Справочник',related_name='items')
    code = models.CharField(max_length=100, verbose_name='Код элемента', null=False)
    value = models.CharField(max_length=100, verbose_name='Значение элемента', null=False)

    class Meta:
        verbose_name = 'Элемент справочника'
        verbose_name_plural = 'Элементы справочника'

    def __str__(self):
        return self.handbook.short_name + ' ' + str(self.id)


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'handbook', 'code', 'value')
