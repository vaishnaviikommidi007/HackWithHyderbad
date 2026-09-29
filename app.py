import streamlit as st

from memory import recall_context, retain_feedback
from reviewer import review_code
from lint import run_linter


TEAM_ID = "demo-team"


st.set_page_config(
    page_title="Code Review Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# -------------------- SESSION STATE --------------------

if "review_result" not in st.session_state:
    st.session_state.review_result = None

if "review_code" not in st.session_state:
    st.session_state.review_code = ""

if "review_memories" not in st.session_state:
    st.session_state.review_memories = []

if "lint_issues" not in st.session_state:
    st.session_state.lint_issues = []


# -------------------- CUSTOM CSS --------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-size: 1.05rem;
        color: #777;
        margin-bottom: 1.5rem;
    }

    .status-card {
        padding: 12px 18px;
        border-radius: 10px;
        border: 1px solid rgba(128,128,128,0.25);
        text-align: center;
        margin-bottom: 20px;
    }

    .memory-card {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(128,128,128,0.25);
        background-color: rgba(128,128,128,0.05);
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .section-title {
        font-size: 1.4rem;
        font-weight: 650;
        margin-top: 15px;
        margin-bottom: 10px;
    }

    .learning-box {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-top: 25px;
        margin-bottom: 20px;
    }

    .step {
        text-align: center;
        padding: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# -------------------- HEADER --------------------

st.markdown(
    '<div class="main-title">🤖 Code Review Agent</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-powered code review that learns your team\'s coding standards.'
    '</div>',
    unsafe_allow_html=True
)


# -------------------- STATUS --------------------

status1, status2, status3 = st.columns(3)

with status1:
    st.markdown(
        '<div class="status-card">🟢<br><b>AI Reviewer</b><br>'
        '<small>Groq-powered analysis</small></div>',
        unsafe_allow_html=True
    )

with status2:
    st.markdown(
        '<div class="status-card">🧠<br><b>Team Memory</b><br>'
        '<small>Hindsight knowledge</small></div>',
        unsafe_allow_html=True
    )

with status3:
    st.markdown(
        '<div class="status-card">🔍<br><b>Code Linter</b><br>'
        '<small>Generic issue detection</small></div>',
        unsafe_allow_html=True
    )


# -------------------- SIDEBAR --------------------

with st.sidebar:

    st.header("🧠 Team Memory")

    memory_count = len(st.session_state.review_memories)

    if memory_count:
        st.success(f"{memory_count} relevant memories retrieved")
    else:
        st.info("Memory will appear after a review.")

    st.divider()

    st.subheader("How it works")

    st.write("1. Submit your code")
    st.write("2. Retrieve team knowledge")
    st.write("3. Generate AI review")
    st.write("4. Give team feedback")
    st.write("5. Remember feedback for future reviews")

    st.divider()

    st.caption("Team ID")
    st.code(TEAM_ID)


# -------------------- INPUT SECTION --------------------

st.markdown(
    '<div class="section-title">📝 Pull Request</div>',
    unsafe_allow_html=True
)

pr_title = st.text_input(
    "PR Title",
    placeholder="Example: Improve user authentication"
)

code = st.text_area(
    "Code",
    height=350,
    placeholder="""Paste your code here...

Example:

def get_user(id):
    try:
        return db.find(id)
    except:
        pass
"""
)


review_button = st.button(
    "🔍 Review Code",
    type="primary",
    use_container_width=True
)


# -------------------- REVIEW PIPELINE --------------------

if review_button:

    if not code.strip():
        st.warning("Please enter some code before reviewing.")
        st.stop()

    with st.spinner("Analyzing code and retrieving team knowledge..."):

        # Generic linter
        try:
            lint_issues = run_linter(code)
            st.session_state.lint_issues = lint_issues
        except Exception:
            st.session_state.lint_issues = []

        # Hindsight memory
        try:
            memories = recall_context(
                TEAM_ID,
                code
            )

            st.session_state.review_memories = memories

        except Exception as e:

            memories = []

            st.session_state.review_memories = []

            st.warning(
                f"Team memory temporarily unavailable: {e}"
            )

        # Groq reviewer
        try:

            result = review_code(
                code,
                pr_title=pr_title,
                memories=memories
            )

        except Exception as e:

            st.error(f"Review failed: {e}")
            st.stop()

    if "error" in result:

        st.error(result["error"])
        st.stop()

    st.session_state.review_result = result
    st.session_state.review_code = code


# -------------------- RESULTS --------------------

if st.session_state.review_result:

    result = st.session_state.review_result

    comments = result.get("comments", [])

    memories = st.session_state.review_memories

    lint_count = len(st.session_state.lint_issues)

    # ---------------- SUMMARY ----------------

    st.divider()

    st.markdown(
        '<div class="section-title">📊 Review Summary</div>',
        unsafe_allow_html=True
    )

    summary1, summary2, summary3 = st.columns(3)

    with summary1:
        st.metric(
            "Linter Issues",
            lint_count
        )

    with summary2:
        st.metric(
            "Memories Retrieved",
            len(memories)
        )

    with summary3:
        st.metric(
            "AI Comments",
            len(comments)
        )


    # ---------------- MEMORY SUMMARY ----------------

    if memories:

        st.markdown(
            '<div class="section-title">🧠 Team Knowledge Used</div>',
            unsafe_allow_html=True
        )

        st.info(
            f"{len(memories)} relevant team memories were retrieved "
            "and provided to the AI reviewer."
        )

        with st.expander(
            "View retrieved team memories",
            expanded=False
        ):

            for i, memory in enumerate(memories, 1):

                memory_text = memory.get(
                    "text",
                    ""
                )

                if memory_text:

                    st.markdown(
                        f"""
                        <div class="memory-card">
                        <b>Memory {i}</b><br><br>
                        {memory_text}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


    # ---------------- REVIEW COMMENTS ----------------

    st.markdown(
        '<div class="section-title">🔎 Review Comments</div>',
        unsafe_allow_html=True
    )


    if not comments:

        st.success(
            "🎉 No review comments found. Your code looks good!"
        )


    for i, comment in enumerate(comments):

        severity = comment.get(
            "severity",
            "info"
        ).upper()

        suggestion = comment.get(
            "suggestion",
            ""
        )

        reason = comment.get(
            "reason",
            ""
        )

        evidence = comment.get(
            "evidence"
        )

        rule_update = comment.get(
            "rule_update"
        )

        memory_ref = comment.get(
            "memory_ref"
        )

        # Severity icon
        if severity == "ERROR":
            icon = "🔴"
        elif severity == "WARNING":
            icon = "🟠"
        else:
            icon = "🔵"


        with st.container(border=True):

            st.markdown(
                f"### {icon} {severity} — Comment {i + 1}"
            )


            if comment.get("line"):

                st.write(
                    f"**📍 Line:** {comment['line']}"
                )


            if suggestion:

                st.markdown("**💡 Suggestion**")

                st.info(
                    suggestion
                )


            if reason:

                st.markdown("**Why?**")

                st.write(
                    reason
                )


            # Memory used for this particular comment

            if memory_ref:

                st.markdown("**🧠 Memory Used**")

                st.markdown(
                    f"""
                    <div class="memory-card">
                    {memory_ref}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # Evidence

            if evidence:

                st.markdown("**📊 Team Evidence**")

                st.success(
                    evidence
                )


            # Rule update

            if rule_update:

                st.markdown("**🔄 Rule Update**")

                st.write(
                    rule_update
                )


            # Feedback buttons

            col1, col2, col3 = st.columns(3)


            with col1:

                if st.button(
                    "✅ Accept",
                    key=f"accept_{i}",
                    use_container_width=True
                ):

                    try:

                        retain_feedback(
                            TEAM_ID,
                            suggestion,
                            "accepted"
                        )

                        st.success(
                            "Feedback saved as accepted."
                        )

                    except Exception as e:

                        st.error(
                            f"Failed to save feedback: {e}"
                        )


            with col2:

                if st.button(
                    "❌ Reject",
                    key=f"reject_{i}",
                    use_container_width=True
                ):

                    try:

                        retain_feedback(
                            TEAM_ID,
                            suggestion,
                            "rejected"
                        )

                        st.success(
                            "Feedback saved as rejected."
                        )

                    except Exception as e:

                        st.error(
                            f"Failed to save feedback: {e}"
                        )


            with col3:

                if st.button(
                    "💬 We do it this way",
                    key=f"custom_{i}",
                    use_container_width=True
                ):

                    try:

                        retain_feedback(
                            TEAM_ID,
                            suggestion,
                            "rejected",
                            note="Team does it differently."
                        )

                        st.success(
                            "Team preference saved."
                        )

                    except Exception as e:

                        st.error(
                            f"Failed to save feedback: {e}"
                        )


    # ---------------- LEARNING FLOW ----------------

    st.markdown(
        """
        <div class="learning-box">

        <h3>🧠 How the Agent Learns</h3>

        <div style="display:flex; justify-content:space-between;">

        <div class="step">
        <b>1️⃣</b><br>
        Submit Code
        </div>

        <div class="step">
        <b>2️⃣</b><br>
        Retrieve Memory
        </div>

        <div class="step">
        <b>3️⃣</b><br>
        AI Review
        </div>

        <div class="step">
        <b>4️⃣</b><br>
        Team Feedback
        </div>

        <div class="step">
        <b>5️⃣</b><br>
        Remember
        </div>

        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# -------------------- FOOTER --------------------

st.divider()

st.caption(
    "🤖 Code Review Agent • "
    "AI Review + Team Memory + Continuous Learning"
)

