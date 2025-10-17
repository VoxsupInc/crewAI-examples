from crewai.tools import tool
import ast
import operator
import re


@tool("Calculator tool")
def CalculatorTool(operation: str) -> float:
    """Useful to perform any mathematical calculations, like sum, minus, multiplication, division, etc. 
    The input to this tool should be a mathematical expression, a couple examples are `200*7` or `5000/2*10`."""
    try:
        allowed_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.Mod: operator.mod,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos,
        }
        
        if not re.match(r'^[0-9+\-*/().% ]+$', operation):
            raise ValueError("Invalid characters in mathematical expression")
        
        tree = ast.parse(operation, mode='eval')
        
        def _eval_node(node):
            if isinstance(node, ast.Expression):
                return _eval_node(node.body)
            elif isinstance(node, ast.Constant):
                return node.value
            elif isinstance(node, ast.Num):
                return node.n
            elif isinstance(node, ast.BinOp):
                left = _eval_node(node.left)
                right = _eval_node(node.right)
                op = allowed_operators.get(type(node.op))
                if op is None:
                    raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
                return op(left, right)
            elif isinstance(node, ast.UnaryOp):
                operand = _eval_node(node.operand)
                op = allowed_operators.get(type(node.op))
                if op is None:
                    raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
                return op(operand)
            else:
                raise ValueError(f"Unsupported node type: {type(node).__name__}")
        
        result = _eval_node(tree)
        return result
        
    except (SyntaxError, ValueError, ZeroDivisionError, TypeError) as e:
        raise ValueError(f"Calculation error: {str(e)}")
    except Exception:
        raise ValueError("Invalid mathematical expression")
