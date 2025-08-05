from django.urls import path
from .views import create_invoice, invoice_pdf, invoice_history, invoice_detail

app_name = 'billing'

urlpatterns = [
    path('', create_invoice, name='create_invoice'),
    path('history/', invoice_history, name='invoice_history'),
    path('invoice/<int:invoice_id>/', invoice_detail, name='invoice_detail'),
    path('invoice/<int:invoice_id>/pdf/', invoice_pdf, name='invoice_pdf'),
    

]
