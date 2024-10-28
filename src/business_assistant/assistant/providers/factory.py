from typing import Dict, Any
from .base import BaseAssistantProvider
from .anthropic import AnthropicAssistant
from .openai import OpenAIAssistant
from ..core.knowledge import KnowledgeBase


class AssistantFactory:

    @staticmethod
    def create_assistant(
            provider: str,
            knowledge_base: KnowledgeBase,
            config: Dict[str, Any]
    ) -> BaseAssistantProvider:
        providers = {
            "anthropic": AnthropicAssistant,
            "openai": OpenAIAssistant
        }

        if provider not in providers:
            raise ValueError(f"Provider não suportado: {provider}")

        assistant_class = providers[provider]
        return assistant_class(knowledge_base=knowledge_base, **config)