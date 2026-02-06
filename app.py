import streamlit as st

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="College Helpdesk Assistant",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 College Helpdesk Assistant")
st.caption("Answers are provided strictly from official college data.")

# ---------------- Load Data File ----------------
@st.cache_data
def load_data():
    with open("data.txt", "r", encoding="utf-8") as f:
        return f.read()

college_data = load_data()

# ---------------- Answer Logic ----------------
def get_answer(question):
    q = question.lower()
    lines = college_data.splitlines()

    keywords = {
        "course": "COURSES:",
        "location": "LOCATION:",
        "where": "LOCATION:",
        "apply": "ADMISSION APPLY:",
        "admission": "ADMISSION APPLY:",
        "document": "ADMISSION DOCUMENTS:",
        "fee": "FEES:",
        "scholarship": "SCHOLARSHIPS:",
        "semester": "SEMESTER START:",
        "attendance": "ATTENDANCE:",
        "hall": "HALL TICKET:",
        "result": "RESULTS:",
        "hostel": "HOSTEL:",
        "wifi": "WIFI:",
        "placement": "PLACEMENTS:",
        "company": "PLACEMENT COMPANIES:",
        "contact": "CONTACT:",
        "phone": "CONTACT:",
        "office": "OFFICE HOURS:",
        "timing": "OFFICE HOURS:",
        "other websites": "OTHER WEBSITES:",
        "about": "OTHER WEBSITES:",
        "hi": "HI:",
        "hello": "HI:"
    }

    section_key = None
    for word, section in keywords.items():
        if word in q:
            section_key = section
            break

    if not section_key:
        return "Information not available."

    capture = False
    answer_lines = []

    for line in lines:
        if line.strip() == section_key:
            capture = True
            continue
        if capture:
            if line.strip().endswith(":"):
                break
            answer_lines.append(line)

    answer = " ".join(answer_lines).strip()
    return answer if answer else "Information not available."

# ---------------- Chat UI ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

question = st.chat_input("Ask about admissions, fees, hostel, placements...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    answer = get_answer(question)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)
