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

# Light CSS to add subtle card-like boxes
st.markdown("""
<style>
.box {
    padding: 1.2rem;
    background: white;
    border-radius: 10px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    margin-bottom: 1.2rem;
}
</style>
""", unsafe_allow_html=True)


st.title(" Mappi – Personalized Exercise Proof of Concept")


# ============================
# TOP SECTION (Inputs ←→ Output)
# ============================

top_left, top_right = st.columns([0.45, 0.55])

# -----------------------------------
# LEFT SIDE — INPUTS
# -----------------------------------
with top_left:

    # Student Profile Box
    st.markdown("<div class='box'>", unsafe_allow_html=True)
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

    st.subheader("Interests")
    categories = st.multiselect(
        "Select 1–3 interest categories",
        ["Sport", "Music", "Movies & Series", "Videogames", "Animals", "Technology", "Art & Drawing"]
    )

    st.write("Add detail for each selected category:")
    free_interest_inputs = {
        cat: st.text_input(f"{cat} – specific detail (e.g., favourite team, artist…)") 
        for cat in categories
    }

    st.markdown("</div>", unsafe_allow_html=True)

    # Exercise box
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.header("2. Exercise Selection")

    exercise_bank = {
        "Arithmetic (1a)": {
            "1A – Percentage Increase": "A price is 80 kr and increases by 20%. What is the new price?",
            "1A – Rounding": "Round the number 47.68 to one decimal place.",
            "1A – Change Factor": "A value of 50 is multiplied by a factor of 1.2. What is the new value?",
            "1A – Exponents Comparison": "Compare the numbers 3^4 and 5^3. Which one is larger?",
            "1A – Basic Calculation": "Compute: 48 ÷ 6 × 4."
        },

        "Algebra (1b)": {
            "1B – Simplify Expression": "Simplify: 3(x + 2) − x.",
            "1B – Linear Equation": "Solve the equation: 2x − 5 = 15.",
            "1B – Factorization": "Factorize the expression: x^2 − 9.",
            "1B – Simplifying with Parentheses": "Simplify: 5a − 2(3a − 4).",
            "1B – Inequality": "Solve the inequality: 4x + 3 > 19."
        },

        "Functions, Geometry & Probability (1c)": {
            "1C – Linear Functions (Slope)": "Given points (2, 3) and (5, 9), find the slope of the line.",
            "1C – Exponential Expression": "Evaluate the expression: 2 × 3^4.",
            "1C – Similar Triangles": "A triangle has sides 6, 8, and 10. A similar triangle has a shortest side of 3. What is the length of the longest side?",
            "1C – Area & Dimensions": "A rectangle is 5 cm wide and has an area of 45 cm². What is its length?",
            "1C – Probability (Independent Events)": "A coin is flipped twice. What is the probability of getting two heads?"
        }
    }


    # First dropdown: Category
    selected_category = st.selectbox("Select a category", list(exercise_bank.keys()))

    # Second dropdown: specific exercise inside the chosen category
    selected_exercise_name = st.selectbox(
        "Choose an exercise",
        list(exercise_bank[selected_category].keys())
    )

    original_exercise = exercise_bank[selected_category][selected_exercise_name]

    st.markdown("</div>", unsafe_allow_html=True)


# --------------------------------------------------------
# STUDENT PROFILE + PROMPT
# --------------------------------------------------------
student_profile = {
    "programme": selected_programme,
    "interests": free_interest_inputs
}

prompt = f"""
You are a math problem writer.

Rewrite the following exercise by personalizing its context based on the student's interests and high school programme.

CRITICAL CONSTRAINTS:
- Do NOT change the mathematical structure.
- Do NOT change the numbers.
- Do NOT change the level of difficulty.
- Do NOT add any explanation, solution, or commentary.

OUTPUT FORMAT (VERY IMPORTANT):
- Return ONLY the rewritten exercise text.
- Do NOT add labels like "Personalized context", "Exercise:", "Solution:" or similar.
- Do NOT use bullet points or numbering. Just a single problem statement.

Student profile:
{json.dumps(student_profile, indent=2)}

Exercise:
\"\"\"{original_exercise}\"\"\"
"""


# --------------------------------------------------------
# CALL OPENAI
# --------------------------------------------------------
def generate_personalized(prompt):
    try:
        completion = client.chat.completions.create(
            model="gpt-4.1",
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
# RIGHT SIDE — OUTPUT
# --------------------------------------------------------
with top_right:

    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.header("📘 Output: Exercises")

    st.subheader("Original Exercise")
    st.code(original_exercise)

    st.subheader("Personalized Exercise")

    st.markdown(f"""
    <div style="
        font-size: 1.15rem; 
        line-height: 1.6; 
        background-color: #e8f5e9;
        border-left: 6px solid #4CAF50;
        padding: 1rem;
        border-radius: 6px;
    ">
    {personalized_text}
    </div>
    """, unsafe_allow_html=True)


    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------------
# DIAGNOSTICS (Bottom full width)
# --------------------------------------------------------
st.markdown("---")
st.header("🛠 Diagnostics")

diag1, diag2, diag3 = st.columns(3)

with diag1:
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.subheader("Student Profile (JSON)")
    st.json(student_profile)
    st.markdown("</div>", unsafe_allow_html=True)

with diag2:
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.subheader("Constructed Prompt")
    st.code(prompt, language="text")
    st.markdown("</div>", unsafe_allow_html=True)

with diag3:
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.subheader("Raw Model Response")
    st.code(personalized_text, language="text")
    st.markdown("</div>", unsafe_allow_html=True)
