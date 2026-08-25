import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime
import time


# ============================================================
# CONFIGURATION
# ============================================================

BACKEND = "http://127.0.0.1:8000"
API = f"{BACKEND}/api/v1/predict"
HEALTH_API = f"{BACKEND}/health"


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="GenAI News Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background: linear-gradient(
            135deg,
            #020617 0%,
            #0f172a 50%,
            #111827 100%
        );
        color: white;
    }

    /* Glass cards */
    .glass {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        transition: transform 0.2s ease;
    }

    .glass:hover {
        transform: translateY(-2px);
    }

    /* Prediction colors */
    .neon-green {
        color: #22c55e;
        text-shadow: 0 0 8px #22c55e;
    }

    .neon-red {
        color: #ef4444;
        text-shadow: 0 0 8px #ef4444;
    }

    .neon-yellow {
        color: #f59e0b;
        text-shadow: 0 0 8px #f59e0b;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        background: linear-gradient(
            90deg,
            #6366f1,
            #22c55e
        );
        color: white;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(34, 197, 94, 0.5);
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
    }

    /* Text area */
    textarea {
        border-radius: 12px !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "last_analysis" not in st.session_state:
    st.session_state.last_analysis = None

if "example_text" not in st.session_state:
    st.session_state.example_text = ""


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def check_backend_health():
    """
    Check whether FastAPI backend is running.
    """

    try:
        response = requests.get(
            HEALTH_API,
            timeout=5
        )

        return response.status_code == 200

    except requests.exceptions.RequestException:
        return False


def safe_api_call(text):
    """
    Send news article to FastAPI backend.

    Returns:
        data, error
    """

    try:

        response = requests.post(
            API,
            json={
                "text": text
            },
            timeout=60
        )

        # Handle HTTP errors
        if response.status_code != 200:

            try:
                error_data = response.json()

                detail = error_data.get(
                    "detail",
                    "Backend returned an error."
                )

                return None, (
                    f"API error {response.status_code}: "
                    f"{detail}"
                )

            except Exception:

                return None, (
                    f"API error: "
                    f"{response.status_code}"
                )

        # Parse JSON
        data = response.json()

        return data, None

    except requests.exceptions.ConnectionError:

        return None, (
            "❌ Cannot connect to the backend.\n\n"
            "Make sure FastAPI is running:\n"
            "uvicorn main:app --reload"
        )

    except requests.exceptions.Timeout:

        return None, (
            "⏱️ Backend request timed out.\n"
            "Please try again."
        )

    except requests.exceptions.JSONDecodeError:

        return None, (
            "❌ Backend returned an invalid response."
        )

    except requests.exceptions.RequestException as e:

        return None, f"❌ Request error: {str(e)}"

    except Exception as e:

        return None, f"❌ Unexpected error: {str(e)}"


def add_to_history(data):

    """
    Add successful analysis to history.
    """

    history_item = data.copy()

    history_item["timestamp"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    st.session_state.history.insert(
        0,
        history_item
    )

    # Keep latest 20
    st.session_state.history = (
        st.session_state.history[:20]
    )


def clear_history():

    st.session_state.history = []
    st.session_state.last_analysis = None


def normalize_prediction(data):

    """
    Safely obtain final prediction.
    """

    prediction = data.get(
        "final_prediction",
        data.get(
            "prediction",
            "UNKNOWN"
        )
    )

    if prediction is None:
        prediction = "UNKNOWN"

    return str(prediction).upper()


def get_confidence(data):

    try:

        confidence = float(
            data.get(
                "confidence",
                0
            )
        )

        return confidence

    except (ValueError, TypeError):

        return 0


def get_probability(data, key):

    """
    Safely obtain probability values.
    """

    try:

        value = float(
            data.get(
                key,
                0
            )
        )

        return value

    except (ValueError, TypeError):

        return 0


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🧠 GenAI System")

    st.markdown("---")

    # Backend status

    with st.spinner("Checking backend..."):

        is_backend_up = check_backend_health()

    if is_backend_up:

        st.success("✅ Backend Online")

    else:

        st.error("❌ Backend Offline")

        st.caption(
            "Start FastAPI using:\n"
            "`uvicorn main:app --reload`"
        )

    st.markdown("---")

    # Navigation

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "📊 Analytics",
            "🌐 Sources",
            "🕒 History"
        ]
    )

    st.markdown("---")

    # Example news

    with st.expander("📄 Example News"):

        if st.button(
            "Use Fake News Example",
            use_container_width=True
        ):

            st.session_state.example_text = (
                "BREAKING: Scientists discover that "
                "chocolate is the #1 cause of cancer! "
                "Major study shows 100% of cancer patients "
                "ate chocolate in their lifetime. "
                "Big Pharma doesn't want you to know this!"
            )

            st.rerun()

        if st.button(
            "Use Real News Example",
            use_container_width=True
        ):

            st.session_state.example_text = (
                "NASA's Perseverance rover has successfully "
                "collected a sample of Martian rock. "
                "The sample will be returned to Earth by "
                "a future mission for analysis. "
                "This marks a major milestone in Mars exploration."
            )

            st.rerun()

    st.markdown("---")

    # Clear history

    if st.button(
        "🗑️ Clear History",
        use_container_width=True
    ):

        clear_history()

        st.success("History cleared!")

        st.rerun()


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.title("🧠 News Intelligence Dashboard")

    st.markdown(
        """
        Analyze news articles using Machine Learning,
        NLP, Generative AI and real-time verification.
        """
    )

    st.markdown("---")

    # Default article

    default_text = st.session_state.example_text

    news = st.text_area(
        "📰 Paste News Article",
        value=default_text,
        height=250,
        placeholder=(
            "Paste a news article here..."
        )
    )

    col1, col2 = st.columns(
        [3, 1]
    )

    with col1:

        analyze_btn = st.button(
            "🚀 Analyze News",
            use_container_width=True
        )

    with col2:

        clear_btn = st.button(
            "🔄 Clear",
            use_container_width=True
        )

    if clear_btn:

        st.session_state.example_text = ""
        st.session_state.last_analysis = None

        st.rerun()

    # ========================================================
    # ANALYZE
    # ========================================================

    if analyze_btn:

        if not news.strip():

            st.warning(
                "⚠️ Please paste a news article first."
            )

        elif not is_backend_up:

            st.error(
                "❌ Backend is unreachable."
            )

            st.info(
                "Start the backend with:\n\n"
                "`uvicorn main:app --reload`"
            )

        else:

            with st.spinner(
                "🧠 AI is analyzing the news..."
            ):

                progress = st.progress(0)

                for i in range(100):

                    if i < 40:
                        time.sleep(0.005)

                    progress.progress(i + 1)

                progress.empty()

                data, error = safe_api_call(
                    news
                )

            # =================================================
            # API ERROR
            # =================================================

            if error:

                st.error(error)

                st.warning(
                    "The backend could not complete "
                    "the analysis."
                )

            # =================================================
            # SUCCESS
            # =================================================

            else:

                st.session_state.last_analysis = data

                add_to_history(data)

                final = normalize_prediction(
                    data
                )

                confidence = get_confidence(
                    data
                )

                # Prediction color

                if final == "REAL":

                    color = "neon-green"

                elif final == "FAKE":

                    color = "neon-red"

                else:

                    color = "neon-yellow"

                # =================================================
                # RESULT CARD
                # =================================================

                st.markdown(
                    f"""
                    <div class="glass">

                    <h1 class="{color}">
                    🔥 {final}
                    </h1>

                    <p>
                    {
                        data.get(
                            "verification_status",
                            "Verification unavailable"
                        )
                    }
                    </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # =================================================
                # METRICS
                # =================================================

                c1, c2, c3, c4 = st.columns(4)

                c1.metric(
                    "Prediction",
                    data.get(
                        "prediction",
                        final
                    )
                )

                c2.metric(
                    "Confidence",
                    f"{confidence:.2f}%"
                )

                c3.metric(
                    "Category",
                    data.get(
                        "category",
                        "Unknown"
                    )
                )

                c4.metric(
                    "Risk Level",
                    data.get(
                        "warning",
                        "N/A"
                    )
                )

                st.markdown("---")

                # =================================================
                # PROBABILITY CHART
                # =================================================

                real_prob = get_probability(
                    data,
                    "real_prob"
                )

                fake_prob = get_probability(
                    data,
                    "fake_prob"
                )

                if real_prob > 0 or fake_prob > 0:

                    probability_df = pd.DataFrame(
                        {
                            "Type": [
                                "Real",
                                "Fake"
                            ],
                            "Score": [
                                real_prob,
                                fake_prob
                            ]
                        }
                    )

                    fig = px.pie(
                        probability_df,
                        names="Type",
                        values="Score",
                        hole=0.45,
                        title="Prediction Probability",
                        color="Type",
                        color_discrete_map={
                            "Real": "#22c55e",
                            "Fake": "#ef4444"
                        }
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                # =================================================
                # EXPLANATION
                # =================================================

                st.subheader(
                    "🧠 Prediction Indicators"
                )

                explanations = data.get(
                    "explanation",
                    []
                )

                if explanations:

                    for item in explanations:

                        st.success(
                            str(item)
                        )

                else:

                    st.info(
                        "No prediction indicators available."
                    )

                # =================================================
                # AI EXPLANATION
                # =================================================

                st.subheader(
                    "🤖 AI Explanation"
                )

                ai_explanation = data.get(
                    "ai_explanation",
                    "No AI explanation available."
                )

                st.info(
                    ai_explanation
                )

                # =================================================
                # VERIFICATION
                # =================================================

                st.subheader(
                    "🔎 Verification"
                )

                verification_status = data.get(
                    "verification_status",
                    "Unavailable"
                )

                st.write(
                    verification_status
                )

                # =================================================
                # RAG VERIFICATION
                # =================================================

                rag = data.get(
                    "rag_verification",
                    {}
                )

                if rag:

                    with st.expander(
                        "🧩 RAG Verification Details"
                    ):

                        if isinstance(
                            rag,
                            dict
                        ):

                            st.json(rag)

                        else:

                            st.write(rag)


# ============================================================
# ANALYTICS
# ============================================================

elif page == "📊 Analytics":

    st.title(
        "📊 System Analytics"
    )

    if not st.session_state.history:

        st.warning(
            "No analysis data available yet."
        )

        st.info(
            "Go to Dashboard and analyze "
            "some news articles."
        )

    else:

        df = pd.DataFrame(
            st.session_state.history
        )

        # =====================================================
        # SUMMARY METRICS
        # =====================================================

        total = len(df)

        real_count = (
            len(
                df[
                    df["prediction"]
                    .astype(str)
                    .str.upper()
                    == "REAL"
                ]
            )
            if "prediction" in df.columns
            else 0
        )

        fake_count = (
            len(
                df[
                    df["prediction"]
                    .astype(str)
                    .str.upper()
                    == "FAKE"
                ]
            )
            if "prediction" in df.columns
            else 0
        )

        avg_confidence = (
            pd.to_numeric(
                df["confidence"],
                errors="coerce"
            ).mean()
            if "confidence" in df.columns
            else 0
        )

        m1, m2, m3, m4 = st.columns(4)

        m1.metric(
            "Total Analyses",
            total
        )

        m2.metric(
            "Real News",
            real_count
        )

        m3.metric(
            "Fake News",
            fake_count
        )

        m4.metric(
            "Avg Confidence",
            f"{avg_confidence:.2f}%"
        )

        st.markdown("---")

        # =====================================================
        # PREDICTION DISTRIBUTION
        # =====================================================

        if "prediction" in df.columns:

            st.subheader(
                "📈 Prediction Distribution"
            )

            prediction_df = (
                df["prediction"]
                .value_counts()
                .reset_index()
            )

            prediction_df.columns = [
                "Prediction",
                "Count"
            ]

            fig = px.bar(
                prediction_df,
                x="Prediction",
                y="Count",
                color="Prediction",
                color_discrete_map={
                    "REAL": "#22c55e",
                    "FAKE": "#ef4444"
                },
                title="Real vs Fake News"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # =====================================================
        # CONFIDENCE TREND
        # =====================================================

        if "confidence" in df.columns:

            st.subheader(
                "📊 Confidence Trend"
            )

            confidence_df = df.copy()

            confidence_df[
                "confidence"
            ] = pd.to_numeric(
                confidence_df[
                    "confidence"
                ],
                errors="coerce"
            )

            confidence_df = (
                confidence_df
                .dropna(
                    subset=["confidence"]
                )
                .reset_index(drop=True)
            )

            if not confidence_df.empty:

                fig2 = px.line(
                    confidence_df,
                    y="confidence",
                    markers=True,
                    title="Prediction Confidence"
                )

                fig2.update_yaxes(
                    title="Confidence (%)"
                )

                st.plotly_chart(
                    fig2,
                    use_container_width=True
                )

        # =====================================================
        # RECENT ACTIVITY
        # =====================================================

        st.subheader(
            "🕒 Recent Activity"
        )

        columns = [
            column
            for column in [
                "prediction",
                "confidence",
                "category",
                "timestamp"
            ]
            if column in df.columns
        ]

        if columns:

            st.dataframe(
                df.head(10)[columns],
                use_container_width=True
            )

        else:

            st.dataframe(
                df.head(10),
                use_container_width=True
            )


# ============================================================
# SOURCES
# ============================================================

elif page == "🌐 Sources":

    st.title(
        "🌐 Fact Check Sources"
    )

    if not st.session_state.history:

        st.warning(
            "Run an analysis first."
        )

    else:

        latest = (
            st.session_state.history[0]
        )

        realtime = latest.get(
            "realtime_verification",
            {}
        )

        if not isinstance(
            realtime,
            dict
        ):

            realtime = {}

        sources = realtime.get(
            "results",
            []
        )

        # =====================================================
        # VERIFICATION STATUS
        # =====================================================

        status = latest.get(
            "verification_status",
            "Unavailable"
        )

        st.info(
            f"Verification status: {status}"
        )

        # =====================================================
        # SOURCES
        # =====================================================

        if not sources:

            st.warning(
                "No verification sources were returned."
            )

            st.caption(
                "This can happen if the real-time "
                "search service is unavailable."
            )

        else:

            trusted = [
                source
                for source in sources
                if source.get(
                    "trusted",
                    False
                )
            ]

            untrusted = [
                source
                for source in sources
                if not source.get(
                    "trusted",
                    False
                )
            ]

            if trusted:

                st.subheader(
                    "✅ Trusted Sources"
                )

                for source in trusted:

                    title = source.get(
                        "title",
                        "Untitled source"
                    )

                    url = source.get(
                        "url",
                        ""
                    )

                    st.success(
                        f"📰 {title}"
                    )

                    if url:

                        st.markdown(
                            f"[Open Source]({url})"
                        )

            if untrusted:

                st.subheader(
                    "⚠️ Other Sources"
                )

                for source in untrusted:

                    title = source.get(
                        "title",
                        "Untitled source"
                    )

                    url = source.get(
                        "url",
                        ""
                    )

                    st.warning(
                        f"📰 {title}"
                    )

                    if url:

                        st.markdown(
                            f"[Open Source]({url})"
                        )


# ============================================================
# HISTORY
# ============================================================

elif page == "🕒 History":

    st.title(
        "🕒 Analysis History"
    )

    if not st.session_state.history:

        st.warning(
            "No analysis history available."
        )

    else:

        for idx, item in enumerate(
            st.session_state.history
        ):

            timestamp = item.get(
                "timestamp",
                "Unknown time"
            )

            prediction = item.get(
                "prediction",
                item.get(
                    "final_prediction",
                    "UNKNOWN"
                )
            )

            confidence = get_confidence(
                item
            )

            with st.expander(
                f"{timestamp} — "
                f"{prediction} "
                f"({confidence:.2f}%)"
            ):

                c1, c2, c3 = st.columns(3)

                c1.metric(
                    "Prediction",
                    prediction
                )

                c2.metric(
                    "Confidence",
                    f"{confidence:.2f}%"
                )

                c3.metric(
                    "Category",
                    item.get(
                        "category",
                        "N/A"
                    )
                )

                st.write(
                    "**Risk Level:**"
                )

                st.warning(
                    item.get(
                        "warning",
                        "N/A"
                    )
                )

                st.write(
                    "**Verification:**"
                )

                st.write(
                    item.get(
                        "verification_status",
                        "Unavailable"
                    )
                )

                st.write(
                    "**AI Explanation:**"
                )

                st.info(
                    item.get(
                        "ai_explanation",
                        "No explanation available."
                    )
                )

                explanations = item.get(
                    "explanation",
                    []
                )

                if explanations:

                    st.write(
                        "**Prediction Indicators:**"
                    )

                    for explanation in explanations:

                        st.success(
                            str(explanation)
                        )

                # Delete entry

                if st.button(
                    "🗑️ Delete This Entry",
                    key=f"delete_{idx}"
                ):

                    st.session_state.history.pop(
                        idx
                    )

                    st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "🧠 GenAI News Intelligence System | "
    "Machine Learning + NLP + Generative AI"
)