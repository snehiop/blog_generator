import streamlit as st
import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

model = ChatOpenAI(model="gpt-4o", temperature=0.4)

st.set_page_config(page_title="AI Blog Generator", layout="wide")
st.title("📄 AI Blog Generator from JSON Files")

uploaded_files = st.file_uploader("📤 Upload at least 3 JSON files", type="json", accept_multiple_files=True)

if uploaded_files and len(uploaded_files) >= 3:
    json_data = [json.load(file) for file in uploaded_files]

    context = "\n\n".join(
        [f"JSON {i+1}:\n{json.dumps(j, indent=2)[:1500]}..." for i, j in enumerate(json_data)]
    )

    # 1. Generate Title
    title_msgs = [
        SystemMessage(content="You are a content strategist. Write a catchy blog title from JSON context."),
        HumanMessage(content=f"Context:\n{context}\n\nOnly output the title.")
    ]
    title = model.invoke(title_msgs).content.strip()
    st.subheader("📝 Title")
    st.success(title)

    # 2. Generate Outline
    outline_msgs = [
        SystemMessage(content="You are a blog strategist. Create a clean outline."),
        HumanMessage(content=f"Based on title: {title}\nContext:\n{context}\n\nWrite the outline:")
    ]
    outline = model.invoke(outline_msgs).content.strip()
    st.subheader("📋 Outline")
    st.markdown(outline)

    # 3. Generate Blog Content
    content_msgs = [
        SystemMessage(content="You are a blog writer. Generate the blog."),
        HumanMessage(content=f"Use title:\n{title}\n\nOutline:\n{outline}\n\nContext:\n{context}\n\nWrite blog content:")
    ]
    content = model.invoke(content_msgs).content.strip()
    st.subheader("📄 Blog Content")
    st.markdown(content)

    # 4. Save to Markdown
    if st.button("💾 Save Blog to final_output.md"):
        with open("final_output.md", "w", encoding="utf-8") as f:
            f.write(content)
        st.success("Saved to final_output.md")

    # 5. Feedback Loop
    st.subheader("🔁 Feedback / Improvements?")
    feedback = st.text_area("Suggest edits or rewrite instructions:")
    if st.button("Regenerate Blog with Feedback"):
        feedback_msgs = [
            SystemMessage(content="You're a blog writer. Regenerate based on feedback."),
            HumanMessage(content=f"""
Feedback: {feedback}
Title: {title}
Outline: {outline}
Context: {context}
""")
        ]
        revised = model.invoke(feedback_msgs).content.strip()
        st.subheader("🆕 Updated Blog")
        st.markdown(revised)

else:
    st.info("Please upload at least 3 JSON files to begin.")

