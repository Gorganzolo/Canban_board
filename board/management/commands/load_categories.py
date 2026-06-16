from django.core.management.base import BaseCommand
from board.models import Category

class Command(BaseCommand):
    help = 'Предзаполнение базы данных начальными категориями'

    def handle(self, *args, **kwargs):
        categories = [
            "Танки",
            "Хилы",
            "ДД",
            "Торговцы",
            "Гилдмастеры",
            "Квестгиверы",
            "Кузнецы",
            "Кожевники",
            "Зельевары",
            "Мастера заклинаний"
        ]

        for cat_name in categories:
            cat, created = Category.objects.get_or_create(name=cat_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создана категория: {cat_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Категория уже существует: {cat_name}'))

        self.stdout.write(self.style.SUCCESS('Предзаполнение категорий завершено.'))