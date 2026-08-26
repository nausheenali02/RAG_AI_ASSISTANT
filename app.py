import streamlit as st

from rag import (
    process_document,
    generate_summary,
    ask_question
)

from styles import load_styles


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="RAG AI Assistant",
    page_icon="🤖",
    layout="centered"
)

load_styles()


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_action" not in st.session_state:
    st.session_state.selected_action = None

if "summary" not in st.session_state:
    st.session_state.summary = None

if "document_name" not in st.session_state:
    st.session_state.document_name = None

if "rag_data" not in st.session_state:
    st.session_state.rag_data = None


# ============================================================
# HEADER
# ============================================================

st.title("🤖 RAG AI Assistant")

st.caption(
    "Chat with your documents using "
    "Retrieval-Augmented Generation"
)


# ============================================================
# FILE UPLOAD
# ============================================================

st.subheader(" Upload your document")

uploaded_file = st.file_uploader(
    "Drop your file here",
    type=["pdf", "docx", "txt"],
    label_visibility="collapsed"
)


# ============================================================
# DOCUMENT PROCESSING
# ============================================================

if uploaded_file is not None:

    # --------------------------------------------------------
    # Detect new document
    # --------------------------------------------------------

    if (
        st.session_state.document_name
        != uploaded_file.name
    ):

        st.session_state.document_name = (
            uploaded_file.name
        )

        st.session_state.messages = []

        st.session_state.selected_action = None

        st.session_state.summary = None

        with st.spinner(
            "Processing your document..."
        ):

            st.session_state.rag_data = (
                process_document(uploaded_file)
            )


    # --------------------------------------------------------
    # Document ready
    # --------------------------------------------------------

    st.success(
        f"✅ {uploaded_file.name} is ready"
    )


    # ========================================================
    # ACTION SELECTION
    # ========================================================

    st.divider()

    st.subheader(
        "What would you like to do?"
    )


    # ========================================================
    # TWO OPTIONS SIDE BY SIDE
    # ========================================================

    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    with col1:

        with st.container(border=True):


            st.markdown(
                "**Summarize Document**"
            )

            st.caption(
                "Get the main points, findings "
                "and conclusion."
            )

            if st.button(
                "🪄 Summarize",
                key="summary_button",
                use_container_width=True
            ):

                st.session_state.selected_action = (
                    "summary"
                )

                st.rerun()


    # --------------------------------------------------------
    # CHAT
    # --------------------------------------------------------

    with col2:

        with st.container(border=True):


            st.markdown(
                "**Chat with Document**"
            )

            st.caption(
                "Ask questions and get answers "
                "from your document."
            )

            if st.button(
                "💬 Start Chat",
                key="chat_button",
                use_container_width=True
            ):

                st.session_state.selected_action = (
                    "chat"
                )

                st.rerun()


    # ========================================================
    # SUMMARY MODE
    # ========================================================

    if (
        st.session_state.selected_action
        == "summary"
    ):

        st.divider()

        st.subheader(
            " Document Summary"
        )


        if st.button(
            "✨ Generate Summary",
            use_container_width=True
        ):

            with st.spinner(
                "Generating summary..."
            ):

                st.session_state.summary = (
                    generate_summary(
                        st.session_state.rag_data
                    )
                )


        if st.session_state.summary:

            st.markdown(
                st.session_state.summary
            )


    # ========================================================
    # CHAT MODE
    # ========================================================

    elif (
        st.session_state.selected_action
        == "chat"
    ):

        st.divider()

        st.subheader(
            "💬 Chat with your document"
        )


        # ----------------------------------------------------
        # Previous messages
        # ----------------------------------------------------

        for message in (
            st.session_state.messages
        ):

            with st.chat_message(
                message["role"]
            ):

                st.markdown(
                    message["content"]
                )


        # ----------------------------------------------------
        # Chat input
        # ----------------------------------------------------

        question = st.chat_input(
            "Ask anything about your document..."
        )


        if question:

            # -----------------------------------------------
            # User message
            # -----------------------------------------------

            with st.chat_message("user"):

                st.markdown(question)


            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question
                }
            )


            # -----------------------------------------------
            # AI response
            # -----------------------------------------------

            with st.chat_message(
                "assistant"
            ):

                with st.spinner(
                    "Thinking..."
                ):

                    response, sources = ask_question(
                        st.session_state.rag_data,
                        question
                    )


                st.markdown(response)


            # -----------------------------------------------
            # Save response
            # -----------------------------------------------

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response
                }
            )


            # -----------------------------------------------
            # Sources
            # -----------------------------------------------

            if sources:

                st.markdown("### Sources")

                for source in sources:

                    st.write(
                        f" {source}"
                    )