import streamlit as st
import pdfplumber
import google.generativeai as genai

# ---------------------
# PAGE CONFIG
# ---------------------

st.set_page_config(
    page_title="AI Mock Interview Assistant",
    page_icon="🎤",
    layout="wide"
)

# ---------------------
# GEMINI CONFIG
# ---------------------

genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"]
)

model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------------
# TITLE
# ---------------------

st.title("🎤 AI Mock Interview Assistant")

st.write(
    "Upload your resume and practice AI-generated interview questions."
)

# ---------------------
# RESUME UPLOAD
# ---------------------

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

if uploaded_file:

    resume_text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            if text:
                resume_text += text + " "

    st.success("Resume uploaded successfully!")

    st.subheader("Resume Preview")

    st.text_area(
        "",
        resume_text[:1000],
        height=200
    )

    # ---------------------
    # QUESTION GENERATION
    # ---------------------

    if st.button("Generate Interview Questions"):

        prompt = f"""
        Analyze the following resume:

        {resume_text}

        Generate 5 interview questions.

        Questions should be relevant to:
        - Skills
        - Projects
        - Technical knowledge

        Only provide numbered questions.
        """

        with st.spinner("Generating Questions..."):

            response = model.generate_content(prompt)

            questions = response.text

            st.session_state["questions"] = questions

    if "questions" in st.session_state:

        st.subheader("Generated Questions")

        st.write(
            st.session_state["questions"]
        )

        answer = st.text_area(
            "Type Your Answer Here"
        )

        if st.button("Evaluate Answer"):

            evaluation_prompt = f"""
            Interview Question:

            {st.session_state['questions']}

            Candidate Answer:

            {answer}

            Evaluate:

            1. Technical Accuracy
            2. Communication
            3. Confidence
            4. Suggestions

            Give score out of 10.
            """

            with st.spinner("Evaluating..."):

                result = model.generate_content(
                    evaluation_prompt
                )

                st.subheader(
                    "AI Evaluation"
                )

                st.write(
                    result.text
                )

else:
    st.info(
        "Upload a resume to begin."
    )