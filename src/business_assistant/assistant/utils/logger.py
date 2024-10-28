import logging
from typing import Optional


class AssistantLogger:
    """Configuração de logging para o assistente."""

    @staticmethod
    def setup_logger(name: str, level: Optional[int] = None) -> logging.Logger:
        """Configura e retorna um logger."""
        logger = logging.getLogger(name)

        if level:
            logger.setLevel(level)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger