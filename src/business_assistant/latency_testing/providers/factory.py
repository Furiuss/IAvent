from typing import Dict, Type
from .base import LLMProvider
from .anthropic import AnthropicProvider
from .openai import OpenAIProvider


class ProviderFactory:
    """Factory para criar instâncias de provedores LLM"""

    _providers: Dict[str, Type[LLMProvider]] = {
        'anthropic': AnthropicProvider,
        'openai': OpenAIProvider
    }

    @classmethod
    def create(cls, provider_name: str, **kwargs) -> LLMProvider:
        """
        Cria uma instância do provedor especificado

        Args:
            provider_name: Nome do provedor ('anthropic' ou 'openai')
            **kwargs: Argumentos de inicialização para o provedor

        Returns:
            LLMProvider: Instância inicializada do provedor
        """
        if provider_name not in cls._providers:
            raise ValueError(f"Provedor não suportado: {provider_name}")

        provider = cls._providers[provider_name]()
        provider.initialize(**kwargs)
        return provider

    @classmethod
    def register_provider(cls, name: str, provider_class: Type[LLMProvider]):
        """Registra um novo provedor"""
        cls._providers[name] = provider_class