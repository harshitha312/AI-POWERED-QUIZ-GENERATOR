import streamlit as st
from question_generator import QuestionGenerator
from fetch_topic_text import fetch_topic_text
from PIL import Image
from ocr_easyocr import extract_text_from_image

qg = QuestionGenerator()

def run_quiz_interface():
    quiz_data = st.session_state.quiz_data
    st.subheader("Answer the following questions:")

    for idx, q in enumerate(quiz_data):
        st.markdown(f"**{idx + 1}. {q['question']}**")
        picked = st.radio(
            f"Choose the correct answer (Q{idx+1}):",
            q["options"],
            key=f"q_{idx}",
            index=None  # Prevents pre-selection
        )
        st.markdown("---")

    if st.button("Submit Quiz") and not st.session_state.get("submitted", False):
        if all(f"q_{i}" in st.session_state for i in range(len(quiz_data))):
            st.session_state.user_answers = {
                i: st.session_state[f"q_{i}"] for i in range(len(quiz_data))
            }
            st.session_state.submitted = True
        else:
            st.warning("Please answer all questions before submitting.")

    if st.session_state.get("submitted", False):
        score = sum([
            st.session_state.user_answers[i] == q["answer"]
            for i, q in enumerate(quiz_data)
        ])
        st.success(f"You got {score} out of {len(quiz_data)} correct!")

        # Show explanations for incorrect answers
        st.markdown("### ❌ Explanations for incorrect answers:")
        for i, q in enumerate(quiz_data):
            user_ans = st.session_state.user_answers[i]
            if user_ans != q["answer"]:
                st.markdown(f"**Q{i+1}. {q['question']}**")
                st.markdown(f"**Your Answer:** {user_ans}")
                st.markdown(f"**Correct Answer:** {q['answer']}")
                st.markdown(f"**Explanation:** {q.get('explanation', 'No explanation provided.')}**")
                st.markdown("---")

        if st.button("Retake Quiz"):
            for key in list(st.session_state.keys()):
                if key.startswith("q_"):
                    del st.session_state[key]
            st.session_state.generated = False
            st.session_state.submitted = False
            st.session_state.user_answers = {}
            st.experimental_rerun()

# ----------------------- UI START -----------------------

st.title("\U0001F9E0 AI Quiz Question Generator")

input_type = st.radio("Select input type:", ["Topic", "Text", "Image"])
num_questions = st.slider("How many questions would you like to generate? (Max 20)", 1, 20, 5)

if "generated" not in st.session_state:
    st.session_state.generated = False
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# INPUT HANDLING
if not st.session_state.generated:
    if input_type == "Topic":
        topic = st.text_input("Enter a topic to generate questions:")
        if st.button("Generate") and topic.strip():
            with st.spinner("Fetching content from Wikipedia..."):
                summary = fetch_topic_text(topic.strip())
            if summary:
                st.session_state.quiz_data = qg.generate_questions_with_options(summary, num_questions)
                st.session_state.generated = True
            else:
                st.error("Couldn't fetch content for that topic.")

    elif input_type == "Text":
        text_input = st.text_area("Enter text to generate questions from:")
        if st.button("Generate") and text_input.strip():
            st.session_state.quiz_data = qg.generate_questions_with_options(text_input.strip(), num_questions)
            st.session_state.generated = True

    elif input_type == "Image":
        uploaded_file = st.file_uploader("Upload an image containing text:")
        if st.button("Generate") and uploaded_file:
            image = Image.open(uploaded_file)
            text = extract_text_from_image(image)
            if text:
                st.session_state.quiz_data = qg.generate_questions_with_options(text, num_questions)
                st.session_state.generated = True
            else:
                st.error("Couldn't extract any text from the image.")

# SHOW QUIZ INTERFACE
if st.session_state.generated:
    run_quiz_interface()
