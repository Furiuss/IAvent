from typing import Dict, Any


class PromptTemplates:
    """Templates de prompts para diferentes situações."""

    @staticmethod
    def get_base_prompt(context: Dict[str, Any]) -> str:
        return """
        Você é um assistente especializado em {domain}.
        Use as seguintes informações do contexto para responder:
        {context}

        Responda de forma {style}.
        """.format(**context)