import streamlit as st
import requests
import time
from prepare_vector_db import create_db_from_text, create_db_from_files  # Adjust the import path accordingly
from remove_vector_store import remove_all_vectorstores

# URL của FastAPI server
FASTAPI_SERVER_URL = "http://localhost:8000/answer/"

def call_fastapi(question):
    """Gửi câu hỏi đến FastAPI server và trả về câu trả lời."""
    response = requests.post(FASTAPI_SERVER_URL, json={"question": question})
    if response.status_code == 200:
        return response.json()["answer"]
    else:
        return "Error: Could not retrieve answer from the server."

def main():
    # Hiển thị logo ở góc trái trên cùng
    logo_path = "assets/images/snape.jpg"  # Đường dẫn đến file ảnh
    try:
        st.image(logo_path, width=100)  # Hiển thị logo riêng biệt
    except Exception:
        st.error("Logo không hiển thị! Kiểm tra đường dẫn hình ảnh.")

    # Hiển thị tiêu đề bên dưới logo
    st.title("ChatBot RAG")

    # Tab cấu hình
    tab1, tab2 = st.tabs(["Process Text/PDF", "Ask a Question"])

    with tab1:
        st.header("Text and PDF Processor")

        # Text input
        raw_text = st.text_area("Enter Text Here:")
        if st.button("Process Text"):
            if raw_text != "":
                create_db_from_text(raw_text)
                st.success("Text processed successfully!")
            else:
                st.warning("Please enter text")

        # PDF file input
        if st.button("Process PDF from folder data"):
            create_db_from_files()
            st.success("PDF processed successfully!")

        if st.button("Delete all database vectors"):
            remove_all_vectorstores()
            st.success("Removed database vectors successfully!")

    with tab2:
        st.header("Chat with AI")

        # Khởi tạo lịch sử trò chuyện
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Tạo khung chứa lịch sử trò chuyện với CSS tùy chỉnh
        chat_history_box = st.empty()

        chat_history_style = """
        <style>
        .chat-history {
            border: 1px solid #ccc;
            border-radius: 10px;
            padding: 10px;
            background-color: #67cee4;
            height: 400px;
            overflow-y: auto;
            font-size: 14px;
        }
        </style>
        """

        # Hiển thị CSS
        st.markdown(chat_history_style, unsafe_allow_html=True)

        # Hiển thị lịch sử trò chuyện trong khung tùy chỉnh
        chat_history = ""
        for message in st.session_state.messages:
            if message["role"] == "user":
                chat_history += f'<div style="color: #004466;"><b>You:</b> {message["content"]}</div>'
            else:
                chat_history += f'<div style="color: #00334d;"><b>AI:</b> {message["content"]}</div>'
        chat_history_box.markdown(f'<div class="chat-history">{chat_history}</div>', unsafe_allow_html=True)

        # Tạo vùng nhập prompt ở dưới bằng st.chat_input
        prompt = st.chat_input("Enter your prompt below:")

        if prompt:  # Khi người dùng nhập prompt
            # Hiển thị tin nhắn người dùng ngay lập tức
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Cập nhật lịch sử trò chuyện
            chat_history = ""
            for message in st.session_state.messages:
                if message["role"] == "user":
                    chat_history += f'<div style="color: #004466;"><b>You:</b> {message["content"]}</div>'
                else:
                    chat_history += f'<div style="color: #00334d;"><b>AI:</b> {message["content"]}</div>'
            chat_history_box.markdown(f'<div class="chat-history">{chat_history}</div>', unsafe_allow_html=True)

            # Xử lý câu trả lời của AI
            with st.spinner("Generating response..."):
                start_time = time.time()
                response = call_fastapi(prompt)
                inference_time = time.time() - start_time
                st.success(f"Response generated in {inference_time:.2f} seconds.")

            # Thêm câu trả lời của AI vào lịch sử
            st.session_state.messages.append({"role": "assistant", "content": response})

            # Cập nhật lịch sử sau khi có phản hồi của AI
            chat_history = ""
            for message in st.session_state.messages:
                if message["role"] == "user":
                    chat_history += f'<div style="color: #004466;"><b>You:</b> {message["content"]}</div>'
                else:
                    chat_history += f'<div style="color: #00334d;"><b>AI:</b> {message["content"]}</div>'
            chat_history_box.markdown(f'<div class="chat-history">{chat_history}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
