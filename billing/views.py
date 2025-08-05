from django.shortcuts import render, redirect
from .forms import InvoiceForm
from .models import Invoice
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import FileResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

def calculate_price(data):
    gold_weight = data['gross_weight']
    base_gold_value = gold_weight * data['gold_rate']
    making_charge = base_gold_value * data['making_charge_percent'] / 100
    subtotal = base_gold_value + making_charge + data['stone_price']
    gst = subtotal * 0.03
    cgst = sgst = gst / 2
    total = subtotal + gst
    return total, cgst, sgst

@login_required
def create_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            total, cgst, sgst = calculate_price(form.cleaned_data)
            invoice.total_price = total
            invoice.cgst = cgst
            invoice.sgst = sgst
            invoice.save()
            return redirect('billing:invoice_detail', invoice_id=invoice.id)
    else:
        form = InvoiceForm()
    return render(request, 'billing_form.html', {'form': form})

@login_required
def invoice_history(request):
    query = request.GET.get('q', '')
    invoices = Invoice.objects.filter(
        Q(customer_name__icontains=query) |
        Q(mobile_number__icontains=query)
    ).order_by('-date')
    return render(request, 'billing_history.html', {'invoices': invoices, 'query': query})

@login_required
def invoice_pdf(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Jewellery Shop Invoice", styles['Title']))
    elements.append(Spacer(1, 12))

    for field in [
        f"Customer: {invoice.customer_name}",
        f"Mobile: {invoice.mobile_number}",
        # f"Ornament: {invoice.ornament_type}",
        f"Gross Weight: {invoice.gross_weight}g",
        f"Stone Weight: {invoice.stone_weight}g",
        f"Gold Rate: ₹{invoice.gold_rate}",
        f"Stone Price: ₹{invoice.stone_price}",
        f"Making Charge: {invoice.making_charge_percent}%",
        f"CGST: ₹{invoice.cgst:.2f}",
        f"SGST: ₹{invoice.sgst:.2f}",
        f"Total Price: ₹{invoice.total_price:.2f}"
    ]:
        elements.append(Paragraph(field, styles['Normal']))
        elements.append(Spacer(1, 8))

    doc.build(elements)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='invoice.pdf')


@login_required
def invoice_detail(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    return render(request, 'invoice_detail.html', {'invoice': invoice})
