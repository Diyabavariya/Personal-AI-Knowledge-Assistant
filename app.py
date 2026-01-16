import os
from flask import Flask, render_template, request, session

# ------------------ YOUR EXISTING IMPORTS ------------------
from main import generate_response, load_all_documents
from conversation.state import ConversationState
from ingestion.loader import load_file
from ingestion.cleaner import clean_text
from ingestion.chunker import chunk_text
from ingestion.embeddings import EmbeddingGenerator
from ingestion.retrieval import InMemoryVectorStore
# -----------------------------------------------------------

app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates"
)

app.secret_key = "dev-secret-key"

# ------------------ GLOBAL STORAGE ------------------
VECTOR_STORES = {}          # session_id -> vector_store
CONVERSATION_STATES = {}    # session_id -> ConversationState
embedder = EmbeddingGenerator()
# ----------------------------------------------------

UPLOAD_ROOT = "uploads"
os.makedirs(UPLOAD_ROOT, exist_ok=True)


# ------------------ SESSION UTIL ------------------
def get_session_id():
    if "session_id" not in session:
        session["session_id"] = os.urandom(8).hex()
    return session["session_id"]


def get_session_folder():
    session_id = get_session_id()
    folder = os.path.join(UPLOAD_ROOT, session_id)
    os.makedirs(folder, exist_ok=True)
    return folder
# --------------------------------------------------


# ------------------ BUILD VECTOR STORE ------------------
def build_vector_store_for_session(folder_path):
    docs = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            text = load_file(file_path)
            docs.append({"text": text, "source": filename})
        except:
            pass

    all_chunks = []
    for doc in docs:
        cleaned = clean_text(doc["text"])
        chunks = chunk_text(cleaned)
        for c in chunks:
            all_chunks.append({"text": c, "source": doc["source"]})

    if not all_chunks:
        return None

    texts = [c["text"] for c in all_chunks]
    embeddings = embedder.embed_texts(texts)

    return InMemoryVectorStore(
        embeddings=embeddings,
        metadatas=all_chunks
    )
# ---------------------------------------------------------


# ------------------ ROUTES ------------------
@app.route("/", methods=["GET", "POST"])
def home():
    answer = None
    session_id = get_session_id()

    if session_id not in CONVERSATION_STATES:
        CONVERSATION_STATES[session_id] = ConversationState()

    if request.method == "POST":
        question = request.form.get("question")

        vector_store = VECTOR_STORES.get(session_id)

        if not vector_store:
            answer = "Please upload documents first."
        else:
            answer = generate_response(
                user_input=question,
                state=CONVERSATION_STATES[session_id],
                embedder=embedder,
                vector_store=vector_store
            )

    return render_template("index.html", answer=answer)


@app.route("/upload", methods=["POST"])
def upload():
    session_id = get_session_id()
    folder = get_session_folder()

    files = request.files.getlist("files")
    for file in files:
        if file.filename:
            file.save(os.path.join(folder, file.filename))

    VECTOR_STORES[session_id] = build_vector_store_for_session(folder)
    CONVERSATION_STATES[session_id] = ConversationState()

    return render_template("index.html", answer="Documents uploaded successfully.")


@app.route("/reset", methods=["POST"])
def reset():
    session_id = get_session_id()

    VECTOR_STORES.pop(session_id, None)
    CONVERSATION_STATES.pop(session_id, None)

    folder = get_session_folder()
    for f in os.listdir(folder):
        os.remove(os.path.join(folder, f))

    return render_template("index.html", answer="Session reset. Upload new documents.")
# ---------------------------------------------------------


if __name__ == "__main__":
    app.run(debug=True)
