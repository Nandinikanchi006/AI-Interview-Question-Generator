import streamlit as st
import pdfplumber

# ---------------------
# PAGE CONFIG
# ---------------------

st.set_page_config(page_title="AI Mock Interview Assistant")

# Simple placeholder state to avoid NameErrors
if "questions" not in st.session_state:
    st.session_state["questions"] = ""

resume_text = ""
role = ""
difficulty = "Medium"


class SimpleModel:
    def generate_content(self, prompt: str):
        class R:
            def __init__(self, text):
                self.text = text

        # very simple placeholder response
        return R("[Placeholder generated content based on prompt]\n" + prompt[:500])


model = SimpleModel()


st.title("AI Mock Interview Assistant")

uploaded_file = st.file_uploader("Upload resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            pages = [p.extract_text() or "" for p in pdf.pages]
        resume_text = "\n".join(pages)
    except Exception:
        resume_text = uploaded_file.getvalue().decode(errors="ignore")

role = st.text_input("Target Role", value=role)
difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], index=1)

tab1, tab2, tab3 = st.tabs(["Resume Preview", "Practice", "Analytics"])

with tab1:
    st.subheader("Resume Preview")
    st.text_area("", resume_text[:10000], height=300)

with tab2:
    if not resume_text:
        st.info("Upload a resume to begin.")
    else:
        if st.button("Generate Interview Questions"):
            prompt = f"Resume:\n\n{resume_text}\n\nTarget Role:\n{role}\n\nDifficulty:\n{difficulty}\n\nGenerate: 10 technical, 5 HR, 5 project questions."
            with st.spinner("Generating Questions..."):
                response = model.generate_content(prompt)
                st.session_state["questions"] = response.text

        if st.session_state.get("questions"):
            st.subheader("Generated Questions")
            st.write(st.session_state["questions"])

            answer = st.text_area("Type Your Answer Here")

            if st.button("Evaluate Answer"):
                evaluation_prompt = f"Interview Questions:\n{st.session_state['questions']}\n\nCandidate Answer:\n{answer}\n\nEvaluate: 1. Technical Accuracy 2. Communication 3. Confidence 4. Suggestions. Give score out of 10."
                with st.spinner("Evaluating..."):
                    result = model.generate_content(evaluation_prompt)
                    st.subheader("AI Evaluation")
                    st.write(result.text)

with tab3:
    st.subheader("Analytics")
    st.write("Role:", role)
    st.write("Difficulty:", difficulty)