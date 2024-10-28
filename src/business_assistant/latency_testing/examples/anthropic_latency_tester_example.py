import os

from ..providers.factory import ProviderFactory
from ..core.tester import LatencyTester


def main():
    # Criar provedor via factory
    provider = ProviderFactory.create(
        'anthropic',
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        model='claude-3-sonnet-20240229'
    )

    # Criar e configurar o testador
    tester = LatencyTester(provider)

    # Executar testes
    metrics = tester.run_batch_test(
        prompt="Qual é a capital do Brasil?",
        num_requests=5,
        delay=1.0
    )

    # Exportar resultados
    tester.export_results("anthropic_test_results.json")

    print(f"Latência média: {metrics.average:.2f}s")
    print(f"Percentil 90: {metrics.p90:.2f}s")


if __name__ == "__main__":
    main()