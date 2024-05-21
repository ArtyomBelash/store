from django.db import models
from django.urls import reverse
from store import settings


def upload_to(instance, filename):
    return f'products/{instance.name}/{filename}'


class Product(models.Model):
    name = models.CharField(max_length=120, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    short_description = models.CharField(max_length=255, verbose_name='Краткое описание"', blank=True, null=True)
    slug = models.SlugField(verbose_name='Url', unique=True, db_index=True)
    image = models.ImageField(upload_to=upload_to, verbose_name='Фото', blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products',
                                 verbose_name='Категория')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', args=[self.slug])

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Category(models.Model):
    name = models.CharField(max_length=120, verbose_name='')
    description = models.TextField()
    slug = models.SlugField(unique=True, verbose_name='')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', args=[self.slug])

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
    body = models.TextField('Коментарий')
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'Автор: {self.author.username if self.author else "Удаленный аккаунт"} - Продукт: {self.product}'

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
