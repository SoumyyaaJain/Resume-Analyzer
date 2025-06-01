import streamlit as st
from utils.ats_checker import ats_friendly_check
from utils.parser import extract_text_from_file, extract_basic_info
from utils.section_extractor import extract_sections
from utils.quality_checker import (
    check_grammar, check_readability,
    check_passive_voice, detect_weak_action_verbs,
    detect_quantified_achievements,
    check_formatting_consistency, check_resume_length
)
from utils.job_classifier import (
    predict_job_role,
    predict_with_confidence,
    get_top_n_roles,
    explain_prediction
)
from utils.skill_analyzer import (
    classify_skills,
    detect_employment_gaps,
    is_chronological,
    score_section
)
from utils.job_matcher import match_resume_to_jd

import os
import tempfile
import pandas as pd
import plotly.express as px  # <- Don't forget this import!

st.set_page_config(page_title="Smart Resume Analyzer", layout="wide")
st.title("📄 Resume Analyzer")
st.markdown("Upload your resume to get detailed insights and feedback.")

# File uploader
uploaded_file = st.file_uploader("Upload Resume (.pdf or .docx)", type=["pdf", "docx"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.read())
        resume_path = tmp.name

    with st.spinner("🔍 Extracting resume text..."):
        text = extract_text_from_file(resume_path)
        basic_info = extract_basic_info(text)
        sections = extract_sections(text)

    # Job Role Prediction
    st.subheader("Predicted Job Role")
    predicted_role = predict_job_role(text)
    st.success(f"This resume is most likely for the role of: **{predicted_role}**")

    role, confidence = predict_with_confidence(text)
    st.write(f"📊 Prediction Confidence: `{confidence:.2f}%`")

    top_roles = get_top_n_roles(text)
    st.markdown("**Top 3 Predicted Roles:**")

    # Display role list as bullets
    for r, c in top_roles:
        st.write(f"- {r} ({c:.2f}%)")

    # Plotly bar chart
    top_roles_df = pd.DataFrame(top_roles, columns=["Role", "Confidence"])
    fig = px.bar(
        top_roles_df,
        x="Confidence",
        y="Role",
        orientation="h",
        title="Top 3 Predicted Roles with Confidence",
        labels={"Confidence": "Confidence (%)", "Role": "Job Role"},
        color="Confidence",
        color_continuous_scale="Blues"
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Why this role?**")
    st.info(explain_prediction(text))

    # 📬 Basic Info
    st.subheader("Basic Information Extracted")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Email:** {basic_info['email'] or 'Not found'}")
        st.markdown(f"**Phone:** {basic_info['phone'] or 'Not found'}")
    with col2:
        st.markdown(f"**LinkedIn:** {basic_info['linkedin'] or 'Not found'}")
        st.markdown(f"**GitHub:** {basic_info['github'] or 'Not found'}")
        st.markdown(f"**Portfolio:** {basic_info['portfolio'] or 'Not found'}")

    # 📑 Sections
    st.markdown("---")
    st.subheader("📑 Resume Sections")
    for section, content in sections.items():
        with st.expander(f"🔹 {section.title()}"):
            st.write(content.strip() or "Not found")

    # 📏 Resume Length
    st.markdown("---")
    st.subheader("📏 Resume Length Evaluation")
    st.info(check_resume_length(text))

    # Quality Checks
    st.markdown("---")
    st.subheader("📊 Resume Quality Evaluation")
    for section, content in sections.items():
        st.markdown(f"### {section.title()}")
        if not content.strip():
            st.warning("⚠️ No content found in this section.")
            continue

        grammar_errors, suggestions = check_grammar(content)
        st.write(f"✅ Grammar Issues: {grammar_errors}")
        if suggestions:
            st.write("📝 Suggestions:")
            for sug in suggestions:
                st.write(f"- {sug}")

        readability = check_readability(content)
        st.write(f" Readability: {readability['flesch_score']:.2f} (Grade: {readability['grade_level']})")

        passive_count = check_passive_voice(content)
        st.write(f" Passive Sentences: {passive_count}")

        weak_verbs = detect_weak_action_verbs(content)
        st.write(f" Weak Verbs: {', '.join(weak_verbs) if weak_verbs else 'None'}")

        has_metrics = detect_quantified_achievements(content)
        st.write(f" Uses Quantified Achievements: {'✅ Yes' if has_metrics else '❌ No'}")

        formatting_issues = check_formatting_consistency(content)
        if formatting_issues:
            st.warning(" Formatting Issues Detected:")
            for issue in formatting_issues:
                st.write(f"- {issue}")
        else:
            st.success("✅ Formatting looks consistent.")
        st.markdown("---")

    #  Skill & Experience
    st.subheader(" Skill & Experience Analysis")
    for section, content in sections.items():
        st.markdown(f"###  {section.title()}")
        if not content.strip():
            st.warning("⚠️ No content found in this section.")
            continue

        hard_skills, soft_skills = classify_skills(content)
        employment_gaps = detect_employment_gaps(content)
        chronological = is_chronological(content)
        section_score = score_section(content)

        st.write(f" Hard Skills: {', '.join(hard_skills) if hard_skills else 'None found'}")
        st.write(f" Soft Skills: {', '.join(soft_skills) if soft_skills else 'None found'}")

        if employment_gaps:
            st.warning(f"⏳ Employment Gaps Detected: {employment_gaps}")
        else:
            st.success("✅ No Employment Gaps Detected")

        st.write(f" Experience in Chronological Order: {'✅ Yes' if chronological else '❌ No'}")
        st.write(f" Section Score: `{section_score}/100`")
        st.markdown("---")

    # ATS-Friendliness
    st.subheader(" ATS-Friendliness Check")
    ats_results = ats_friendly_check(resume_path, text)

    col1, col2 = st.columns(2)
    with col1:
        st.write(f" **File Type:** `{ats_results['extension']}`")
        st.write("✅ **File Format Valid:**" if ats_results['file_ok'] else "❌ **Not a valid ATS-friendly file**")
        st.write(" **Multi-column Layout Detected:**" if ats_results['multi_column'] else "✅ **Single-column format (Good for ATS)**")

    with col2:
        st.write(" **Tables Present:**" if ats_results['tables_present'] else "✅ **No tables detected (Good for ATS)**")
        st.write(" **Standard Headers Found:**")
        st.write(", ".join(ats_results['headers_found']) or "None")

        st.warning("⚠️ **Missing Standard Headers:**")
        st.write(", ".join(ats_results['headers_missing']) or "None")

    #  Job Matching
    st.markdown("---")
    st.subheader(" Job Matching Engine")

    jd_option = st.radio("Provide Job Description by:", ["Upload File", "Enter Text Manually"])
    jd_text = ""

    if jd_option == "Upload File":
        jd_file = st.file_uploader("Upload Job Description (.pdf or .docx)", type=["pdf", "docx"], key="jd_upload")
        if jd_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(jd_file.name)[1]) as jd_tmp:
                jd_tmp.write(jd_file.read())
                jd_text = extract_text_from_file(jd_tmp.name)
    else:
        jd_text = st.text_area("Paste the Job Description here", height=250)

    if jd_text:
        match_score, missing_keywords, suggestions = match_resume_to_jd(text, jd_text)

        st.write(f" **Resume Match Score:** `{match_score}%`")
        st.progress(match_score)

        st.markdown(" **Missing Keywords:**")
        if missing_keywords:
            st.write(", ".join(missing_keywords))
        else:
            st.success(" No important keywords missing!")

        st.markdown("✍️ **Suggestions to Improve Match:**")
        if suggestions:
            for s in suggestions:
                st.write(f"- {s}")
        else:
            st.success("Your resume aligns well with the job description!")

else:
    st.info("Please upload a .pdf or .docx resume to begin.")
