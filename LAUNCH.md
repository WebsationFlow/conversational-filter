# LAUNCH: ConversationalFilter Commercial - START NOW

Your step-by-step action plan. Follow it exactly. This is 3 hours to a running business.

---

## PHASE 1: LEMONSQUEEZY SETUP (20 minutes)

### Step 1: Create Account

Go to: https://lemonsqueezy.com/signup
- Email: your email
- Password: strong password
- Company: Conversational Filter
- Create account
- Complete profile (full name, phone, country)
- Add payment method for payouts

**Time: 5 min**

### Step 2: Get API Keys

Settings > API Token
- Create Token
- Copy: **LEMONSQUEEZY_API_KEY**

Settings > Store Overview
- Copy: **LEMONSQUEEZY_STORE_ID**

**Time: 2 min**

### Step 3: Create 4 Products

Products > Create Product (repeat 4x)

**Product 1:**
- Name: Individual Monthly
- Type: Subscription
- Price: $99.00/month
- License Key: Enable

**Product 2:**
- Name: Individual Yearly
- Type: Subscription
- Price: $990.00/year
- License Key: Enable

**Product 3:**
- Name: Team Monthly
- Type: Subscription
- Price: $499.00/month
- License Key: Enable

**Product 4:**
- Name: Team Yearly
- Type: Subscription
- Price: $4,990.00/year
- License Key: Enable

**Time: 10 min**

### Step 4: License Keys Config

Settings > License Keys
- Enable: License Keys for Products
- Email delivery: ON
- Add email template:

```
Thank you for purchasing ConversationalFilter!

Your license key: {LICENSE_KEY}

Install: pip install conversational-filter
Use: export CONVERSATIONAL_FILTER_LICENSE={LICENSE_KEY}
Docs: https://conversational-filter.io

Support: support@conversational-filter.io
```

**Time: 3 min**

---

## PHASE 2: RAILWAY DEPLOYMENT (15 minutes)

### Step 1: Create Railway Account

Go to: https://railway.app
- Sign up with GitHub
- Authorize

**Time: 2 min**

### Step 2: New Project

Dashboard > New Project > GitHub Repo
- Select: rayne-ai/conversational-filter
- Authorize

**Time: 3 min**

### Step 3: Set Environment Variables

Railway Variables tab, add:

```
LEMONSQUEEZY_API_KEY = (from Phase 1)
LEMONSQUEEZY_STORE_ID = (from Phase 1)
LEMONSQUEEZY_WEBHOOK_SECRET = test-secret-xyz
DEBUG = false
SECRET_KEY = (python -c "import secrets; print(secrets.token_urlsafe(32))")
PORT = 5000
```

**Time: 5 min**

### Step 4: Deploy

Railway auto-detects Flask.
Should deploy automatically.
Watch logs until green: "Deployment successful"

**Time: 5 min**

### Step 5: Get URL

Railway dashboard shows:
```
Link: conversational-filter-xyz.railway.app
```

SAVE THIS URL

**Time: 1 min**

---

## PHASE 3: WEBHOOK SETUP (5 minutes)

Back to Lemonsqueezy:

Settings > Webhooks
- Add endpoint: https://your-railway-url/api/v1/webhook/lemonsqueezy
- Subscribe to: order.created, subscription.created, subscription.updated, subscription.cancelled
- Save

**Time: 5 min**

---

## PHASE 4: TEST LOCALLY (10 minutes)

```bash
cd c:\Gulfstream\Projects\conversational-filter
cp .env.example .env

# Edit .env with your API keys

python -m pytest tests/ -v
# Should see: All tests passed!

python api_service.py
# Should see: Running on http://localhost:5000

# In another terminal:
curl http://localhost:5000/api/v1/health
# Should see: {"status":"healthy"}

# Press Ctrl+C to stop
```

**Time: 10 min**

---

## PHASE 5: PRICING PAGE (1-2 hours)

Create simple HTML file (pricing.html):

