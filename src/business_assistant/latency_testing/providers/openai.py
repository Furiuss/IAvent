from models_tests.utils.latency_checker import LLMProvider
from typing import Dict, Any
from openai import OpenAI

class OpenAIProvider(LLMProvider):

    def initialize(self, **kwargs):
        self.api_key = kwargs.get('api_key')
        self.model = kwargs.get('model', 'gpt-4')
        self.client = OpenAI(api_key=self.api_key)

    def generate_response(self, prompt: str, **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=kwargs.get('max_tokens', 1024)
        )
        return response.choices[0].message.content

    def get_model_info(self) -> Dict[str, Any]:
        return {
            "provider": "OpenAI",
            "model": self.model
        }