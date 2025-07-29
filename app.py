import os
import streamlit as st
import fitz  # PyMuPDF for PDF text extraction
from typing_extensions import TypedDict

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END

# -------------------------
# ✅ SET YOUR GEMINI API KEY HERE
# -------------------------
os.environ["GOOGLE_API_KEY"] = "AIzaSyDk7PllVv2Xf3I1Ggx2JzGxTeHtmak5S2c"

if not os.environ.get("GOOGLE_API_KEY"):
    st.error("❌ Google Gemini API key not found!")
    st.stop()

# -------------------------
# ✅ Initialize Gemini LLM
# -------------------------
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# -------------------------
# ✅ Define State for Workflow
# -------------------------
class State(TypedDict):
    application: str
    job_role: str
    experience_level: str
    skill_match: str
    response: str

# -------------------------
# ✅ LangGraph Nodes
# -------------------------
def categorize_experience(state: State) -> State:
    prompt = ChatPromptTemplate.from_template(
        "You are a recruiter. Based on the following job application, categorize the candidate as "
        "'Entry-level', 'Mid-level', or 'Senior-level'.\n"
        "Job Role: {job_role}\n"
        "Application: {application}"
    )
    chain = prompt | llm
    experience_level = chain.invoke(state).content.strip()
    return {"experience_level": experience_level}

def assess_skillset(state: State) -> State:
    prompt = ChatPromptTemplate.from_template(
        "You are reviewing a resume for the role of {job_role}. "
        "Does the candidate's skillset match the job requirements?\n"
        "Respond with only 'Match' or 'No Match'.\n"
        "Application: {application}"
    )
    chain = prompt | llm
    skill_match = chain.invoke(state).content.strip()
    return {"skill_match": skill_match}

def schedule_hr_interview(state: State) -> State:
    return {"response": "✅ Candidate has been shortlisted for an HR interview."}

def escalate_to_recruiter(state: State) -> State:
    return {"response": "⚠️ Candidate has senior-level experience but doesn't match job skills. Escalating to recruiter."}

def reject_application(state: State) -> State:
    return {"response": "❌ Candidate doesn't meet job requirements and has been rejected."}

# -------------------------
# ✅ LangGraph Flow Logic
# -------------------------
workflow = StateGraph(State)
workflow.add_node("categorize_experience", categorize_experience)
workflow.add_node("assess_skillset", assess_skillset)
workflow.add_node("schedule_hr_interview", schedule_hr_interview)
workflow.add_node("escalate_to_recruiter", escalate_to_recruiter)
workflow.add_node("reject_application", reject_application)

def route_app(state: State) -> str:
    if state["skill_match"] == "Match":
        return "schedule_hr_interview"
    elif state["experience_level"] == "Senior-level":
        return "escalate_to_recruiter"
    else:
        return "reject_application"

workflow.add_edge(START, "categorize_experience")
workflow.add_edge("categorize_experience", "assess_skillset")
workflow.add_conditional_edges("assess_skillset", route_app)
workflow.add_edge("schedule_hr_interview", END)
workflow.add_edge("escalate_to_recruiter", END)
workflow.add_edge("reject_application", END)

app_graph = workflow.compile()

# -------------------------
# ✅ Run Screening
# -------------------------
def run_candidate_screening(application: str, job_role: str):
    return app_graph.invoke({
        "application": application,
        "job_role": job_role
    })

# -------------------------
# ✅ Resume Extraction
# -------------------------
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    return "\n".join([page.get_text() for page in doc])

# -------------------------
# ✅ Streamlit UI
# -------------------------
st.set_page_config(page_title="AI Resume Screener", page_icon="🤖")
st.title("🤖 AI Resume Screener")

job_role = st.text_input("🧑‍💼 Enter the job role you are hiring for:")

uploaded_file = st.file_uploader("📄 Upload resume (PDF or TXT)", type=["pdf", "txt"])

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        application_text = extract_text_from_pdf(uploaded_file)
    else:
        application_text = uploaded_file.read().decode("utf-8")

    st.subheader("📜 Resume Preview")
    st.text_area("✏️ Resume Text:", value=application_text, height=200)

    if st.button("🚀 Run Screening"):
        if not job_role.strip():
            st.warning("⚠️ Please enter a job role before running screening.")
            st.stop()

        with st.spinner("🔍 Analyzing the resume using Gemini..."):
            results = run_candidate_screening(application_text, job_role)

        st.success("✅ Screening Complete!")
        st.subheader("📊 Results")
        st.write("**🧑‍💼 Job Role:**", job_role)
        st.write("**📈 Experience Level:**", results["experience_level"])
        st.write("**🛠️ Skill Match:**", results["skill_match"])
        st.write("**📝 Final Decision:**", results["response"])
