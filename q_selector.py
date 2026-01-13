import streamlit as st
import random

# --- Page Configuration ---
st.set_page_config(
    page_title="Seminar Question Picker",
    page_icon="🎓",
    layout="centered"
)

# --- Session State Initialization ---
# We use session_state to remember the lists between button clicks
if 'questions_pool' not in st.session_state:
    st.session_state.questions_pool = []
if 'asked_questions' not in st.session_state:
    st.session_state.asked_questions = []
if 'current_question' not in st.session_state:
    st.session_state.current_question = None

# --- Sidebar: Input Area ---
with st.sidebar:
    st.header("📝 Setup")
    st.write("Paste your list of questions below (one per line).")
    
    # Input field
    raw_text = st.text_area("Question List", height=300)
    
    # Load Button
    if st.button("Load/Reset Questions", type="primary"):
        if raw_text.strip():
            # Split text by new lines and remove empty strings
            questions = [q.strip() for q in raw_text.split('\n') if q.strip()]
            st.session_state.questions_pool = questions
            st.session_state.asked_questions = []
            st.session_state.current_question = None
            st.success(f"Loaded {len(questions)} questions!")
        else:
            st.warning("Please paste some text first.")

    st.markdown("---")
    st.caption("Instructions: Paste questions, click Load, then use the main screen to pick questions.")

# --- Main App Interface ---
st.title("🎓 Seminar Discussion")

# 1. The Selection Button
# We place this at the top so it's easy to hit "Next"
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    pick_button = st.button("🎲 Pick Random Question", use_container_width=True)

# Logic for picking a question
if pick_button:
    if st.session_state.questions_pool:
        # Select a random question
        selected = random.choice(st.session_state.questions_pool)
        
        # Update State: Remove from pool, add to history, set as current
        st.session_state.questions_pool.remove(selected)
        st.session_state.asked_questions.append(selected)
        st.session_state.current_question = selected
    else:
        st.error("No questions remaining in the pool!")

# 2. Large Display Area
st.divider()

if st.session_state.current_question:
    st.markdown(
        f"""
        <div style="text-align: center; padding: 50px; background-color: #f0f2f6; border-radius: 10px; border: 2px solid #dcdcdc;">
            <h1 style="color: #333; font-size: 40px;">{st.session_state.current_question}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <div style="text-align: center; color: gray; padding: 50px;">
            <h3>Waiting to start...</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# 3. Lists Management (History and Remaining)
# Using expanders to keep the main view clean for the projector
col_history, col_remaining = st.columns(2)

with col_history:
    with st.expander("📂 Asked Questions History", expanded=True):
        if st.session_state.asked_questions:
            # Show reversed so the most recent is at the top
            for i, q in enumerate(reversed(st.session_state.asked_questions), 1):
                st.markdown(f"**{len(st.session_state.asked_questions) - i + 1}.** {q}")
        else:
            st.write("No questions asked yet.")

with col_remaining:
    with st.expander(f"📥 Remaining Pool ({len(st.session_state.questions_pool)})", expanded=False):
        if st.session_state.questions_pool:
            for q in st.session_state.questions_pool:
                st.markdown(f"- {q}")
        else:
            st.write("Pool is empty.")
