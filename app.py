import streamlit as st
from pypdf import PdfReader

from data.job_roles import JOB_ROLES
from data.recommendations import RECOMMENDATIONS
from src.semantic_matcher import (
    analyze_skill,
    calculate_jd_similarity
)


# ========================================================
# PAGE CONFIGURATION
# ========================================================

st.set_page_config(
    page_title="AI Career & Skill Gap Analyzer",
    page_icon="🎯",
    layout="wide"
)


# ========================================================
# CUSTOM UI STYLING
# ========================================================

st.markdown(
    """
    <style>

    /* ---------------------------------------------------
       MAIN PAGE
    --------------------------------------------------- */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* ---------------------------------------------------
       HERO SECTION
    --------------------------------------------------- */

    .hero {
        text-align: center;
        padding: 1.5rem 0 2rem 0;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
        letter-spacing: -1px;
    }

    .hero-subtitle {
        font-size: 1.15rem;
        color: #6b7280;
        margin-bottom: 1rem;
    }

    .hero-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 999px;
        background: #eef2ff;
        color: #4f46e5;
        font-size: 0.85rem;
        font-weight: 600;
    }


    /* ---------------------------------------------------
       SETUP CARD
    --------------------------------------------------- */

    .setup-card {
        padding: 1.4rem;
        border-radius: 18px;
        background: #f8fafc;
        border: 1px solid #e5e7eb;
        margin-bottom: 1.5rem;
    }


    /* ---------------------------------------------------
       SECTION HEADERS
    --------------------------------------------------- */

    .section-title {
        font-size: 1.5rem;
        font-weight: 750;
        margin-top: 0.8rem;
        margin-bottom: 1rem;
    }


    /* ---------------------------------------------------
       METRIC CARDS
    --------------------------------------------------- */

    .metric-card {
        padding: 1.3rem;
        border-radius: 16px;
        background: #f8fafc;
        border: 1px solid #e5e7eb;
        text-align: center;
        min-height: 120px;
    }

    .metric-number {
        font-size: 2rem;
        font-weight: 750;
    }

    .metric-label {
        font-size: 0.9rem;
        color: #6b7280;
        margin-top: 0.3rem;
    }


    /* ---------------------------------------------------
       INFO CARDS
    --------------------------------------------------- */

    .info-card {
        padding: 1rem 1.2rem;
        border-radius: 14px;
        background: #ffffff;
        border: 1px solid #e5e7eb;
        margin-bottom: 0.8rem;
    }


    /* ---------------------------------------------------
       TAB SPACING
    --------------------------------------------------- */

    .stTabs {
        margin-top: 1rem;
    }


    /* ---------------------------------------------------
       FOOTER
    --------------------------------------------------- */

    .footer {
        text-align: center;
        color: #9ca3af;
        font-size: 0.85rem;
        padding: 2rem 0 1rem 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ========================================================
# HERO / PROJECT HEADER
# ========================================================

st.markdown("""<div style="text-align:center; padding:25px 10px 30px 10px;">

<div style="display:inline-block; padding:8px 18px; border-radius:25px; background-color:#eef2ff; color:#4f46e5; font-size:14px; font-weight:600; margin-bottom:15px;">
AI • NLP • Career Intelligence
</div>

<h1 style="font-size:42px; font-weight:800; text-align:center; margin:0 0 8px 0;">
AI Career & Skill Gap Analyzer
</h1>

<p style="font-size:18px; color:#9ca3af; text-align:center; margin:0;">
AI-powered career intelligence platform for resume analysis, skill-gap detection and job matching
</p>

</div>""", unsafe_allow_html=True)


# ========================================================
# RESUME + CAREER SETUP
# ========================================================

st.markdown(
    '<div class="section-title">Analysis Setup</div>',
    unsafe_allow_html=True
)

setup_col1, setup_col2 = st.columns([1, 2])


with setup_col1:

    target_role = st.selectbox(
        "Target Career",
        list(JOB_ROLES.keys())
    )


with setup_col2:

    uploaded_file = st.file_uploader(
        "Upload Your Resume",
        type=["pdf"],
        help="Upload your resume in PDF format."
    )


# ========================================================
# MAIN ANALYSIS
# ========================================================

if uploaded_file is not None:

    # ====================================================
    # PDF TEXT EXTRACTION
    # ====================================================

    reader = PdfReader(uploaded_file)

    resume_text = ""

    for page in reader.pages:

        text = page.extract_text()

        if text:
            resume_text += text + "\n"


    # ====================================================
    # AVAILABLE SKILLS
    # ====================================================

    skills = [

        "Python",
        "SQL",
        "Java",
        "C++",

        "Machine Learning",
        "Deep Learning",
        "Data Science",

        "Pandas",
        "NumPy",
        "Scikit-learn",

        "TensorFlow",
        "PyTorch",

        "Power BI",
        "Tableau",
        "Excel",

        "Git",
        "GitHub",

        "Streamlit",

        "NLP",
        "Computer Vision"

    ]


    # ====================================================
    # DETECT SKILLS
    # ====================================================

    detected_skills = []

    resume_text_lower = resume_text.lower()

    for skill in skills:

        if skill.lower() in resume_text_lower:

            detected_skills.append(skill)


    # ====================================================
    # REQUIRED SKILLS
    # ====================================================

    required_skills = JOB_ROLES[target_role]


    # ====================================================
    # SKILL GAP ANALYSIS
    # ====================================================

    matched_skills = []

    missing_skills = []

    for skill in required_skills:

        if skill in detected_skills:

            matched_skills.append(skill)

        else:

            missing_skills.append(skill)


    total_required = len(required_skills)


    if total_required > 0:

        match_percentage = (
            len(matched_skills) / total_required
        ) * 100

    else:

        match_percentage = 0


    # ====================================================
    # CAREER COMPATIBILITY
    # ====================================================

    career_results = []

    for role, role_skills in JOB_ROLES.items():

        role_matched = 0

        for skill in role_skills:

            if skill in detected_skills:

                role_matched += 1


        if len(role_skills) > 0:

            percentage = (
                role_matched / len(role_skills)
            ) * 100

        else:

            percentage = 0


        career_results.append(
            {
                "role": role,
                "percentage": percentage,
                "matched": role_matched,
                "total": len(role_skills)
            }
        )


    career_results = sorted(
        career_results,
        key=lambda x: x["percentage"],
        reverse=True
    )


    # ====================================================
    # AI CAREER SEMANTIC ANALYSIS
    # ====================================================

    ai_career_results = []

    for role, role_skills in JOB_ROLES.items():

        role_scores = []

        for skill in role_skills:

            result = analyze_skill(
                resume_text,
                skill
            )

            role_scores.append(
                result["semantic_score"]
            )


        if role_scores:

            average_score = (
                sum(role_scores)
                / len(role_scores)
            )

        else:

            average_score = 0


        ai_career_results.append(
            {
                "role": role,
                "score": average_score
            }
        )


    ai_career_results = sorted(
        ai_career_results,
        key=lambda x: x["score"],
        reverse=True
    )


    # ====================================================
    # AI SKILL MATCH ANALYSIS
    # ====================================================

    ai_results = []

    for skill in required_skills:

        result = analyze_skill(
            resume_text,
            skill
        )

        ai_results.append(result)


    # ====================================================
    # RESUME IMPROVEMENT SUGGESTIONS
    # ====================================================

    improvement_suggestions = []

    resume_lower = resume_text.lower()


    # Missing skills

    if missing_skills:

        improvement_suggestions.append(
            f"Add or develop these skills for the "
            f"{target_role} role: "
            + ", ".join(missing_skills)
            + "."
        )


    # Projects

    if (
        "project" not in resume_lower
        and "projects" not in resume_lower
    ):

        improvement_suggestions.append(
            "Add a Projects section containing "
            "2–3 relevant academic or personal projects."
        )


    # Experience

    experience_keywords = [
        "internship",
        "intern",
        "experience",
        "work experience",
        "employment"
    ]

    has_experience = any(
        keyword in resume_lower
        for keyword in experience_keywords
    )

    if not has_experience:

        improvement_suggestions.append(
            "Consider adding internship, training, "
            "freelance, or relevant practical experience "
            "if available."
        )


    # GitHub

    if "github" not in resume_lower:

        improvement_suggestions.append(
            "Add your GitHub profile to showcase "
            "your projects and coding work."
        )


    # LinkedIn

    if "linkedin" not in resume_lower:

        improvement_suggestions.append(
            "Add your LinkedIn profile to make your "
            "professional profile easier for recruiters to find."
        )


    # Contact

    if "@" not in resume_text:

        improvement_suggestions.append(
            "Make sure your professional email address "
            "is clearly visible in the resume."
        )


    # Skills section

    if "skills" not in resume_lower:

        improvement_suggestions.append(
            "Add a clearly organized Technical Skills section."
        )


    # Certifications

    if (
        "certification" not in resume_lower
        and "certifications" not in resume_lower
    ):

        improvement_suggestions.append(
            "Consider adding relevant certifications, "
            "courses, or NPTEL/online learning achievements."
        )


    # ====================================================
    # RESUME QUALITY SCORE
    # ====================================================

    skills_score = 0
    projects_score = 0
    experience_score = 0
    education_score = 0
    profile_score = 0


    # Skills score

    if len(detected_skills) >= 8:

        skills_score = 20

    elif len(detected_skills) >= 5:

        skills_score = 15

    elif len(detected_skills) >= 3:

        skills_score = 10

    elif len(detected_skills) > 0:

        skills_score = 5


    # Projects score

    project_keywords = [
        "project",
        "projects",
        "developed",
        "built",
        "implemented"
    ]

    project_count = sum(
        resume_lower.count(keyword)
        for keyword in project_keywords
    )

    if (
        "project" in resume_lower
        or "projects" in resume_lower
    ):

        if project_count >= 5:

            projects_score = 20

        elif project_count >= 3:

            projects_score = 15

        else:

            projects_score = 10


    # Experience score

    if any(
        keyword in resume_lower
        for keyword in experience_keywords
    ):

        experience_score = 20


    # Education score

    education_keywords = [
        "education",
        "b.tech",
        "btech",
        "bachelor",
        "degree",
        "university",
        "college"
    ]

    education_matches = sum(
        keyword in resume_lower
        for keyword in education_keywords
    )

    if education_matches >= 3:

        education_score = 20

    elif education_matches >= 1:

        education_score = 10


    # Profile score

    profile_items = 0

    if "@" in resume_text:

        profile_items += 1

    if "linkedin" in resume_lower:

        profile_items += 1

    if "github" in resume_lower:

        profile_items += 1

    if any(
        keyword in resume_lower
        for keyword in ["phone", "mobile", "contact"]
    ):

        profile_items += 1


    if profile_items >= 4:

        profile_score = 20

    elif profile_items == 3:

        profile_score = 15

    elif profile_items == 2:

        profile_score = 10

    elif profile_items == 1:

        profile_score = 5


    resume_score = (
        skills_score
        + projects_score
        + experience_score
        + education_score
        + profile_score
    )


    # ====================================================
    # CAREER CHART DATA
    # ====================================================

    chart_data = {

        "Career": [
            result["role"]
            for result in career_results
        ],

        "Match Percentage": [
            result["percentage"]
            for result in career_results
        ]

    }


    # ====================================================
    # RESUME SCORE DATA
    # ====================================================

    resume_score_data = {

        "Category": [
            "Skills",
            "Projects",
            "Experience",
            "Education",
            "Profile"
        ],

        "Score": [
            skills_score,
            projects_score,
            experience_score,
            education_score,
            profile_score
        ]

    }


    # ====================================================
    # SUCCESS STATUS
    # ====================================================

    st.success(
        f"✅ Resume analyzed successfully: {uploaded_file.name}"
    )


    # ====================================================
    # DASHBOARD TABS
    # ====================================================

    resume_tab, career_tab, learning_tab,job_tab, report_tab = st.tabs(
        [
            "📊 Resume Analysis",
            "🚀 Career Intelligence",
            "🎓 Learning Roadmap",
            "💼 Job Match",
            "📥 Download Report"
        ]
    )


    # ========================================================
    # TAB 1 — RESUME ANALYSIS
    # ========================================================

    with resume_tab:

        st.markdown(
            '<div class="section-title">Resume Overview</div>',
            unsafe_allow_html=True
        )


        # Resume information

        info1, info2, info3 = st.columns(3)


        with info1:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-number">
                        {uploaded_file.size / 1024:.1f}
                    </div>
                    <div class="metric-label">
                        Resume Size (KB)
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        with info2:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-number">
                        {len(resume_text):,}
                    </div>
                    <div class="metric-label">
                        Characters Extracted
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        with info3:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-number">
                        {len(detected_skills)}
                    </div>
                    <div class="metric-label">
                        Skills Detected
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        # Extracted text

        st.markdown(
            '<div class="section-title">Extracted Resume Text</div>',
            unsafe_allow_html=True
        )

        with st.expander(
            "View Extracted Resume Content"
        ):

            st.text_area(
                "Resume Content",
                resume_text,
                height=300
            )


        # Detected skills

        st.markdown(
            '<div class="section-title">Detected Skills</div>',
            unsafe_allow_html=True
        )


        if detected_skills:

            skill_columns = st.columns(3)

            for index, skill in enumerate(
                detected_skills
            ):

                with skill_columns[index % 3]:

                    st.write(
                        f"• {skill}"
                    )

        else:

            st.warning(
                "No skills detected in the resume."
            )


        # Required skills

        st.markdown(
            f'<div class="section-title">'
            f'Skills Required for {target_role}'
            f'</div>',
            unsafe_allow_html=True
        )


        required_columns = st.columns(3)

        for index, skill in enumerate(
            required_skills
        ):

            with required_columns[index % 3]:

                st.info(
                    f"🔹 {skill}"
                )


        # Skill gap metrics

        st.markdown(
            '<div class="section-title">Skill Gap Analysis</div>',
            unsafe_allow_html=True
        )


        metric1, metric2, metric3 = st.columns(3)


        with metric1:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-number">
                        {match_percentage:.1f}%
                    </div>
                    <div class="metric-label">
                        Overall Skill Match
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        with metric2:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-number">
                        {len(matched_skills)}
                    </div>
                    <div class="metric-label">
                        Skills Matched
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        with metric3:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-number">
                        {len(missing_skills)}
                    </div>
                    <div class="metric-label">
                        Skills Missing
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        st.progress(
            int(match_percentage)
        )


        st.caption(
            f"Your resume currently matches "
            f"{match_percentage:.1f}% of the required skills "
            f"for {target_role}."
        )


        # Matched and missing

        matched_col, missing_col = st.columns(2)


        with matched_col:

            st.markdown(
                "### Matched Skills"
            )

            if matched_skills:

                for skill in matched_skills:

                    st.success(
                        f"✓ {skill}"
                    )

            else:

                st.info(
                    "No matching skills found."
                )


        with missing_col:

            st.markdown(
                "### Missing Skills"
            )

            if missing_skills:

                for skill in missing_skills:

                    st.error(
                        f"✗ {skill}"
                    )

            else:

                st.success(
                    "You have all the required skills!"
                )


        # Resume summary

        st.markdown(
            '<div class="section-title">Analysis Summary</div>',
            unsafe_allow_html=True
        )


        summary1, summary2 = st.columns(2)


        with summary1:

            st.write(
                f"**Target Career:** {target_role}"
            )

            st.write(
                f"**Skills Detected:** "
                f"{len(detected_skills)}"
            )

            st.write(
                f"**Required Skills:** "
                f"{len(required_skills)}"
            )


        with summary2:

            st.write(
                f"**Matched Skills:** "
                f"{len(matched_skills)}"
            )

            st.write(
                f"**Missing Skills:** "
                f"{len(missing_skills)}"
            )

            st.write(
                f"**Skill Match:** "
                f"{match_percentage:.1f}%"
            )


        # Resume improvement

        st.markdown(
            '<div class="section-title">'
            'Resume Improvement Suggestions'
            '</div>',
            unsafe_allow_html=True
        )


        if improvement_suggestions:

            for index, suggestion in enumerate(
                improvement_suggestions,
                start=1
            ):

                st.info(
                    f"**{index}.** {suggestion}"
                )

        else:

            st.success(
                "Your resume contains the main sections "
                "checked by the analyzer."
            )


        # Resume quality

        st.markdown(
            '<div class="section-title">'
            'Resume Quality Score'
            '</div>',
            unsafe_allow_html=True
        )


        score_col1, score_col2 = st.columns([1, 2])


        with score_col1:

            st.metric(
                "Overall Resume Score",
                f"{resume_score}/100"
            )


        with score_col2:

            st.progress(
                resume_score
            )

            if resume_score >= 80:

                st.success(
                    "Excellent resume completeness!"
                )

            elif resume_score >= 60:

                st.info(
                    "Good resume, but there are areas "
                    "that can be improved."
                )

            elif resume_score >= 40:

                st.warning(
                    "Your resume needs some improvements."
                )

            else:

                st.error(
                    "Your resume needs significant improvement."
                )


        # Score breakdown

        st.markdown(
            "### Score Breakdown"
        )


        score1, score2, score3 = st.columns(3)


        with score1:

            st.metric(
                "Skills",
                f"{skills_score}/20"
            )

            st.metric(
                "Projects",
                f"{projects_score}/20"
            )


        with score2:

            st.metric(
                "Experience",
                f"{experience_score}/20"
            )

            st.metric(
                "Education",
                f"{education_score}/20"
            )


        with score3:

            st.metric(
                "Profile",
                f"{profile_score}/20"
            )


        # Score visualization

        st.markdown(
            '<div class="section-title">'
            'Resume Score Visualization'
            '</div>',
            unsafe_allow_html=True
        )


        st.bar_chart(
            resume_score_data,
            x="Category",
            y="Score"
        )


        # Category details

        st.markdown(
            "### Category Details"
        )


        detail1, detail2 = st.columns(2)


        with detail1:

            st.write(
                f"**Skills:** {skills_score}/20"
            )

            st.progress(
                skills_score / 20
            )


            st.write(
                f"**Projects:** {projects_score}/20"
            )

            st.progress(
                projects_score / 20
            )


            st.write(
                f"**Experience:** {experience_score}/20"
            )

            st.progress(
                experience_score / 20
            )


        with detail2:

            st.write(
                f"**Education:** {education_score}/20"
            )

            st.progress(
                education_score / 20
            )


            st.write(
                f"**Profile:** {profile_score}/20"
            )

            st.progress(
                profile_score / 20
            )


        st.caption(
            "Each category contributes up to 20 points, "
            "giving a maximum resume score of 100."
        )


    # ========================================================
    # TAB 2 — CAREER INTELLIGENCE
    # ========================================================

    with career_tab:

        st.markdown(
            '<div class="section-title">'
            'Career Intelligence Dashboard'
            '</div>',
            unsafe_allow_html=True
        )


        st.write(
            "Explore how your current resume aligns with "
            "different career paths using skill matching "
            "and NLP semantic analysis."
        )


        # Career compatibility

        st.markdown(
            "### Career Compatibility"
        )


        for result in career_results:

            role = result["role"]

            percentage = result["percentage"]

            matched = result["matched"]

            total = result["total"]


            st.write(
                f"**{role}** — "
                f"{percentage:.1f}% "
                f"({matched}/{total} skills)"
            )


            st.progress(
                int(percentage)
            )


        # Career chart

        st.markdown(
            "### Career Compatibility Chart"
        )


        st.bar_chart(
            chart_data,
            x="Career",
            y="Match Percentage"
        )


        # AI career recommendation

        st.markdown(
            "### AI Career Recommendation"
        )


        st.write(
            "The NLP model calculates semantic similarity "
            "between your resume and the skills required "
            "for each career role."
        )


        for result in ai_career_results:

            role = result["role"]

            score = result["score"]


            st.write(
                f"**{role}** — "
                f"{score * 100:.1f}% semantic similarity"
            )


            st.progress(
                min(
                    int(score * 100),
                    100
                )
            )


        # Selected role skill visualization

        st.markdown(
            f"### {target_role} Skill Analysis"
        )


        skill_chart_data = {

            "Skill": required_skills,

            "Match": [

                100
                if skill in matched_skills
                else 0

                for skill in required_skills

            ]

        }


        st.bar_chart(
            skill_chart_data,
            x="Skill",
            y="Match"
        )


        # AI skill match

        st.markdown(
            "### AI Skill Match Analysis"
        )


        st.write(
            "The system combines keyword detection "
            "and NLP semantic similarity to analyze "
            "your skills."
        )


        for result in ai_results:

            skill = result["skill"]

            score = result["semantic_score"]

            status = result["status"]


            if status == "Strong Match":

                st.success(
                    f"🟢 {skill} — Strong Match "
                    f"({score * 100:.1f}% semantic similarity)"
                )


            elif status == "Possible Match":

                st.warning(
                    f"🟡 {skill} — Possible Match "
                    f"({score * 100:.1f}% semantic similarity)"
                )


            else:

                st.error(
                    f"🔴 {skill} — Skill Gap "
                    f"({score * 100:.1f}% semantic similarity)"
                )
    # ========================================================
    # TAB 3 — LEARNING ROADMAP
    # ========================================================
    
    with learning_tab:
    
        st.markdown(
            '<div class="section-title">'
            '🎓 Personalized Learning Roadmap'
            '</div>',
            unsafe_allow_html=True
        )
    
    
        if missing_skills:
    
            st.write(
                "Your roadmap is generated automatically "
                "from the skills missing for your selected career."
            )
    
    
            for index, skill in enumerate(
                missing_skills,
                start=1
            ):
    
                recommendation = (
                    RECOMMENDATIONS.get(skill)
                )
    
    
                if recommendation:
    
                    with st.expander(
                        f"{index}. {skill} — "
                        f"{recommendation.get('duration', 'Not specified')}"
                    ):
    
                        st.markdown(
                            "### What to Learn"
                        )
    
                        st.write(
                            recommendation.get(
                                "learn",
                                f"Learn the fundamentals "
                                f"of {skill}."
                            )
                        )
    
    
                        st.markdown(
                            "### Key Topics"
                        )
    
    
                        for topic in recommendation.get(
                            "topics",
                            []
                        ):
    
                            st.write(
                                f"• {topic}"
                            )
    
    
                        st.markdown(
                            "### Practice Project"
                        )
    
    
                        st.write(
                            recommendation.get(
                                "practice",
                                "Practice this skill through "
                                "a small project."
                            )
                        )
    
    
                        st.markdown(
                            "### Learning Objective"
                        )
    
    
                        st.write(
                            recommendation.get(
                                "objective",
                                "Build practical knowledge "
                                "through hands-on learning."
                            )
                        )
    
    
                else:
    
                    with st.expander(
                        f"{index}. {skill}"
                    ):
    
                        st.write(
                            f"Learn the fundamentals of {skill} "
                            "and practice it through a project."
                        )
    
    
        else:
    
            st.success(
                "No major skill gaps found for "
                f"{target_role}!"
            )

    # ========================================================
    # TAB 4 — JOB MATCH
    # ========================================================

    with job_tab:

        st.markdown(
            '<div class="section-title">'
            'Job Description Analyzer'
            '</div>',
            unsafe_allow_html=True
        )


        st.write(
            "Paste a real job description to compare "
            "its requirements with your resume."
        )


        job_description = st.text_area(
            "Paste Job Description",
            height=250,
            placeholder=(
                "Example:\n"
                "We are looking for a Data Scientist with "
                "strong Python, SQL, Machine Learning, "
                "Pandas, NumPy and Statistics skills..."
            )
        )


        if job_description.strip():

            jd_text_lower = job_description.lower()


            # Detect JD skills

            jd_detected_skills = []


            for skill in skills:

                if skill.lower() in jd_text_lower:

                    jd_detected_skills.append(skill)


            # Compare skills

            jd_matched_skills = []

            jd_missing_skills = []


            for skill in jd_detected_skills:

                if skill in detected_skills:

                    jd_matched_skills.append(skill)

                else:

                    jd_missing_skills.append(skill)


            # JD match percentage

            total_jd_skills = len(
                jd_detected_skills
            )


            if total_jd_skills > 0:

                jd_match_percentage = (
                    len(jd_matched_skills)
                    / total_jd_skills
                ) * 100

            else:

                jd_match_percentage = 0


            # ------------------------------------------------
            # JD SUMMARY
            # ------------------------------------------------

            st.markdown(
                "### Job Description Match"
            )


            jd_col1, jd_col2, jd_col3 = st.columns(3)


            with jd_col1:

                st.metric(
                    "JD Match",
                    f"{jd_match_percentage:.1f}%"
                )


            with jd_col2:

                st.metric(
                    "Skills Matched",
                    len(jd_matched_skills)
                )


            with jd_col3:

                st.metric(
                    "Skills Missing",
                    len(jd_missing_skills)
                )


            st.progress(
                int(jd_match_percentage)
            )


            # Skills detected

            st.markdown(
                "### Skills Detected in Job Description"
            )


            if jd_detected_skills:

                skill_cols = st.columns(3)

                for index, skill in enumerate(
                    jd_detected_skills
                ):

                    with skill_cols[index % 3]:

                        st.info(
                            f"🔹 {skill}"
                        )

            else:

                st.warning(
                    "No skills from the analyzer's current "
                    "skill database were detected."
                )


            # Matched and missing

            jd_match_col, jd_missing_col = st.columns(2)


            with jd_match_col:

                st.markdown(
                    "### Skills You Already Have"
                )


                if jd_matched_skills:

                    for skill in jd_matched_skills:

                        st.success(
                            f"✓ {skill}"
                        )

                else:

                    st.info(
                        "No matching skills were detected."
                    )


            with jd_missing_col:

                st.markdown(
                    "### Skills You Need to Develop"
                )


                if jd_missing_skills:

                    for skill in jd_missing_skills:

                        st.error(
                            f"✗ {skill}"
                        )

                else:

                    st.success(
                        "Your resume contains all "
                        "detected JD skills!"
                    )


            # ------------------------------------------------
            # AI JOB FIT
            # ------------------------------------------------

            st.markdown(
                '<div class="section-title">'
                'AI Job Fit Analysis'
                '</div>',
                unsafe_allow_html=True
            )


            st.write(
                "This analysis uses semantic similarity "
                "to compare the overall meaning of your "
                "resume with the job description."
            )


            jd_semantic_score = calculate_jd_similarity(
                resume_text,
                job_description
            )


            semantic_percentage = (
                jd_semantic_score * 100
            )


            fit_col1, fit_col2 = st.columns(2)


            with fit_col1:

                st.metric(
                    "Semantic Match",
                    f"{semantic_percentage:.1f}%"
                )


            with fit_col2:

                st.metric(
                    "Resume Skills",
                    len(detected_skills)
                )


            st.progress(
                min(
                    int(semantic_percentage),
                    100
                )
            )


            # AI fit summary

            st.markdown(
                "### AI Fit Summary"
            )


            if semantic_percentage >= 60:

                st.success(
                    "Your resume has strong overall semantic "
                    "alignment with this job description. "
                    "Your experience and technical background "
                    "appear relevant to the role."
                )


            elif semantic_percentage >= 40:

                st.warning(
                    "Your resume has moderate semantic alignment "
                    "with this job description. You have relevant "
                    "areas, but some parts of your background may "
                    "need to be strengthened."
                )


            else:

                st.info(
                    "The semantic alignment is currently limited. "
                    "Consider gaining more relevant skills, "
                    "projects, or experience related to this job "
                    "description."
                )


            # Strengths

            st.markdown(
                "### Relevant Strengths"
            )


            if jd_matched_skills:

                strengths_text = ", ".join(
                    jd_matched_skills
                )

                st.write(
                    f"Your resume contains several skills "
                    f"relevant to this job: "
                    f"**{strengths_text}**."
                )

            else:

                st.write(
                    "No direct skill matches were detected "
                    "from the current skill database."
                )


            # Areas to improve

            st.markdown(
                "### Areas to Improve"
            )


            if jd_missing_skills:

                for skill in jd_missing_skills:

                    st.write(
                        f"🔹 Strengthen your knowledge or "
                        f"practical experience in **{skill}**."
                    )

            else:

                st.success(
                    "No additional skill gaps were detected "
                    "from the current skill database."
                )


            # Preparation

            st.markdown(
                "### Preparation Focus"
            )


            if jd_missing_skills:

                st.write(
                    "For better alignment with this position, "
                    "focus on the missing skills and demonstrate "
                    "them through projects, coursework, "
                    "certifications, or practical experience "
                    "where applicable."
                )

            else:

                st.write(
                    "Continue strengthening your existing skills "
                    "and showcase relevant projects and practical "
                    "experience in your resume."
                )


            # Learning recommendations

            if jd_missing_skills:

                st.markdown(
                    "### Recommended Learning"
                )


                for index, skill in enumerate(
                    jd_missing_skills,
                    start=1
                ):

                    recommendation = (
                        RECOMMENDATIONS.get(skill)
                    )


                    if recommendation:

                        with st.expander(
                            f"{index}. {skill} — "
                            f"{recommendation.get('duration', 'Not specified')}"
                        ):

                            st.markdown(
                                "#### What to Learn"
                            )

                            st.write(
                                recommendation.get(
                                    "learn",
                                    f"Learn the fundamentals "
                                    f"of {skill}."
                                )
                            )


                            st.markdown(
                                "#### Key Topics"
                            )


                            for topic in recommendation.get(
                                "topics",
                                []
                            ):

                                st.write(
                                    f"• {topic}"
                                )


                            st.markdown(
                                "#### Practice Project"
                            )


                            st.write(
                                recommendation.get(
                                    "practice",
                                    "Practice this skill "
                                    "through a small project."
                                )
                            )


                    else:

                        with st.expander(
                            f"{index}. {skill}"
                        ):

                            st.write(
                                f"Learn the fundamentals "
                                f"of {skill} and practice it "
                                f"through a project."
                            )


        else:

            st.info(
                "Paste a job description above to "
                "activate AI job matching."
            )


    

    # ========================================================
    # TAB 5 — DOWNLOAD REPORT
    # ========================================================

    with report_tab:

        st.markdown(
            '<div class="section-title">'
            'Career Analysis Report'
            '</div>',
            unsafe_allow_html=True
        )

        st.write(
            "Download a complete text report containing "
            "your career analysis, skill gaps, resume score, "
            "career compatibility and AI semantic analysis."
        )

        report = f"""
    AI CAREER & SKILL GAP ANALYZER
    ================================

    TARGET CAREER
    -------------
    {target_role}

    RESUME
    ------
    {uploaded_file.name}

    OVERALL SKILL MATCH
    -------------------
    {match_percentage:.1f}%

    RESUME QUALITY SCORE
    --------------------
    {resume_score}/100

    SKILLS DETECTED
    ---------------
    """

        for skill in detected_skills:
            report += f"✓ {skill}\n"

        report += """

    MATCHED SKILLS
    --------------
    """

        for skill in matched_skills:
            report += f"✓ {skill}\n"

        report += """

    MISSING SKILLS
    --------------
    """

        for skill in missing_skills:
            report += f"✗ {skill}\n"

        report += """

    PERSONALIZED LEARNING ROADMAP
    -----------------------------
    """

        for skill in missing_skills:

            recommendation = RECOMMENDATIONS.get(skill)

            if recommendation:

                report += f"""

    {skill}
    Duration: {recommendation.get("duration", "Not specified")}

    What to Learn:
    {recommendation.get("learn", "Not available")}

    Key Topics:
    """

                for topic in recommendation.get("topics", []):
                    report += f"- {topic}\n"

                report += f"""

    Practice Project:
    {recommendation.get("practice", "Not available")}

    Learning Objective:
    {recommendation.get("objective", "Not available")}

    """

        report += """

    CAREER COMPATIBILITY
    --------------------
    """

        for result in career_results:

            report += (
                f"{result['role']}: "
                f"{result['percentage']:.1f}% "
                f"({result['matched']}/{result['total']} skills)\n"
            )

        report += """

    AI SEMANTIC ANALYSIS
    --------------------
    """

        for result in ai_career_results:

            report += (
                f"{result['role']}: "
                f"{result['score'] * 100:.1f}% "
                f"semantic similarity\n"
            )

        report += f"""

    RESUME SCORE BREAKDOWN
    ----------------------
    Skills: {skills_score}/20
    Projects: {projects_score}/20
    Experience: {experience_score}/20
    Education: {education_score}/20
    Profile: {profile_score}/20

    ================================
    Generated by AI Career & Skill Gap Analyzer
    """

        st.download_button(
            label="📥 Download Career Analysis Report",
            data=report,
            file_name="career_skill_gap_report.txt",
            mime="text/plain"
        )


    # ========================================================
    # FOOTER
    # ========================================================

    st.markdown(
        """
        <div class="footer">
            AI Career & Skill Gap Analyzer •
            Resume Intelligence • NLP • Career Analytics
        </div>
        """,
        unsafe_allow_html=True
    )


else:

    # ========================================================
    # EMPTY STATE
    # ========================================================

    st.markdown(
        """
        <div class="info-card">

        ### Ready to Analyze Your Career?

        Select your target career and upload your resume
        to unlock:

        - Resume analysis
        - AI skill detection
        - Career compatibility
        - NLP-based career intelligence
        - Job description matching
        - Personalized learning roadmap
        - Resume quality scoring
        - Downloadable analysis report

        </div>
        """,
        unsafe_allow_html=True
    )