import time
from typing import List, Dict
import statistics
from datetime import datetime
import json
import numpy as np
from ..providers import LLMProvider
from .metrics import LatencyMetrics

class LatencyTester:
    def __init__(self, provider: LLMProvider):
        """
        Inicializa o testador de latência

        Args:
            provider (LLMProvider): Instância do provedor de LLM
        """
        self.provider = provider
        self.latencies: List[float] = []
        self.errors: List[Dict] = []

    def make_test_request(self, prompt: str, **kwargs) -> float:
        """
        Faz uma requisição de teste e retorna a latência

        Args:
            prompt (str): Texto para enviar na requisição
            **kwargs: Argumentos adicionais para passar ao provedor

        Returns:
            float: Tempo de latência em segundos
        """
        start_time = time.time()
        try:
            self.provider.generate_response(prompt, **kwargs)
            latency = time.time() - start_time
            self.latencies.append(latency)
            return latency

        except Exception as e:
            error_info = {
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "prompt": prompt
            }
            self.errors.append(error_info)
            raise

    def run_batch_test(
            self,
            prompt: str,
            num_requests: int = 10,
            delay: float = 1.0,
            **kwargs
    ) -> LatencyMetrics:
        """
        Executa múltiplos testes de latência

        Args:
            prompt (str): Texto para enviar nas requisições
            num_requests (int): Número de requisições para fazer
            delay (float): Delay entre requisições em segundos
            **kwargs: Argumentos adicionais para passar ao provedor

        Returns:
            LatencyMetrics: Métricas calculadas dos testes
        """
        print(f"Iniciando teste em lote com {num_requests} requisições...")

        for i in range(num_requests):
            try:
                latency = self.make_test_request(prompt, **kwargs)
                print(f"Requisição {i + 1}/{num_requests}: {latency:.2f}s")
                if i < num_requests - 1:
                    time.sleep(delay)
            except Exception as e:
                print(f"Erro na requisição {i + 1}: {str(e)}")

        return self.calculate_metrics()

    def calculate_metrics(self) -> LatencyMetrics:
        """Calcula métricas estatísticas das latências registradas"""
        if not self.latencies:
            raise ValueError("Nenhum dado de latência disponível")

        return LatencyMetrics(
            average=statistics.mean(self.latencies),
            minimum=min(self.latencies),
            maximum=max(self.latencies),
            p50=np.percentile(self.latencies, 50),
            p90=np.percentile(self.latencies, 90),
            p95=np.percentile(self.latencies, 95),
            p99=np.percentile(self.latencies, 99),
            total_requests=len(self.latencies),
            failed_requests=len(self.errors),
            timestamp=datetime.now().isoformat(),
            model_info=self.provider.get_model_info()
        )

    def export_results(self, filename: str):
        """Exporta os resultados dos testes para um arquivo JSON"""
        results = {
            "metrics": self.calculate_metrics().__dict__,
            "raw_latencies": self.latencies,
            "errors": self.errors
        }

        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)

    def clear_history(self):
        """Limpa o histórico de latências e erros"""
        self.latencies = []
        self.errors = []