import argparse
import sys
from v2_one.models.database import engine, Base
from v2_one.models.management import wipe_database
from v2_one.rag.extractor import extract_text_from_pdf
from v2_one.rag.chunker import chunk_text


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

    # Start command (previous logic)
    start_parser = subparsers.add_parser("start", help="Start the application")
    start_parser.add_argument(
        "--test-mode", action="store_true", help="Wipe database on startup for testing."
    )

    args = parser.parse_args()

    if args.command == "ingest":
        print(f"Ingesting {args.pdf_path}...")
        text = extract_text_from_pdf(args.pdf_path)
        chunks = chunk_text(text, chunk_size=args.chunk_size, overlap=args.overlap)
        print(f"Extracted {len(text)} characters.")
        print(f"Created {len(chunks)} chunks.")
        for i, chunk in enumerate(chunks[:3]):
            print(f"--- Chunk {i} ---\n{chunk[:100]}...")
        if len(chunks) > 3:
            print("...")

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
