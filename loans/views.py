import json
import logging
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SiteConfig, LoanAmount, LoanApplication

logger = logging.getLogger(__name__)


def get_site_config():
    try:
        return SiteConfig.objects.get(is_active=True)
    except SiteConfig.DoesNotExist:
        return SiteConfig()


def home(request):
    config = get_site_config()
    return render(request, 'loans/home.html', {'config': config})


def apply_view(request):
    config = get_site_config()
    return render(request, 'loans/apply.html', {'config': config})


def processing_view(request):
    name = request.GET.get('name', '')
    phone = request.GET.get('phone', '')
    config = get_site_config()
    return render(request, 'loans/processing.html', {
        'config': config,
        'name': name,
        'phone': phone,
    })


def loan_offers_view(request):
    name = request.GET.get('name', '')
    phone = request.GET.get('phone', '')
    national_id = request.GET.get('national_id', '')
    loan_type = request.GET.get('loan_type', '')
    config = get_site_config()
    loan_amounts = LoanAmount.objects.filter(is_active=True)
    return render(request, 'loans/loan_offers.html', {
        'config': config,
        'name': name,
        'phone': phone,
        'national_id': national_id,
        'loan_type': loan_type,
        'loan_amounts': loan_amounts,
    })


def payment_success_view(request):
    config = get_site_config()
    receipt = request.GET.get('receipt', '')
    name = request.GET.get('name', '')
    amount = request.GET.get('amount', '')
    return render(request, 'loans/payment_success.html', {
        'config': config,
        'receipt': receipt,
        'name': name,
        'amount': amount,
    })


def privacy_view(request):
    config = get_site_config()
    return render(request, 'loans/privacy.html', {'config': config})


def terms_view(request):
    config = get_site_config()
    return render(request, 'loans/terms.html', {'config': config})


def contact_view(request):
    config = get_site_config()
    return render(request, 'loans/contact.html', {'config': config})


@csrf_exempt
def submit_application(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name', '').strip()
            phone = data.get('phone', '').strip()
            national_id = data.get('national_id', '').strip()
            loan_type = data.get('loan_type', '').strip()

            if not all([name, phone, national_id, loan_type]):
                return JsonResponse({'success': False, 'error': 'All fields are required.'}, status=400)

            ip = request.META.get('REMOTE_ADDR')
            LoanApplication.objects.create(
                full_name=name,
                phone_number=phone,
                national_id=national_id,
                loan_type=loan_type,
                ip_address=ip,
            )
            return JsonResponse({'success': True})
        except Exception as e:
            logger.error(f"Application submission error: {e}")
            return JsonResponse({'success': False, 'error': 'Server error.'}, status=500)
    return JsonResponse({'success': False, 'error': 'Method not allowed.'}, status=405)


def get_loan_amounts_api(request):
    amounts = list(LoanAmount.objects.filter(is_active=True).values('amount', 'tax_revenue'))
    return JsonResponse({'amounts': amounts})
