# Tala Mkopo Extra — Django Clone with M-Pesa Integration

A full-stack Django clone of talamkopo.site with **M-Pesa Buy Goods Online (Till)** STK Push integration, fully configurable from the Django admin panel.

## ✨ Features

- **Home page** — Hero card, 3-step process, feature cards, trust badges
- **Apply page** — Form with real-time validation (Name, Phone, National ID, Loan Type)
- **Processing page** — Animated progress bar with status steps
- **Loan Offers page** — Grid of loan amounts, confirm payment modal, STK Push, status polling
- **Payment Success page** — Receipt display after successful payment
- **Static pages** — Privacy Policy, Terms of Service, Contact
- **Django Admin** — Full control over M-Pesa config, site settings, loan amounts, and transactions

## 🔐 M-Pesa Configuration (Pre-configured)

**Admin Panel:** `/admin/` → **MPESA** → **M-Pesa Configurations**

| Field | Value |
|---|---|
| **Consumer Key** | `DOLtaDp5VDvHWmUDQi9AW1XcWr3u4kK6` |
| **Consumer Secret** | `CgUOQBO5MthfGWzf` |
| **Business Short Code** | `4125331` |
| **Party B (Till)** | `4125331` |
| **Passkey** | `4e4522aaaa817de43c3d28e3c6180ed6270fec8e686e0aae3e1ede547b03843c` |
| **Environment** | Production (Live) |
| **Transaction Type** | CustomerBuyGoodsOnline (locked) |
| **STK Push URL** | `https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest` |
| **Callback URL** | Removed (not needed for Buy Goods) |

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run migrations
python manage.py migrate

# 3. Create superuser (if needed)
python manage.py createsuperuser

# 4. Load initial data (optional)
python seed_data.py

# 5. Collect static files
python manage.py collectstatic

# 6. Run development server
python manage.py runserver

# 7. Open http://127.0.0.1:8000/
```

## 📊 Admin Panel Sections

### M-Pesa Configurations (Admin → MPESA → M-Pesa Configurations)
- **Consumer Key & Secret** — Daraja API credentials
- **Business Short Code** — Till number (4125331)
- **Party B** — Till number for Buy Goods Online
- **Passkey** — Lipa Na M-Pesa Online Passkey
- **Account Reference** — Shown on M-Pesa prompt
- **Transaction Description** — Shown on M-Pesa prompt
- **Environment** — Production or Sandbox
- **Transaction Type** — Locked to Buy Goods Online

### Site Configuration (Admin → LOANS → Site Configurations)
Control site name, tagline, max loan amount, interest rate, loan term, and footer text.

### Loan Amount Options (Admin → LOANS → Loan Amount Options)
Add, edit, enable/disable, and reorder loan amounts and their associated tax revenue fees.

### Loan Applications (Admin → LOANS → Loan Applications)
View all submitted applications with status tracking.

### M-Pesa Transactions (Admin → MPESA → M-Pesa Transactions)
View all STK Push transactions with status, receipt numbers, and full callback data.

## 🌐 URL Structure

| URL | Description |
|---|---|
| `/` | Home page |
| `/apply` | Loan application form |
| `/processing` | Processing animation |
| `/loan-offers` | Loan amount selection + payment |
| `/payment-success` | Payment confirmation |
| `/privacy` | Privacy Policy |
| `/terms` | Terms of Service |
| `/contact` | Contact page |
| `/admin/` | Django admin panel |
| `/mpesa/stk-push/` | STK Push API endpoint |
| `/mpesa/callback/` | M-Pesa callback endpoint |
| `/mpesa/status/<id>/` | Transaction status polling |

## 📦 Tech Stack

- **Backend**: Django 5.2, Python 3.11
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Static files**: WhiteNoise
- **M-Pesa**: Safaricom Daraja API v1 (STK Push - Buy Goods Online)
- **Frontend**: Vanilla HTML/CSS/JS (no framework)

## 🚢 Production Deployment

1. Set `DEBUG=False` in environment variables
2. Set a strong `SECRET_KEY`
3. Configure your database (PostgreSQL recommended)
4. Use gunicorn + nginx
5. Set `CSRF_TRUSTED_ORIGINS` to your domain
6. M-Pesa is already configured for production (environment = Production)

## 🔄 How M-Pesa STK Push Works

1. User selects loan amount on `/loan-offers`
2. System calculates tax (5% of loan amount)
3. User clicks "Get Loan Now"
4. Django calls Daraja API with STK Push request
5. M-Pesa prompt appears on user's phone
6. User enters M-Pesa PIN
7. Payment is confirmed and loan is disbursed

## 📝 Admin Credentials

- **Username**: `admin`
- **Password**: `admin1234`

## 📄 License

© 2025 Tala Mkopo Extra. Licensed by CBK.
