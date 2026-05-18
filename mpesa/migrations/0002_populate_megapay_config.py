from django.db import migrations

def populate_megapay_config(apps, schema_editor):
    MegaPayConfig = apps.get_model('mpesa', 'MegaPayConfig')
    # Create or update the default config
    MegaPayConfig.objects.update_or_create(
        name="Default MegaPay Config",
        defaults={
            "api_key": "MGPY5nBRzeut",
            "email": "smilejaym711@gmail.com",
            "callback_url": "https://swiftloans.up.railway.app/mpesa/callback/",
            "is_active": True
        }
    )

class Migration(migrations.Migration):

    dependencies = [
        ('mpesa', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_megapay_config),
    ]
