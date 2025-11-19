# src/distractor_generator.py

from sense2vec import Sense2Vec

class DistractorGenerator:
    def __init__(self):
        self.s2v = Sense2Vec().from_disk("C:\Users\Gunnam Harshitha\Downloads\sense2vec-2.0.2\sense2vec-2.0.2")  # adjust the path!

    def generate_distractors(self, answer: str, num_distractors: int = 3):
        """
        Generate distractors for the given answer.
        """
        try:
            sense = self.s2v.get_best_sense(answer)
            most_similar = self.s2v.most_similar(sense, n=num_distractors + 5)
            distractors = []
            for word, score in most_similar:
                if word.lower() != answer.lower() and word.lower() not in distractors:
                    distractors.append(word.split('|')[0])
                if len(distractors) >= num_distractors:
                    break
            return distractors
        except Exception as e:
            print(f"Error generating distractors: {e}")
            return []
