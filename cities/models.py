from django.db import models

# Create your models here.
from django.urls import reverse_lazy


class City(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название города')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name']

    def get_absolute_url(self):
        return reverse_lazy('cities:detail', kwargs={'pk': self.pk})

