import os

from business_assistant.assistant.core.hydbrid_knowledge import HybridKnowledgeBase
from business_assistant.assistant.providers.factory import AssistantFactory


async def main():
    kb = HybridKnowledgeBase(
        documentation_path="business_assistant/documentacao.json",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        max_local_results=3,
        similarity_threshold=0.3,
        use_api_threshold=0.5
    )

    # Configurar e criar assistente
    config = {
        "api_key": os.getenv("ANTHROPIC_API_KEY"),
        "model": "claude-3-opus-20240229"
    }

    assistant = AssistantFactory.create_assistant(
        provider="anthropic",
        knowledge_base=kb,
        config=config
    )

    # Exemplo de uso
    response = await assistant.chat("Qual o CFOP para venda dentro do estado?")
    print(response)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())