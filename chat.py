from groq import Groq
import os
from utils import add_message_to_chat_box
from dotenv import load_dotenv

load_dotenv("key.env")
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

def generate_answer_with_llm(query, context):
    # Формируем сообщение для модели
    input_text = f"{query}\n\nContext:\n{context}"

    # Используем модель Groq для обработки запроса
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": input_text,
            }
        ],
        model="llama-3.1-70b-versatile",  # Указываем нужную модель
        max_tokens=3500
    )

    print(query)
    print(context)
    
    return chat_completion.choices[0].message.content


def send_message(input_box, chat_box, documents, current_document, indexer):
    question = input_box.get().strip()
    if not question:
        add_message_to_chat_box(chat_box, "Пожалуйста, введите вопрос.", "bot")
        return

    doc_name = current_document.get()
    if not doc_name:
        add_message_to_chat_box(chat_box, "Сначала выберите документ.", "bot")
        return

    # Добавляем вопрос пользователя
    add_message_to_chat_box(chat_box, question, "user")

    # Поиск в индексе
    results = indexer.search(question, doc_name=doc_name, top_k=3)
    
    if results:
        context = "\n".join([block for _, block, _ in results])
        response = generate_answer_with_llm(question, context)
    else:
        response = "Бот: Не удалось найти релевантный текст."

    # Добавляем ответ бота
    add_message_to_chat_box(chat_box, response, "bot")

    # Сохраняем чат в историю
    documents[doc_name]["chat"].append(question)
    documents[doc_name]["chat"].append(response)

    # Очищаем поле ввода
    input_box.delete(0, "end")



def update_scroll_region(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))
    
def switch_to_chat(doc_name, current_document, chat_box, documents, selected_card, doc_list_frame):
    # Устанавливаем текущий документ
    current_document.set(doc_name)

    # Очищаем чат-бокс
    for widget in chat_box.winfo_children():
        widget.destroy()  # Удаляем все дочерние виджеты

    # Загружаем историю чата для выбранного документа
    chat_messages = documents[doc_name]["chat"]
    for i, message in enumerate(chat_messages):
        sender = "user" if i % 2 == 0 else "bot"
        add_message_to_chat_box(chat_box, message, sender)

    # Обновляем выделение текущего документа
    if selected_card:
        selected_card.configure(border_width=3, border_color="black")

        
