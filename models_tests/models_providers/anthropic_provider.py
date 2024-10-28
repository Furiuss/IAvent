from models_tests.utils.latency_checker import LLMProvider
from typing import Dict, Any
from anthropic import Anthropic

class AnthropicProvider(LLMProvider):

    def initialize(self, **kwargs):
        self.api_key = kwargs.get('api_key')
        self.model = kwargs.get('model', 'claude-3-sonnet-20240229')
        self.client = Anthropic(api_key=self.api_key)

    def generate_response(self, prompt: str, **kwargs) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=kwargs.get('max_tokens', 1024),
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    def get_model_info(self) -> Dict[str, Any]:
        return {
            "provider": "Anthropic",
            "model": self.model
        }