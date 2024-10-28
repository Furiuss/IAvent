from dataclasses import dataclass
from typing import Dict, Any
from datetime import datetime

@dataclass
class LatencyMetrics:
    """Classe para armazenar métricas de latência de uma sessão de testes"""
    average: float
    minimum: float
    maximum: float
    p50: float
    p90: float
    p95: float
    p99: float
    total_requests: int
    failed_requests: int
    timestamp: str
    model_info: Dict[str, Any]

    @classmethod
    def create_empty(cls) -> 'LatencyMetrics':
        """Cria uma instância vazia de métricas"""
        return cls(
            average=0.0,
            minimum=0.0,
            maximum=0.0,
            p50=0.0,
            p90=0.0,
            p95=0.0,
            p99=0.0,
            total_requests=0,
            failed_requests=0,
            timestamp=datetime.now().isoformat(),
            model_info={}
        )