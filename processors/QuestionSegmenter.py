from typing import List, Dict
import re

class QuestionSegmenter:
    MAIN_Q_RE = re.compile(r'^\d+')
    LETTER_SUB_RE = re.compile(r'^\(?[a-z]\)')
    ROMAN_SUB_RE = re.compile(r'^\(?[ivx]+\)')

    def segment(self, ocr_results: List[dict]) -> Dict[str, dict]:
        """
        Segment OCR blocks into a hierarchical question structure.
        """
        questions = {}
        current_main = None
        current_sub = None

        for block in ocr_results:
            text = block["text"].strip()

            # Check for main question
            if self.MAIN_Q_RE.match(text):
                main_num = self.MAIN_Q_RE.match(text).group()
                questions[main_num] = {}
                current_main = main_num
                current_sub = None
                continue

            # Check for lettered subpart
            elif self.LETTER_SUB_RE.match(text) and current_main:
                sub_letter = self.LETTER_SUB_RE.match(text).group().strip("()")
                questions[current_main][sub_letter] = text[len(self.LETTER_SUB_RE.match(text).group()):].strip()
                current_sub = sub_letter
                continue

            # Check for roman numeral subpart
            elif self.ROMAN_SUB_RE.match(text) and current_main:
                roman_num = self.ROMAN_SUB_RE.match(text).group().strip("()")
                if current_sub is None:
                    questions[current_main][roman_num] = text[len(self.ROMAN_SUB_RE.match(text).group()):].strip()
                else:
                    # If inside a lettered subpart, store as nested
                    if isinstance(questions[current_main][current_sub], str):
                        questions[current_main][current_sub] = {roman_num: text[len(self.ROMAN_SUB_RE.match(text).group()):].strip()}
                    else:
                        questions[current_main][current_sub][roman_num] = text[len(self.ROMAN_SUB_RE.match(text).group()):].strip()
                continue

            # Otherwise, append to current subpart
            else:
                if current_main and current_sub:
                    if isinstance(questions[current_main][current_sub], str):
                        questions[current_main][current_sub] += " " + text
                    else:
                        # Find last roman subpart
                        last_roman = list(questions[current_main][current_sub].keys())[-1]
                        questions[current_main][current_sub][last_roman] += " " + text
                elif current_main:
                    # If no subpart, append to main question directly
                    questions[current_main]["_text"] = questions[current_main].get("_text", "") + " " + text

        print(questions)
        return questions
