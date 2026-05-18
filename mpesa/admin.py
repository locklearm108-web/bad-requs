from django.contrib import admin
from django.utils.html import format_html
from .models import MegaPayConfig, MegaPayTransaction


@admin.register(MegaPayConfig)
class MegaPayConfigAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    fields = ['name', 'api_key', 'email', 'callback_url', 'is_active', 'created_at', 'updated_at']
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


@admin.register(MegaPayTransaction)
class MegaPayTransactionAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'applicant_name', 'loan_amount_display', 'tax_amount_display', 'status_badge', 'megapay_receipt_number', 'created_at']
    list_filter = ['status', 'loan_type', 'created_at']
    search_fields = ['phone_number', 'applicant_name', 'national_id', 'megapay_receipt_number', 'transaction_request_id']
    readonly_fields = [
        'transaction_request_id', 'response_code',
        'response_description', 'customer_message', 'result_code', 'result_desc',
        'megapay_receipt_number', 'transaction_date', 'created_at', 'updated_at'
    ]
    fieldsets = (
        ('Applicant Details', {
            'fields': ('applicant_name', 'phone_number', 'national_id', 'loan_type', 'loan_amount', 'amount')
        }),
        ('Transaction Status', {
            'fields': ('status', 'megapay_receipt_number', 'transaction_date', 'result_code', 'result_desc')
        }),
        ('MegaPay Response', {
            'fields': ('transaction_request_id', 'response_code', 'response_description', 'customer_message'),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def loan_amount_display(self, obj):
        return f"Ksh {int(obj.loan_amount):,}"
    loan_amount_display.short_description = "Loan Amount"

    def tax_amount_display(self, obj):
        return f"Ksh {int(obj.amount):,}"
    tax_amount_display.short_description = "Tax Paid"

    def status_badge(self, obj):
        colors = {
            'pending': '#f59e0b',
            'success': '#10b981',
            'failed': '#ef4444',
            'cancelled': '#6b7280',
            'timeout': '#f97316',
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background:{};color:white;padding:3px 10px;border-radius:12px;font-size:12px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = "Status"

    def has_add_permission(self, request):
        return False
