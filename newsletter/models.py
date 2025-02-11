from django.db import models


class Newsletter(models.Model):
    email = models.EmailField(null=False, blank=False, unique=True)

    def __str__(self):
        return self.email
