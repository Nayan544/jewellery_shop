from django import forms
from .models import Invoice

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'customer_name', 'mobile_number',
            'gross_weight', 'stone_type', 'gold_rate', 'stone_price',
            'making_charge_percent'
        ]
