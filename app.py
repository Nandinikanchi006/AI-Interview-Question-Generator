import streamlit as st
import pdfplumber
import google.generativeai as genai
import plotly.express as px

# ---------------------
# PAGE CONFIG
# ---------------------

st.set_page_config(
    page_title="AI Interview Question Generator Pro",
    page_icon="🎤",
    layout="wide"
)

# ---------------------
# PREMIUM UI
# ---------------------

st.markdown("""
<style>

.stApp{
background: linear-gradient(
-45deg,
#0f172a,
#1e3a8a,
#7c3aed,
#06b6d4
);
background-size:400% 400%;
animation:gradient 15s ease infinite;
}

@keyframes gradient{
0%{background-position:0% 50%;}
50%{background-position:100% 50%;}
100%{background-position:0% 50%;}
}

.hero{
padding:25px;
border-radius:20px;
background:rgba(255,255,255,0.08);
backdrop-filter:blur(10px);
text-align:center;
margin-bottom:20px;
}

h1,h2,h3,p,label{
color:white !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------------
# GEMINI
# ---------------------

genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"]
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# ---------------------
# SESSION STATE
# ---------------------

if "questions" not in st.session_state:
    st.session_state["questions"] = ""

# ---------------------
# HEADER
# ---------------------

st.markdown("""
<div class="hero">

<h1>
🎤 AI Interview Question Generator Pro
</h1>

<p>
Generate AI-powered interview questions from your resume.
</p>

</div>
""", unsafe_allow_html=True)

# ---------------------
# SIDEBAR
# ---------------------

with st.sidebar:

    st.title("⚙️ Settings")

    role = st.selectbox(
        "Select Role",
        [
            "Software Engineer",
            "Data Scientist",
            "ML Engineer",
            "AI Engineer",
            "Data Analyst"
        ]
    )

    difficulty = st.selectbox(
        "Difficulty",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

# ---------------------
# FILE UPLOAD
# ---------------------

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

resume_text = ""

if uploaded_file:

    with pdfplumber.open(uploaded_file) as pdf:

        for page in pdf.pages:

            text = page.extract_text()

            if text:
                resume_text += text + " "

# ---------------------
# TABS
# ---------------------

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📄 Resume",
        "🎯 Questions",
        "📂 Project Questions",
        "📊 Analytics"
    ]
)


# ---------------------
# TAB 1
# ---------------------

with tab1:

    st.subheader("Resume Preview")

    st.text_area(
        "",
        resume_text[:5000],
        height=300
    )

# ---------------------
# TAB 2
# ---------------------

with tab2:

    if not resume_text:

        st.info(
            "Upload a resume first."
        )

    else:

        if st.button(
            "🚀 Generate Interview Questions"
        ):

            prompt = f"""
            Resume:

            {resume_text}

            Role:

            {role}

            Difficulty:

            {difficulty}

            Generate:

            - 10 Technical Questions
            - 5 HR Questions
            - 5 Project Questions

            Format nicely.
            """

            with st.spinner(
                "Generating..."
            ):

                response = model.generate_content(
                    prompt
                )

                st.session_state[
                    "questions"
                ] = response.text

                st.balloons()

        if st.session_state["questions"]:

            st.subheader(
                "Generated Questions"
            )

            st.write(
                st.session_state["questions"]
            )

            answer = st.text_area(
                "Type Your Answer"
            )

            if st.button(
                "Evaluate Answer"
            ):

                evaluation_prompt = f"""
                Questions:

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

                with st.spinner(
                    "Evaluating..."
                ):

                    result = model.generate_content(
                        evaluation_prompt
                    )

                    st.subheader(
                        "AI Evaluation"
                    )

                    st.write(
                        result.text
                    )
# ---------------------
# TAB 3 - PROJECT QUESTIONS
# ---------------------

with tab3:

    st.subheader("📂 Project Interview Questions")

    project_name = st.text_input(
        "Project Name"
    )

    project_description = st.text_area(
        "Project Description",
        height=200
    )

    if st.button(
        "🚀 Generate Project Questions"
    ):

        if project_description:

            project_prompt = f"""
            Project Name:
            {project_name}

            Project Description:
            {project_description}

            Generate:

            15 interview questions.

            Include:
            - Technical Questions
            - Design Questions
            - Challenges Faced
            - Deployment Questions
            - Future Improvements

            Format nicely.
            """

            with st.spinner(
                "Generating Project Questions..."
            ):

                response = model.generate_content(
                    project_prompt
                )

                st.session_state[
                    "project_questions"
                ] = response.text

                st.balloons()

    if "project_questions" in st.session_state:

        st.markdown("### Generated Project Questions")

        st.write(
            st.session_state[
                "project_questions"
            ]
        )
# ---------------------
# TAB 4 - ANALYTICS
# ---------------------

with tab4:

    st.subheader(
        "Analytics Dashboard"
    )

    data = {
        "Category": [
            "Technical",
            "HR",
            "Project"
        ],
        "Questions": [
            10,
            5,
            5
        ]
    }

    fig = px.pie(
        data,
        names="Category",
        values="Questions",
        title="Question Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Role",
        role
    )

    c2.metric(
        "Difficulty",
        difficulty
    )

    c3.metric(
        "Questions",
        "20"
    )