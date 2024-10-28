class AssistantError(Exception):
    """Classe base para exceções do assistente."""
    pass

class ProviderError(AssistantError):
    """Erro relacionado ao provider do assistente."""
    pass

class KnowledgeBaseError(AssistantError):
    """Erro relacionado à base de conhecimento."""
    pass

class ContextError(AssistantError):
    """Erro relacionado ao gerenciamento de contexto."""
    pass