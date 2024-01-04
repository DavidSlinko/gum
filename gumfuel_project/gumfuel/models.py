from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название сплитов')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Сплит'
        verbose_name_plural = 'Сплиты'


class Exercise(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название упражнения')
    content = models.TextField(verbose_name='Краткое описание упражнения')
    content_full = models.TextField(verbose_name='Полное описание упражнения')
    photo1 = models.ImageField(upload_to='photos/', verbose_name='Первое фото', blank=True, null=True)
    photo2 = models.ImageField(upload_to='photos/', verbose_name='Второе фото', blank=True, null=True)
    photo3 = models.ImageField(upload_to='photos/', verbose_name='Третье фото', blank=True, null=True)
    created_add = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория сплита')

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автоор', blank=True, null=True)

    link_video = models.CharField(max_length=250, blank=True, null=True, verbose_name='Ссылка видео')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('gumfuel_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Упражнение'
        verbose_name_plural = 'Упражнения'


# Модель кеомментариев

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Комментатор')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, verbose_name='Упражнение')
    text = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

# Модель профиля

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name='Фото профиля')
    phone_number = models.CharField(max_length=30, blank=True, null=True, verbose_name='Номер телефона')
    about_me = models.CharField(max_length=200, blank=True, null=True, verbose_name='Осебе')
    published = models.BooleanField(default=True, verbose_name='Право на добовления постов')

    def __str__(self):
        return self.user.username

    # метод для получения фото профиля
    def get_photo(self):
        try:
            return self.photo.url
        except:
            return 'https://st3.depositphotos.com/15648834/17930/v/600/depositphotos_179308454-stock-illustration-unknown-person-silhouette-glasses-profile.jpg'


    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профиль'
