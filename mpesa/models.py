from django.db import models


class MegaPayConfig(models.Model):
    """Admin-configurable MegaPay API settings."""
    name = models.CharField(max_length=100, default="Default MegaPay Config")
    is_active = models.BooleanField(default=True, help_text="Only one config should be active at a time.")
    api_key = models.CharField(max_length=255, help_text="MegaPay API Key")
    email = models.EmailField(help_text="Email associated with MegaPay Account")
    callback_url = models.URLField(default='https://skillfam.com/payments/callback/', help_text="MegaPay Webhook Callback URL")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "MegaPay Configuration"
        verbose_name_plural = "MegaPay Configurations"

    def __str__(self):
        return f"{self.name} {'[ACTIVE]' if self.is_active else ''}"

    def save(self, *args, **kwargs):
        if self.is_active:
            MegaPayConfig.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class MegaPayTransaction(models.Model):
    """Records every MegaPay STK Push transaction."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('timeout', 'Timeout'),
    ]
    phone_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    applicant_name = models.CharField(max_length=200, blank=True)
    national_id = models.CharField(max_length=20, blank=True)
    loan_type = models.CharField(max_length=50, blank=True)
    transaction_request_id = models.CharField(max_length=100, blank=True, db_index=True)
    response_code = models.CharField(max_length=10, blank=True)
    response_description = models.TextField(blank=True)
    customer_message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    result_code = models.CharField(max_length=10, blank=True)
    result_desc = models.TextField(blank=True)
    megapay_receipt_number = models.CharField(max_length=50, blank=True)
    transaction_date = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "MegaPay Transaction"
        verbose_name_plural = "MegaPay Transactions"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.phone_number} - Ksh {self.amount} - {self.status}"
