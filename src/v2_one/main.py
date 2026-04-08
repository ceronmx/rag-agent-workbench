import argparse
import sys
import os
from v2_one.models.database import engine, Base, SessionLocal, Chunk
from v2_one.models.management import wipe_database
from v2_one.rag.extractor import extract_text_from_pdf
from v2_one.rag.chunker import chunk_text
from v2_one.models.ollama_client import get_embeddings, restructure_query


def main():
    parser = argparse.ArgumentParser(description="v2-one RAG Project")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Ingest command
    ingest_parser = subparsers.add_parser("ingest", help="Ingest a PDF file")
    ingest_parser.add_argument("pdf_path", type=str, help="Path to the PDF file")
    ingest_parser.add_argument(
        "--chunk-size", type=int, default=1000, help="Size of each chunk"
    )
    ingest_parser.add_argument(
        "--overlap", type=int, default=200, help="Overlap between chunks"
    )
    ingest_parser.add_argument(
        "--document-name", type=str, help="Name of the document (defaults to filename)"
    )

    # Query command (Restructuration + Embedding)
    query_parser = subparsers.add_parser("query", help="Query the RAG system")
    query_parser.add_argument("question", type=str, help="Your question")

    # Start command
    start_parser = subparsers.add_parser("start", help="Start the application")
    start_parser.add_argument(
        "--test-mode", action="store_true", help="Wipe database on startup for testing."
    )

    args = parser.parse_args()

    if args.command == "ingest":
        doc_name = args.document_name or os.path.basename(args.pdf_path)
        print(f"Ingesting {args.pdf_path} as '{doc_name}'...")
        text = extract_text_from_pdf(args.pdf_path)
        chunks_text = chunk_text(text, chunk_size=args.chunk_size, overlap=args.overlap)
        print(f"Extracted {len(text)} characters. Created {len(chunks_text)} chunks.")

        print("Generating embeddings...")
        embeddings = get_embeddings(chunks_text)

        print("Storing in database...")
        db = SessionLocal()
        try:
            Base.metadata.create_all(bind=engine)
            for i, (txt, emb) in enumerate(zip(chunks_text, embeddings)):
                chunk = Chunk(
                    text=txt, document_name=doc_name, chunk_index=i, embedding=emb
                )
                db.add(chunk)
            db.commit()
            print(f"Successfully ingested {len(chunks_text)} chunks.")
        except Exception as e:
            print(f"Error storing chunks: {e}")
            db.rollback()
        finally:
            db.close()

    elif args.command == "query":
        print(f"User Question: {args.question}")

        # 1. Restructure
        print("Restructuring query...")
        optimized_q = restructure_query(args.question)
        print(f"Optimized Query: {optimized_q}")

        # 2. Embed
        print("Generating query embedding...")
        query_emb = get_embeddings([optimized_q])[0]
        print(f"Query embedded (dim: {len(query_emb)}).")

        print("Query processing complete. Vector search is the next step.")

    elif args.command == "start":
        print("Starting v2-one...")
        if args.test_mode:
            wipe_database()
        else:
            Base.metadata.create_all(bind=engine)
            print("Database schema verified.")
        print("Application is ready.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
