"""A bounded arithmetic evaluator for controlled experiments.

Never use eval() or exec() on agent-generated code or prompts.
"""
import ast
import math
import operator

_OPERATORS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
              ast.Div: operator.truediv, ast.Pow: operator.pow}
_UNARY = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def arithmetic(expression: str) -> float:
    """Evaluate simple arithmetic while limiting complexity and magnitudes."""
    if not isinstance(expression, str) or len(expression) > 120:
        raise ValueError("Expression must be text of at most 120 characters")
    tree = ast.parse(expression, mode="eval")
    if sum(1 for _ in ast.walk(tree)) > 35:
        raise ValueError("Expression too complex")

    def visit(node):
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            value = float(node.value)
        elif isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY:
            value = _UNARY[type(node.op)](visit(node.operand))
        elif isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Pow) and (abs(right) > 8 or abs(left) > 1e5):
                raise ValueError("Exponent out of bounds")
            try:
                value = _OPERATORS[type(node.op)](left, right)
            except (ZeroDivisionError, OverflowError) as exc:
                raise ValueError("Invalid arithmetic") from exc
        else:
            raise ValueError("Unsupported expression")
        if not math.isfinite(value) or abs(value) > 1e12:
            raise ValueError("Result out of bounds")
        return value

    return visit(tree)


def check_answer(expression: str, answer: float, tolerance: float = 1e-9) -> bool:
    """Check a numeric answer against independently evaluated arithmetic."""
    if type(answer) not in (int, float) or not math.isfinite(answer):
        return False
    if not (0 <= tolerance <= 0.01):
        raise ValueError("Invalid tolerance")
    return math.isclose(arithmetic(expression), answer, rel_tol=tolerance, abs_tol=tolerance)
