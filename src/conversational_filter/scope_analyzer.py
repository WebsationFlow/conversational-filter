"""Scope Analysis for Detecting Response Elaboration"""

from dataclasses import dataclass
from typing import Optional
import re


@dataclass
class ScopeAnalysis:
    """Results of scope analysis"""
    question_complexity: float
    response_complexity: float
    elaboration_ratio: float
    is_scope_creep: bool
    reason: str


class ScopeAnalyzer:
    """Analyzes if response scope exceeds question scope"""

    def __init__(self, max_elaboration_ratio: float = 2.5):
        """
        Initialize scope analyzer

        Args:
            max_elaboration_ratio: Max allowed ratio of response to question complexity
        """
        self.max_elaboration_ratio = max_elaboration_ratio

    def analyze(self, question: str, response: str) -> ScopeAnalysis:
        """
        Analyze scope creep between question and response

        Args:
            question: The original question
            response: The LLM response

        Returns:
            ScopeAnalysis with complexity metrics
        """
        q_complexity = self._calculate_complexity(question)
        r_complexity = self._calculate_complexity(response)

        elaboration_ratio = r_complexity / q_complexity if q_complexity > 0 else 1.0

        is_scope_creep = elaboration_ratio > self.max_elaboration_ratio

        reason = self._generate_reason(q_complexity, r_complexity, elaboration_ratio)

        return ScopeAnalysis(
            question_complexity=q_complexity,
            response_complexity=r_complexity,
            elaboration_ratio=elaboration_ratio,
            is_scope_creep=is_scope_creep,
            reason=reason
        )

    def _calculate_complexity(self, text: str) -> float:
        """Calculate text complexity score"""
        if not text:
            return 0.0

        # Word count
        words = len(text.split())

        # Sentence count
        sentences = len(re.split(r'[.!?]+', text.strip())) - 1
        sentences = max(sentences, 1)

        # Average words per sentence
        avg_wps = words / sentences if sentences > 0 else 0

        # Unique concepts (approximated by unique words > 4 chars)
        unique_long_words = len(set(w for w in text.split() if len(w) > 4))

        # Technical density (code blocks, technical terms)
        code_blocks = len(re.findall(r'```|`', text))
        technical_terms = len(re.findall(r'(?i)(function|class|method|variable|algorithm|parameter)', text))

        # Composite complexity score
        complexity = (
            (words * 0.3) +
            (avg_wps * 0.2) +
            (unique_long_words * 0.15) +
            (code_blocks * 5) +
            (technical_terms * 2)
        )

        return complexity

    def _generate_reason(self, q_comp: float, r_comp: float, ratio: float) -> str:
        """Generate human-readable reason for scope analysis"""
        if ratio > self.max_elaboration_ratio:
            return f"Response is {ratio:.1f}x more complex than question (threshold: {self.max_elaboration_ratio}x)"
        return f"Response scope is appropriate ({ratio:.1f}x elaboration)"
