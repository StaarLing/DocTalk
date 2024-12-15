import customtkinter as ctk
from handlers import load_document, on_select
from chat import update_scroll_region, send_message

def create_main_window(app, documents, switch_to_chat, indexer):
    app.selected_card = None
    current_document = ctk.StringVar(app)

    left_frame = ctk.CTkFrame(app, corner_radius=10, fg_color="transparent")
    left_frame.pack(side="left", fill="y", padx=10, pady=10)

    upload_button = ctk.CTkButton(
        left_frame, 
        text="Загрузить документ", 
        command=lambda: load_document(documents, current_document, doc_list_frame,indexer, 
                                      switch_to_chat, chat_box, app )
    )
    upload_button.pack(pady=10)

    canvas = ctk.CTkCanvas(left_frame, bg="#2b2b2b", bd=0, highlightthickness=0) 
    canvas.pack(side="left", fill="both", expand=True)


    scrollbar = ctk.CTkScrollbar(left_frame, orientation="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    doc_list_frame = ctk.CTkFrame(canvas, corner_radius=5, fg_color="transparent")
    canvas.create_window((0, 0), window=doc_list_frame, anchor="nw")
    doc_list_frame.bind("<Configure>", lambda e: update_scroll_region(canvas))

    # Правая часть (чат)
    right_frame = ctk.CTkFrame(app, corner_radius=10)
    right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    chat_title = ctk.CTkLabel(right_frame, textvariable=current_document, font=("Arial", 16))
    chat_title.pack(pady=5)

    chat_box = ctk.CTkScrollableFrame(right_frame, corner_radius=10)  # Используем прокручиваемую рамку
    chat_box.pack(pady=10, padx=10, fill="both", expand=True)

    input_box = ctk.CTkEntry(right_frame, placeholder_text="Введите вопрос...")
    input_box.pack(side="left", fill="x", padx=10, pady=10, expand=True)

    send_button = ctk.CTkButton(
        right_frame, 
        text="Отправить", 
        command=lambda: send_message(input_box, chat_box, documents, current_document, indexer)
    )
    send_button.pack(side="right", padx=10, pady=10)

    # Добавление документов в список
    for doc_name in documents:
        selected_card = ctk.CTkButton(
            doc_list_frame,
            text=doc_name,
            command=lambda name=doc_name: on_select(name, current_document, chat_box, documents, 
                                                    doc_list_frame, switch_to_chat, selected_card, app)  
        )
        selected_card.pack(pady=5)

    return app