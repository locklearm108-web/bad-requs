from django.contrib import admin
from django.utils.html import format_html
from .models import SiteConfig, LoanAmount, LoanApplication


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'max_loan_amount', 'interest_rate', 'loan_term_months', 'is_active']
    fieldsets = (
        ('Site Branding', {
            'fields': ('site_name', 'tagline', 'hero_subtitle', 'footer_text', 'is_active')
        }),
        ('Loan Settings', {
            'fields': ('max_loan_amount', 'interest_rate', 'loan_term_months'),
        }),
    )


@admin.register(LoanAmount)
class LoanAmountAdmin(admin.ModelAdmin):
    list_display = ['amount_display', 'tax_revenue_display', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    ordering = ['order', 'amount']

    def amount_display(self, obj):
        return f"Ksh {obj.amount:,}"
    amount_display.short_description = "Loan Amount"

    def tax_revenue_display(self, obj):
        return f"Ksh {obj.tax_revenue:,}"
    tax_revenue_display.short_description = "Tax Revenue"


@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone_number', 'national_id', 'loan_type', 'amount_display', 'status_badge', 'created_at']
    list_filter = ['status', 'loan_type', 'created_at']
    search_fields = ['full_name', 'phone_number', 'national_id']
    readonly_fields = ['created_at', 'updated_at', 'ip_address']

    def amount_display(self, obj):
        return f"Ksh {obj.selected_amount:,}" if obj.selected_amount else "-"
    amount_display.short_description = "Amount"

    def status_badge(self, obj):
        colors = {
            'pending': '#f59e0b',
            'approved': '#10b981',
            'rejected': '#ef4444',
            'paid': '#3b82f6',
            'disbursed': '#8b5cf6',
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background:{};color:white;padding:3px 10px;border-radius:12px;font-size:12px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = "Status"
