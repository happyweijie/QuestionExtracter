from typing import List

class QuestionSegmenter:
    def segment(self, ocr_results: List[dict]) -> List[List[dict]]:
        """
        Naive example: start a new question when text begins with a number + dot (e.g., "1.", "2.")
        """
        questions = []
        current_question = []

        for block in ocr_results:
            if block["text"].strip().startswith(tuple(str(i) + "." for i in range(1, 101))):
                if current_question:
                    questions.append(current_question)
                current_question = [block]
            else:
                current_question.append(block)

        if current_question:
            questions.append(current_question)

        return questions