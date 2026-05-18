import requests
import json
import logging
from .models import MegaPayConfig, MegaPayTransaction

logger = logging.getLogger(__name__)


def get_active_config():
    try:
        return MegaPayConfig.objects.get(is_active=True)
    except MegaPayConfig.DoesNotExist:
        return None


def initiate_stk_push(phone_number, amount, loan_amount, applicant_name, national_id, loan_type):
    """
    Initiate STK Push payment via MegaPay API.
    
    Args:
        phone_number: Customer phone number
        amount: Amount to charge (tax/fee)
        loan_amount: Loan amount being requested
        applicant_name: Full name of applicant
        national_id: National ID number
        loan_type: Type of loan
    
    Returns:
        dict: Success/failure response with transaction details
    """
    config = get_active_config()
    if not config:
        return {"success": False, "error": "MegaPay not configured. Contact admin."}

    # Normalize phone number to 254XXXXXXXXX
    phone = phone_number.strip().replace(" ", "").replace("-", "")
    if phone.startswith("0"):
        phone = "254" + phone[1:]
    elif phone.startswith("+"):
        phone = phone[1:]

    # Prepare MegaPay request
    payload = {
        "api_key": config.api_key,
        "email": config.email,
        "amount": int(amount),
        "msisdn": phone,
        "reference": f"{national_id}-{loan_type}",
    }

    headers = {
        "Content-Type": "application/json",
    }

    url = "https://megapay.co.ke/backend/v1/initiatestk"

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        data = response.json()
        logger.info(f"MegaPay STK Push response: {data}")

        # Create transaction record
        transaction = MegaPayTransaction.objects.create(
            phone_number=phone_number,
            amount=amount,
            loan_amount=loan_amount,
            applicant_name=applicant_name,
            national_id=national_id,
            loan_type=loan_type,
            transaction_request_id=data.get("transaction_request_id", ""),
            response_code=data.get("success", ""),
            response_description=data.get("massage", ""),
            customer_message=data.get("massage", "Check your phone for the M-Pesa prompt."),
        )

        if data.get("success") == "200":
            return {
                "success": True,
                "transaction_request_id": data.get("transaction_request_id"),
                "customer_message": data.get("massage", "Check your phone for the M-Pesa prompt."),
                "transaction_id": transaction.id,
            }
        else:
            transaction.status = "failed"
            transaction.save()
            return {"success": False, "error": data.get("massage", "STK push failed.")}

    except Exception as e:
        logger.error(f"STK Push exception: {e}")
        return {"success": False, "error": "Network error. Please try again."}


def check_transaction_status(transaction_request_id):
    """
    Check the status of a transaction via MegaPay API.
    
    Args:
        transaction_request_id: The transaction request ID from initiation
    
    Returns:
        dict: Transaction status details
    """
    config = get_active_config()
    if not config:
        return {"status": "error", "error": "MegaPay not configured."}

    payload = {
        "api_key": config.api_key,
        "email": config.email,
        "transaction_request_id": transaction_request_id,
    }

    headers = {
        "Content-Type": "application/json",
    }

    url = "https://megapay.co.ke/backend/v1/transactionstatus"

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        data = response.json()
        logger.info(f"MegaPay Status Check response: {data}")

        try:
            transaction = MegaPayTransaction.objects.get(transaction_request_id=transaction_request_id)
            return {
                "status": transaction.status,
                "receipt": transaction.megapay_receipt_number,
                "result_desc": transaction.result_desc,
            }
        except MegaPayTransaction.DoesNotExist:
            return {"status": "pending"}

    except Exception as e:
        logger.error(f"Status check exception: {e}")
        return {"status": "error", "error": str(e)}
