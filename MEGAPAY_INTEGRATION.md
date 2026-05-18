# MegaPay Integration Guide

This document outlines the changes made to replace M-Pesa STK Push integration with MegaPay.

## Overview

The all-loans application has been successfully migrated from M-Pesa Daraja API to MegaPay API for payment processing. MegaPay provides a simpler, more straightforward integration for STK Push payments.

## Key Changes

### 1. Database Models (`mpesa/models.py`)

**Replaced:**
- `MpesaConfig` → `MegaPayConfig`
- `MpesaTransaction` → `MegaPayTransaction`

**MegaPayConfig Fields:**
- `api_key`: Your MegaPay API Key
- `email`: Email associated with your MegaPay account
- `callback_url`: Webhook URL for payment notifications
- `is_active`: Boolean flag for active configuration

**MegaPayTransaction Fields:**
- `transaction_request_id`: Unique identifier from MegaPay (replaces M-Pesa's `checkout_request_id`)
- `megapay_receipt_number`: Receipt number from successful payment
- Other fields remain similar for transaction tracking

### 2. Payment Service (`mpesa/services.py`)

**New Functions:**
- `initiate_stk_push()`: Initiates STK Push via MegaPay API
- `check_transaction_status()`: Polls transaction status from MegaPay

**API Endpoints Used:**
- **Initiate STK Push**: `POST https://megapay.co.ke/backend/v1/initiatestk`
- **Check Status**: `POST https://megapay.co.ke/backend/v1/transactionstatus`

**Request Format:**
```json
{
    "api_key": "your_api_key",
    "email": "your_email@example.com",
    "amount": 100,
    "msisdn": "254768783443",
    "reference": "unique_reference"
}
```

### 3. Views (`mpesa/views.py`)

**Updated Endpoints:**
- `initiate_stk_push_view()`: Handles STK Push initiation requests
- `megapay_callback()`: Processes MegaPay webhook callbacks
- `transaction_status()`: Returns current transaction status

**Callback Handling:**
MegaPay sends webhook notifications with the following structure:
```json
{
    "ResponseCode": 0,
    "ResponseDescription": "Success...",
    "TransactionID": "...",
    "TransactionReceipt": "...",
    "TransactionDate": "...",
    "Msisdn": "..."
}
```

### 4. Frontend Templates (`templates/loans/loan_offers.html`)

**JavaScript Updates:**
- Changed `checkoutRequestId` to `transactionRequestId`
- Updated API endpoint references from `/mpesa/status/{id}/` to use `transaction_request_id`
- Maintained same user experience and UI flow

### 5. URL Routing (`mpesa/urls.py`)

**Updated Routes:**
- `/mpesa/stk-push/` → `initiate_stk_push_view()`
- `/mpesa/callback/` → `megapay_callback()`
- `/mpesa/status/<transaction_request_id>/` → `transaction_status()`

### 6. Admin Interface (`mpesa/admin.py`)

**Updated Admin Classes:**
- `MegaPayConfigAdmin`: Manages MegaPay configuration
- `MegaPayTransactionAdmin`: Displays transaction history with MegaPay-specific fields

## Setup Instructions

### 1. Configure MegaPay Credentials

1. Log in to your [MegaPay Dashboard](https://megapay.co.ke/user)
2. Navigate to **Linked Accounts**
3. Copy your **API Key**
4. Note your registered **Email**

### 2. Add Configuration to Django Admin

1. Access Django admin at `/admin/`
2. Navigate to **MegaPay Configuration**
3. Create a new configuration with:
   - **Name**: Default MegaPay Config
   - **API Key**: Your MegaPay API key
   - **Email**: Your MegaPay account email
   - **Callback URL**: Your webhook URL (e.g., `https://yourdomain.com/mpesa/callback/`)
   - **Is Active**: Check this box

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Update Settings (if needed)

Ensure your Django settings include:
```python
INSTALLED_APPS = [
    # ...
    'mpesa',  # MegaPay payment app
]
```

## Payment Flow

1. **User Selects Loan**: Customer selects a loan amount on the offers page
2. **Initiate Payment**: Frontend calls `/mpesa/stk-push/` with payment details
3. **MegaPay STK Push**: MegaPay sends STK prompt to customer's phone
4. **Customer Enters PIN**: Customer enters M-Pesa PIN to authorize payment
5. **MegaPay Webhook**: MegaPay sends callback notification to your webhook URL
6. **Status Update**: Transaction status is updated in database
7. **Redirect to Success**: Frontend detects success and redirects to payment success page

## Response Codes

| Code | Description |
|------|-------------|
| 0 | Success. Request accepted for processing |
| 1 | The balance is insufficient for the transaction |
| 1032 | Request cancelled by user |
| 1037 | DS timeout user cannot be reached |
| 1025 | An error occurred while sending a push request |
| 9999 | An error occurred while sending a push request |
| 2001 | The initiator information is invalid |
| 1019 | Transaction has expired |
| 1001 | Unable to lock subscriber, a transaction is already in process |

## Testing

### Test with MegaPay Sandbox

MegaPay provides a sandbox environment for testing:
1. Use test phone numbers provided by MegaPay
2. Test API credentials are available in your dashboard
3. No real money is charged during testing

### Example Test Request

```bash
curl -X POST https://megapay.co.ke/backend/v1/initiatestk \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "your_test_api_key",
    "email": "test@example.com",
    "amount": 100,
    "msisdn": "254768783443",
    "reference": "test_ref_001"
  }'
```

## Error Handling

The application handles the following error scenarios:

1. **Missing Configuration**: Returns error if MegaPay config is not set up
2. **Network Errors**: Catches connection timeouts and displays user-friendly messages
3. **Invalid Credentials**: MegaPay returns specific error codes for authentication failures
4. **Transaction Timeout**: Polls for 30 attempts (90 seconds) before timing out

## Logging

All MegaPay API calls are logged for debugging:
- Request/response data
- Errors and exceptions
- Callback processing

Check logs at: `logs/django.log` (if configured)

## Migration from M-Pesa

If you're migrating from M-Pesa:

1. **Backup existing data**: Export M-Pesa transactions before running migrations
2. **Run migrations**: This will create new MegaPay tables
3. **Update configuration**: Add MegaPay credentials in admin
4. **Test thoroughly**: Verify payment flow works end-to-end
5. **Monitor**: Watch logs and transaction history during initial deployment

## Support

For MegaPay API support, visit:
- [MegaPay Documentation](https://megapay.co.ke/documentation)
- [MegaPay Dashboard](https://megapay.co.ke/user)

## Files Modified

- `mpesa/models.py` - Updated models
- `mpesa/services.py` - Updated payment service
- `mpesa/views.py` - Updated views and callbacks
- `mpesa/urls.py` - Updated URL routing
- `mpesa/admin.py` - Updated admin interface
- `mpesa/migrations/0001_initial.py` - New migrations
- `templates/loans/loan_offers.html` - Updated frontend
