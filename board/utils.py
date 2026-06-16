from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_new_reply_email(reply):
    subject = f'Новый отклик на ваше объявление "{reply.post.title}"'
    message = f'Здравствуйте!\n\nНа ваше объявление "{reply.post.title}" поступил новый отклик от пользователя {reply.author.email}.\n\nТекст отклика:\n{reply.text}\n\nПосмотреть все отклики вы можете в личном кабинете.'

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@mmorpgboard.com',
        [reply.post.author.email],
        fail_silently=False,
    )

def send_reply_accepted_email(reply):
    subject = f'Ваш отклик на объявление "{reply.post.title}" принят!'
    message = f'Здравствуйте!\n\nАвтор объявления "{reply.post.title}" принял ваш отклик.\n\nТекст вашего отклика:\n{reply.text}'

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@mmorpgboard.com',
        [reply.author.email],
        fail_silently=False,
    )