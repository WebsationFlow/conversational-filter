"""User Profile and Learning Style Management"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, Any
import json


class LearningStyle(str, Enum):
    """Supported learning styles"""
    CONVERSATIONAL = "conversational"
    TUTORIAL = "tutorial"
    REFERENCE = "reference"
    EXAMPLES_FIRST = "examples_first"


@dataclass
class UserProfile:
    """Represents a user's learning preferences"""
    learning_style: LearningStyle = LearningStyle.CONVERSATIONAL
    max_elaboration_ratio: float = 2.5
    prefers_examples: bool = False
    technical_level: str = "intermediate"  # beginner, intermediate, advanced
    preferred_language: Optional[str] = None
    context_preference: str = "balanced"  # minimal, balanced, comprehensive
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate and normalize fields"""
        if isinstance(self.learning_style, str):
            self.learning_style = LearningStyle(self.learning_style)

    def to_dict(self) -> Dict[str, Any]:
        """Convert profile to dictionary"""
        return {
            'learning_style': self.learning_style.value,
            'max_elaboration_ratio': self.max_elaboration_ratio,
            'prefers_examples': self.prefers_examples,
            'technical_level': self.technical_level,
            'preferred_language': self.preferred_language,
            'context_preference': self.context_preference,
            'metadata': self.metadata
        }

    def to_json(self) -> str:
        """Convert profile to JSON string"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserProfile':
        """Create profile from dictionary"""
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str) -> 'UserProfile':
        """Create profile from JSON string"""
        data = json.loads(json_str)
        return cls.from_dict(data)


# Predefined user profiles for common use cases
CONCISE_LEARNER = UserProfile(
    learning_style=LearningStyle.CONVERSATIONAL,
    max_elaboration_ratio=1.5,  # Very strict - no elaboration
    context_preference="minimal"
)

DETAILED_LEARNER = UserProfile(
    learning_style=LearningStyle.TUTORIAL,
    max_elaboration_ratio=4.0,  # Very permissive
    context_preference="comprehensive"
)

CODE_FIRST_LEARNER = UserProfile(
    learning_style=LearningStyle.EXAMPLES_FIRST,
    max_elaboration_ratio=2.5,
    prefers_examples=True
)

TUTORIAL_LEARNER = UserProfile(
    learning_style=LearningStyle.TUTORIAL,
    max_elaboration_ratio=3.0,
    context_preference="comprehensive"
)
