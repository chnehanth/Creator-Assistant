import streamlit as st
from utils import generate_content

st.set_page_config(page_title="AI Content Creator", layout="centered")

# CSS styling
st.markdown("""
    <style>
    .stApp {
        background-color: #222222;
        color: white;
    }       
    .result-box {
        background-color: #f9f9f9;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        color: black;
    }
    hr.custom-line {
        border: none;
        height: 1px;
        background-color: #ccc;
        margin: 8px 0;
    }
    .info-text {
        text-align: center; 
        color: gray; 
        font-style: italic; 
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎥 AI Content Creator Assistant")
st.subheader("Generate ideas, scripts, hashtags, and SEO keywords using GPT")

groq_api_key = st.secrets["GROQ_API_KEY"]

topic = st.text_input("Enter a topic or keyword")
if st.button("Generate Content") and topic:
    with st.spinner("Generating content..."):
        try:
            content_list = generate_content(topic, groq_api_key)
            st.session_state["ideas"] = content_list
            st.session_state["selected_index"] = 0
        except Exception as e:
            st.error(f"Error: {e}")
            st.session_state["ideas"] = []
            st.session_state["selected_index"] = None

ideas = st.session_state.get("ideas", [])

if ideas:
    titles = [idea["title"] for idea in ideas]
    selected_title = st.selectbox("Choose an idea to view its details", titles)
    selected_index = titles.index(selected_title)
    selected = ideas[selected_index]

    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.markdown(f"### 🧠 Content Idea\n**{selected['title']}**")
    st.markdown('<hr class="custom-line">', unsafe_allow_html=True)

    st.markdown("### 📝 Script")
    st.write(selected.get("script", "No script available."))
    st.markdown('<hr class="custom-line">', unsafe_allow_html=True)

    st.markdown("### 🔥 Hashtags")
    st.write(", ".join(selected.get("hashtags", [])))
    st.markdown('<hr class="custom-line">', unsafe_allow_html=True)

    st.markdown("### 📈 SEO Keywords")
    st.write(", ".join(selected.get("seo_keywords", [])))
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown("""
        <div class="info-text">
            Please enter a topic and click <strong>'Generate Content'</strong> to see results here.
        </div>
    """, unsafe_allow_html=True)

