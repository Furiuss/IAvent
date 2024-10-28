from typing import Dict, List, Optional
import json
from anthropic import Anthropic
import time


class HybridKnowledgeBase:
    def __init__(self, documentation_path: str, api_key: str, max_local_results: int = 3,
                 similarity_threshold: float = 0.3, use_api_threshold: float = 0.5):
        self.documentacao = self._load_documentation(documentation_path)
        self.client = Anthropic(api_key=api_key)
        self.max_local_results = max_local_results
        self.similarity_threshold = similarity_threshold
        self.use_api_threshold = use_api_threshold
        self.search_index = self._build_search_index()

    def _build_search_index(self) -> Dict:
        """Constrói índice de busca local"""
        return {str(k): str(v) for k, v in self.documentacao.items()}

    def _calculate_similarity(self, query: str, text: str) -> float:
        """Calcula similaridade entre query e texto"""
        query_words = set(query.lower().split())
        text_words = set(text.lower().split())
        intersection = query_words.intersection(text_words)
        return len(intersection) / max(len(query_words), len(text_words))

    def get_info(self, query: str, force_mode: Optional[str] = None) -> Dict:
        """
        Busca informações usando modo híbrido ou forçando um modo específico

        Args:
            query: Pergunta do usuário
            force_mode: 'local' ou 'api' para forçar um modo específico

        Returns:
            Dict com resultados e metadados da busca
        """
        start_time = time.time()

        # Primeiro tenta busca local
        local_results = self._local_search(query) if force_mode != 'api' else None

        # Decide se usa API baseado na qualidade dos resultados locais
        use_api = force_mode == 'api' or (
                force_mode != 'local' and
                (not local_results or
                 max(r['score'] for r in local_results) < self.use_api_threshold)
        )

        if use_api:
            results = self._api_search(query)
            mode_used = 'api'
        else:
            results = local_results
            mode_used = 'local'

        return {
            'results': results,
            'mode_used': mode_used,
            'processing_time': time.time() - start_time
        }

    def _local_search(self, query: str) -> List[Dict]:
        """Realiza busca local na base de conhecimento"""
        results = []

        for key, value in self.search_index.items():
            key_score = max(self._calculate_similarity(kw, key)
                            for kw in query.lower().split())
            value_score = max(self._calculate_similarity(kw, value)
                              for kw in query.lower().split())
            max_score = max(key_score, value_score)

            if max_score >= self.similarity_threshold:
                results.append({
                    'key': key,
                    'value': value,
                    'score': max_score
                })

        return sorted(results,
                      key=lambda x: x['score'],
                      reverse=True)[:self.max_local_results]

    def _api_search(self, query: str) -> Dict:
        """Realiza busca usando a API do Claude"""
        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                messages=[{
                    "role": "user",
                    "content": (f"{self._get_context_documentation()}\n\n"
                                f"Pergunta: {query}")
                }],
                max_tokens=1000
            )
            return {'response': response.content[0].text}
        except Exception as e:
            return {'error': str(e)}

    def _load_documentation(self, path: str) -> Dict:
        """
        Carrega a documentação do sistema que será usada como referência
        """
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _get_context_documentation(self) -> str:
        """
        Obtem o contexto da documentação para envio ao Claude
        """
        return f"Documentação do sistema fiscal: {json.dumps(self.documentacao, ensure_ascii=False)}"