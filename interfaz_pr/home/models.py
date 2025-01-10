from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_created = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created']

    def _str_(self):
        return self.title
