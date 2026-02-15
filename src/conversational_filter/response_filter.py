"""Response Filtering and Truncation Logic"""

from dataclasses import dataclass, field
from typing import List, Optional
import re


@dataclass
class FilteredResponse:
    """Response after filtering"""
    original_response: str
    filtered_response: str
    clarifying_question: Optional[str] = None
    filters_applied: List[str] = field(default_factory=list)
    elaboration_ratio: float = 1.0


class ResponseFilter:
    """Filters LLM responses based on scope analysis"""

    def __init__(self, max_length_chars: int = 500):
        """
        Initialize response filter

        Args:
            max_length_chars: Maximum characters for filtered response
        """
        self.max_length_chars = max_length_chars

    def filter(
        self,
        response: str,
        is_scope_creep: bool,
        elaboration_ratio: float = 1.0
    ) -> FilteredResponse:
        """
        Filter a response based on scope analysis

        Args:
            response: The original response
            is_scope_creep: Whether scope creep was detected
            elaboration_ratio: Elaboration ratio from analysis

        Returns:
            FilteredResponse with filtered content
        """
        filters_applied = []
        filtered = response
        clarifying_question = None

        if is_scope_creep:
            # Truncate to first main point
            filtered, truncated = self._truncate_to_core(response)
            if truncated:
                filters_applied.append('truncation')

            # Create clarifying question
            clarifying_question = self._generate_clarifying_question(response)
            filters_applied.append('clarifying_question')

        return FilteredResponse(
            original_response=response,
            filtered_response=filtered,
            clarifying_question=clarifying_question,
            filters_applied=filters_applied,
            elaboration_ratio=elaboration_ratio
        )

    def _truncate_to_core(self, text: str, target_chars: int = 300) -> tuple:
        """Truncate to core message, respecting sentence boundaries"""
        if len(text) <= target_chars:
            return text, False

        # Find sentence boundaries near target length
        sentences = re.split(r'(?<=[.!?])\s+', text)

        result = []
        current_length = 0

        for sentence in sentences:
            if current_length + len(sentence) > target_chars and result:
                break
            result.append(sentence)
            current_length += len(sentence) + 1

        truncated_text = ' '.join(result)
        if truncated_text.endswith(','):
            truncated_text = truncated_text[:-1]

        return truncated_text.rstrip() + '...' if truncated_text != text else text, True

    def _generate_clarifying_question(self, response: str) -> str:
        """Generate a clarifying question to invite further detail"""
        questions = [
            "Want me to dive deeper?",
            "Need more detail on any part?",
            "Should I elaborate on anything?",
            "Want more examples?",
            "Need me to explain that further?",
        ]

        # Simple heuristic: use different questions based on response length
        idx = min(len(response) // 500, len(questions) - 1)
        return questions[idx]
