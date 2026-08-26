import os
import tempfile

from dotenv import load_dotenv

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI
)

from langchain_community.vectorstores import Chroma

from langchain_core.prompts import (
    ChatPromptTemplate
)

from langchain_core.output_parsers import (
    StrOutputParser
)

from langchain_core.runnables import (
    RunnablePassthrough
)


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# GEMINI
# ============================================================

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)


llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=0
)


# ============================================================
# PROCESS DOCUMENT
# ============================================================

def process_document(uploaded_file):

    file_extension = (
        uploaded_file.name
        .split(".")[-1]
        .lower()
    )


    # --------------------------------------------------------
    # Temporary file
    # --------------------------------------------------------

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=f".{file_extension}"
    ) as temp_file:

        temp_file.write(
            uploaded_file.getvalue()
        )

        temp_path = temp_file.name


    # --------------------------------------------------------
    # Loader
    # --------------------------------------------------------

    if file_extension == "pdf":

        loader = PyPDFLoader(
            temp_path
        )

    elif file_extension == "docx":

        loader = Docx2txtLoader(
            temp_path
        )

    elif file_extension == "txt":

        loader = TextLoader(
            temp_path,
            encoding="utf-8"
        )

    else:

        raise ValueError(
            "Unsupported file type."
        )


    # --------------------------------------------------------
    # Load
    # --------------------------------------------------------

    docs = loader.load()


    # --------------------------------------------------------
    # Split
    # --------------------------------------------------------

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    splits = splitter.split_documents(
        docs
    )


    # --------------------------------------------------------
    # Vector store
    # --------------------------------------------------------

    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings
    )


    # --------------------------------------------------------
    # Retriever
    # --------------------------------------------------------

    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k": 4
        }
    )


    # ========================================================
    # RAG PROMPT
    # ========================================================

    system_prompt = """
You are an AI assistant answering questions
about the uploaded document.

Use ONLY the retrieved context to answer
the user's question.

If the answer cannot be found in the
retrieved context, say:

"I don't know based on the uploaded document."

Do not invent information.

Keep the answer clear and concise.

Context:
{context}
"""


    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt
            ),
            (
                "human",
                "{question}"
            )
        ]
    )


    # ========================================================
    # RAG CHAIN
    # ========================================================

    rag_chain = (
        {
            "context": (
                retriever
                | format_docs
            ),

            "question":
                RunnablePassthrough()
        }

        | prompt

        | llm

        | StrOutputParser()
    )


    # ========================================================
    # SUMMARY PROMPT
    # ========================================================

    summary_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are a document summarization assistant.

Summarize ONLY the provided document.

Include:

1. Main topic
2. Important points
3. Key findings
4. Important conclusions

Do not add information that is not
present in the document.
"""
            ),

            (
                "human",
                """
Summarize this document:

{document}
"""
            )
        ]
    )


    summary_chain = (
        summary_prompt
        | llm
        | StrOutputParser()
    )


    # ========================================================
    # RETURN EVERYTHING
    # ========================================================

    return {
        "splits": splits,
        "retriever": retriever,
        "rag_chain": rag_chain,
        "summary_chain": summary_chain
    }


# ============================================================
# FORMAT DOCUMENTS
# ============================================================

def format_docs(documents):

    return "\n\n".join(
        document.page_content
        for document in documents
    )


# ============================================================
# GENERATE SUMMARY
# ============================================================

def generate_summary(rag_data):

    document_text = "\n\n".join(
        document.page_content
        for document in rag_data["splits"]
    )

    return rag_data[
        "summary_chain"
    ].invoke(
        {
            "document": document_text
        }
    )


# ============================================================
# ASK QUESTION
# ============================================================

def ask_question(
    rag_data,
    question
):

    retriever = rag_data[
        "retriever"
    ]

    rag_chain = rag_data[
        "rag_chain"
    ]


    # --------------------------------------------------------
    # Retrieve documents
    # --------------------------------------------------------

    retrieved_docs = retriever.invoke(
        question
    )


    # --------------------------------------------------------
    # Generate answer
    # --------------------------------------------------------

    response = rag_chain.invoke(
        question
    )


    # --------------------------------------------------------
    # Sources
    # --------------------------------------------------------

    sources = set()


    for doc in retrieved_docs:

        page = doc.metadata.get(
            "page"
        )

        source_file = doc.metadata.get(
            "source",
            "Uploaded document"
        )


        if page is not None:

            filename = os.path.basename(
                source_file
            )

            sources.add(
                f"{filename} — Page {page + 1}"
            )

        else:

            sources.add(
                os.path.basename(
                    source_file
                )
            )


    return response, sorted(sources)