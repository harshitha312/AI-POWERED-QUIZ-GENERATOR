from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

class QuestionGenerator:
    def __init__(self):
        self.model_name = "valhalla/t5-base-qg-hl"
        self.tokenizer = T5Tokenizer.from_pretrained(self.model_name, legacy=False)  # use new tokenizer behavior
        self.model = T5ForConditionalGeneration.from_pretrained(self.model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def generate(self, context: str, num_return_sequences: int = 5):
        prompt = f"<hl> {context} <hl>"
        inputs = self.tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        num_beams = max(num_return_sequences, 5)  # num_beams must be >= num_return_sequences
        outputs = self.model.generate(
            **inputs,
            max_length=64,
            num_beams=num_beams,
            num_return_sequences=num_return_sequences,
            early_stopping=True,
            no_repeat_ngram_size=2,
            # Removed unsupported temperature argument
        )
        questions = [self.tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
        # Remove duplicates and empty questions
        questions = list(dict.fromkeys(q for q in questions if q.strip()))
        return questions[:num_return_sequences]
