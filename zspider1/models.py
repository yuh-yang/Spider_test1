from django.db import models
# -*- coding: utf-8 -*-
# Create your models here.

class Website(models.Model):
    head = models.TextField()
    date = models.TextField()
    text = models.TextField()

    def __str__(self):
        return self.name

