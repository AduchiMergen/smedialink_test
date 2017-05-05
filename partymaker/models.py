from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import mail_admins
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class User(AbstractBaseUser):
    photo = models.ImageField(verbose_name='Фото')
    name = models.CharField(max_length=255, verbose_name='Имя')

    USERNAME_FIELD = 'name'


class Order(models.Model):
    DRINK_CHOICE = (
        (None, 'выберите пожалуйста'),
        (0, 'Чай'),
        (1, 'Кофе'),
        (2, 'Сок'),
    )
    MEMBER_CHOICE = (
        (None, 'выберите пожалуйста'),
        (True, 'Да'),
        (False, 'Нет'),
    )

    user = models.OneToOneField(User)
    is_member = models.BooleanField(choices=MEMBER_CHOICE, blank=False, null=False)
    drink = models.IntegerField(choices=DRINK_CHOICE, blank=False, null=False)


@receiver(post_save, sender=Order, dispatch_uid="new_order")
def send_new_order_email(instance, created, *args, **kwargs):
    if created:
        mail_admins(
            subject='Пользователь создал приглашение',
            message='Пользователь создал приглашение:\n'
                    'Пользователь: {name}\n'
                    'Присутствие: {member}\n'
                    'Напиток: {drink}'.format(
                        name=instance.user.name,
                        member=instance.get_is_member_display(),
                        drink=instance.get_drink_display(),
                    ),
            fail_silently=True,
        )


@receiver(post_delete, sender=Order, dispatch_uid="del_order")
def send_del_order_email(instance, *args, **kwargs):
    mail_admins(
        subject='Пользователь удалил приглашение',
        message='Пользователь удалил приглашение:\n'
                'Пользователь: {name}\n'
                'Присутствие: {member}\n'
                'Напиток: {drink}'.format(
                    name=instance.user.name,
                    member=instance.get_is_member_display(),
                    drink=instance.get_drink_display(),
                ),
        fail_silently=True,
    )
