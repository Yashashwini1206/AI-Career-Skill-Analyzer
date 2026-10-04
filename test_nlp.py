from src.semantic_matcher import calculate_similarity


resume = """
I developed predictive models using supervised learning
and analyzed datasets using Python.
"""

skills = [
    "Machine Learning",
    "Cooking",
    "SQL"
]

for skill in skills:

    score = calculate_similarity(resume, skill)

    print(f"{skill}: {score:.2f}")