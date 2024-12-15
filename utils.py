import customtkinter as ctk

def add_message_to_chat_box(chat_box, message, sender):
    """
    Добавляет сообщение в чат-бокс с выравниванием:
    - Вопросы справа (пользователь),
    - Ответы слева (бот).
    """
    # Создаём рамку для сообщения
    frame = ctk.CTkFrame(chat_box, corner_radius=10, fg_color="lightgray" if sender == "bot" else "#0078D7")
    frame.pack(fill="x", padx=10, pady=5, anchor="e" if sender == "user" else "w")
    
    # Добавляем текст сообщения в рамку
    label = ctk.CTkLabel(
        frame, 
        text=message, 
        text_color="white" if sender == "user" else "black",
        wraplength=400, 
        justify="left" if sender == "bot" else "right"
    )
    label.pack(padx=10, pady=5)

    # Обновляем и прокручиваем до конца
    chat_box.update_idletasks()

