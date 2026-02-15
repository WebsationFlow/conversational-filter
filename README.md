# ConversationalFilter

Smart response filtering for LLMs. Stop over-explanation, prevent scope creep, and get concise answers.

## What It Does

ConversationalFilter detects when LLM responses are getting too verbose and automatically:
- Truncates unnecessary elaboration
- Prevents scope creep beyond the original question
- Adds smart clarifying questions instead of dumping information
- Adapts to user expertise level

Works with any LLM: Ollama, OpenAI, Anthropic, and more via LiteLLM.

## Quick Start

```bash
pip install conversational-filter
```

```python
from conversational_filter import ConversationalFilter

cf = ConversationalFilter()
result = cf.filter_response(
    question="How do I reverse a list in Python?",
    response="To reverse a list in Python, you can use several methods. First, let me explain what a list is. A list is a data structure that... [500 more words]"
)

print(result.filtered_response)
# "Use list.reverse() for in-place or list[::-1] for a new list."
```

## API

Live API available at `https://conversational-filter-production.up.railway.app`

```bash
# Health check
curl https://conversational-filter-production.up.railway.app/api/v1/health

# List products
curl https://conversational-filter-production.up.railway.app/api/v1/products

# Filter a response (requires license key)
curl -X POST https://conversational-filter-production.up.railway.app/api/v1/filter \
  -H "Content-Type: application/json" \
  -H "X-License-Key: YOUR_LICENSE_KEY" \
  -d '{"question": "How do I reverse a list?", "response": "Long verbose response here..."}'
```

## Commercial Licenses

| Plan | Price | Details |
|------|-------|---------|
| Individual Monthly | $99/mo | 1 developer, commercial use |
| Individual Yearly | $990/yr | 2 months free |
| Team Monthly | $499/mo | Up to 5 developers |
| Team Yearly | $4,990/yr | 2 months free |

**[View Pricing & Purchase](https://websationflow.github.io/conversational-filter/)**

All licenses include:
- Commercial use rights
- All API features
- License key delivered via email
- Support

## License

Commercial license required for production use. See [pricing page](https://websationflow.github.io/conversational-filter/) for details.
