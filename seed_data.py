import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'talamkopo.settings')
django.setup()

from django.contrib.auth.models import User
from mpesa.models import MegaPayConfig
from loans.models import LoanAmount, SiteConfig

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@talamkopo.local', 'admin123')
    print("✓ Superuser created: admin / admin123")

# Create MegaPay config with provided credentials
if not MegaPayConfig.objects.exists():
    config = MegaPayConfig.objects.create(
        name="Default MegaPay Config",
        is_active=True,
        api_key='MGPY5nBRzeut',
        email='smilejaym711@gmail.com',
        callback_url='https://swiftcash-ke-production.up.railway.app/mpesa/callback/'
    )
    print(f"✓ MegaPay Config created: {config.name}")
    print(f"  - API Key: {config.api_key[:5]}...")
    print(f"  - Email: {config.email}")

# Create site configuration
if not SiteConfig.objects.exists():
    site_config = SiteConfig.objects.create(
        site_name="Tala Mkopo Extra",
        tagline="Get the financial support you need with our simple, transparent loan process",
        max_loan_amount=100000,
        interest_rate=10.00,
        loan_term_months=2,
        footer_text="© 2025 Tala Mkopo Extra. Licensed by CBK."
    )
    print(f"✓ Site Configuration created")

# Create loan amount options
loan_amounts = [5500, 7800, 9800, 11200, 16800, 21200, 25600, 30000, 35400, 39800, 44200, 48600, 53000, 57400, 61800, 66200, 70600, 75000, 79400, 83800, 88200, 92600, 97000, 100000]
created_count = 0
for idx, amount in enumerate(loan_amounts):
    if not LoanAmount.objects.filter(amount=amount).exists():
        tax = int(amount * 0.05)
        LoanAmount.objects.create(
            amount=amount,
            tax_revenue=tax,
            is_active=True,
            order=idx
        )
        created_count += 1

if created_count > 0:
    print(f"✓ Created {created_count} loan amount options")

print("\n✅ Database seeded successfully!")
