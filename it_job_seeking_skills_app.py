"""IT Job Seeking Skills Analysis - BCA Semester V project prototype.

Run with:
    pip install -r requirements.txt
    streamlit run it_job_seeking_skills_app.py

This application uses transparent rule-based skill matching. It does not train
or use a machine-learning model.
"""

import matplotlib.pyplot as plt
import streamlit as st


ROLE_SKILLS = {
    "Python Developer": ["Python", "Git", "SQL", "APIs", "Debugging"],
    "Web Developer": ["HTML", "CSS", "JavaScript", "Git", "Responsive Design"],
    "Data Analyst": ["Python", "SQL", "Excel", "Statistics", "Data Visualization"],
    "Machine Learning Engineer": [
        "Python",
        "Statistics",
        "Machine Learning",
        "Pandas",
        "Model Evaluation",
    ],
    "Software Tester": ["Testing", "Test Cases", "Bug Reporting", "SQL", "Automation"],
}

ALL_SKILLS = sorted({skill for skills in ROLE_SKILLS.values() for skill in skills})


def calculate_match(selected_skills, required_skills):
    """Return matched skills, missing skills, and an equal-weight match percentage."""
    selected = set(selected_skills)
    required = set(required_skills)
    matched = selected.intersection(required)
    missing = required.difference(selected)
    percentage = (len(matched) / len(required) * 100) if required else 0.0
    return matched, missing, percentage


st.set_page_config(
    page_title="IT Job Seeking Skills Analysis",
    page_icon="💼",
    layout="wide",
)

st.title("IT Job Seeking Skills Analysis")
st.write("Compare your selected skills with five illustrative IT role requirements.")
st.caption(
    "This rule-based score measures exact overlap with the listed requirements. "
    "It is an educational guide, not a hiring prediction."
)

with st.sidebar:
    st.header("Skill Input")
    selected_skills = st.multiselect(
        "Select skills you can demonstrate",
        options=ALL_SKILLS,
        help="Choose skills supported by coursework, practice, or project evidence.",
    )
    focus_role = st.selectbox("Role for detailed gap analysis", list(ROLE_SKILLS))

results = []
for role, required_skills in ROLE_SKILLS.items():
    matched, missing, percentage = calculate_match(selected_skills, required_skills)
    results.append(
        {
            "Role": role,
            "Match (%)": round(percentage, 1),
            "Matched Skills": ", ".join(sorted(matched)) or "None",
            "Skills to Explore": ", ".join(sorted(missing)) or "No listed gaps",
        }
    )

metric_a, metric_b, metric_c = st.columns(3)
metric_a.metric("Skills selected", len(selected_skills))
metric_b.metric("Roles compared", len(ROLE_SKILLS))
best_result = max(results, key=lambda result: result["Match (%)"])
metric_c.metric("Highest current match", f"{best_result['Match (%)']:.1f}%")

st.subheader("Role Comparison")
st.dataframe(results, use_container_width=True, hide_index=True)

left, right = st.columns([1.35, 1])
with left:
    st.subheader("Role Match Chart")
    figure, axis = plt.subplots(figsize=(8, 4.5))
    names = [result["Role"] for result in results]
    scores = [result["Match (%)"] for result in results]
    bars = axis.bar(names, scores, color="#176B78")
    axis.set_ylabel("Skill overlap (%)")
    axis.set_ylim(0, 100)
    axis.set_title("Selected Skills Compared With Role Requirements")
    axis.tick_params(axis="x", labelrotation=20)
    for bar, score in zip(bars, scores):
        axis.text(bar.get_x() + bar.get_width() / 2, score + 2, f"{score:.0f}%", ha="center", fontsize=9)
    figure.tight_layout()
    st.pyplot(figure)
    plt.close(figure)

with right:
    st.subheader(f"Skill Gap: {focus_role}")
    matched, missing, percentage = calculate_match(selected_skills, ROLE_SKILLS[focus_role])
    st.metric("Match percentage", f"{percentage:.1f}%")
    st.markdown("**Matched skills**")
    st.write(", ".join(sorted(matched)) if matched else "No required skills matched yet.")
    st.markdown("**Skills to explore**")
    st.write(", ".join(sorted(missing)) if missing else "All listed skills are selected.")

if not selected_skills:
    st.info("Select at least one skill from the sidebar to see meaningful results.")

st.divider()
st.caption("Formula: matched required skills / total required skills × 100")
