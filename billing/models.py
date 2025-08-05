from django.db import models

class Invoice(models.Model):
    customer_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    # ornament_type = models.CharField(max_length=100)
    gross_weight = models.FloatField()
    stone_type = models.CharField(max_length=100)
    gold_rate = models.FloatField()
    stone_price = models.FloatField()
    making_charge_percent = models.FloatField()
    cgst = models.FloatField()
    sgst = models.FloatField()
    total_price = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.date.strftime('%d-%m-%Y')}"
