import os

from ingestion.loader import load_file
from ingestion.cleaner import clean_text
from ingestion.chunker import build_semantic_blocks
from ingestion.embeddings import EmbeddingGenerator
from ingestion.retrieval import VectorStore
from generation.llm_answer import llm_answer


from generation.answer_formatter import (
    format_definition,
    format_explanation,
    format_comparison,
    is_weak_answer
)

from conversation.state import ConversationState


# ----------------------------
# LOAD DOCUMENTS
# ----------------------------

def load_all_documents(folder_path):
    documents = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            try:
                text = load_file(file_path)
                documents.append({
                    "text": text,
                    "source": filename
                })
            except Exception as e:
                print(f"Skipping {filename}: {e}")

    return documents


# ----------------------------
# RESPONSE GENERATION (RAG)
# ----------------------------

def generate_response(user_input, state, embedder, vector_store):
    # Embed the query
    query_embedding = embedder.embed_texts([user_input])[0]

    # Retrieve relevant document chunks
    docs = vector_store.search(query_embedding, top_k=4)
    context = "\n".join(docs)

    if not context.strip():
        return "No relevant information found in documents."

    # Let LLM handle answering + formatting
    return llm_answer(user_input, context)



# ----------------------------
# MAIN CHAT LOOP
# ----------------------------

def main():
    # STEP 1: LOAD DOCUMENTS
    docs = load_all_documents("data/raw_docs")

    if not docs:
        print("No documents found in data/raw_docs")
        return

    # STEP 2: CLEAN + CHUNK
    all_chunks = []

    for doc in docs:
        cleaned_text = clean_text(doc["text"])
        blocks = build_semantic_blocks(cleaned_text)

        for block in blocks:
            all_chunks.append({
                "text": block,
                "source": doc["source"]
            })

    if not all_chunks:
        print("No chunks created from documents")
        return

    # STEP 3: EMBEDDINGS
    texts = [c["text"] for c in all_chunks]

    embedder = EmbeddingGenerator()
    embeddings = embedder.embed_texts(texts)

    # STEP 4: VECTOR STORE (FIXED)
    vector_store = VectorStore(
        embeddings=embeddings,
        texts=texts
    )

    print(f"Indexed {len(all_chunks)} chunks from {len(docs)} documents.\n")

    # STEP 5: CHAT
    state = ConversationState()

    print("Personal AI Assistant is ready.")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        response = generate_response(
            user_input=user_input,
            state=state,
            embedder=embedder,
            vector_store=vector_store
        )

        state.add("user", user_input)
        state.add("assistant", response)

        print("\nAssistant:", response, "\n")


if __name__ == "__main__":
    main()
