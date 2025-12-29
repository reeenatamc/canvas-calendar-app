from django.db import models
from django.utils import timezone
from datetime import timedelta


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('HIGH', '🔥 Urgente'),
        ('MEDIUM', '⚡ Normal'),
        ('LOW', '☕ Relajado'),
    ]

    # Datos de Canvas
    canvas_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField(null=True, blank=True)
    platform_type = models.CharField(max_length=50)  # 'assignment', 'quiz', etc.

    # Datos de Tu Asistente Personal
    is_completed = models.BooleanField(default=False)
    student_notes = models.TextField(blank=True, null=True)  # Para tus apuntes extra
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Lógica Inteligente: Auto-asignar prioridad según fecha
        if self.due_date and not self.is_completed:
            time_diff = self.due_date - timezone.now()
            if time_diff < timedelta(days=2):
                self.priority = 'HIGH'
            elif time_diff < timedelta(days=7):
                self.priority = 'MEDIUM'
            else:
                self.priority = 'LOW'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.priority})"