
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="IT Job Seeking Skills Analysis",
    page_icon="💻",
    layout="wide"
)

# Job roles and required skills
jobs = {
    "Python Developer": {
        "Python", "SQL", "Git", "Problem Solving"
    },
    "Web Developer": {
        "HTML", "CSS", "JavaScript", "Git"
    },
    "Data Analyst": {
        "Python", "SQL", "Excel", "Statistics"
    },
    "Machine Learning Engineer": {
        "Python", "SQL", "Machine Learning",
        "Statistics"
    },
    "Software Tester": {
        "Python", "SQL", "Problem Solving",
        "Communication"
    }
}

all_skills = sorted(set.union(*jobs.values()))

# Page heading
st.title("💻 IT Job Seeking Skills Analysis")
st.write(
    "Analyze your skills, discover suitable IT jobs "
    "and identify skills you need to improve."
)

st.divider()

# Student information
st.header("1. Student Profile")

name = st.text_input("Enter your name")

qualification = st.selectbox(
    "Select qualification",
    ["BCA", "BSc IT", "BTech", "MCA", "Other"]
)

skills = st.multiselect(
    "Select the skills you currently have",
    all_skills,
    help="Select only the skills you have learned."
)

target_role = st.selectbox(
    "Choose your preferred job role",
    ["All Roles"] + list(jobs.keys())
)

if st.button("Analyze My Skills", type="primary"):

    if not name.strip():
        st.warning("Please enter your name.")

    elif not skills:
        st.warning("Please select at least one skill.")

    else:
        student_skills = set(skills)

        st.divider()
        st.header("2. Your Analysis Results")

        st.success(
            f"Welcome, {name}! Your profile has been analyzed."
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("Qualification", qualification)
        col2.metric("Skills Selected", len(student_skills))
        col3.metric("Job Roles Analyzed", len(jobs))

        # Match student skills with job requirements
        results = []

        for role, required_skills in jobs.items():

            matched = student_skills & required_skills
            missing = required_skills - student_skills

            score = round(
                len(matched) / len(required_skills) * 100
            )

            results.append({
                "Job Role": role,
                "Match (%)": score,
                "Matched Skills": ", ".join(sorted(matched))
                    if matched else "None",
                "Missing Skills": ", ".join(sorted(missing))
                    if missing else "None"
            })

        df = pd.DataFrame(results)

        # Filter by preferred role if selected
        if target_role != "All Roles":
            display_df = df[df["Job Role"] == target_role]
        else:
            display_df = df

        display_df = display_df.sort_values(
            "Match (%)", ascending=False
        )

        # Job recommendations
        st.subheader("3. Job Role Matching")

        st.caption(
            "Match percentage is calculated from the "
            "number of required skills you selected."
        )

        st.dataframe(
            display_df,
            hide_index=True,
            use_container_width=True
        )

        best_match = display_df.iloc[0]

        st.info(
            f"Best matching role in this selection: "
            f"{best_match['Job Role']} "
            f"({best_match['Match (%)']}% skill match)."
        )

        # Bar chart
        st.subheader("4. Job Match Chart")

        chart_data = display_df.sort_values("Match (%)")

        fig, ax = plt.subplots(figsize=(9, 4))

        ax.barh(
            chart_data["Job Role"],
            chart_data["Match (%)"]
        )

        ax.set_xlabel("Required Skills Matched (%)")
        ax.set_xlim(0, 100)
        ax.set_title("Your Skills vs IT Job Requirements")

        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        # Skill gap analysis
        st.subheader("5. Skill Gap Analysis")

        for _, row in display_df.iterrows():

            with st.expander(
                f"{row['Job Role']} — {row['Match (%)']}% match"
            ):
                st.write("**Matched skills:**")
                st.write(row["Matched Skills"])

                st.write("**Skills to learn:**")
                st.write(row["Missing Skills"])

        # Recommendations
        st.subheader("6. Learning Recommendations")

        if target_role == "All Roles":
            recommendation_roles = jobs
        else:
            recommendation_roles = {
                target_role: jobs[target_role]
            }

        missing_skills = set()

        for role, required in recommendation_roles.items():
            missing_skills.update(required - student_skills)

        if missing_skills:
            st.write(
                "Focus on learning these missing skills:"
            )

            for skill in sorted(missing_skills):
                st.write(f"- {skill}")

        else:
            st.success(
                "You have selected all the listed skills "
                "for your chosen job requirements."
            )

        st.caption(
            "Note: This is an educational prototype using "
            "sample job requirements. A skill match does not "
            "guarantee employment or measure actual proficiency."
        )
