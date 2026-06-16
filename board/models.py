from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name="Категория")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Post(models.Model):
    title = models.CharField(max_length=128, verbose_name="Заголовок")
    content = HTMLField(verbose_name="Текст объявления")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts", verbose_name="Автор")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="posts", verbose_name="Категория")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-created_at"]

class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="replies", verbose_name="Объявление")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="replies", verbose_name="Автор отклика")
    text = models.TextField(verbose_name="Текст отклика")
    is_accepted = models.BooleanField(default=False, verbose_name="Принят")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Отклик от {self.author} на {self.post}"

    class Meta:
        verbose_name = "Отклик"
        verbose_name_plural = "Отклики"
        ordering = ["-created_at"]
