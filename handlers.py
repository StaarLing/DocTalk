from tkinter import filedialog
from PIL import Image, ImageTk
import customtkinter as ctk
import textwrap
import os
import re
import PyPDF2
import docx

def load_document(documents, current_document, doc_list_frame, indexer, switch_to_chat, chat_box, app):
    file_path = filedialog.askopenfilename(
        filetypes=[("Document files", "*.pdf *.docx"), ("All files", "*.*")]
    )
    if not file_path:
        return

    file_name = os.path.basename(file_path)
    if file_name in documents:
        print("Этот документ уже загружен.")
        return

    # Предобработка документа
    if file_path.endswith(".pdf"):
        raw_text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        raw_text = extract_text_from_docx(file_path)
    else:
        print("Неподдерживаемый формат файла.")
        return

    cleaned_text = clean_text(raw_text)
    text_blocks = split_text_into_blocks(cleaned_text)

    # Сохранение документа
    documents[file_name] = {
        "path": file_path,
        "text_blocks": text_blocks,
        "chat": []
    }

    # Обновление индекса
    indexer.build_index(documents)
    
    # Добавление документа в список в интерфейсе
    add_document_to_list(
        doc_list_frame=doc_list_frame,
        doc_name=file_name,
        image_path="assets/file_template.png",  # Замените на путь к изображению для карточек документов
        switch_to_chat=switch_to_chat,  # Передайте вашу функцию переключения на чат
        current_document=current_document,
        chat_box=chat_box,  # Передайте виджет чата, если нужно
        documents=documents,
        app=app  # Передайте объект приложения, если используется
    )
    
    print(f"Документ {file_name} успешно загружен и проиндексирован.")

    
def add_document_to_list(doc_list_frame, doc_name, image_path, switch_to_chat, current_document, chat_box, documents, app):
    card = ctk.CTkFrame(doc_list_frame, corner_radius=10, fg_color="#242424", border_color="#242424", border_width=3)
    card.pack(fill="both", padx=5, pady=5)

    img = Image.open(image_path)
    img = img.resize((50, 50))
    img = ImageTk.PhotoImage(img)

    img_label = ctk.CTkLabel(card, image=img, text="", width=75)
    img_label.image = img
    img_label.pack(side="left", padx=10, pady=10)

    wrapped_name = "\n".join(textwrap.wrap(doc_name, width=23))
    text_label = ctk.CTkLabel(card, text=wrapped_name, font=("Arial", 14), wraplength=250, justify="left")
    text_label.pack(side="left", padx=10, pady=10)

    card.bind("<Button-1>", lambda e: on_select(
        doc_name, current_document, chat_box, documents, doc_list_frame, switch_to_chat, card, app
    ))
    img_label.bind("<Button-1>", lambda e: on_select(
        doc_name, current_document, chat_box, documents, doc_list_frame, switch_to_chat, card, app
    ))
    text_label.bind("<Button-1>", lambda e: on_select(
        doc_name, current_document, chat_box, documents, doc_list_frame, switch_to_chat, card, app
    ))


def on_select(doc_name, current_document, chat_box, documents, doc_list_frame, switch_to_chat, card, app):
    if app.selected_card is not None:
        app.selected_card.configure(border_color="#242424", border_width=3)

    app.selected_card = card
    app.selected_card.configure(border_color="#1f6aa5", border_width=3)

    switch_to_chat(doc_name, current_document, chat_box, documents, None, doc_list_frame)



def extract_text_from_pdf(file_path):
    """Извлечение текста из PDF с помощью PyPDF2"""
    try:
        with open(file_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        print(f"Ошибка при чтении PDF: {e}")
        return ""

def extract_text_from_docx(file_path):
    """Извлечение текста из Word-документа с помощью python-docx"""
    try:
        doc = docx.Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()])
    except Exception as e:
        print(f"Ошибка при чтении DOCX: {e}")
        return ""

def clean_text(text):
    """Очистка текста от ненужных элементов"""
    # Убираем лишние пробелы и служебные символы
    text = re.sub(r"\s+", " ", text)
    # Пример удаления номеров страниц или сносок
    text = re.sub(r"Стр\.\s*\d+", "", text)
    return text.strip()

def split_text_into_blocks(text, block_size=300):
    words = text.split()
    blocks = []
    for i in range(0, len(words), block_size):
        blocks.append(" ".join(words[i:i + block_size]))
    return blocks





