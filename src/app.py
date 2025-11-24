import streamlit as st
import json
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Page setup
st.set_page_config(page_title="Mappi Personalized Exercise PoC", layout="wide")

st.title("🧪 Mappi – Personalized Exercise Prototype")

st.write("""
This prototype demonstrates how math exercises can be personalized using:
- A student profile (programme + interests)  
- A dynamically generated prompt  
- An LLM that rewrites the context without changing the mathematics  
""")

# ============================
# LAYOUT: TOP SECTION
# Left → inputs
# Right → original + personalized exercises
# ============================

top_left, top_right = st.columns([0.45, 0.55])

# -----------------------------------
# LEFT COLUMN — INPUTS
# -----------------------------------
with top_left:
    st.header("1. Student Profile")

    st.subheader("High School Programme")
    programmes = [
        "Naturvetenskapsprogrammet (NA) – Science",
        "Teknikprogrammet (TE) – Technology",
        "Ekonomiprogrammet (EK) – Economics",
        "Samhällsvetenskapsprogrammet (SA) – Social Sciences",
        "Humanistiska programmet (HU) – Humanities",
        "Estetiska programmet (ES) – Arts",
        "Vocational – Child and Recreation (BF)",
        "Vocational – Building and Construction (BA)",
        "Vocational – Electricity and Energy (EE)",
        "Vocational – Vehicle and Transport (FT)",
        "Vocational – Business and Administration (HA)",
        "Vocational – Handicraft (HV)",
        "Vocational – Hotel and Tourism (HT)",
        "Vocational – Industrial Technology (IN)",
        "Vocational – Natural Resource Use (NB)",
        "Vocational – Restaurant and Food (RL)",
        "Vocational – HVAC and Property Maintenance (VF)",
        "Vocational – Health and Social Care (VO)"
    ]

    selected_programme = st.selectbox("Select the student's programme", programmes)

    # Interests
    st.subheader("Interests")
    categories = st.multiselect(
        "Select 1–3 interest categories",
        ["Sport", "Music", "Movies & Series", "Videogames", "Animals", "Technology", "Art & Drawing"]
    )

    st.write("Add detail for each selected category:")
    free_interest_inputs = {}
    for cat in categories:
        free_interest_inputs[cat] = st.text_input(f"{cat} – specific detail (e.g., favourite team, artist…)")

    # -----------------------------------
    # Exercise Selection
    # -----------------------------------
    st.header("2. Exercise Selection")

    exercises = {
        "Percentages": "A quantity increases by 20%. What is the new value?",
        "Change Factors": "A value is multiplied by a factor of 1.2. What is the new value?",
        "Linear Equation": "Solve: 2x - 5 = 15.",
        "Basic Algebra": "Simplify: 3(x + 2) - x.",
        "Linear Functions": "Given points (2,3) and (5,9), find the slope."
    }

    selected_exercise_key = st.selectbox("Choose an exercise", list(exercises.keys()))
    original_exercise = exercises[selected_exercise_key]

# --------------------------------------------------------
# BUILD STUDENT PROFILE + PROMPT
# --------------------------------------------------------
student_profile = {
    "programme": selected_programme,
    "interests": free_interest_inputs
}

prompt = f"""
Rewrite the following exercise by personalizing its context based on the student's interests and high school programme.
Do NOT change:
- the mathematical structure
- the numbers
- the level of difficulty
- the required reasoning steps

Student profile:
{json.dumps(student_profile, indent=2)}

Exercise:
\"\"\"{original_exercise}\"\"\"
"""

# --------------------------------------------------------
# CALL OPENAI (UPDATED FOR SDK 2.8.1)
# --------------------------------------------------------
def generate_personalized(prompt):
    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You rewrite math problems by changing ONLY the context."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error calling OpenAI API:\n{e}"

personalized_text = generate_personalized(prompt)

# --------------------------------------------------------
# RIGHT COLUMN — OUTPUT ONLY (NO DIAGNOSTICS HERE)
# --------------------------------------------------------
with top_right:
    st.header("📘 Output: Exercises")

    st.subheader("Original Exercise")
    st.code(original_exercise)

    st.subheader("Personalized Exercise")
    st.success(personalized_text)

# --------------------------------------------------------
# BOTTOM SECTION — DIAGNOSTICS (FULL WIDTH)
# --------------------------------------------------------
st.markdown("---")
st.header("🛠 Diagnostics")

diag1, diag2, diag3 = st.columns(3)

with diag1:
    st.subheader("Student Profile (JSON)")
    st.json(student_profile)

with diag2:
    st.subheader("Constructed Prompt")
    st.code(prompt, language="text")

with diag3:
    st.subheader("Raw Model Response")
    st.code(personalized_text, language="text")
