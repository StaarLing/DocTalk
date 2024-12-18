# DocTalk: Чат с Документами

## Описание
**DocTalk** — это приложение для интерактивной работы с документами. С его помощью пользователи могут загружать файлы форматов **PDF** и **DOCX**, задавать вопросы на основе их содержания и получать ответы, используя возможности больших языковых моделей (LLM) и технологии поиска похожих текстов.

## Основные возможности
- Загрузка и обработка документов (**PDF**, **DOCX**).
- Разделение текста на блоки для удобной обработки.
- Индексация текстовых блоков с использованием **SentenceTransformer** и **FAISS** для быстрого поиска.
- Генерация ответов с помощью интеграции LLM (модель “**llama-3.1-70b-versatile**”).
- Автоматическое сохранение истории чата для каждого документа.
- Удобный пользовательский интерфейс на базе **CustomTkinter**.

## Установка
### Шаг 1: Клонируйте репозиторий
```bash
git clone https://github.com/username/docktalk.git
cd docktalk
```

### Шаг 2: Создайте виртуальное окружение
```bash
python -m venv venv
source venv/bin/activate  # Для Linux/Mac
venv\Scripts\activate   # Для Windows
```

### Шаг 4: Настройте ключ API
Создайте файл `key.env` в корне проекта и добавьте в него:
```env
GROQ_API_KEY=your_api_key_here
```

### Шаг 5: Убедитесь, что файл `key.env` добавлен в `.gitignore`
```bash
echo "key.env" >> .gitignore
```

## Использование
### Запуск приложения
1. Запустите приложение:
   ```bash
   python mainApp.py
   ```
2. Загрузите документ через пользовательский интерфейс.
3. Выберите документ из списка.
4. Задавайте вопросы на основе содержимого документа.

## Основные зависимости
- **Python 3.8+**
- **CustomTkinter**: для создания пользовательского интерфейса.
- **FAISS**: для быстрого поиска по эмбеддингам.
- **SentenceTransformer**: для получения векторных представлений текстов.
- **python-dotenv**: для безопасного управления конфиденциальными данными через файл `.env`.
- **PyPDF2** и **python-docx**: для извлечения текста из документов.

## Архитектура
### Основные компоненты
1. **Обработка документов**:
   - Текст извлекается из загружаемых файлов.
   - Текст очищается и разбивается на блоки по 300 токенов.

2. **Индексация**:
   - Для каждого блока текста создаются эмбеддинги с помощью `SentenceTransformer`.
   - Эмбеддинги индексируются с использованием FAISS.

3. **Чат**:
   - Пользователь вводит запрос, который преобразуется в эмбеддинг.
   - Выполняется поиск в индексе по близости эмбеддингов.
   - На основе найденного текста и запроса генерируется ответ с использованием LLM.

## Безопасность
API-ключ сохраняется в локальном файле `key.env`, который не отслеживается Git. Для защиты данных:
- Никогда не публикуйте `key.env` в репозитории.
- Настройте `.gitignore` для исключения конфиденциальных файлов.

## Пример работы
1. Загрузите документ (например, `example.pdf`).
2. Задайте вопрос: "Какие основные пункты указаны во введении?"
3. Приложение найдёт подходящий текст и сгенерирует ответ.

## Возможные улучшения
- Поддержка других форматов файлов (например, Excel).
- Улучшение UX/UI.
- Поддержка длинных контекстов с использованием возможностей Llama-3.1 (128k токенов).

## Контакты
- Автор: StaarLing
- Email: puhov665@gmail.com
- GitHub: https://github.com/StaarLing