import customtkinter as ctk
from gui import create_main_window
from chat import switch_to_chat
from indexer import Indexer

documents = {}
indexer = Indexer()

root = ctk.CTk()
root.title("DocTalk")
root.geometry("1200x600")

create_main_window(root, documents, switch_to_chat, indexer)

root.mainloop()