from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch
import random
import re
from typing import List
import spacy

class QuestionGenerator:
    def __init__(self):
        self.tokenizer = T5Tokenizer.from_pretrained("iarfmoose/t5-base-question-generator")
        self.model = T5ForConditionalGeneration.from_pretrained("iarfmoose/t5-base-question-generator")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.model.to(self.device)
        self.nlp = spacy.load("en_core_web_sm")  # Load NLP model
        self.used_options = set()  # Track globally used options

    def _split_sentences(self, text: str) -> List[str]:
        return re.split(r'(?<=[.!?])\s+', text.strip())

    def _generate_questions(self, context: str, n: int) -> List[str]:
        prompt = f"<hl> {context} <hl>"
        cleaned = set()
        attempts = 0
        max_attempts = 8

        while len(cleaned) < n and attempts < max_attempts:
            inputs = self.tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            num_return_sequences = max(n * 4, 20)
            num_beams = max(num_return_sequences, 10)

            outputs = self.model.generate(
                **inputs,
                max_length=64,
                num_beams=num_beams,
                num_return_sequences=num_return_sequences,
                early_stopping=True,
                no_repeat_ngram_size=2
            )

            raw_questions = [self.tokenizer.decode(out, skip_special_tokens=True) for out in outputs]

            for q in raw_questions:
                q = re.sub(r"[^a-zA-Z0-9 ]*hl[^a-zA-Z0-9 ]*|[=<>/?]+", "", q).strip()
                q = re.sub(r"\s+\w(?=\?)", "", q).strip()
                if not q:
                    continue
                q = q[0].upper() + q[1:] if len(q) > 1 else q.upper()
                if not q.endswith("?"):
                    q += "?"
                cleaned.add(q.lower())

            attempts += 1

        final_questions = list(cleaned)
        if len(final_questions) < n:
            print(f"\u26a0\ufe0f Warning: Only {len(final_questions)} unique questions generated. Requested: {n}")

        return [q.capitalize() for q in final_questions[:n]]

    def _extract_answer(self, question: str, context: str) -> str:
        doc = self.nlp(context)
        q_words = set(w.lower() for w in re.findall(r"\w+", question))
        best_phrase, best_score = "", 0

        for chunk in doc.noun_chunks:
            chunk_words = set(w.lower() for w in chunk.text.split())
            score = len(q_words.intersection(chunk_words))
            if score > best_score and len(chunk.text.strip()) > 3:
                best_score = score
                best_phrase = chunk.text.strip()

        return best_phrase if best_score > 0 else "No clear answer found"

    def _generate_options(self, correct_answer: str, context: str, n: int = 4) -> List[str]:
        options = [correct_answer]
        self.used_options.add(correct_answer.lower())

        # Use spaCy to extract potential distractors
        doc = self.nlp(context)
        candidate_phrases = set()

        for chunk in doc.noun_chunks:
            phrase = chunk.text.strip()
            if (phrase and phrase.lower() != correct_answer.lower()
                    and phrase.lower() not in self.used_options
                    and len(phrase.split()) <= 6):
                candidate_phrases.add(phrase)

        # Randomize and select distractors
        distractors = list(candidate_phrases)
        random.shuffle(distractors)

        for d in distractors:
            if len(options) >= n:
                break
            options.append(d)
            self.used_options.add(d.lower())

        # Fallback if not enough distractors (use variations)
        filler_count = 1
        while len(options) < n:
            fake_option = f"{correct_answer} (variation {filler_count})"
            options.append(fake_option)
            self.used_options.add(fake_option.lower())
            filler_count += 1

        random.shuffle(options)
        return options

    def _generate_explanation(self, question: str, answer: str, context: str) -> str:
        # Improved explanation generation
        explanation = ""
        doc = self.nlp(context)
        for sent in doc.sents:
            if answer.lower() in sent.text.lower():
                explanation = sent.text.strip()
                break

        if not explanation:
            explanation = f"The answer '{answer}' is derived from the content, which best matches the question."

        return f"Explanation: {explanation}"

    def generate_questions_with_options(self, context: str, num_questions: int = 5):
        questions = self._generate_questions(context, num_questions)
        bundled = []
        self.used_options = set()  # Reset for each new batch

        for q in questions:
            correct = self._extract_answer(q, context)
            options = self._generate_options(correct, context)
            bundled.append({
                "question": q,
                "options": options,
                "answer": correct,
                "explanation": self._generate_explanation(q, correct, context)
            })

        return bundled
