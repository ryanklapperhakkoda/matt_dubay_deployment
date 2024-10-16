import streamlit as st
import PyPDF2
import difflib
from openai import OpenAI
from io import StringIO
from dotenv import load_dotenv
import os

load_dotenv()

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def compare_pdfs(pdf1_text, pdf2_text):
    differ = difflib.Differ()
    diff = list(differ.compare(pdf1_text.splitlines(), pdf2_text.splitlines()))
    return diff

def summarize_differences(pdf1_text, pdf2_text):
    client = OpenAI()

    system_prompt = f"""
    You are a helpful assistant tasked with summarizing the differences between two documents. Your goal is to identify and clearly articulate the key distinctions between the content, structure, or style of these documents.

    Here is the first document:
    <document1>
    {pdf1_text}
    </document1>

    Here is the second document:
    <document2>
    {pdf2_text}
    </document2>

    To summarize the differences between these documents, please follow these steps:

    1. Carefully read and analyze both documents.
    2. Identify the main topics or themes in each document.
    3. Compare the content, focusing on:
    a. Information present in one document but not the other
    b. Conflicting information or viewpoints
    c. Differences in emphasis or detail
    4. Note any differences in structure, such as organization, headings, or formatting.
    5. Observe any variations in writing style, tone, or language use.

    Present your summary of the differences in the following format:

    <summary>
    1. Content Differences:
    [List the main content differences you've identified]

    2. Structural Differences:
    [Describe any notable differences in document structure]

    3. Stylistic Differences:
    [Explain any significant differences in writing style or tone]

    4. Overall Assessment:
    [Provide a brief overall assessment of how different the documents are and what the most significant differences are]
    </summary>

    Be concise but thorough in your summary, focusing on the most important and noticeable differences between the documents. If you find that the documents are very similar in some aspects, you may note this briefly, but concentrate primarily on the differences."""
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Summarize the key differences between these documents"}
        ]
    )
    
    return response.choices[0].message

def main():
    st.title("PDF Compare Module")

    uploaded_files = st.file_uploader("Choose PDF files", accept_multiple_files=True, type="pdf")

    if len(uploaded_files) == 2:
        pdf1_text = extract_text_from_pdf(uploaded_files[0])
        pdf2_text = extract_text_from_pdf(uploaded_files[1])
        
        diff = compare_pdfs(pdf1_text, pdf2_text)
        
        st.subheader("Differences:")
        diff_text = "\n".join(diff)
        st.text_area("Raw Differences", diff_text, height=300)
        
        if st.button("Summarize Differences"):
            summary = summarize_differences(pdf1_text, pdf2_text)
            st.subheader("Summary of Differences:")
            st.write(summary)
        else:
            st.write("Please upload exactly two PDF files to compare.")

if __name__ == "__main__":
    main()