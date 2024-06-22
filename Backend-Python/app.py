import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
def get_pdftext(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=8000,
        chunk_overlap=500,
        length_function=len)
    chunks = text_splitter.split_text(text)
    return chunks

def main():
   st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")

   st.header("Chat with multiple  PDFs :books:")
   st.text_input("ASk a Question abpout Document :")

   with st.sidebar:
       st.subheader("Your Document")
       pdf_docs = st.file_uploader("Uploader your PDF here and click on Process ", accept_multiple_files=True)
       if st.button("Process"):
           with st.spinner("Processing"):
               #get PDF Text
               raw_text = get_pdftext(pdf_docs)

               #get the text chunks
               text_chunks = get_text_chunks(raw_text)
               st.write(text_chunks)
               #Create  vector store



if __name__ == '__main__':
    main()