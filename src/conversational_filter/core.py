"""Core ConversationalFilter Orchestrator"""

from typing import Optional
from .user_profile import UserProfile, LearningStyle
from .scope_analyzer import ScopeAnalyzer
from .response_filter import ResponseFilter, FilteredResponse


class ConversationalFilter:
    """
    Main orchestrator for filtering LLM responses
    Detects scope creep and enforces conversational discipline
    """

    def __init__(self, user_profile: Optional[UserProfile] = None):
        """
        Initialize ConversationalFilter

        Args:
            user_profile: Optional UserProfile for personalized filtering
        """
        self.user_profile = user_profile or UserProfile()
        self.scope_analyzer = ScopeAnalyzer(
            max_elaboration_ratio=self.user_profile.max_elaboration_ratio
        )
        self.response_filter = ResponseFilter()

    def filter_response(self, question: str, response: str) -> FilteredResponse:
        """
        Filter an LLM response for scope appropriateness

        Args:
            question: The original question
            response: The LLM response to filter

        Returns:
            FilteredResponse with filtering applied
        """
        # Analyze scope creep
        analysis = self.scope_analyzer.analyze(question, response)

        # Filter response if needed
        filtered = self.response_filter.filter(
            response,
            analysis.is_scope_creep,
            analysis.elaboration_ratio
        )

        return filtered

    def call_and_filter(
        self,
        question: str,
        llm_client=None,
        **llm_kwargs
    ) -> FilteredResponse:
        """
        Call an LLM and filter the response

        Args:
            question: The question to ask
            llm_client: Optional LLM client (must have __call__ method)
            **llm_kwargs: Additional arguments for LLM call

        Returns:
            FilteredResponse with LLM response filtered
        """
        if not llm_client:
            raise ValueError("llm_client is required for call_and_filter")

        # Call the LLM
        response = llm_client(question, **llm_kwargs)

        # Filter the response
        return self.filter_response(question, response)

    def get_system_prompt(self) -> str:
        """
        Get a system prompt tailored to the user's learning style

        Returns:
            System prompt string for the LLM
        """
        base_prompt = "You are a helpful assistant providing concise, focused answers."

        style_prompts = {
            LearningStyle.CONVERSATIONAL: "Keep responses conversational and to the point. Avoid unnecessary elaboration.",
            LearningStyle.TUTORIAL: "Provide step-by-step explanations with examples where helpful.",
            LearningStyle.REFERENCE: "Provide comprehensive, reference-style documentation.",
            LearningStyle.EXAMPLES_FIRST: "Lead with code examples or practical demonstrations first.",
        }

        style_specific = style_prompts.get(
            self.user_profile.learning_style,
            "Be clear and concise."
        )

        technical_prompts = {
            "beginner": "Explain concepts in simple terms, define technical jargon.",
            "intermediate": "Use technical terminology as appropriate.",
            "advanced": "Assume strong technical knowledge, use advanced terminology freely."
        }

        technical_specific = technical_prompts.get(
            self.user_profile.technical_level,
            ""
        )

        parts = [base_prompt, style_specific]
        if technical_specific:
            parts.append(technical_specific)

        return " ".join(parts)
