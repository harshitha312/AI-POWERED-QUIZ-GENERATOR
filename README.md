# 🧠 OCR-Based Automatic Question Generator

This project is an AI-powered pipeline that extracts text from images and automatically generates quiz questions with multiple-choice options and explanations using advanced NLP techniques.

## 📌 Features

- 🔍 **Text Extraction from Images** using Tesseract OCR.
- 🤖 **Question Generation** using pre-trained T5 Transformer models.
- 🎯 **Answer Extraction** based on context and question matching.
- 📝 **MCQ Options** with intelligent distractors using NLP.
- 🧾 **Explanations** for each answer to aid understanding.

## 📂 Project Structure

├── ocr_easyocr.py # Extracts text from image using Tesseract OCR
├── generate_questions.py # Simple question generation using valhalla/t5-base-qg-hl
├── question_generator.py # Advanced question generation with MCQs and explanations using iarfmoose/t5-base

bash
Copy
Edit

## 🚀 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/ocr-question-generator.git
   cd ocr-question-generator
Install Dependencies

bash
Copy
Edit
pip install torch torchvision transformers pillow pytesseract spacy
python -m spacy download en_core_web_sm
Install Tesseract

On Ubuntu:

bash
Copy
Edit
sudo apt-get install tesseract-ocr
On Windows: Download installer

Ensure Tesseract is accessible via your system PATH. Example for Windows:

python
Copy
Edit
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
🛠️ How It Works
Image Text Extraction

ocr_easyocr.py uses Tesseract to extract raw text from an image file.

Question Generation

generate_questions.py produces basic questions from a block of text.

question_generator.py produces advanced questions with options and explanations.

Bundled Output Example

json
Copy
Edit
{
  "question": "What is the capital of France?",
  "options": ["Paris", "London", "Berlin", "Madrid"],
  "answer": "Paris",
  "explanation": "Explanation: The capital of France is Paris."
}
📸 Example Usage
python
Copy
Edit
from PIL import Image
from ocr_easyocr import extract_text_from_image
from question_generator import QuestionGenerator

# Load and process image
img = Image.open("example_image.jpg")
text = extract_text_from_image(img)

# Generate questions
qg = QuestionGenerator()
results = qg.generate_questions_with_options(text)

for item in results:
    print(item)
📘 Models Used
valhalla/t5-base-qg-hl - For basic question generation

iarfmoose/t5-base-question-generator - For MCQ generation

🧪 Testing
Make sure you have a sample .jpg or .png image with printed English text. Run the demo script to test the full pipeline.

✅ TODO
Add a GUI or Web interface using Streamlit or Flask

Allow PDF input (using pdf2image)

Export questions to JSON or CSV
