import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import MegaPayTransaction
from .services import initiate_stk_push, check_transaction_status

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def initiate_stk_push_view(request):
    """Initiate STK Push payment via MegaPay."""
    try:
        data = json.loads(request.body)
        phone = data.get('phone', '').strip()
        amount = data.get('amount', 0)
        loan_amount = data.get('loan_amount', 0)
        applicant_name = data.get('name', '')
        national_id = data.get('national_id', '')
        loan_type = data.get('loan_type', '')

        if not phone or not amount:
            return JsonResponse({'success': False, 'error': 'Phone and amount are required.'}, status=400)

        result = initiate_stk_push(phone, amount, loan_amount, applicant_name, national_id, loan_type)
        return JsonResponse(result)
    except Exception as e:
        logger.error(f"STK push view error: {e}")
        return JsonResponse({'success': False, 'error': 'Server error. Please try again.'}, status=500)


@csrf_exempt
def megapay_callback(request):
    """Receives MegaPay payment callback webhook."""
    try:
        data = json.loads(request.body)
        logger.info(f"MegaPay Callback received: {json.dumps(data)}")

        # MegaPay callback format
        transaction_id = data.get('TransactionID', '')
        response_code = str(data.get('ResponseCode', ''))
        response_desc = data.get('ResponseDescription', '')
        transaction_request_id = data.get('TransactionID', '')
        receipt = data.get('TransactionReceipt', '')
        transaction_date = data.get('TransactionDate', '')

        try:
            transaction = MegaPayTransaction.objects.get(transaction_request_id=transaction_request_id)
            transaction.result_code = response_code
            transaction.result_desc = response_desc

            if response_code == '0':
                transaction.status = 'success'
                transaction.megapay_receipt_number = receipt
                transaction.transaction_date = transaction_date
            elif response_code == '1032':
                transaction.status = 'cancelled'
            elif response_code == '1037':
                transaction.status = 'timeout'
            else:
                transaction.status = 'failed'

            transaction.save()
        except MegaPayTransaction.DoesNotExist:
            logger.warning(f"Transaction not found for TransactionID: {transaction_request_id}")

    except Exception as e:
        logger.error(f"Callback processing error: {e}")

    return JsonResponse({'ResponseCode': 0, 'ResponseDescription': 'Accepted'})


def transaction_status(request, transaction_request_id):
    """Check transaction status."""
    result = check_transaction_status(transaction_request_id)
    return JsonResponse(result)
