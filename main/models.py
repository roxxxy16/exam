from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """Расширенный профиль пользователя — ФИО, дата рождения, телефон."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField('ФИО', max_length=200)
    birth_date = models.DateField('Дата рождения')
    phone = models.CharField('Телефон', max_length=20)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'{self.full_name} ({self.user.username})'


class Application(models.Model):
    """Заявка пользователя на курс обучения вождению речного транспорта."""

    TRANSPORT_CHOICES = [
        ('boat', 'Катер'),
        ('cruise', 'Круизный лайнер'),
        ('yacht', 'Яхта'),
    ]

    PAYMENT_CHOICES = [
        ('card', 'Банковская карта'),
        ('cash', 'Наличные'),
        ('transfer', 'Безналичный перевод'),
    ]

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_DONE = 'done'
    STATUS_CHOICES = [
        (STATUS_NEW, 'Новая'),
        (STATUS_IN_PROGRESS, 'Идет обучение'),
        (STATUS_DONE, 'Обучение завершено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    transport_type = models.CharField('Вид транспорта', max_length=20, choices=TRANSPORT_CHOICES)
    start_date = models.DateField('Дата начала обучения')
    payment_method = models.CharField('Способ оплаты', max_length=20, choices=PAYMENT_CHOICES)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    created_at = models.DateTimeField('Создана', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f'Заявка №{self.pk} — {self.get_transport_type_display()}'

    @property
    def can_be_reviewed(self):
        """Отзыв доступен только после смены статуса администратором."""
        return self.status != self.STATUS_NEW and not hasattr(self, 'review')


class Review(models.Model):
    """Отзыв пользователя об оказанной услуге обучения."""
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='review')
    rating = models.PositiveSmallIntegerField('Оценка', choices=[(i, str(i)) for i in range(1, 6)])
    text = models.TextField('Текст отзыва')
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Отзыв к заявке №{self.application_id}'
