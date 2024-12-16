import customtkinter as ctk

def add_message_to_chat_box(chat_box, message, sender):
    """
    Добавляет сообщения в чат с оформлением, похожим на Telegram:
    - Сообщения бота слева, серый фон.
    - Сообщения пользователя справа, голубой фон.
    """
    # Определяем параметры стиля для бота и пользователя
    if sender == "bot":
        frame_anchor = "w"  # Выравнивание слева
        frame_bg = "#f1f1f1"  # Светло-серый фон
        text_color = "black"
    else:
        frame_anchor = "e"  # Выравнивание справа
        frame_bg = "#0088cc"  # Голубой фон для пользователя
        text_color = "white"

    # Создаем контейнер для сообщения
    frame = ctk.CTkFrame(chat_box, fg_color=frame_bg, corner_radius=15)
    frame.pack(padx=10, pady=5, anchor=frame_anchor)

    # Добавляем текст сообщения в контейнер
    label = ctk.CTkLabel(
        frame,
        text=message,
        wraplength=400,  # Ширина текста
        text_color=text_color,
        font=("Arial", 12),
        justify="left" if sender == "bot" else "right",
    )
    label.pack(padx=10, pady=5)

    # Автопрокрутка чата вниз
    chat_box.update_idletasks()
    chat_box._parent_canvas.yview_moveto(1.0)  # Прокрутка вниз


