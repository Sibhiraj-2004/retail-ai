import streamlit as st
import requests
import uuid

FASTAPI_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Financial Advisor", layout="wide")

# =========================
# PAGE TOGGLE
# =========================
page = st.sidebar.radio("Choose Page", ["Admin", "User"])


# =========================
# ADMIN PAGE
# =========================
if page == "Admin":
    st.title("🔐 Admin Portal - Upload Documents")

    ADMIN_KEY = "admin123"
    password = st.text_input("Enter Admin Password", type="password")

    if password == "":
        st.info("Enter password to continue")

    elif password == ADMIN_KEY:

        uploaded_file = st.file_uploader("Upload PDF/TXT", type=["pdf", "txt"])

        if uploaded_file is not None:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}

            try:
                response = requests.post(
                    f"{FASTAPI_URL}/api/v1/upload",
                    files=files
                )

                if response.status_code == 200:
                    st.success("✅ File uploaded successfully!")
                else:
                    st.error(f"❌ Upload failed: {response.text}")

            except Exception as e:
                st.error(f"Error: {e}")

    else:
        st.error("❌ Incorrect admin password")


# =========================
# USER PAGE
# =========================
elif page == "User":
    st.title("💰 AI Financial Advisor - User Portal")

    # Initialize sessions
    if "sessions" not in st.session_state:
        st.session_state.sessions = {}

    if "current_session" not in st.session_state:
        session_id = str(uuid.uuid4())
        st.session_state.current_session = session_id
        st.session_state.sessions[session_id] = []

    # Sidebar chats
    st.sidebar.subheader("💬 Chats")

    if st.sidebar.button("➕ New Chat"):
        session_id = str(uuid.uuid4())
        st.session_state.current_session = session_id
        st.session_state.sessions[session_id] = []

    for sid in st.session_state.sessions:
        if st.sidebar.button(
            f"Chat {list(st.session_state.sessions).index(sid)+1}",
            key=sid
        ):
            st.session_state.current_session = sid

    messages = st.session_state.sessions[st.session_state.current_session]

    # Display messages
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input
    if prompt := st.chat_input("Ask your financial question"):

        # Save user message
        messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            response = requests.post(
                f"{FASTAPI_URL}/api/v1/query",
                json={"query": prompt}
            )

            if response.status_code == 200:
                answer = response.json().get("response", "No response received")
            else:
                answer = f"Error: {response.text}"

        except Exception as e:
            answer = f"Server error: {e}"

        # Save assistant response
        messages.append({"role": "assistant", "content": answer})

        with st.chat_message("assistant"):
            st.markdown(answer)