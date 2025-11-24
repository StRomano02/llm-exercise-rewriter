# Personalized Math Exercise Rewriter — Proof of Concept

This project explores how mathematics can become more engaging and intuitive through **personalized learning experiences**.

Students can select their **Swedish high school programme**, describe a few **personal interests**, and choose from a set of exercises spanning:

- **Arithmetic (1a)** — percentages, rounding, exponents, basic operations  
- **Algebra (1b)** — simplification, equations, factorization, inequalities  
- **Functions, Geometry & Probability (1c)** — slopes, similar triangles, areas, probability  

Based on these inputs, an LLM rewrites the context of the chosen math problem while **preserving the mathematical structure**, creating an experience that feels *more connected, familiar, and meaningful* to the student.

## 🧪 Why wait? Give it a shot!

👉 https://llm-exercise-rewriter-rbpjxf9chuipj7lyu2wseo.streamlit.app/#f5b0b85f


## 📌 Features

- Choose among **17 Swedish high school programmes**, including:
  - Science (NA), Technology (TE), Economics (EK), Social Sciences (SA), Humanities (HU), Arts (ES), and the full set of Vocational programmes  
- Add **personal interests** with custom details  
- Pick from **15 curated exercises** across the 1a–1b–1c levels  
- Get a rewritten exercise where:
  - ✔️ the math stays identical  
  - ✔️ only the *context* changes  
  - ✔️ everything is tailored to the student  

## 🔐 Running Locally

```bash
streamlit run src/app.py
```

