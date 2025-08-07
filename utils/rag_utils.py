import os
import threading
from sklearn.metrics.pairwise import cosine_similarity
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from models.embeddings import embed_text

DOCUMENTS = []
DOCUMENTS_LOCK = threading.Lock()

def process_documents(folder_path="./data"):
    documents = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
                chunks = text.split("\n\n")  # naive chunking
                for chunk in chunks:
                    if chunk.strip():
                        documents.append({
                            "text": chunk,
                            "embedding": embed_text(chunk)
                        })
    return documents

def load_documents(folder_path="./data"):
    global DOCUMENTS
    with DOCUMENTS_LOCK:
        if not DOCUMENTS:
            DOCUMENTS = process_documents(folder_path)
    return DOCUMENTS

def retrieve_relevant_chunks(query, documents, top_k=3):
    try:
        top_k = int(top_k)
        query_embedding = embed_text(query).reshape(1, -1)
        doc_embeddings = [doc["embedding"] for doc in documents]
        similarities = cosine_similarity(query_embedding, doc_embeddings)[0]
        top_indices = similarities.argsort()[::-1][:top_k]
        top_chunks = [documents[i]["text"] for i in top_indices]
        return top_chunks
    except Exception as e:
        print(f"[ERROR] retrieve_relevant_chunks failed: {str(e)}")
        return []

class DocumentChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if not event.is_directory and event.event_type in ["created", "modified", "deleted"]:
            reload_documents()

def reload_documents(folder_path="./data"):
    global DOCUMENTS
    with DOCUMENTS_LOCK:
        DOCUMENTS = process_documents(folder_path)
    print("[INFO] Documents reloaded due to file system change.")

def start_watchdog(folder_path="./data"):
    event_handler = DocumentChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    observer.daemon = True
    observer.start()
    print(f"[INFO] Watching folder for changes: {folder_path}")
