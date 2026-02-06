import os
os.environ["TRANSFORMERS_NO_TF"] = "1"

import streamlit as st
import pandas as pd

from auth import authenticate
from utils.pdf_utils import pdf_to_images
from ocr.trocr_engine import extract_text
from scoring.final_score import calculate_score
from plagiarism.detector import plagiarism_score
from analytics.dashboard import show_analytics

# -------------------------------------------------
# CONSTANTS
# -------------------------------------------------
MODEL_PDF_PATH = "storage/model_answer.pdf"

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="MindGrade++",
    page_icon="🧠",
    layout="wide"
)

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "role" not in st.session_state:
    st.session_state.role = None

# -------------------------------------------------
# LOGIN PAGE
# -------------------------------------------------
if not st.session_state.role:
    st.title("🔐 MindGrade++ Login")

    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input("Username")
    with col2:
        password = st.text_input("Password", type="password")

    if st.button("Login"):
        role = authenticate(username, password)
        if role:
            st.session_state.role = role
            st.success(f"Logged in as {role.capitalize()}")
            st.rerun()
        else:
            st.error("Invalid credentials")

# -------------------------------------------------
# MAIN DASHBOARD
# -------------------------------------------------
else:
    st.sidebar.success(f"Role: {st.session_state.role.upper()}")
    st.title("🧠 MindGrade++ – Intelligent Subjective Answer Evaluation")

    # ---------------- TEACHER DASHBOARD ----------------
    if st.session_state.role == "teacher":
        st.subheader("👩‍🏫 Teacher Dashboard")

        model_pdf = st.file_uploader(
            "📘 Upload Model Answer PDF",
            type=["pdf"]
        )

        if model_pdf:
            os.makedirs("storage", exist_ok=True)
            with open(MODEL_PDF_PATH, "wb") as f:
                f.write(model_pdf.read())

            st.success("Model answer PDF uploaded and saved successfully")

    # ---------------- STUDENT DASHBOARD ----------------
    if st.session_state.role == "student":
        st.subheader("👨‍🎓 Student Dashboard")
        st.info("Upload your answer sheet to view evaluated results.")

        if not os.path.exists(MODEL_PDF_PATH):
            st.warning("Model answer not uploaded by teacher yet.")
    
    # ---------------- COMMON INPUT ----------------
    student_pdf = st.file_uploader(
        "✍️ Upload Student Answer PDF",
        type=["pdf"]
    )

    marks = st.number_input(
        "Marks per Question",
        min_value=1,
        max_value=20,
        value=5
    )

    # -------------------------------------------------
    # EVALUATION PIPELINE
    # -------------------------------------------------
    if os.path.exists(MODEL_PDF_PATH) and student_pdf:
        with st.spinner("Processing PDFs and extracting text..."):
            with open(MODEL_PDF_PATH, "rb") as f:
                model_images = pdf_to_images(f.read())

            student_images = pdf_to_images(student_pdf.read())

        total_score = 0
        max_total = 0
        results = []

        st.divider()

        for i, (m_img, s_img) in enumerate(
            zip(model_images, student_images)
        ):
            st.subheader(f"📘 Question {i+1}")

            model_text = extract_text(m_img)
            student_text = extract_text(s_img)

            score, explanation = calculate_score(
                student_text,
                model_text,
                marks
            )

            plag_score = plagiarism_score(
                student_text, model_text
            )

            col1, col2 = st.columns(2)

            # -------- Model Answer (Teacher only) --------
            with col1:
                if st.session_state.role == "teacher":
                    st.markdown("**Model Answer (Extracted)**")
                    st.text_area(
                        f"Model Answer {i+1}",
                        model_text,
                        height=150
                    )
                else:
                    st.markdown("**Model Answer**")
                    st.info("Hidden for students")

            # -------- Student Answer (Both) --------
            with col2:
                st.markdown("**Student Answer (Extracted)**")
                st.text_area(
                    f"Student Answer {i+1}",
                    student_text,
                    height=150
                )

            st.metric("Score", f"{score} / {marks}")
            st.caption(f"🧬 Plagiarism Similarity: {plag_score}")

            with st.expander("📊 Explainable Evaluation"):
                st.json(explanation)

            total_score += score
            max_total += marks

            results.append({
                "Question": i + 1,
                "Score": score,
                "Max Marks": marks,
                "Semantic Similarity": explanation["Semantic Similarity"],
                "Keyword Match": explanation["Keyword Match"],
                "Grammar Errors": explanation["Grammar Errors"],
                "Length Score": explanation["Length Score"],
                "Plagiarism Score": plag_score
            })

            st.divider()

        # ---------------- FINAL SCORE ----------------
        st.success(f"🎯 Final Score: {total_score} / {max_total}")

        # ---------------- TEACHER ANALYTICS ----------------
        if st.session_state.role == "teacher":
            show_analytics(results)

            df = pd.DataFrame(results)
            csv = df.to_csv(index=False)

            st.download_button(
                "⬇️ Download Results CSV",
                csv,
                "evaluation_results.csv",
                "text/csv"
            )

    # ---------------- LOGOUT ----------------
    if st.sidebar.button("Logout"):
        st.session_state.role = None
        st.rerun()
