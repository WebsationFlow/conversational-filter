"""
Test suite for ConversationalFilter.

Tests core filtering functionality with realistic examples.
"""

import sys
sys.path.insert(0, '../src')

from conversational_filter import (
    ConversationalFilter,
    ScopeAnalyzer,
    ResponseFilter,
    UserProfile,
    CONCISE_LEARNER,
)


def test_scope_creep_detection():
    """Test scope creep detection."""
    analyzer = ScopeAnalyzer()

    question = "How do I authenticate users?"
    response = """
Authentication is a fundamental cybersecurity concept. Let me explain the complete landscape:

1. Password-based authentication
   - Salting and hashing
   - Rainbow tables
   - Brute force attacks
   
2. Multi-factor authentication
   - TOTP
   - SMS
   - Biometric
   
3. OAuth 2.0
   - Grant types
   - Authorization flow
   - Refresh tokens
   
4. SAML
   - XML-based protocol
   - SAML assertions
   - Service providers
   
5. LDAP
6. Kerberos
7. JWT tokens
8. Session tokens

[10 more paragraphs of elaboration...]
"""

    is_creep = analyzer.is_scope_creep(question, response)
    ratio = analyzer.get_elaboration_ratio(question, response)

    print(f"TEST: Scope creep detection")
    print(f"  Question: '{question}'")
    print(f"  Response length: {len(response)} chars")
    print(f"  Scope creep detected: {is_creep}")
    print(f"  Elaboration ratio: {ratio:.2f}x")
    assert is_creep, "Should detect scope creep"
    assert ratio > 2.0, "Ratio should be high"
    print("  [PASS]\n")


def test_response_filtering():
    """Test response filtering."""
    filter = ResponseFilter()

    question = "What's the difference between let and const?"
    response = """
let and const are both block-scoped declarations in JavaScript.

The key difference is that:
- let allows reassignment
- const prevents reassignment

For example:
let x = 1;
x = 2;  // OK

const y = 1;
y = 2;  // Error

It's important to note that this is a fundamental concept in modern JavaScript...
[unnecessary elaboration about JavaScript history, ES6, etc]
"""

    result = filter.apply_filters(
        question=question,
        response=response,
        elaboration_ratio=2.3,
        scope_creep_detected=True,
    )

    print(f"TEST: Response filtering")
    print(f"  Filters applied: {result.filters_applied}")
    print(f"  Clarifying question: {result.clarifying_question}")
    assert result.is_filtered, "Should have applied filters"
    assert len(result.filtered_response) < len(result.original_response)
    print("  [PASS]\n")


def test_user_profile():
    """Test user profile loading."""
    profile = UserProfile(prefer_concise=True, max_response_words=250)

    print(f"TEST: User profile")
    print(f"  Profile: {profile}")
    print(f"  Elaboration threshold: {profile.get_elaboration_ratio_threshold()}")
    assert profile.prefer_concise
    assert profile.max_response_words == 250
    print("  [PASS]\n")


def test_conversational_filter():
    """Test full ConversationalFilter integration."""
    cf = ConversationalFilter(
        model="ollama:mistral",  # Note: this won't be called in tests
        user_profile=CONCISE_LEARNER,
    )

    question = "How do I connect to a database?"
    response = """
You can connect to a database using various methods depending on your language and database type.

For Python with SQLite:
import sqlite3
conn = sqlite3.connect('database.db')

For Node.js with MongoDB:
const MongoClient = require('mongodb');

For Java with PostgreSQL:
try (Connection conn = DriverManager.getConnection(url, user, password)) {

You might also want to know about connection pooling, which is an advanced topic...
[more unnecessary details]
"""

    filtered = cf.filter_response(question, response)

    print(f"TEST: ConversationalFilter integration")
    print(f"  Original length: {len(filtered.original_response)}")
    print(f"  Filtered length: {len(filtered.filtered_response)}")
    print(f"  Elaboration ratio: {filtered.elaboration_ratio:.2f}x")
    print(f"  Filters: {filtered.filters_applied}")
    print(f"  Clarifying Q: {filtered.clarifying_question}")

    print("\n  Original response:")
    print(f"  {filtered.original_response[:200]}...")
    print("\n  Filtered response:")
    print(f"  {filtered.filtered_response}")

    assert filtered.is_filtered, "Should have filtered"
    assert filtered.clarifying_question, "Should have clarifying question"
    print("\n  [PASS]\n")


def test_system_prompt_generation():
    """Test system prompt generation."""
    cf = ConversationalFilter(
        model="ollama:mistral",
        user_profile=CONCISE_LEARNER,
    )

    prompt = cf.create_system_prompt()

    print(f"TEST: System prompt generation")
    print(f"  Generated prompt:\n{prompt}\n")
    assert "conversational" in prompt.lower()
    assert "concise" in prompt.lower()
    print("  [PASS]\n")


if __name__ == "__main__":
    print("=" * 60)
    print("ConversationalFilter Test Suite")
    print("=" * 60 + "\n")

    try:
        test_scope_creep_detection()
        test_response_filtering()
        test_user_profile()
        test_conversational_filter()
        test_system_prompt_generation()

        print("=" * 60)
        print("All tests passed! [OK]")
        print("=" * 60)
    except AssertionError as e:
        print(f"\n[FAIL] TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR]: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
