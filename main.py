import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from app.graphs import graph
from app.tools.cv_parser_tool import cv_parser_tool
import tempfile
import os
import json


# ── Page Config 
def setup_page_config():
    st.set_page_config(
        page_title="CareerLens",
        page_icon="🔭",
        layout="wide",
        initial_sidebar_state="expanded"
    )


# ── CSS 
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

    :root {
        --bg-primary: #0a0a0f;
        --bg-secondary: #12121a;
        --bg-card: #1a1a26;
        --accent-cyan: #00e5ff;
        --accent-purple: #b44dff;
        --accent-green: #00ff9d;
        --accent-orange: #ff6b35;
        --text-primary: #e8e8f0;
        --text-secondary: #8888aa;
        --border: #2a2a40;
    }

    * { font-family: 'DM Sans', sans-serif; }
    .stApp { background-color: var(--bg-primary); color: var(--text-primary); }

    section[data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border);
    }
    section[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

    .career-lens-header {
        font-family: 'Space Mono', monospace;
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -1px;
        margin-bottom: 0.2rem;
    }

    .career-lens-tagline {
        color: var(--text-secondary);
        font-size: 0.85rem;
        font-weight: 300;
        letter-spacing: 0.5px;
        margin-bottom: 1.5rem;
    }

    .stChatMessage {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        margin-bottom: 0.75rem !important;
    }
    .stChatMessage[data-testid="chat-message-user"] {
        border-left: 3px solid var(--accent-cyan) !important;
    }
    .stChatMessage[data-testid="chat-message-assistant"] {
        border-left: 3px solid var(--accent-purple) !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple)) !important;
        color: #000 !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'Space Mono', monospace !important;
        font-size: 0.8rem !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover { opacity: 0.85 !important; transform: translateY(-1px) !important; }

    .stFileUploader {
        background: var(--bg-card) !important;
        border: 1px dashed var(--accent-cyan) !important;
        border-radius: 12px !important;
    }

    .agent-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-family: 'Space Mono', monospace;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-top: 0.5rem;
    }
    .agent-rag { background: rgba(0,229,255,0.15); color: var(--accent-cyan); border: 1px solid var(--accent-cyan); }
    .agent-sql { background: rgba(180,77,255,0.15); color: var(--accent-purple); border: 1px solid var(--accent-purple); }
    .agent-cv  { background: rgba(0,255,157,0.15); color: var(--accent-green); border: 1px solid var(--accent-green); }

    .rag-source {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-left: 3px solid var(--accent-orange);
        border-radius: 8px;
        padding: 12px 16px;
        margin-top: 8px;
        font-size: 0.8rem;
        color: var(--text-secondary);
    }
    .rag-source-title {
        color: var(--accent-orange);
        font-family: 'Space Mono', monospace;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 6px;
    }

    .token-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 12px;
        margin-top: 8px;
    }
    .token-label { color: var(--text-secondary); font-size: 0.75rem; font-family: 'Space Mono', monospace; }
    .token-value { color: var(--accent-green); font-size: 1rem; font-family: 'Space Mono', monospace; font-weight: 700; }

    .cv-uploaded {
        background: rgba(0,255,157,0.1);
        border: 1px solid var(--accent-green);
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 0.8rem;
        color: var(--accent-green);
        font-family: 'Space Mono', monospace;
        margin-top: 8px;
    }

    hr { border-color: var(--border) !important; margin: 1rem 0 !important; }
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: var(--bg-primary); }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent-cyan); }
    </style>
    """, unsafe_allow_html=True)


# ── Session State 
def init_session_state():
    defaults = {
        "messages": [],
        "user_background": None,
        "cv_uploaded": False,
        "agent_used": None,
        "rag_result": None,
        "total_tokens": 0,
        "show_rag_source": {},
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ── Helper 
AGENT_MAP = {
    "rag_agent":         ("agent-rag", "🔍 RAG Agent"),
    "sql_agent":         ("agent-sql", "🗄️ SQL Agent"),
    "cv_analysis_agent": ("agent-cv",  "📊 CV Analysis Agent"),
}

def render_agent_badge(agent_used: str):
    agent_class, agent_label = AGENT_MAP.get(agent_used, ("agent-rag", agent_used))
    st.markdown(
        f'<span class="agent-badge {agent_class}">{agent_label}</span>',
        unsafe_allow_html=True
    )


# ── Sidebar Components 
def _render_cv_uploader():
    st.markdown("#### 📄 Upload CV Kamu")
    uploaded_file = st.file_uploader("Format PDF", type=["pdf"], label_visibility="collapsed")

    if uploaded_file is not None and not st.session_state.cv_uploaded:
        with st.spinner("🔍 Memproses CV kamu..."):
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name
                result = cv_parser_tool.invoke(tmp_path)
                
                parsed = json.loads(result)
                
                formatted_background = f"""
                    Job Title: {parsed.get('job_title')}

                    Skills:
                    {', '.join(parsed.get('skills', []))}

                    Experience:
                    {parsed.get('experiences')}

                    Education:
                    {parsed.get('educations')}
                    """
                    
                st.session_state.user_background = formatted_background
                st.session_state.cv_file_path = tmp_path
                st.session_state.cv_uploaded = True
                st.success("✅ CV berhasil diproses!")
            except Exception as e:
                st.error(f"❌ Gagal memproses CV: {e}")

    if st.session_state.cv_uploaded:
        st.markdown('<div class="cv-uploaded">✅ CV sudah diupload</div>', unsafe_allow_html=True)


def _render_agent_info():
    st.markdown("#### 🤖 Agent Terakhir")
    if st.session_state.agent_used:
        render_agent_badge(st.session_state.agent_used)
    else:
        st.markdown('<span style="color:#555;font-size:0.8rem;">Belum ada percakapan</span>', unsafe_allow_html=True)


def _render_token_usage():
    st.markdown("#### ⚡ Penggunaan Token")
    st.markdown(f"""
    <div class="token-card">
        <div class="token-label">TOTAL TOKEN SESI INI</div>
        <div class="token-value">{st.session_state.total_tokens:,}</div>
    </div>
    """, unsafe_allow_html=True)


def _render_clear_button():
    if st.button("🗑️ Hapus Percakapan", use_container_width=True):
        st.session_state.messages = []
        st.session_state.agent_used = None
        st.session_state.rag_result = None
        st.session_state.show_rag_source = {}
        st.session_state.total_tokens = 0
        st.rerun()


def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="career-lens-header">🔭 CareerLens</div>', unsafe_allow_html=True)
        st.markdown('<div class="career-lens-tagline">Asisten karir berbasis AI untuk jobseeker</div>', unsafe_allow_html=True)
        st.markdown("---")
        _render_cv_uploader()
        st.markdown("---")
        _render_agent_info()
        st.markdown("---")
        _render_token_usage()
        st.markdown("---")
        _render_clear_button()
        st.markdown("---")
        st.markdown(
            '<div style="color:#555;font-size:0.7rem;font-family:Space Mono,monospace;text-align:center;">CareerLens v1.0 · Powered by GPT-4o</div>',
            unsafe_allow_html=True
        )


# ── Example Questions 
EXAMPLE_QUESTIONS = [
    "Skill apa yang paling banyak dibutuhkan di bidang IT?",
    "Berapa banyak resume di kategori Finance?",
    "Rekomendasikan pekerjaan untuk background data science",
    "Analisis skill gap untuk posisi Software Engineer",
]

def render_example_questions():
    if st.session_state.messages:
        return
    st.markdown("**💡 Coba tanyakan:**")
    cols = st.columns(2)
    for i, question in enumerate(EXAMPLE_QUESTIONS):
        with cols[i % 2]:
            if st.button(f"💬 {question}", use_container_width=True, key=f"example_{i}"):
                st.session_state.messages.append({"role": "user", "content": question})
                st.rerun()


# ── RAG Source Toggle 
def _render_rag_toggle(index: int, rag_result: str):
    show_key = f"show_rag_{index}"
    if show_key not in st.session_state.show_rag_source:
        st.session_state.show_rag_source[show_key] = False

    label = "📚 Sembunyikan Sumber RAG" if st.session_state.show_rag_source[show_key] else "📚 Lihat Sumber RAG"
    if st.button(label, key=f"rag_btn_{index}"):
        st.session_state.show_rag_source[show_key] = not st.session_state.show_rag_source[show_key]
        st.rerun()

    if st.session_state.show_rag_source.get(show_key, False):
        st.markdown(f"""
        <div class="rag-source">
            <div class="rag-source-title">📖 SUMBER DARI VECTOR DATABASE</div>
            {rag_result[:600]}...
        </div>
        """, unsafe_allow_html=True)


# ── Chat History 
def render_chat_history():
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant":
                if message.get("agent_used"):
                    render_agent_badge(message["agent_used"])
                if message.get("rag_result"):
                    _render_rag_toggle(i, message["rag_result"])


# ── Graph Invocation 
def _invoke_graph(prompt: str):
    try:
        state_input = {
            "messages": [
                HumanMessage(content=msg["content"]) if msg["role"] == "user"
                else AIMessage(content=msg["content"])
                for msg in st.session_state.messages
            ],
            "user_background": st.session_state.user_background,
            "cv_uploaded": st.session_state.cv_uploaded,
            "cv_file_path": st.session_state.get("cv_file_path")
        }

        result = graph.invoke(state_input)
        response_content = result["messages"][-1].content
        agent_used = result.get("agent_used")
        rag_result = result.get("rag_result")

        # Estimasi token
        st.session_state.total_tokens += len(prompt.split()) + len(response_content.split())

        return response_content, agent_used, rag_result

    except Exception as e:
        return f"Maaf, terjadi kesalahan: {str(e)}", None, None


# ── Chat Input 
def handle_chat_input():
    if prompt := st.chat_input("Tanya tentang karir, CV, atau pasar kerja..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("🤔 Sedang menganalisis..."):
                response_content, agent_used, rag_result = _invoke_graph(prompt)

            st.markdown(response_content)
            if agent_used:
                render_agent_badge(agent_used)
            if rag_result:
                _render_rag_toggle(len(st.session_state.messages), rag_result)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response_content,
            "agent_used": agent_used,
            "rag_result": rag_result,
        })
        st.session_state.agent_used = agent_used
        st.session_state.rag_result = rag_result
        st.rerun()

def main():
    setup_page_config()
    load_css()
    init_session_state()
    render_sidebar()

    st.markdown("### 💬 Mulai Percakapan")
    st.markdown(
        '<div style="color:#8888aa;font-size:0.85rem;margin-bottom:1rem;">Tanya apa saja tentang karir, CV, atau pasar kerja. Upload CV kamu di sidebar untuk analisis yang lebih personal.</div>',
        unsafe_allow_html=True
    )

    render_example_questions()
    render_chat_history()
    handle_chat_input()


if __name__ == "__main__":
    main()