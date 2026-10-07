from pathlib import Path

from langchain_core.tools import tool
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


KB_PATH = Path(__file__).resolve().parent.parent / "knowledge_base"


def load_documents():
    documents = []

    for file in KB_PATH.glob("*.md"):

        text = file.read_text(encoding="utf-8")

        sections = text.split("\n## ")

        for section in sections:

            section = section.strip()

            if section:
                documents.append({
                    "source": file.name,
                    "content": section
                })

    return documents


documents = load_documents()


@tool
def rag(query: str) -> str:
    """
    Search the internal company knowledge base for authoritative information about company policies, support procedures, ticket statuses, refunds, security, escalation, and internal processes.

Use this tool to retrieve existing internal knowledge and provide answers grounded in the returned passages. It returns relevant document excerpts, source filenames, and relevance scores.

If the knowledge base does not contain sufficient information, report that limitation rather than inventing a policy.

Do not use search_public_web to substitute public information for an internal company policy. Do not use this tool to modify tickets; use update_support_ticket for authorized database changes.



    """

    if not documents:
        return (
            "The internal knowledge base is empty. "
            "No internal information is available."
        )

    texts = [
        document["content"]
        for document in documents
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        sublinear_tf=True
    )

    vectors = vectorizer.fit_transform(texts)

    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(
        query_vector,
        vectors
    )[0]

    ranked_indexes = similarities.argsort()[::-1]

    # Minimum similarity required to consider
    # a document genuinely relevant.
    MIN_RELEVANCE = 0.10

    results = []

    for index in ranked_indexes[:3]:

        score = similarities[index]

        if score < MIN_RELEVANCE:
            continue

        results.append(
            f"Source: {documents[index]['source']}\n"
            f"Relevance: {score:.2f}\n"
            f"Policy:\n{documents[index]['content']}"
        )

    if not results:
        return (
            "NO_RELEVANT_INTERNAL_INFORMATION_FOUND\n"
            "The internal knowledge base does not contain "
            "sufficient information to answer this question."
        )

    return (
        "RELEVANT_INTERNAL_INFORMATION_FOUND\n\n"
        + "\n\n---\n\n".join(results)
    )