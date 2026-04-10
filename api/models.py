from django.db import models


class Student(models.Model):
    full_name = models.CharField(
        max_length=255,
        verbose_name="ФИО",
        help_text="Введите полное имя студента"
    )
    group = models.CharField(max_length=20, verbose_name="Группа")
    email = models.EmailField(unique=True, verbose_name="Email")
    total_points = models.PositiveIntegerField(
        default=0,
        verbose_name="Суммарные баллы"
    )

    def __str__(self):
        return self.full_name


class Event(models.Model):
    LEVEL_CHOICES = [
        ('university', 'Внутривузовский'),
        ('regional', 'Региональный'),
        ('national', 'Всероссийский'),
    ]

    name = models.CharField(max_length=255, verbose_name="Название мероприятия")
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        verbose_name="Уровень"
    )
    date = models.DateField(verbose_name="Дата проведения")

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"


class Request(models.Model):
    ROLE_CHOICES = [
        ('participant', 'Участник'),
        ('winner', 'Победитель/Призер'),
        ('organizer', 'Организатор'),
    ]
    STATUS_CHOICES = [
        ('pending', 'На модерации'),
        ('approved', 'Одобрена'),
        ('rejected', 'Отклонена'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='requests'
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    supporting_document = models.FileField(
        upload_to='documents/',
        blank=True,
        null=True,
        verbose_name="Подтверждающий документ"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    moderated_at = models.DateTimeField(null=True, blank=True)
    points_awarded = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('student', 'event')

    def __str__(self):
        return f"Заявка {self.student.full_name} - {self.event.name}"
