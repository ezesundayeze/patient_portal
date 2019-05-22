# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


# Create your models here.

class UserAgreement(models.Model):
    created_on = models.DateTimeField() # to be add when creating the doc
    accepted_on = models.DateTimeField(null=True) # to be added from the back end\
    accepted_by = models.IntegerField(null=True) # patient username id
    notes = models.TextField()
    active = models.BooleanField(help_text="Check this box to set the is note active, to deactivate it please un check this box.")

    class Meta:
        db_table = 'user_agreements'
