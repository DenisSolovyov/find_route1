from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
from cities.models import City


class Train(models.Model):
    name = models.CharField(max_length=50, unique=True,
                            verbose_name='Название поезда')
    travel_time = models.PositiveSmallIntegerField(verbose_name='Время в пути')
    from_city = models.ForeignKey(City, on_delete=models.CASCADE,
                                  related_name='from_city_set',
                                  verbose_name='Город отправления')
    to_city = models.ForeignKey('cities.City', on_delete=models.CASCADE,
                                related_name='to_city_set',
                                verbose_name='Город прибытия')

    def __str__(self):
        return f'Поезд №{self.name} из города {self.from_city}'

    class Meta:
        verbose_name = 'Поезд'
        verbose_name_plural = 'Поезда'
        ordering = ['travel_time']

    def clean(self):
        """переопределяем метод для проверки существует ли уже такой же поезд"""

        if self.from_city == self.to_city:
            raise ValidationError('Измените город прибытия/отправления')
        qs = Train.objects.filter(from_city=self.from_city,
                                  to_city=self.to_city,
                                  travel_time=self.travel_time).exclude(
            pk=self.pk)
        """exclude исключает из queryset запись, которую мы проверяем 
                  (нужно для нормального редактирования записей)"""
        if qs.exists():
            """если запись есть"""
            raise ValidationError('Необходимо изменить время в пути')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        """super использует поведение класса"""


"""Данная валидация не сработает при массов сохранении записей 
(bulk) так как они не вызывают метод save()"""
