# ConversationalFilter - Commercial Setup Guide

**Your Complete Guide to Monetizing ConversationalFilter**

---

## Table of Contents

1. [Quick Overview](#quick-overview)
2. [Lemonsqueezy Setup (Recommended)](#lemonsqueezy-setup)
3. [Alternative: Stripe Setup](#alternative-stripe-setup)
4. [Hosted API Deployment](#hosted-api-deployment)
5. [Email Automation](#email-automation)
6. [Analytics & Monitoring](#analytics-monitoring)
7. [Customer Onboarding](#customer-onboarding)
8. [Support & Maintenance](#support-maintenance)

---

## Quick Overview

**What you're setting up:**
- Automated billing (Lemonsqueezy handles payments)
- License key generation and validation
- Hosted API service for filtering
- Customer onboarding automation
- Monthly recurring revenue (MRR)

**What requires zero maintenance:**
- Payment processing
- Customer billing/invoicing
- License key generation
- Email notifications
- Tax compliance

**What you'll deploy:**
- Simple REST API (100 lines of code)
- GitHub Actions (automated)
- Lemonsqueezy integration (theirs, not yours)

---

## Lemonsqueezy Setup (Recommended)

**Why Lemonsqueezy?**
- Designed for indie developers
- No transaction fees for digital products
- Built-in subscription management
- Automatic invoicing
- License key generation
- Webhook support
- Flat 5% fee (vs 2.9% + 30c for Stripe)

### Step 1: Create Lemonsqueezy Account

1. Go to https://lemonsqueezy.com
2. Sign up for free account
3. Complete profile (you'll get paid faster if complete)
4. Add payment details for payouts

### Step 2: Create Your Products

Lemonsqueezy will create these for you:

**Individual Tier:**
- **Monthly**: $99/month
  - 1 developer
  - Commercial use license
  - Email support

- **Yearly**: $990/year (save 10%)
  - Same as monthly
  - Annual billing discount

**Team Tier:**
- **Monthly**: $499/month
  - Up to 5 developers
  - Team support
  - Priority support

- **Yearly**: $4,990/year (save 10%)

**Enterprise:**
- Custom pricing
- Dedicated support
- Custom features
- Seat-based licensing

### Step 3: Configure License Keys

In Lemonsqueezy dashboard:

1. Go to Settings → License Keys
2. Enable "License Keys for Products"
3. Set key format: `{STORE_ID}-{ORDER_ID}-{RANDOM}`
4. Enable "Deliver License Keys via Email"

### Step 4: Get Your API Keys

1. Settings → API Tokens
2. Create new token
3. Copy:
   - `LEMONSQUEEZY_API_KEY`
   - `LEMONSQUEEZY_STORE_ID`
   - `LEMONSQUEEZY_WEBHOOK_SECRET`

### Step 5: Configure Webhooks

1. Settings → Webhooks
2. Add endpoint: `https://api.conversational-filter.io/api/v1/webhook/lemonsqueezy`
3. Subscribe to events:
   - `order.created` (new purchase)
   - `subscription.created` (new subscription)
   - `subscription.updated` (renewal)
   - `subscription.cancelled` (churn)

---

## Alternative: Stripe Setup

If you prefer Stripe:

### Step 1: Create Stripe Account
- https://stripe.com

### Step 2: Create Products
- Build → Products & Prices
- Create products matching Lemonsqueezy offerings

### Step 3: Get API Keys
- Developers → API Keys
- Copy publishable and secret keys

### Step 4: Payment Links
- Use Stripe Payment Links (no code needed)
- Share links in pricing page

### Step 5: License Key Management
- Stripe doesn't auto-generate keys
- Use webhook to trigger your own key generation
- Send keys via email manually or automated

### Code Integration (Stripe)

```python
from conversational_filter.licensing import StripeIntegration

stripe = StripeIntegration(
    api_key=os.getenv('STRIPE_SECRET_KEY')
)

# Create checkout
session = stripe.create_checkout_session(
    price_id="price_1234567890",
    customer_email="user@example.com",
    success_url="https://...",
    cancel_url="https://..."
)
```

---

## Hosted API Deployment

**Option A: Railway.app (Easiest)**

1. Go to https://railway.app
2. Sign in with GitHub
3. New Project → GitHub Repo → select your repo
4. Set environment variables:
   ```
   LEMONSQUEEZY_API_KEY=<your_key>
   LEMONSQUEEZY_STORE_ID=<your_store_id>
   DEBUG=false
   ```
5. Railway auto-detects Flask app
6. Gets automatic domain: `conversational-filter-xyz.railway.app`
7. Free tier: 500 hours/month (runs 24/7 for ~$5/month)

**Option B: Heroku**

1. Go to https://heroku.com
2. Create new app
3. Connect GitHub repo
4. Enable auto-deploy on main branch
5. Set config vars
6. Domain: `conversational-filter.herokuapp.com`
7. Cost: $7/month (Eco Dyno)

**Option C: AWS Lambda (Serverless)**

1. Package Flask app with Zappa
2. Deploy to AWS Lambda
3. API Gateway routes requests
4. Cost: Pay per request (~$0.20 per million requests)

**Recommended: Railway** (simplest, cheapest for startup)

---

## Email Automation

Use Mailgun (free tier: 5000 emails/month):

### Setup Mailgun

1. Go to https://mailgun.com
2. Sign up free
3. Get API key
4. Set up domain `mail.conversational-filter.io`

### Automated Emails

```python
import mailgun

def send_license_email(customer_name, email, license_key):
    mailgun.send({
        'from': 'hello@conversational-filter.io',
        'to': email,
        'subject': 'Your ConversationalFilter License Key',
        'text': f'''
Dear {customer_name},

Thank you for purchasing ConversationalFilter!

Your license key: {license_key}

Installation:
1. pip install conversational-filter[all]
2. Set environment: export CONVERSATIONAL_FILTER_LICENSE={license_key}
3. Use in code: from conversational_filter import ConversationalFilter

Support: support@conversational-filter.io
'''
    })
```

### Automation Flow

1. Customer purchases on Lemonsqueezy
2. Lemonsqueezy webhook → your API
3. API → Mailgun send
4. Email lands in customer inbox

---

## Analytics & Monitoring

### Track Key Metrics (Automated)

```python
# In api_service.py
from datetime import datetime
import json

def log_metrics(event_type, license_key=None, status=None):
    '''Log usage for analytics.'''
    with open('metrics.jsonl', 'a') as f:
        f.write(json.dumps({
            'timestamp': datetime.now().isoformat(),
            'event': event_type,
            'license': license_key,
            'status': status,
        }) + '\n')
```

### Monthly Revenue Report (Automated)

```python
# Run monthly via cron job
def generate_revenue_report():
    '''Generate MRR report from Lemonsqueezy.'''
    lemonsqueezy = LemonsqueezyIntegration()

    # Fetch subscriptions from API
    subs = lemonsqueezy.get_active_subscriptions()

    # Calculate MRR
    mrr = sum(
        sub['price'] for sub in subs
        if sub['status'] == 'active'
    )

    # Email report
    send_email(
        to='you@conversational-filter.io',
        subject=f'Monthly Revenue Report: ${mrr}',
        body=f'{len(subs)} active subscriptions\nMRR: ${mrr}'
    )
```

---

## Customer Onboarding

### Self-Service Checkout Flow

1. Customer lands on `/pricing`
2. Clicks "Buy Now"
3. Redirected to Lemonsqueezy checkout
4. Completes payment
5. Lemonsqueezy sends license key email
6. Customer uses license key in code

### Automated Onboarding Email Sequence

Send automatically via webhooks:

**Email 1 (Immediate): License Key**
```
Subject: Your ConversationalFilter License Key

[license key]

Next steps:
- Install: pip install conversational-filter
- Use in code
- Read documentation
- Contact support
```

**Email 2 (Day 1): Getting Started Guide**
```
Subject: Getting Started with ConversationalFilter

Quick setup guide
Code examples
Documentation link
Support contact
```

**Email 3 (Day 7): Usage Tips**
```
Subject: Tips for Better Results

Best practices
Example workflows
Common questions
```

**Email 4 (Day 30): Feedback Survey**
```
Subject: How's ConversationalFilter Working?

Quick survey
Feature requests
Referral program info
```

---

## Support & Maintenance

### Zero-Touch Support System

1. **FAQ Page**: Covers 90% of questions
   - Installation troubleshooting
   - Configuration help
   - Common errors
   - API documentation

2. **Email Templates**: Auto-responder
   ```
   Thank you for contacting ConversationalFilter support.

   Answers to common questions: [FAQ link]

   If your issue isn't covered, reply to this email.
   ```

3. **GitHub Issues**: For bug reports
   - Use issue templates
   - Link to FAQ
   - Automated responses

4. **Discord Community**: Optional
   - Let users help each other
   - Minimal moderation needed
   - Reduces support burden

### Maintenance Automation

**Automated Updates:**
- GitHub Actions runs tests on every push
- Only deploy if all tests pass
- Auto-update dependencies monthly
- Security patches immediately

**Monitoring:**
```python
# Uptime monitoring (UptimeRobot free tier)
# Alerts if API down
# Automatic restart via Railway
```

**Billing Reconciliation:**
- Lemonsqueezy handles all billing
- Weekly payout reports (automated)
- Monthly reconciliation (automated)

---

## Monthly Operations

### Hour 1: Setup (One-time)

- [ ] Lemonsqueezy account
- [ ] API keys configured
- [ ] Webhooks setup
- [ ] Railway deployment
- [ ] Email templates
- [ ] DNS routing

### Hour 1: Ongoing (Monthly)

- [ ] Check revenue dashboard (5 min)
- [ ] Review customer feedback (10 min)
- [ ] Deploy any bug fixes (5 min)
- [ ] Send monthly metrics email (2 min)

**Total:** ~20 minutes/month

---

## Expected Revenue (First Year)

### Conservative Scenario

- Month 1-2: 0 customers (setup phase)
- Month 3-6: 5-10 customers = $500-1000/month
- Month 7-12: 20-30 customers = $2000-3000/month
- **Year 1 Total: ~$15,000 MRR**

### Growth Scenario

- Month 1-2: 0 customers
- Month 3: 5 customers
- Month 6: 15 customers
- Month 9: 30 customers
- Month 12: 50 customers
- **Year 1 Total: ~$30,000+ MRR**

### Enterprise Scenario

- 2-3 mid-market deals at $5k/month
- 100+ individual subscriptions
- **Year 1 Total: $50,000+ MRR**

---

## Checklist: Ready to Launch

**Backend:**
- [x] Licensing module built
- [x] API service ready
- [x] Lemonsqueezy integration
- [x] GitHub Actions workflows
- [ ] Deploy to Railway
- [ ] Configure environment variables
- [ ] Test webhooks

**Frontend:**
- [ ] Create `/pricing` page
- [ ] Checkout button links
- [ ] License validation page
- [ ] FAQ/documentation
- [ ] Contact form

**Operations:**
- [ ] Lemonsqueezy account created
- [ ] Products configured
- [ ] Webhooks tested
- [ ] Email templates ready
- [ ] Support process documented

---

## Next Steps

1. **This Week**: Deploy API to Railway
2. **Next Week**: Create pricing page and checkout flow
3. **Week 3**: Test with beta customers (friends/colleagues)
4. **Week 4**: Public launch

---

## Support

Questions about setup?

1. Check GitHub Issues
2. Review this guide
3. Email: setup@conversational-filter.io (auto-responder)

**By the Light of Love and Wisdom, this is a sustainable business model.**
