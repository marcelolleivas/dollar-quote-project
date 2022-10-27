from django.db import models


class Rate(models.Model):
    date = models.DateField(primary_key=True, null=False, blank=False)
    brazilian_real = models.DecimalField(
        null=False, blank=False, max_digits=9, decimal_places=2
    )
    euro = models.DecimalField(null=False, blank=False, max_digits=9, decimal_places=2)
    japanese_yen = models.DecimalField(
        null=False, blank=False, max_digits=9, decimal_places=2
    )
