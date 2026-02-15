# QUICK LAUNCH CHECKLIST

Print this or keep open while executing LAUNCH.md

---

## PHASE 1: LEMONSQUEEZY (20 min)

**Step 1** [ ] Go to lemonsqueezy.com/signup
- [ ] Sign up
- [ ] Verify email
- [ ] Complete profile (name, phone, country)
- [ ] Add payment method (for payouts)

**Step 2** [ ] Get API Keys
- [ ] Settings > API Token > Create
- [ ] Copy and save: LEMONSQUEEZY_API_KEY
- [ ] Settings > Store Overview
- [ ] Copy and save: LEMONSQUEEZY_STORE_ID

**Step 3** [ ] Create 4 Products
- [ ] Individual Monthly ($99/month)
- [ ] Individual Yearly ($990/year)
- [ ] Team Monthly ($499/month)
- [ ] Team Yearly ($4990/year)
- [ ] Enable License Keys on each

**Step 4** [ ] License Key Setup
- [ ] Settings > License Keys > Enable
- [ ] Add email template with license instructions
- [ ] Enable automatic email delivery

---

## PHASE 2: RAILWAY (15 min)

**Step 1** [ ] Go to railway.app
- [ ] Sign up with GitHub

**Step 2** [ ] New Project
- [ ] Select: rayne-ai/conversational-filter
- [ ] Authorize GitHub

**Step 3** [ ] Environment Variables
- [ ] Add LEMONSQUEEZY_API_KEY
- [ ] Add LEMONSQUEEZY_STORE_ID
- [ ] Add LEMONSQUEEZY_WEBHOOK_SECRET (random value like "xyz123")
- [ ] Add DEBUG=false
- [ ] Add SECRET_KEY (python generated)
- [ ] Add PORT=5000

**Step 4** [ ] Deploy
- [ ] Wait for auto-deployment
- [ ] Confirm green status
- [ ] Copy public URL

---

## PHASE 3: WEBHOOKS (5 min)

**Step 1** [ ] Back to Lemonsqueezy
- [ ] Settings > Webhooks
- [ ] Add endpoint: https://your-railway-url/api/v1/webhook/lemonsqueezy
- [ ] Subscribe to: order.created, subscription.created, subscription.updated, subscription.cancelled
- [ ] Save

---

## PHASE 4: LOCAL TEST (10 min)

**Step 1** [ ] Setup
- [ ] cd c:\Gulfstream\Projects\conversational-filter
- [ ] cp .env.example .env
- [ ] Edit .env with your API keys

**Step 2** [ ] Test
- [ ] python -m pytest tests/ -v (all should pass)
- [ ] python api_service.py (should start)
- [ ] curl http://localhost:5000/api/v1/health (should respond)
- [ ] Ctrl+C to stop

---

## PHASE 5: PRICING PAGE (1-2 hours)

**Step 1** [ ] Create HTML file with pricing
- [ ] 4 pricing cards
- [ ] Buy buttons
- [ ] Links to Lemonsqueezy checkout

**Step 2** [ ] Get checkout links
- [ ] In Lemonsqueezy: Products > each product > Share button
- [ ] Copy 4 links
- [ ] Paste into HTML buttons

**Step 3** [ ] Deploy
- [ ] GitHub Pages (easiest)
- [ ] Or Vercel, or your hosting

---

## PHASE 6: ANNOUNCE (30 min)

**Step 1** [ ] Reddit post
- [ ] r/LocalLLM or r/Python
- [ ] Announce ConversationalFilter
- [ ] Share link to pricing page

**Step 2** [ ] Twitter/X
- [ ] Tweet about launch
- [ ] Include link

**Step 3** [ ] Update GitHub
- [ ] Add Commercial section to README
- [ ] Link to pricing page

---

## PHASE 7: REVENUE (Passive)

**Step 1** [ ] Monitor Lemonsqueezy
- [ ] Customer buys?
- [ ] Check Lemonsqueezy dashboard
- [ ] License key sent? (check email)
- [ ] Money depositing? (watch account)

**Step 2** [ ] Celebrate
- [ ] First customer = you're live
- [ ] Second customer = you have a business
- [ ] Third customer = you have sustainable income

---

## FINAL CHECKLIST

- [ ] All 7 phases completed
- [ ] Lemonsqueezy account live
- [ ] Railway API live
- [ ] Webhooks configured
- [ ] Local tests pass
- [ ] Pricing page deployed
- [ ] Announced on social
- [ ] Waiting for first customer

---

Time spent: ~3 hours
Revenue potential: $18k-80k Year 1
Monthly operations: 15 minutes
Sustainability: INFINITE

You're done. You launched.
