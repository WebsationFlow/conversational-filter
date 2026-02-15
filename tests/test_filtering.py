"""
Test suite for ConversationalFilter.

Tests core filtering functionality with realistic examples.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from conversational_filter import (
    ConversationalFilter,
    ScopeAnalyzer,
    ResponseFilter,
    UserProfile,
    LearningStyle,
    FilteredResponse,
)
from conversational_filter.user_profile import CONCISE_LEARNER


def test_scope_creep_detection():
    """Test scope creep detection."""
    analyzer = ScopeAnalyzer(max_elaboration_ratio=2.5)

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

Each has different use cases. Password-based is simplest but least secure.
OAuth is good for third-party integrations. JWT is stateless and scalable.
"""

    analysis = analyzer.analyze(question, response)

    print("TEST: Scope creep detection")
    print(f"  Question: '{question}'")
    print(f"  Response length: {len(response)} chars")
    print(f"  Scope creep detected: {analysis.is_scope_creep}")
    print(f"  Elaboration ratio: {analysis.elaboration_ratio:.2f}x")
    print(f"  Reason: {analysis.reason}")
    assert analysis.is_scope_creep, "Should detect scope creep"
    assert analysis.elaboration_ratio > 2.0, "Ratio should be high"
    print("  [PASS]\n")


def test_scope_analyzer_appropriate_response():
    """Test that appropriate responses are NOT flagged."""
    analyzer = ScopeAnalyzer(max_elaboration_ratio=2.5)

    question = "What's the difference between let and const in JavaScript?"
    response = "let allows reassignment, const does not. Both are block-scoped."

    analysis = analyzer.analyze(question, response)

    print("TEST: Appropriate response not flagged")
    print(f"  Ratio: {analysis.elaboration_ratio:.2f}x")
    print(f"  Scope creep: {analysis.is_scope_creep}")
    assert not analysis.is_scope_creep, "Short answer should NOT be scope creep"
    print("  [PASS]\n")


def test_response_filtering():
    """Test response filtering when scope creep detected."""
    rf = ResponseFilter()

    response = """
let and const are both block-scoped declarations in JavaScript.

The key difference is that let allows reassignment while const prevents it.

For example:
let x = 1;
x = 2;  // OK

const y = 1;
y = 2;  // Error

It's important to note that this is a fundamental concept in modern JavaScript.
You should also consider var, which is function-scoped rather than block-scoped.
Additionally, there are temporal dead zones to consider with let and const.
Furthermore, const doesn't make objects immutable - only the binding is constant.
You might also want to know about Object.freeze() for true immutability.
"""

    result = rf.filter(
        response=response,
        is_scope_creep=True,
        elaboration_ratio=2.5,
    )

    print("TEST: Response filtering")
    print(f"  Filters applied: {result.filters_applied}")
    print(f"  Clarifying question: {result.clarifying_question}")
    assert len(result.filters_applied) > 0, "Should have applied filters"
    assert len(result.filtered_response) < len(result.original_response), "Filtered should be shorter"
    assert result.clarifying_question is not None, "Should have clarifying question"
    print("  [PASS]\n")


def test_no_filtering_when_appropriate():
    """Test that appropriate responses pass through unchanged."""
    rf = ResponseFilter()

    response = "Use JWT tokens stored in httpOnly cookies."

    result = rf.filter(
        response=response,
        is_scope_creep=False,
        elaboration_ratio=1.2,
    )

    print("TEST: No filtering when appropriate")
    print(f"  Filters applied: {result.filters_applied}")
    assert len(result.filters_applied) == 0, "Should NOT have applied filters"
    assert result.filtered_response == response, "Response should be unchanged"
    assert result.clarifying_question is None, "Should NOT have clarifying question"
    print("  [PASS]\n")


def test_user_profile():
    """Test user profile creation and serialization."""
    profile = UserProfile(
        learning_style=LearningStyle.CONVERSATIONAL,
        max_elaboration_ratio=1.5,
        context_preference="minimal"
    )

    print("TEST: User profile")
    print(f"  Style: {profile.learning_style.value}")
    print(f"  Max ratio: {profile.max_elaboration_ratio}")
    print(f"  Context: {profile.context_preference}")
    assert profile.learning_style == LearningStyle.CONVERSATIONAL
    assert profile.max_elaboration_ratio == 1.5

    # Test serialization round-trip
    json_str = profile.to_json()
    restored = UserProfile.from_json(json_str)
    assert restored.learning_style == profile.learning_style
    assert restored.max_elaboration_ratio == profile.max_elaboration_ratio
    print("  [PASS]\n")


def test_predefined_profiles():
    """Test predefined user profiles."""
    print("TEST: Predefined profiles")
    print(f"  CONCISE_LEARNER ratio: {CONCISE_LEARNER.max_elaboration_ratio}")
    assert CONCISE_LEARNER.max_elaboration_ratio == 1.5
    assert CONCISE_LEARNER.learning_style == LearningStyle.CONVERSATIONAL
    assert CONCISE_LEARNER.context_preference == "minimal"
    print("  [PASS]\n")


def test_conversational_filter_integration():
    """Test full ConversationalFilter integration."""
    cf = ConversationalFilter(user_profile=CONCISE_LEARNER)

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

You might also want to know about connection pooling, which is an advanced topic
that involves maintaining a pool of database connections for reuse rather than
creating new connections for each request. This significantly improves performance
in production environments. Additionally, consider using an ORM like SQLAlchemy
or Prisma for more complex database interactions.
"""

    filtered = cf.filter_response(question, response)

    print("TEST: ConversationalFilter integration")
    print(f"  Original length: {len(filtered.original_response)}")
    print(f"  Filtered length: {len(filtered.filtered_response)}")
    print(f"  Elaboration ratio: {filtered.elaboration_ratio:.2f}x")
    print(f"  Filters: {filtered.filters_applied}")
    print(f"  Clarifying Q: {filtered.clarifying_question}")
    assert filtered.elaboration_ratio > 1.0, "Should have elaboration ratio > 1"
    print("  [PASS]\n")


def test_system_prompt_generation():
    """Test system prompt generation for different profiles."""
    cf = ConversationalFilter(user_profile=CONCISE_LEARNER)
    prompt = cf.get_system_prompt()

    print("TEST: System prompt generation")
    print(f"  Generated prompt: {prompt[:100]}...")
    assert "conversational" in prompt.lower(), "Should mention conversational style"
    print("  [PASS]\n")


if __name__ == "__main__":
    print("=" * 60)
    print("ConversationalFilter Test Suite")
    print("=" * 60 + "\n")

    try:
        test_scope_creep_detection()
        test_scope_analyzer_appropriate_response()
        test_response_filtering()
        test_no_filtering_when_appropriate()
        test_user_profile()
        test_predefined_profiles()
        test_conversational_filter_integration()
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
