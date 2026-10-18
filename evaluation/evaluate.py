import json
import logging
import shutil
from pathlib import Path

import src.config
from src.ingestion import ingest_pdf
from src.chunking import chunk_documents
from src.vector_store import create_vector_store
from src.retrieval import create_retriever
from src.chain import create_rag_chain

logger = logging.getLogger(__name__)

PDF_PATH = Path(
    "data/The room of many colours - a treasury of stories for -- Bond, Ruskin -- ( WeLib.org ).pdf"
)
QUESTIONS_PATH = Path("evaluation/questions.json")
RESULTS_PATH = Path("evaluation/results.json")


def is_abstention(answer):
    text = answer.lower()
    phrases = [
        "i don't know",
        "not in the context",
        "not provided in the context",
        "doesn't contain",
        "does not contain",
        "cannot determine",
        "can't determine",
        "not enough information",
    ]
    return any(phrase in text for phrase in phrases)


def main():
    with QUESTIONS_PATH.open("r", encoding="utf-8") as file:
        questions = json.load(file)

    db_path = Path("chroma_db")
    if db_path.exists():
        shutil.rmtree(db_path)

    documents = ingest_pdf(PDF_PATH)
    chunks = chunk_documents(documents)
    vector_store = create_vector_store(chunks)
    retriever = create_retriever(vector_store)
    rag_chain = create_rag_chain(retriever)

    results = []

    for item in questions:
        question = item["question"]
        expected = item["expected_answer"]
        answerable = item["answerable"]

        print(f"\nQuestion: {question}")

        try:
            answer = rag_chain.invoke(question)
            abstained = is_abstention(answer)

            if answerable:
                status = "REVIEW" if not abstained else "FAIL"
            else:
                status = "PASS" if abstained else "FAIL"

            results.append({
                "question": question,
                "expected_answer": expected,
                "generated_answer": answer,
                "answerable": answerable,
                "status": status,
            })

            print(f"Expected: {expected}")
            print(f"Generated: {answer}")
            print(f"Result: {status}")

        except Exception:
            logger.exception("Evaluation failed for: %s", question)
            results.append({
                "question": question,
                "status": "ERROR",
            })

    with RESULTS_PATH.open("w", encoding="utf-8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)

    print("\n--- Evaluation Summary ---")
    print(f"Total questions: {len(results)}")
    print(f"Passed: {sum(r['status'] == 'PASS' for r in results)}")
    print(f"Failed: {sum(r['status'] == 'FAIL' for r in results)}")
    print(f"Needs review: {sum(r['status'] == 'REVIEW' for r in results)}")
    print(f"Errors: {sum(r['status'] == 'ERROR' for r in results)}")
    print(f"Detailed results saved to: {RESULTS_PATH}")


if __name__ == "__main__":
    main()