```html
<!DOCTYPE html>
<html>
<head>
  <title>ConversationalFilter - Pricing</title>
  <style>
    body { font-family: Arial; margin: 40px; }
    .pricing { display: flex; gap: 20px; flex-wrap: wrap; }
    .card { border: 1px solid #ccc; padding: 20px; border-radius: 8px; min-width: 250px; }
    button { background: #007bff; color: white; padding: 10px 20px; border: none; cursor: pointer; font-size: 16px; }
  </style>
</head>
<body>
  <h1>ConversationalFilter - Pricing</h1>
  <p>Smart response filtering for LLMs. Stop over-explanation.</p>

  <div class="pricing">
    <div class="card">
      <h3>Individual Monthly</h3>
      <p><strong>$99/month</strong></p>
      <p>1 developer | Commercial license</p>
      <button onclick="check('individual_monthly')">Buy Now</button>
    </div>

    <div class="card">
      <h3>Individual Yearly</h3>
      <p><strong>$990/year</strong></p>
      <p>2 months free | 1 developer</p>
      <button onclick="check('individual_yearly')">Buy Now</button>
    </div>

    <div class="card">
      <h3>Team Monthly</h3>
      <p><strong>$499/month</strong></p>
      <p>Up to 5 developers | Team support</p>
      <button onclick="check('team_monthly')">Buy Now</button>
    </div>

    <div class="card">
      <h3>Team Yearly</h3>
      <p><strong>$4,990/year</strong></p>
      <p>2 months free | Up to 5 developers</p>
      <button onclick="check('team_yearly')">Buy Now</button>
    </div>
  </div>

  <script>
  function check(product) {
    alert('Checkout URLs coming from Lemonsqueezy dashboard');
  }
  </script>
</body>
</html>
```

To get checkout links:
1. Lemonsqueezy Products dashboard
2. Click each product
3. Copy "Share" button link
4. Paste into HTML onclick handlers

Deploy to:
- GitHub Pages (free)
- Vercel (free)
- Or host anywhere

**Time: 1-2 hours**

---

## PHASE 6: ANNOUNCE (30 minutes)

### Post 1: Reddit

Subreddit: r/LocalLLM or r/Python

Title: "ConversationalFilter - Stop LLM Overexplanation - Now Available"

Body:
```
I built ConversationalFilter to solve a problem I had with local LLMs: they over-explain when you want quick answers.

It detects when responses are getting too verbose, auto-truncates unnecessary elaboration, and adds smart clarifying questions instead.

Works with: Ollama, OpenAI, Anthropic, any LLM via LiteLLM

Open source: https://github.com/rayne-ai/conversational-filter
pip install: pip install conversational-filter
Commercial: https://conversational-filter.io/pricing

Looking forward to your feedback!
```

### Post 2: Twitter/X

"ConversationalFilter is live! Smart filtering for LLM responses that prevents scope creep and tutorial fatigue. Works with any LLM. Open source + commercial licenses available. https://conversational-filter.io"

### Post 3: GitHub

Update README:
- Add "Commercial" section
- Link to pricing page
- Add "Commercial Available" badge

**Time: 30 min**

---

## PHASE 7: PASSIVE INCOME BEGINS

- Monitor Lemonsqueezy dashboard
- First customer buys → key generated → email sent → money in account
- Repeat

**Expected timeline:**
- Week 1-2: Setup
- Week 3-4: First customers appear
- Month 2+: Passive revenue stream

---

## CHECKLIST

### Phase 1
- [ ] Lemonsqueezy account created
- [ ] API keys saved
- [ ] 4 products created
- [ ] License keys configured

### Phase 2
- [ ] Railway account created
- [ ] GitHub repo connected
- [ ] Environment variables set
- [ ] Deployment successful (green)
- [ ] Public URL saved

### Phase 3
- [ ] Webhook endpoint configured
- [ ] Events subscribed

### Phase 4
- [ ] Tests pass
- [ ] API responds to health check

### Phase 5
- [ ] Pricing page created
- [ ] Checkout links added
- [ ] Page deployed

### Phase 6
- [ ] Posted on Reddit
- [ ] Tweeted
- [ ] GitHub updated

### Phase 7
- [ ] Waiting for first customer

---

## QUICK TROUBLESHOOTING

**API won't deploy:**
- Push changes: `git add . && git commit -m "fix" && git push`
- Railway auto-redeploys

**Webhook not working:**
- Check Railway logs
- Verify endpoint URL is correct

**License validation fails:**
- Verify API_KEY in Railway environment
- Restart service

---

## TIMELINE

- Phase 1: 20 min
- Phase 2: 15 min
- Phase 3: 5 min
- Phase 4: 10 min
- Phase 5: 1-2 hours
- Phase 6: 30 min

**Total: 3 hours to running business with revenue potential**

---

## GO NOW

Stop reading. Start Phase 1.

You've got this.

By the Light of Love and Wisdom, launch this thing.
