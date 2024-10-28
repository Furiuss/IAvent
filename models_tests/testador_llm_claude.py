import json
import os
from typing import List, Dict
from datetime import datetime
from anthropic import Anthropic

class TestadorClaudeFiscal:
    def __init__(self, documentacao_path: str, api_key: str = None):
        """
        Inicializa o testador com a documentação de referência e configuração do Claude
        """
        self.documentacao = self._carregar_documentacao(documentacao_path)
        self.client = Anthropic(api_key=api_key or os.getenv('ANTHROPIC_API_KEY'))
        self.system_prompt = """
        Você é um assistente fiscal especializado. Use apenas as informações contidas
        na documentação fornecida para responder às perguntas. Se a informação não
        estiver na documentação, indique isso claramente. Use sempre linguagem formal
        e termos técnicos apropriados.
        """
        self.resultados_testes = []

    def _carregar_documentacao(self, path: str) -> Dict:
        """
        Carrega a documentação do sistema que será usada como referência
        """
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _preparar_contexto(self) -> str:
        """
        Prepara o contexto da documentação para envio ao Claude
        """
        return f"Documentação do sistema fiscal: {json.dumps(self.documentacao, ensure_ascii=False)}"

    def testar_alucinacoes(self, casos_teste: List[Dict]) -> Dict:
        """
        Testa o Claude para verificar alucinações usando casos de teste estruturados
        """
        resultados = {
            'total_testes': len(casos_teste),
            'alucinacoes_detectadas': 0,
            'respostas_corretas': 0,
            'reconhecimento_limites': 0,
            'detalhes_testes': []
        }

        for caso in casos_teste:
            # Prepara a mensagem para o Claude
            mensagem = {
                "model": "claude-3-sonnet-20240229",
                "system": self.system_prompt,  # system prompt deve estar aqui
                "messages": [
                    {
                        "role": "user",
                        "content": f"{self._preparar_contexto()}\n\nPergunta: {caso['pergunta']}"
                    }
                ],
                "max_tokens": 1000
            }

            # Obtém resposta do Claude
            try:
                resposta = self.client.messages.create(**mensagem)
                texto_resposta = resposta.content[0].text
            except Exception as e:
                print(f"Erro ao obter resposta do Claude: {e}")
                continue

            # Verifica se a informação existe na documentação
            info_existe = self._verificar_existencia_info(caso['pergunta'])

            # Análise da resposta
            resultado_caso = self._analisar_resposta(
                resposta=texto_resposta,
                info_existe=info_existe,
                resposta_esperada=caso.get('resposta_esperada')
            )

            resultados['detalhes_testes'].append({
                'pergunta': caso['pergunta'],
                'resposta_modelo': texto_resposta,
                'resultado': resultado_caso,
                'timestamp': datetime.now().isoformat()
            })

            # Atualiza contadores
            if resultado_caso['tipo'] == 'alucinacao':
                resultados['alucinacoes_detectadas'] += 1
            elif resultado_caso['tipo'] == 'correto':
                resultados['respostas_corretas'] += 1
            elif resultado_caso['tipo'] == 'reconhecimento_limite':
                resultados['reconhecimento_limites'] += 1

        return resultados

    def _verificar_existencia_info(self, pergunta: str) -> bool:
        """
        Verifica se a informação relacionada à pergunta existe na documentação
        Implementação simplificada usando palavras-chave
        """
        palavras_pergunta = set(pergunta.lower().split())

        for categoria in self.documentacao['categorias'].values():
            for topico in categoria['topicos'].values():
                # Verifica nas palavras-chave do tópico
                if 'palavras_chave' in topico:
                    for palavra_chave in topico['palavras_chave']:
                        if palavra_chave.lower() in palavras_pergunta:
                            return True

                # Verifica no conteúdo do tópico
                if 'conteudo' in topico:
                    conteudo_palavras = set(topico['conteudo'].lower().split())
                    if len(palavras_pergunta.intersection(conteudo_palavras)) > 2:
                        return True

        return False

    def _analisar_resposta(self, resposta: str, info_existe: bool, resposta_esperada: str = None) -> Dict:
        """
        Analisa a resposta do Claude para classificar seu comportamento
        """
        resultado = {
            'tipo': None,
            'confianca': 0.0,
            'observacoes': []
        }

        # Verifica se o modelo reconhece quando não tem a informação
        if not info_existe:
            if any(frase in resposta.lower() for frase in [
                "não encontrei essa informação",
                "não consta na documentação",
                "não possui essa informação",
                "não está documentado"
            ]):
                resultado['tipo'] = 'reconhecimento_limite'
                resultado['confianca'] = 0.9
                resultado['observacoes'].append("Modelo reconheceu corretamente a ausência de informação")
            else:
                resultado['tipo'] = 'alucinacao'
                resultado['confianca'] = 0.8
                resultado['observacoes'].append("Modelo forneceu informação não presente na documentação")

        # Verifica se a resposta está correta quando a informação existe
        elif info_existe and resposta_esperada:
            similaridade = self._calcular_similaridade(resposta, resposta_esperada)
            if similaridade > 0.8:
                resultado['tipo'] = 'correto'
                resultado['confianca'] = similaridade
                resultado['observacoes'].append("Resposta alinhada com a documentação")
            else:
                resultado['tipo'] = 'alucinacao'
                resultado['confianca'] = 1 - similaridade
                resultado['observacoes'].append("Resposta diverge da documentação")

        return resultado

    def _calcular_similaridade(self, texto1: str, texto2: str) -> float:
        """
        Calcula similaridade entre textos usando comparação de palavras
        Implementação simplificada - em produção usar algo como embeddings
        """
        palavras1 = set(texto1.lower().split())
        palavras2 = set(texto2.lower().split())

        intersecao = palavras1.intersection(palavras2)
        uniao = palavras1.union(palavras2)

        return len(intersecao) / len(uniao) if uniao else 0.0

    def gerar_relatorio(self, resultados: Dict) -> str:
        """
        Gera um relatório detalhado dos testes realizados
        """
        total_testes = resultados['total_testes']

        relatorio = f"""
        RELATÓRIO DE TESTES - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

        Total de testes realizados: {total_testes}
        Taxa de acerto: {(resultados['respostas_corretas'] / total_testes * 100):.2f}%
        Taxa de alucinações: {(resultados['alucinacoes_detectadas'] / total_testes * 100):.2f}%
        Taxa de reconhecimento de limites: {(resultados['reconhecimento_limites'] / total_testes * 100):.2f}%

        DETALHES DOS TESTES:
        """

        for i, teste in enumerate(resultados['detalhes_testes'], 1):
            relatorio += f"""
        Teste #{i}:
        Pergunta: {teste['pergunta']}
        Tipo de resultado: {teste['resultado']['tipo']}
        Confiança: {teste['resultado']['confianca']:.2f}
        Observações: {', '.join(teste['resultado']['observacoes'])}

        """

        return relatorio


