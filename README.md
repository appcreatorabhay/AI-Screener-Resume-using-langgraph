<img width="420" height="383" alt="First file" src="https://github.com/user-attachments/assets/03cf63c0-0646-4250-96ef-65081cabfc71" />


<img width="434" height="385" alt="image" src="https://github.com/user-attachments/assets/14605e3d-2700-48fb-9c4f-3ec235060920" />



# 🤖 AI Resume Screener with Google Gemini

This Streamlit app uses Google Gemini (via the Generative Language API) to screen job applicants' resumes by:

- Categorizing experience level (Entry-level, Mid-level, Senior-level)
- Assessing skill match for a specified job role
- Providing a final recommendation (Shortlist, Reject, Escalate)

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-username/resume-screener-gemini.git
cd resume-screener-gemini
2. Install dependencies
bash
Copy
Edit
pip install streamlit pymupdf langchain langgraph langchain-google-genai
3. Set your Google Gemini API key
In the app.py file, replace the placeholder with your API key:

python
Copy
Edit
os.environ["GOOGLE_API_KEY"] = "your_google_gemini_api_key_here"
You can obtain a key from Google AI Studio.

4. Run the app
bash
Copy
Edit
streamlit run app.py




