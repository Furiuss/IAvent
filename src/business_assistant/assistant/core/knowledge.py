# src/assistant/core/knowledge.py
from typing import Dict, Any, List
from difflib import SequenceMatcher
import json


class KnowledgeBase:
    def __init__(self, data_source: Dict[str, Any]):
        self.data = data_source
        self._create_search_index()

    def _create_search_index(self) -> None:
        """Cria um índice plano para facilitar a busca."""
        self.search_index = {}

        def flatten_dict(d: Dict[str, Any], prefix: str = "") -> None:
            for key, value in d.items():
                new_key = f"{prefix}.{key}" if prefix else key
                if isinstance(value, dict):
                    flatten_dict(value, new_key)
                else:
                    self.search_index[new_key] = value

        flatten_dict(self.data)

    def _calculate_similarity(self, query: str, text: str) -> float:
        """Calcula a similaridade entre a query e um texto."""
        return SequenceMatcher(None, query.lower(), text.lower()).ratio()

    def get_relevant_info(self, query: str, threshold: float = 0.3) -> str:
        """
        Recupera informações relevantes da base de conhecimento baseado na query.

        Args:
            query: Texto da pergunta do usuário
            threshold: Limiar mínimo de similaridade (0 a 1)

        Returns:
            String contendo informações relevantes encontradas
        """
        relevant_info = []

        # Divide a query em palavras-chave
        keywords = query.lower().split()

        # Procura por correspondências nas chaves e valores
        for key, value in self.search_index.items():
            # Verifica similaridade com a chave
            key_score = max(self._calculate_similarity(kw, key) for kw in keywords)

            # Verifica similaridade com o valor
            value_score = max(self._calculate_similarity(kw, value) for kw in keywords)

            # Usa o maior score entre chave e valor
            max_score = max(key_score, value_score)

            if max_score >= threshold:
                relevant_info.append({
                    'key': key,
                    'value': value,
                    'score': max_score
                })

        # Ordena por relevância e formata a resposta
        relevant_info.sort(key=lambda x: x['score'], reverse=True)

        if not relevant_info:
            return "Não foram encontradas informações relevantes na base de conhecimento."

        # Formata as informações encontradas
        formatted_info = []
        for info in relevant_info[:3]:  # Limita a 3 resultados mais relevantes
            formatted_info.append(f"[{info['key']}]: {info['value']}")

        return "\n".join(formatted_info)

    def update_knowledge(self, new_data: Dict[str, Any]) -> None:
        """
        Atualiza a base de conhecimento com novas informações.

        Args:
            new_data: Dicionário com novos dados para adicionar/atualizar
        """

        def deep_update(source: Dict[str, Any], update_data: Dict[str, Any]) -> None:
            for key, value in update_data.items():
                if key in source and isinstance(source[key], dict) and isinstance(value, dict):
                    deep_update(source[key], value)
                else:
                    source[key] = value

        deep_update(self.data, new_data)
        self._create_search_index()  # Atualiza o índice de busca

    def export_knowledge(self, file_path: str) -> None:
        """
        Exporta a base de conhecimento para um arquivo JSON.

        Args:
            file_path: Caminho do arquivo para salvar
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def import_knowledge(self, file_path: str) -> None:
        """
        Importa base de conhecimento de um arquivo JSON.

        Args:
            file_path: Caminho do arquivo para carregar
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            new_data = json.load(f)
            self.data = new_data
            self._create_search_index()

    def get_categories(self) -> List[str]:
        """Retorna lista de categorias disponíveis na base de conhecimento."""
        return list(self.data.keys())

    def get_category_content(self, category: str) -> Dict[str, Any]:
        """
        Retorna todo o conteúdo de uma categoria específica.

        Args:
            category: Nome da categoria

        Returns:
            Dicionário com o conteúdo da categoria
        """
        return self.data.get(category, {})