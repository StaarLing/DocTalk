import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class Indexer:
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        self.document_indices = {}
        self.text_blocks = []
        self.block_map = {}

    def build_index(self, documents):
        # Для каждого документа создаем отдельный индекс
        for doc_name, doc_data in documents.items():
            all_embeddings = []
            block_id = 0
            doc_index = faiss.IndexFlatL2(384)  # Размерность эмбеддингов (для 'paraphrase-MiniLM-L6-v2')

            for block in doc_data["text_blocks"]:
                # Получаем эмбеддинг для каждого текстового блока
                embedding = self.model.encode(block)
                all_embeddings.append(embedding)
                self.text_blocks.append(block)
                self.block_map[block_id] = (doc_name, block)
                block_id += 1

            # Добавляем все эмбеддинги в индекс документа
            all_embeddings = np.array(all_embeddings).astype('float32')
            doc_index.add(all_embeddings)

            # Сохраняем индекс в словарь по имени документа
            self.document_indices[doc_name] = doc_index

    def search(self, query, doc_name=None, top_k=3):
        # Создаем эмбеддинг для запроса
        query_embedding = self.model.encode([query]).astype('float32')

        results = []

        if doc_name is None:
            # Если документ не указан, ищем везде
            for doc, index in self.document_indices.items():
                distances, indices = index.search(query_embedding, top_k)
                # Добавляем все результаты в список
                for idx, distance in zip(indices[0], distances[0]):
                    if idx != -1:
                        results.append((doc, self.block_map[idx][1], distance))
        else:
            # Если документ указан, ищем только в нем
            doc_index = self.document_indices.get(doc_name)
            if doc_index is None:
                return []
            distances, indices = doc_index.search(query_embedding, top_k)
            for idx, distance in zip(indices[0], distances[0]):
                if idx != -1:
                    results.append((doc_name, self.block_map[idx][1], distance))

        return results
