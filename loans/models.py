from django.db import models


class SiteConfig(models.Model):
    """Admin-configurable site-wide settings."""
    site_name = models.CharField(max_length=100, default="Swiftcash Loans")
    tagline = models.CharField(max_length=200, default="Get Up To Ksh 100,000 Fast")
    max_loan_amount = models.PositiveIntegerField(default=100000)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.0, help_text="Interest rate in %")
    loan_term_months = models.PositiveIntegerField(default=2, help_text="Loan term in months")
    hero_subtitle = models.CharField(max_length=300, default="Low 7.5% interest rate for qualified borrowers")
    footer_text = models.CharField(max_length=200, default="© 2025 Swiftcash Loans. Licensed by CBK.")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configurations"

    def __str__(self):
        return f"{self.site_name} Config"

    def save(self, *args, **kwargs):
        if self.is_active:
            SiteConfig.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class LoanAmount(models.Model):
    """Admin-configurable loan amount options."""
    amount = models.PositiveIntegerField(unique=True)
    tax_revenue = models.PositiveIntegerField(help_text="Tax/fee amount in KES")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Loan Amount Option"
        verbose_name_plural = "Loan Amount Options"
        ordering = ['order', 'amount']

    def __str__(self):
        return f"Ksh {self.amount:,} (Tax: Ksh {self.tax_revenue:,})"


class LoanApplication(models.Model):
    """Stores loan application submissions."""
    LOAN_TYPE_CHOICES = [
        ('business', 'Business Loan'),
        ('personal', 'Personal Loan'),
        ('emergency', 'Emergency Loan'),
        ('education', 'Education Loan'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid'),
        ('disbursed', 'Disbursed'),
    ]

    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    national_id = models.CharField(max_length=20)
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPE_CHOICES)
    selected_amount = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Loan Application"
        verbose_name_plural = "Loan Applications"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.phone_number} - Ksh {self.selected_amount:,} ({self.status})"