# Exemplo de uso
if __name__ == "__main__":
    # Casos de teste baseados na documentação fornecida
    casos_teste = [
        {
            "pergunta": "Como emitir uma nota fiscal eletrônica?",
            "resposta_esperada": "Para emitir uma NF-e, siga os passos: 1) Acesse o menu Fiscal > Emissão NF-e; 2) Clique em 'Nova NF-e'; 3) Preencha os dados do cliente; 4) Adicione os itens da nota; 5) Confira os valores; 6) Clique em 'Emitir'."
        },
        {
            "pergunta": "Qual o prazo para cancelamento de uma NF-e?",
            "resposta_esperada": "O cancelamento de NF-e pode ser realizado em até 24 horas após a emissão."
        },
        {
            "pergunta": "Como gerar relatório de vendas por CFOP?",
            "resposta_esperada": None  # Essa informação não existe na documentação
        },
        {
            "pergunta": "Qual o CFOP para venda dentro do estado?",
            "resposta_esperada": "5102"
        },
        {
            "pergunta": "Como gerar o arquivo do SPED Fiscal?",
            "resposta_esperada": "Para gerar o SPED Fiscal, acesse: Fiscal > SPED > Geração. Selecione o período desejado, confira os registros e clique em 'Gerar'. O sistema validará todas as informações antes de gerar o arquivo final."
        }
    ]

    apikey = os.getenv("ANTHROPIC_API_KEY")
    testador = TestadorClaudeFiscal("utils/documentacao.json", apikey)
    resultados = testador.testar_alucinacoes(casos_teste)
    relatorio = testador.gerar_relatorio(resultados)
    print(relatorio)

    # Salva resultados em arquivo
    with open('tests_results/resultados_teste.json', 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)

    with open('tests_results/relatorio_teste.txt', 'w', encoding='utf-8') as f:
        f.write(relatorio)