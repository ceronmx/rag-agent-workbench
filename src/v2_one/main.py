import argparse
import sys
import os
import json
import asyncio
from v2_one.models.database import engine, Base, SessionLocal, Chunk, vector_search
from v2_one.models.management import wipe_database
from v2_one.utils.migrations import run_migrations
from v2_one.rag.extractor import extract_text_from_pdf
from v2_one.rag.chunker import chunk_text
from v2_one.models.ollama_client import (
    get_embeddings,
    restructure_query,
    generate_answer,
)
from v2_one.rag.engine import rescore_results, assemble_rag_prompt
from v2_one.utils.logger import logger


async def async_main():
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

    # Query command
    query_parser = subparsers.add_parser("query", help="Query the RAG system")
    query_parser.add_argument("question", type=str, help="Your question")
    query_parser.add_argument(
        "--no-rescore", action="store_true", help="Disable LLM rescoring"
    )
    query_parser.add_argument(
        "--top-k", type=int, default=3, help="Number of chunks for final prompt"
    )

    # Start command
    start_parser = subparsers.add_parser("start", help="Start the application")
    start_parser.add_argument(
        "--test-mode", action="store_true", help="Wipe database on startup for testing."
    )

    # Clean-cache command
    subparsers.add_parser(
        "clean-cache", help="Clear temporary Python and build artifacts"
    )

    args = parser.parse_args()

    if args.command == "ingest":
        doc_name = args.document_name or os.path.basename(args.pdf_path)
        logger.info(f"Ingesting {args.pdf_path} as '{doc_name}'...")
        text = extract_text_from_pdf(args.pdf_path)
        chunks_text = chunk_text(text, chunk_size=args.chunk_size, overlap=args.overlap)
        logger.info(
            f"Extracted {len(text)} characters. Created {len(chunks_text)} chunks."
        )

        logger.info("Generating embeddings...")
        embeddings = await get_embeddings(chunks_text)

        logger.info("Storing in database...")
        db = SessionLocal()
        try:
            run_migrations()
            for i, (txt, emb) in enumerate(zip(chunks_text, embeddings)):
                chunk = Chunk(
                    text=txt, document_name=doc_name, chunk_index=i, embedding=emb
                )
                db.add(chunk)
            db.commit()
            logger.info(f"Successfully ingested {len(chunks_text)} chunks.")
        except Exception as e:
            logger.error(f"Error storing chunks: {e}")
            db.rollback()
        finally:
            db.close()

    elif args.command == "query":
        logger.info(f"--- USER QUESTION ---\n{args.question}\n")

        # 1. Restructure
        logger.info("Restructuring query for vector search...")
        optimized_q = await restructure_query(args.question)
        logger.info(f"Optimized Query: {optimized_q}\n")

        # 2. Vector Search
        logger.info("Searching vector database...")
        db = SessionLocal()
        try:
            query_emb_list = await get_embeddings([optimized_q])
            query_emb = query_emb_list[0]
            search_results = vector_search(
                db, query_emb, limit=10
            )  # Get top 10 for rescoring

            if not search_results:
                logger.info("No relevant context found.")
                return

            # 3. Rescore
            final_results = search_results
            if not args.no_rescore:
                logger.info("Rescoring results using LLM...")
                final_results = await rescore_results(optimized_q, search_results)

            # 4. Assemble
            prompt = assemble_rag_prompt(args.question, final_results, top_k=args.top_k)

            # 5. Generate
            logger.info("\n--- GENERATING ANSWER ---")
            answer = await generate_answer(prompt)
            logger.info(answer)

        except Exception as e:
            logger.error(f"Error during query: {e}")
        finally:
            db.close()

    elif args.command == "start":
        logger.info("Starting v2-one...")
        if args.test_mode:
            wipe_database()

        run_migrations()
        logger.info("Application is ready.")
    elif args.command == "clean-cache":
        logger.info("Cleaning cache and temporary artifacts...")
        import shutil

        # Clear __pycache__
        count = 0
        for root, dirs, files in os.walk("."):
            if "__pycache__" in dirs:
                pycache_path = os.path.join(root, "__pycache__")
                try:
                    shutil.rmtree(pycache_path)
                    count += 1
                except Exception as e:
                    logger.error(f"Error removing {pycache_path}: {e}")

        # Clear .pytest_cache
        if os.path.exists(".pytest_cache"):
            try:
                shutil.rmtree(".pytest_cache")
                logger.info("Removed .pytest_cache")
            except Exception as e:
                logger.error(f"Error removing .pytest_cache: {e}")

        logger.info(f"Removed {count} __pycache__ directories.")
        logger.info("Cache cleanup complete.")
    else:
        parser.print_help()


def main():
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
