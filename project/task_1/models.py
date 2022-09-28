from django.db import models


class InputsValues(models.Model):
    json = models.JSONField()
