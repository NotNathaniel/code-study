"""Generate fill-in-the-blank questions from Python code snippets.

This is a minimal prototype that parses a snippet of Python code and
creates a single question where a binary operator is blanked out.  The
resulting question object mimics the style of online coding platforms.
"""

from __future__ import annotations

from dataclasses import dataclass
import ast
from typing import Optional


@dataclass
class Question:
    """Representation of a fill-in-the-blank question."""

    snippet: str
    description: str
    instruction: str
    answer: str
    hint: str


_OPERATOR_STR = {
    ast.Add: "+",
    ast.Sub: "-",
    ast.Mult: "*",
    ast.Div: "/",
}

_OPERATOR_NAME = {
    "+": "addition",
    "-": "subtraction",
    "*": "multiplication",
    "/": "division",
}


def generate_question(code: str) -> Optional[Question]:
    """Parse ``code`` and return a single :class:`Question`.

    The current implementation searches for the first binary operation and
    blanks out its operator.  If no supported operation is found ``None``
    is returned.
    """

    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp) and type(node.op) in _OPERATOR_STR:
            operator = _OPERATOR_STR[type(node.op)]
            segment = ast.get_source_segment(code, node)
            if segment is None:
                continue
            blanked = segment.replace(operator, "___")
            description = (
                f"This expression evaluates ``{ast.unparse(node.left)}`` {operator} "
                f"``{ast.unparse(node.right)}``."
            )
            instruction = "Fill in the blank with the correct operator."
            hint = f"Use the { _OPERATOR_NAME[operator] } operator."
            return Question(blanked, description, instruction, operator, hint)
    return None


def check_answer(question: Question, user_answer: str) -> bool:
    """Return ``True`` if ``user_answer`` matches ``question.answer``."""

    return user_answer.strip() == question.answer


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Provide a Python snippet as an argument.")
        raise SystemExit(1)

    snippet = sys.argv[1]
    q = generate_question(snippet)
    if q is None:
        print("No question could be generated from the snippet.")
    else:
        print(q.snippet)
        print(q.description)
        print(q.instruction)

