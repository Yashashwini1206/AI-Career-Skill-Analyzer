from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load the NLP model
model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_similarity(resume_text, skill):
    """
    Calculate semantic similarity between
    resume text and a required skill.
    """

    resume_embedding = model.encode([resume_text])
    skill_embedding = model.encode([skill])

    similarity = cosine_similarity(
        resume_embedding,
        skill_embedding
    )[0][0]

    return float(similarity)


def analyze_skill(resume_text, skill):
    """
    Analyze whether a skill is strongly present,
    possibly present, or missing.
    """

    # Keyword matching
    keyword_match = skill.lower() in resume_text.lower()

    # Semantic matching
    semantic_score = calculate_similarity(
        resume_text,
        skill
    )

    # Classification
    if keyword_match or semantic_score >= 0.40:
        status = "Strong Match"

    elif semantic_score >= 0.25:
        status = "Possible Match"

    else:
        status = "Skill Gap"

    return {
        "skill": skill,
        "keyword_match": keyword_match,
        "semantic_score": semantic_score,
        "status": status
    }


def calculate_jd_similarity(resume_text, job_description):
    """
    Calculate semantic similarity between
    the complete resume and job description.
    """

    resume_embedding = model.encode([resume_text])
    jd_embedding = model.encode([job_description])

    similarity = cosine_similarity(
        resume_embedding,
        jd_embedding
    )[0][0]

    return float(similarity)