# Railway Deployment Guide

This guide explains how to deploy the MegaPay-integrated all-loans application to Railway with automatic database migrations.

## Automatic Migrations on Deploy

The `Procfile` has been updated to automatically handle database migrations during deployment:

```
release: python3 manage.py makemigrations && python3 manage.py migrate && python3 seed_data.py
web: gunicorn talamkopo.wsgi --log-file -
```

This means:
1. **makemigrations** - Detects any model changes and creates migration files
2. **migrate** - Applies all migrations to the database
3. **seed_data.py** - Populates initial data (loan amounts, config, etc.)
4. **gunicorn** - Starts the web server

## Deployment Steps

### 1. Push to Your Repository
```bash
git add .
git commit -m "Replace M-Pesa with MegaPay integration"
git push origin main
```

### 2. Railway Auto-Deploy
Railway will automatically:
- Detect the push
- Build your application
- Run the `release` command (migrations)
- Start the web server

### 3. Verify Deployment
1. Go to your Railway dashboard
2. Check the **Deployments** tab to see if the build succeeded
3. Look for any errors in the **Logs** tab
4. Once deployed, visit your application URL

## Troubleshooting

### If migrations fail:
1. Check the **Logs** in Railway dashboard
2. Common issues:
   - Database connection errors (check DATABASE_URL variable)
   - Missing dependencies (check requirements.txt)
   - Syntax errors in migration files

### If you need to manually run migrations:
1. Go to your Railway service
2. Click the **"Console"** tab
3. Run:
   ```bash
   python manage.py makemigrations mpesa
   python manage.py migrate
   ```

## Environment Variables

Ensure these are set in your Railway project:

- `DEBUG=False` (for production)
- `SECRET_KEY` (your Django secret key)
- `ALLOWED_HOSTS` (your domain)
- `DATABASE_URL` (automatically set by Railway if using PostgreSQL)

## First-Time Setup

After your first successful deployment:

1. Visit `/admin/` on your deployed app
2. Log in with your Django superuser credentials
3. Navigate to **MegaPay Configuration**
4. Click **Add MegaPay Configuration**
5. Fill in:
   - **Name**: Default MegaPay Config
   - **API Key**: Your MegaPay API key
   - **Email**: Your MegaPay account email
   - **Callback URL**: `https://yourdomain.com/mpesa/callback/`
   - **Is Active**: Check this box
6. Save

## Production Checklist

- [ ] `DEBUG=False` in environment variables
- [ ] `SECRET_KEY` is set and secure
- [ ] `ALLOWED_HOSTS` includes your domain
- [ ] MegaPay credentials configured in admin
- [ ] Test a payment transaction
- [ ] Monitor logs for errors

## Rollback

If something goes wrong after deployment:

1. Go to **Deployments** in Railway
2. Find the previous successful deployment
3. Click the three dots and select **Redeploy**

This will revert to the previous version while you fix issues.

## Support

For Railway-specific issues:
- [Railway Documentation](https://docs.railway.app/)
- [Railway Support](https://railway.app/support)

For MegaPay integration issues:
- See `MEGAPAY_INTEGRATION.md` in the project root
