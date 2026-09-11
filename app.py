import streamlit as st
import ast
import subprocess
import sys
import re
import base64

# ============================================================
# PyGuide - Free AI Coding Helper Prototype
# ============================================================

st.set_page_config(
    page_title="PyGuide",
    page_icon="pyguide_logo.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------
# Styling
# ----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: #07152f;
        color: #ffffff;
    }

    [data-testid="stHeader"] {
        background: #07152f;
    }
        /* 🍀 Falling clover background */
    .clover-rain {
        position: fixed;
        inset: 0;
        width: 100vw;
        height: 100vh;
        overflow: hidden;
        pointer-events: none;
        z-index: 0;
    }

    .clover-rain span {
        position: absolute;
        top: -10vh;
        font-size: 16px;
        opacity: 0.55;
        animation: clover-fall linear infinite;
        user-select: none;
    }

    .clover-rain span:nth-child(1)  { left: 3%;  animation-duration: 12s; animation-delay: -2s; }
    .clover-rain span:nth-child(2)  { left: 9%;  animation-duration: 16s; animation-delay: -8s; font-size: 13px; }
    .clover-rain span:nth-child(3)  { left: 16%; animation-duration: 14s; animation-delay: -5s; }
    .clover-rain span:nth-child(4)  { left: 23%; animation-duration: 18s; animation-delay: -12s; font-size: 14px; }
    .clover-rain span:nth-child(5)  { left: 31%; animation-duration: 13s; animation-delay: -7s; font-size: 12px; }
    .clover-rain span:nth-child(6)  { left: 38%; animation-duration: 17s; animation-delay: -10s; }
    .clover-rain span:nth-child(7)  { left: 45%; animation-duration: 15s; animation-delay: -3s; font-size: 14px; }
    .clover-rain span:nth-child(8)  { left: 52%; animation-duration: 19s; animation-delay: -15s; font-size: 12px; }
    .clover-rain span:nth-child(9)  { left: 59%; animation-duration: 14s; animation-delay: -6s; }
    .clover-rain span:nth-child(10) { left: 66%; animation-duration: 17s; animation-delay: -11s; font-size: 13px; }
    .clover-rain span:nth-child(11) { left: 73%; animation-duration: 13s; animation-delay: -4s; }
    .clover-rain span:nth-child(12) { left: 80%; animation-duration: 18s; animation-delay: -9s; font-size: 14px; }
    .clover-rain span:nth-child(13) { left: 87%; animation-duration: 15s; animation-delay: -13s; font-size: 12px; }
    .clover-rain span:nth-child(14) { left: 94%; animation-duration: 20s; animation-delay: -1s; }

    @keyframes clover-fall {
        0% {
            transform: translate3d(0, -10vh, 0) rotate(0deg);
        }
        25% {
            transform: translate3d(18px, 28vh, 0) rotate(80deg);
        }
        50% {
            transform: translate3d(-15px, 55vh, 0) rotate(180deg);
        }
        75% {
            transform: translate3d(20px, 82vh, 0) rotate(270deg);
        }
        100% {
            transform: translate3d(-10px, 110vh, 0) rotate(360deg);
        }
    }

    [data-testid="stAppViewContainer"] > .main {
        position: relative;
        z-index: 1;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    .pyguide-title {
        font-size: 42px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0;
    }

    .pyguide-subtitle {
        color: #9ecbff;
        font-size: 17px;
        margin-top: 0;
        margin-bottom: 25px;
    }

    .panel {
        background: #0d2145;
        border: 1px solid #1d4078;
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 15px;
    }

    .success-box {
        background: #0d3b2e;
        border: 1px solid #1d8f6e;
        border-radius: 12px;
        padding: 14px;
        color: #d8fff3;
    }

    .hint-box {
        background: #3b2f0d;
        border: 1px solid #9a7b20;
        border-radius: 12px;
        padding: 14px;
        color: #fff3b8;
    }

    .info-box {
        background: #102e55;
        border: 1px solid #2865a8;
        border-radius: 12px;
        padding: 14px;
        color: #dceeff;
    }

    .error-box {
        background: #421b25;
        border: 1px solid #a63b52;
        border-radius: 12px;
        padding: 14px;
        color: #ffe0e7;
    }

    .small-label {
        color: #9ecbff;
        font-size: 14px;
        font-weight: 600;
    }

    div.stButton > button {
        background-color: #1769ff !important;
        color: white !important;
        border: 1px solid #3380ff !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
    }

    div.stButton > button:hover {
        background-color: #3380ff !important;
        color: white !important;
        border-color: #5c9cff !important;
    }

    /* ========================================================
       DARK INPUT SYSTEM - applies to Streamlit + BaseWeb
       ======================================================== */
    div[data-testid="stTextInput"],
    div[data-testid="stTextArea"],
    div[data-baseweb="input"],
    div[data-baseweb="textarea"],
    div[data-baseweb="base-input"] {
        background: #102957 !important;
        background-color: #102957 !important;
        border-radius: 10px !important;
    }

    div[data-testid="stTextInput"] > div,
    div[data-testid="stTextInput"] > div > div,
    div[data-testid="stTextArea"] > div,
    div[data-testid="stTextArea"] > div > div,
    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div {
        background: #102957 !important;
        background-color: #102957 !important;
        border-radius: 10px !important;
    }

    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea,
    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea,
    div[data-baseweb="base-input"] input,
    div[data-baseweb="base-input"] textarea,
    input[type="text"],
    textarea {
        background: #102957 !important;
        background-color: #102957 !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        border: 1px solid #2f6fed !important;
        border-radius: 10px !important;
        caret-color: #ffffff !important;
        box-shadow: none !important;
        outline: none !important;
    }

    div[data-testid="stTextInput"] input:hover,
    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stTextArea"] textarea:hover,
    div[data-testid="stTextArea"] textarea:focus,
    input[type="text"]:hover,
    input[type="text"]:focus,
    textarea:hover,
    textarea:focus {
        background: #102957 !important;
        background-color: #102957 !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        border-color: #3380ff !important;
        box-shadow: 0 0 0 1px #3380ff !important;
    }

    div[data-testid="stTextInput"] input::placeholder,
    div[data-testid="stTextArea"] textarea::placeholder,
    input::placeholder,
    textarea::placeholder {
        color: #8fb9e8 !important;
        -webkit-text-fill-color: #8fb9e8 !important;
        opacity: 1 !important;
    }

    textarea { font-family: Consolas, "Courier New", monospace !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# 🍀 Falling clovers
st.markdown(
    """
    <div class="clover-rain" aria-hidden="true">
        <span>🍀</span><span>🍀</span><span>🍀</span><span>🍀</span>
        <span>🍀</span><span>🍀</span><span>🍀</span><span>🍀</span>
        <span>🍀</span><span>🍀</span><span>🍀</span><span>🍀</span>
        <span>🍀</span><span>🍀</span>
    </div>
    """,
    unsafe_allow_html=True,
)
# ----------------------------
# Helper functions
# ----------------------------
def explain_syntax_error(error):
    message = str(error.msg).lower()

    if "expected ':'" in message:
        return (
            "Python expected a colon (:). "
            "Statements such as if, elif, else, for, while, def and class "
            "normally need a colon at the end."
        )

    if "expected an indented block" in message:
        return (
            "Python found a line that should contain an indented block. "
            "After statements such as if, for, while or def, the next line "
            "needs to be indented."
        )

    if "invalid syntax" in message:
        return (
            "Python could not understand this line. "
            "Check brackets, quotes, colons and spelling around the highlighted line."
        )

    if "unterminated string" in message:
        return (
            "A string was started with a quote but Python could not find "
            "the matching closing quote."
        )

    if "unexpected indent" in message:
        return (
            "This line has more indentation than Python expects. "
            "Check the spaces at the beginning of the line."
        )

    return "Python found a syntax problem. Check the highlighted line and the lines immediately before it."


def suggest_syntax_correction(code, error):
    """Return a corrected full program for common beginner syntax mistakes."""
    lines = code.splitlines()

    if not lines:
        return None

    corrected = lines.copy()

    # Fix common indentation mistakes on elif/else/except/finally.
    # These keywords must line up with the block header they belong to.
    for i, line in enumerate(corrected):
        stripped = line.strip()
        if stripped.startswith(("elif ", "else", "except", "finally")):
            current_indent = len(line) - len(line.lstrip())
            for j in range(i - 1, -1, -1):
                previous = corrected[j]
                previous_stripped = previous.strip()
                previous_indent = len(previous) - len(previous.lstrip())
                if previous_indent <= current_indent and previous_stripped.startswith(("if ", "elif ", "else", "try", "except")):
                    corrected[i] = " " * previous_indent + stripped
                    break

    # Add missing colons to common Python block statements.
    block_words = ("if ", "elif ", "else", "for ", "while ", "def ", "class ", "try", "except", "finally")
    for i, line in enumerate(corrected):
        stripped = line.strip()
        if stripped.startswith(block_words) and not stripped.endswith(":"):
            corrected[i] = line + ":"

    result = "\n".join(corrected)

    # Only return the suggestion if the corrected program is actually valid.
    try:
        ast.parse(result)
        if result != code:
            return result
    except SyntaxError:
        return None

    return None


def explain_runtime_error(error_text):
    text = error_text.lower()

    if "indexerror" in text:
        return (
            "You tried to access a position that does not exist in a list. "
            "Think of a list like numbered boxes: if there are only 3 boxes, "
            "you cannot open box number 6."
        )

    if "nameerror" in text:
        return (
            "Python cannot find the variable or function name you used. "
            "Check its spelling and make sure you created it before using it."
        )

    if "typeerror" in text:
        return (
            "Python received a value of the wrong type. "
            "For example, adding text directly to a number can cause this."
        )

    if "zerodivisionerror" in text:
        return (
            "A number is being divided by zero. "
            "Check the denominator before performing the division."
        )

    if "keyerror" in text:
        return (
            "You tried to access a dictionary key that does not exist. "
            "Check the key name or use a safer lookup."
        )

    if "indentationerror" in text:
        return (
            "Python found an indentation problem. "
            "Make sure related lines use consistent indentation."
        )

    return (
        "Your program ran into a runtime error. "
        "Read the last line of the error first; it usually tells you what went wrong."
    )


def check_logic(code):
    # Simple prototype rules, not a full AI logic analyser.
    if re.search(r"\btotal\s*=\s*price\s*\*\s*quantity\b", code):
        return {
            "found": True,
            "title": "Possible accumulation error",
            "hint": "Are you replacing total each time instead of adding each item's price?",
            "fix": "total += price * quantity",
            "explanation": (
                "If you calculate a total inside a loop, using = replaces the "
                "old total. Using += keeps the old total and adds the new amount."
            ),
        }

    if re.search(r"\bif\s+\w+\s*=\s*[^=]", code):
        return {
            "found": True,
            "title": "Possible condition error",
            "hint": "Inside an if condition, did you mean to compare two values?",
            "fix": "Use == when you want to compare two values.",
            "explanation": (
                "A single = is normally used to assign a value. "
                "A double == is used to compare values."
            ),
        }

    if "average" in code.lower() and re.search(r"average\s*=\s*[^/\n]+$", code, re.MULTILINE):
        return {
            "found": True,
            "title": "Possible average calculation issue",
            "hint": "An average normally needs both a total and the number of values.",
            "fix": "average = total / count",
            "explanation": "Check that you divide the total by the number of values.",
        }

    return {
        "found": False,
        "title": "No common logic error detected",
        "hint": "The prototype did not detect one of its known patterns.",
        "fix": "",
        "explanation": (
            "This free prototype checks a few common mistakes. "
            "It does not understand every possible program logic problem."
        ),
    }


def suggest_logic_correction(code, result):
    """Return the full program with a simple detected logic mistake corrected."""
    if not result.get("found"):
        return None

    lines = code.splitlines()

    for i, line in enumerate(lines):
        if re.search(r"\btotal\s*=\s*price\s*\*\s*quantity\b", line):
            indent = line[:len(line) - len(line.lstrip())]
            lines[i] = indent + "total += price * quantity"
            return "\n".join(lines)

    for i, line in enumerate(lines):
        if re.search(r"\bif\s+\w+\s*=\s*[^=]", line):
            lines[i] = re.sub(r"(\bif\s+\w+)\s*=\s*", r"\1 == ", line)
            return "\n".join(lines)

    if "average" in code.lower():
        for i, line in enumerate(lines):
            if re.match(r"^\s*average\s*=", line):
                indent = line[:len(line) - len(line.lstrip())]
                lines[i] = indent + "average = total / count"
                return "\n".join(lines)

    return None


def run_python_code(code):
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=5,
        )

        return result.stdout, result.stderr, result.returncode

    except subprocess.TimeoutExpired:
        return "", "Execution stopped because it took longer than 5 seconds.", -1

    except Exception as exc:
        return "", str(exc), -1


def check_pseudocode(text):
    """Validate common beginner pseudocode structure before conversion."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return None
    if lines[0].upper() != "START":
        return {"message": "Pseudocode must start with exactly START.", "hint": "Put START as the first non-empty line."}
    if lines[-1].upper() != "END":
        return {"message": f"{lines[-1]} is invalid. Use exactly END.", "hint": "Your pseudocode must finish with END."}
    for i,line in enumerate(lines[1:-1],2):
        u=line.upper()
        if u == "START": return {"message": f"START is in the wrong place (line {i}).", "hint": "START should appear only first."}
        if u == "END": return {"message": f"END is in the wrong place (line {i}).", "hint": "END should appear only last."}
        if (u.startswith(("IF ","ELSE IF ","ELSE"))) and line.endswith(":"):
            return {"message": f"Python-style ':' found on line {i}.", "hint": "Pseudocode conditions do not need a colon."}
        if u == "IF" or u == "ELSE IF":
            return {"message": f"Incomplete condition on line {i}.", "hint": "Add a condition, for example: IF age >= 18."}
        if u.startswith("ELSE "):
            return {"message": f"Invalid ELSE statement on line {i}.", "hint": "Use ELSE by itself, or write a complete ELSE IF condition."}
        for k in ("TAKE","INPUT","READ","DISPLAY","PRINT","OUTPUT","ADD","SUBTRACT","MULTIPLY","DIVIDE","STORE","SET","ASSIGN"):
            if u == k:
                return {"message": f"Incomplete {k} statement on line {i}.", "hint": "Add the value or action that this statement should use."}
    return None


def convert_pseudocode(text):
    lower = text.lower().strip()

    # Example: two numbers and addition
    if (
        ("two numbers" in lower or ("number" in lower and "number" in lower))
        and ("add" in lower or "sum" in lower)
    ):
        code = """a = int(input("Enter first number: "))
b = int(input("Enter second number: "))

result = a + b

print(result)"""

        explanation = (
            "• Take two numbers → input() with int()\n"
            "• Add the numbers → result = a + b\n"
            "• Display the result → print(result)"
        )
        return code, explanation

    # If / else
    if "if" in lower and "else" in lower:
        code = """number = int(input("Enter a number: "))

if number > 0:
    print("Positive")
else:
    print("Not positive")"""

        explanation = (
            "• IF becomes Python's if statement.\n"
            "• ELSE becomes Python's else statement.\n"
            "• The condition ends with a colon (:).\n"
            "• The code inside each block is indented."
        )
        return code, explanation

    # Simple loop
    if "repeat" in lower or "loop" in lower:
        code = """for i in range(5):
    print(i)"""

        explanation = (
            "• REPEAT/LOOP becomes a for loop.\n"
            "• range(5) creates five loop iterations.\n"
            "• The repeated statement is indented."
        )
        return code, explanation

    # Display
    if "display" in lower or "print" in lower:
        code = 'print("Hello")'
        explanation = "• DISPLAY becomes Python's print() function."
        return code, explanation

    return (
        "# PyGuide could not recognise this pseudocode pattern yet.\n"
        "# Try using words such as START, input, add, display, if, else, or repeat.",
        "This prototype currently supports a few common pseudocode patterns.",
    )



def explain_code(code):
    """Create a beginner-friendly explanation of the code."""
    if not code.strip():
        return "There is no code in the editor yet. Paste some Python code and ask me again."

    try:
        tree = ast.parse(code)
    except SyntaxError as error:
        line = getattr(error, "lineno", "?")
        return (
            f"❌ I cannot fully explain the program yet because Python found a syntax "
            f"problem around line {line}.\n\n"
            f"🧸 **In simple words:** {explain_syntax_error(error)}"
        )

    explanations = []

    for node in tree.body:
        if isinstance(node, ast.Assign):
            targets = []
            for target in node.targets:
                if isinstance(target, ast.Name):
                    targets.append(target.id)
            if targets:
                explanations.append(
                    f"• **{', '.join(targets)}** is being created and given a value."
                )

        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Name):
                if node.value.func.id == "print":
                    explanations.append("• `print()` displays information on the screen.")

        elif isinstance(node, ast.If):
            explanations.append(
                "• **if** checks a condition. If the condition is true, its indented code runs."
            )
            if node.orelse:
                explanations.append(
                    "• **else** gives Python another path when the `if` condition is false."
                )

        elif isinstance(node, (ast.For, ast.While)):
            explanations.append(
                "• This is a **loop**, so Python repeats the indented code."
            )

        elif isinstance(node, ast.FunctionDef):
            explanations.append(
                f"• **{node.name}()** is a function. It groups instructions so they can be reused."
            )

        elif isinstance(node, ast.Return):
            explanations.append("• `return` sends a value back from a function.")

        elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            explanations.append("• This line imports tools/modules that the program can use.")

    # Add a simple whole-program description.
    has_input = "input(" in code
    has_print = "print(" in code
    has_if = re.search(r"\bif\b", code) is not None
    has_loop = re.search(r"\b(for|while)\b", code) is not None

    summary_parts = []
    if has_input:
        summary_parts.append("takes input from the user")
    if has_if:
        summary_parts.append("makes a decision with a condition")
    if has_loop:
        summary_parts.append("repeats instructions with a loop")
    if has_print:
        summary_parts.append("shows output on the screen")

    summary = ""
    if summary_parts:
        summary = "🧸 **What your program does:** It " + ", ".join(summary_parts) + ".\n\n"

    if not explanations:
        explanations.append(
            "• The code is syntactically valid, but this prototype does not yet have "
            "a special explanation rule for every Python construct."
        )

    return summary + "\n".join(explanations)


def get_correct_code(code):
    """Return a corrected full program for simple syntax mistakes."""
    if not code.strip():
        return None, None

    try:
        ast.parse(code)
        return code, "Your code already has valid basic Python syntax."
    except SyntaxError as error:
        correction = suggest_syntax_correction(code, error)
        if correction:
            return correction, f"PyGuide corrected the syntax problem near line {error.lineno}."
        return None, (
            f"PyGuide found a syntax problem near line {getattr(error, 'lineno', '?')}, "
            "but this prototype cannot automatically rewrite that particular error yet."
        )


def chat_response(question, code):
    q = question.lower().strip()

    # Explicit code-explanation requests come first.
    if any(phrase in q for phrase in [
        "explain my code",
        "explain this code",
        "explain the code",
        "what does my code do",
        "what does this code do",
        "explain my program",
        "explain this program",
        "how does my code work",
    ]):
        return explain_code(code)

    if any(phrase in q for phrase in [
        "correct my code",
        "fix my code",
        "give me the correct code",
        "show correct code",
        "show me the correct code",
    ]):
        corrected, message = get_correct_code(code)
        if corrected:
            return (
                "🔧 **Correct Code**\n\n"
                f"{message}\n\n"
                "The corrected version is shown below."
            )
        return f"❌ {message}"

    if "indexerror" in q or ("list" in q and ("error" in q or "wrong" in q)):
        return (
            "### 💡 Let's understand it\n\n"
            "`IndexError` means Python tried to access a position in a list "
            "that does not exist. For example, a list with 3 items has indexes "
            "`0`, `1`, and `2`, so asking for index `5` causes this error.\n\n"
            "**What to check:** Look at the index you are using and make sure "
            "it is within the list's valid range.\n\n"
            "💡 **Tip:** Print the list and check how many items it contains."
        )

    if "syntax" in q or "colon" in q:
        return (
            "### 💡 Let's understand it\n\n"
            "A **syntax error** means Python cannot understand the structure of "
            "your code. For example, `if`, `for`, `while`, `def`, and `else` "
            "usually need a `:` at the end because it tells Python that a new "
            "block of code is starting.\n\n"
            "💡 **Tip:** Check the line Python points to and the line immediately "
            "before it, because the actual mistake can sometimes be just above."
        )

    if "nameerror" in q:
        return (
            "### 💡 Let's understand it\n\n"
            "`NameError` usually means Python found a name it does not know. "
            "This often happens when a variable has not been created yet or "
            "its spelling does not match.\n\n"
            "For example, if you create `name` but later write `nmae`, Python "
            "treats them as different names.\n\n"
            "💡 **What to check:** Make sure the variable is defined before you "
            "use it and that its spelling is exactly the same."
        )

    if "indent" in q:
        return (
            "### 💡 Let's understand it\n\n"
            "**Indentation** means the spaces at the beginning of a line. "
            "Python uses indentation to know which instructions belong to the "
            "same block.\n\n"
            "For example, the indented code under an `if` statement runs only "
            "when that condition is true. Consistent indentation, usually "
            "4 spaces, helps Python understand the program's structure."
        )

    if "if" in q or "else" in q:
        return (
            "### 💡 Let's understand it\n\n"
            "`if` lets a program make a decision based on a condition. "
            "If the condition is true, Python runs the indented code under `if`. "
            "If it is false and an `else` exists, Python runs the `else` block.\n\n"
            "For example, `if age >= 18:` checks a condition before deciding "
            "which instructions to run.\n\n"
            "**In short:** condition → choose which block of code runs."
        )

    if "loop" in q or "for" in q or "while" in q:
        return (
            "### 💡 Let's understand it\n\n"
            "A **loop** repeats instructions so you do not have to write the "
            "same code again and again. A `for` loop commonly goes through a "
            "sequence one item at a time. A `while` loop keeps repeating while "
            "its condition is true.\n\n"
            "💡 **Tip:** Think of a loop as a controlled repetition of a block of code."
        )

    if "print" in q:
        return (
            "### 💡 Let's understand it\n\n"
            "`print()` tells Python to display information in the program's "
            "output. For example, `print(\'Hello\')` displays `Hello`.\n\n"
            "It can also display values stored in variables, which makes it "
            "useful for seeing results while your program runs."
        )

    if "input" in q:
        return (
            "### 💡 Let's understand it\n\n"
            "`input()` allows the user to enter information while the program "
            "is running. For example, `name = input(\'Your name: \')` stores "
            "what the user types in `name`.\n\n"
            "One important point: `input()` normally gives the answer as text. "
            "If you need a number, you can use `int(input(...))` to convert it."
        )

    if "what is wrong" in q or "my code" in q or "this code" in q:
        if code.strip():
            try:
                ast.parse(code)
                logic_result = check_logic(code)
                if logic_result["found"]:
                    return (
                        "✅ Your code has valid basic syntax.\n\n"
                        f"🧠 **Possible logic issue:** {logic_result['hint']}\n\n"
                        f"🔧 **Possible fix:** `{logic_result['fix']}`"
                    )
                return (
                    "✅ Your code has valid basic syntax.\n\n"
                    "I did not detect one of the common logic patterns in this prototype. "
                    "Try asking **Explain my code** for a beginner-friendly walkthrough."
                )
            except SyntaxError as error:
                return (
                    f"❌ I found a syntax problem around line {error.lineno}.\n\n"
                    f"🧸 **Simple explanation:** {explain_syntax_error(error)}\n\n"
                    "💡 Start by checking that line and the line immediately before it."
                )

    return (
        "### 💡 Let's figure it out\n\n"
        "Ask me a Python question and I’ll explain the idea in clear, "
        "student-friendly language without skipping the important concept.\n\n"
        "I can help with variables, lists, `if`/`else`, loops, `input()`, "
        "`print()`, syntax errors, runtime errors, and more.\n\n"
        "You can also ask **Explain my code** for a step-by-step walkthrough."
    )

# ============================================================
# Header
# ============================================================
with open("pyguide_logo.png", "rb") as f:
    logo_base64 = base64.b64encode(f.read()).decode()

st.markdown(
    f'''
    <div class="pyguide-title" style="display:flex; align-items:center; gap:15px;">
        <img src="data:image/png;base64,{logo_base64}" width="60">
        <span>PyGuide</span>
    </div>
    ''',
    unsafe_allow_html=True
)

# ============================================================
# Main navigation
# ============================================================
tab1, tab2, tab3 = st.tabs(
    ["🛠️ AI Debugger", "🔄 Pseudocode → Python", "📁 Projects"]
)

# ============================================================
# AI DEBUGGER
# ============================================================
with tab1:
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 💻 Your Python Code")

        code = st.text_area(
            "Code editor",
            value="",
            placeholder="Write or paste your Python code here...",
            height=430,
            label_visibility="collapsed",
            key="code_editor_v2",
        )

    with col2:
        st.markdown("### 🤖 PyGuide Assistant")

        st.info(
            "PyGuide checks your code, gives a hint first, and then helps you understand the problem."
        )

        analyze_col, logic_col, run_col = st.columns(3)

        with analyze_col:
            analyze = st.button(
                "🔍 Analyze",
                use_container_width=True,
                key="analyze_button",
            )

        with logic_col:
            logic = st.button(
                "🧠 Check Logic",
                use_container_width=True,
                key="logic_button",
            )

        with run_col:
            run = st.button(
                "▶️ Run",
                use_container_width=True,
                key="run_button",
            )

        if analyze:
            if not code.strip():
                st.warning("Please enter some Python code first.")
            else:
                try:
                    tree = ast.parse(code)
                    st.success("✅ No basic syntax error found.")

                    if tree.body:
                        logic_result_for_analyze = check_logic(code)
                        if logic_result_for_analyze["found"]:
                            st.warning(f"🧠 {logic_result_for_analyze['title']}")
                            st.markdown(
                                f'<div class="hint-box"><b>💡 Hint:</b> '
                                f'{logic_result_for_analyze["hint"]}</div>',
                                unsafe_allow_html=True,
                            )
                            corrected_analyze = suggest_logic_correction(
                                code, logic_result_for_analyze
                            )
                            st.markdown("### 🔧 Suggested Correct Code")
                            st.code(
                                corrected_analyze or logic_result_for_analyze["fix"],
                                language="python",
                            )
                            st.caption(
                                "You can copy this corrected code or replace the incorrect line."
                            )
                        else:
                            st.markdown(
                                '<div class="info-box">💡 Syntax looks good. '
                                'Now try <b>Check Logic</b> or <b>Run</b>.</div>',
                                unsafe_allow_html=True,
                            )
                except SyntaxError as error:
                    st.error("❌ SyntaxError")

                    line = getattr(error, "lineno", "?")
                    column = getattr(error, "offset", "?")

                    st.markdown(
                        f'<div class="error-box"><b>Problem:</b> {error.msg}<br>'
                        f'<b>Line:</b> {line} &nbsp; <b>Position:</b> {column}</div>',
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        f'<div class="hint-box"><b>💡 Hint:</b> '
                        f'Look carefully at line {line}. '
                        f"Try to find what Python's grammar is expecting.</div>",
                        unsafe_allow_html=True,
                    )

                    st.markdown("### 🧸 Simple explanation")
                    st.write(explain_syntax_error(error))

                    correction = suggest_syntax_correction(code, error)

                    st.markdown("### 🔧 Suggested Correct Code")
                    if correction:
                        st.success("PyGuide found a simple automatic correction.")
                        st.code(correction, language="python")
                        st.caption(
                            "You can copy this corrected code or replace the incorrect line."
                        )
                    else:
                        st.code(code, language="python")
                        st.caption(
                            "PyGuide could not automatically rewrite this specific syntax error yet. "
                            "Use the highlighted line and hint above to make the correction."
                        )

                    with st.expander("Technical error"):
                        st.code(str(error))

        elif logic:
            if not code.strip():
                st.warning("Please enter some Python code first.")
            else:
                result = check_logic(code)

                if result["found"]:
                    st.warning(f"🧠 {result['title']}")

                    st.markdown(
                        f'<div class="hint-box"><b>💡 Hint:</b> '
                        f'{result["hint"]}</div>',
                        unsafe_allow_html=True,
                    )

                    st.markdown("### 🔧 Suggested Correct Code")
                    corrected_logic = suggest_logic_correction(code, result)
                    if corrected_logic:
                        st.code(corrected_logic, language="python")
                        st.caption("Replace the incorrect code with this corrected version if it matches your intended logic.")
                    else:
                        st.code(result["fix"], language="python")

                    st.markdown("### 🧸 Why?")
                    st.write(result["explanation"])
                else:
                    st.success("🧠 No common logic error detected.")
                    st.write(result["explanation"])

        elif run:
            if not code.strip():
                st.warning("Please enter some Python code first.")
            else:
                try:
                    ast.parse(code)
                except SyntaxError as error:
                    st.error(
                        "❌ The program cannot run because it has a syntax error."
                    )
                    st.write(explain_syntax_error(error))
                else:
                    stdout, stderr, returncode = run_python_code(code)

                    if returncode == 0:
                        st.success("✅ Program finished successfully.")

                        if stdout.strip():
                            st.markdown("### 📤 Output")
                            st.code(stdout, language="text")
                        else:
                            st.info("The program ran, but it did not print any output.")

                    else:
                        st.error("❌ Runtime error")

                        error_text = stderr.strip() or stdout.strip()

                        st.markdown(
                            '<div class="hint-box"><b>💡 Hint:</b> '
                            'Read the last part of the error first. '
                            'It usually gives the most useful clue.</div>',
                            unsafe_allow_html=True,
                        )

                        st.markdown("### 🧸 Simple explanation")
                        st.write(explain_runtime_error(error_text))

                        with st.expander("Technical error"):
                            st.code(error_text, language="text")

    st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------------
    # Chatbox
    # ----------------------------
    st.markdown("### 💬 Ask PyGuide")

    question = st.text_input(
        "Ask a question about Python or your code",
        placeholder="Example: Why is my code wrong?",
        key="chat_question_v2",
    )

    if st.button("Send", key="send_chat"):
        if question.strip():
            answer = chat_response(question, code)

            st.markdown(
                '<div class="info-box">',
                unsafe_allow_html=True,
            )
            st.markdown(answer)
            st.markdown("</div>", unsafe_allow_html=True)

            # Add a flowchart only when it helps explain the concept.
            q_lower = question.lower()

            if (
                ("if" in q_lower and "else" in q_lower)
                or "conditional" in q_lower
                or "condition" in q_lower
            ):
                st.markdown("### 🖼️ Visual Explanation")
                st.markdown(
                    """
```text
              START
                ↓
        Check the condition
           ↙          ↘
        TRUE          FALSE
          ↓              ↓
      IF block        ELSE block
           ↘          ↙
                ↓
               END
```
"""
                )

            elif (
                "loop" in q_lower
                or "for loop" in q_lower
                or "while loop" in q_lower
            ):
                st.markdown("### 🖼️ Visual Explanation")
                st.markdown(
                    """
```text
              START
                ↓
        Check loop condition
           ↙          ↘
        TRUE          FALSE
          ↓              ↓
      Run code          END
          ↓
      Repeat/check
          │
          └──────────────→
```
"""
                )

            if any(phrase in question.lower() for phrase in [
                "correct my code",
                "fix my code",
                "give me the correct code",
                "show correct code",
                "show me the correct code",
            ]):
                corrected, message = get_correct_code(code)
                if corrected and corrected != code:
                    st.markdown("### 🔧 Suggested Correct Code")
                    st.code(corrected, language="python")
                    st.caption("Copy this version into the editor if you want to use the correction.")
        else:
            st.warning("Type a question first.")

# ============================================================
# PSEUDOCODE → PYTHON
# ============================================================
with tab2:
    st.markdown("## 🔄 Convert Pseudocode to Python")

    st.write(
        "Write your logic in simple pseudocode and PyGuide will convert "
        "supported patterns into Python."
    )

    pseudocode = st.text_area(
        "Pseudocode",
        height=280,
        placeholder="""Write your pseudocode...""",
        key="pseudocode_input_v2",
    )

    if st.button(
        "✨ Convert to Python",
        use_container_width=True,
        key="convert_button",
    ):
        if not pseudocode.strip():
            st.warning("Please enter pseudocode first.")
        else:
            pseudo_error = check_pseudocode(pseudocode)
            if pseudo_error:
                st.error("❌ Pseudocode Error")
                st.write(pseudo_error["message"])
                st.markdown(
                    f'<div class="hint-box"><b>💡 Hint:</b> {pseudo_error["hint"]}</div>',
                    unsafe_allow_html=True,
                )
            else:
                python_code, explanation = convert_pseudocode(pseudocode)

                st.markdown("### 🐍 Python Code")
                st.code(python_code, language="python")

                st.markdown("### 🧸 How PyGuide mapped it")
                st.write(explanation)

# ============================================================
# PROJECTS
# ============================================================
with tab3:
    st.markdown("## 📁 Projects")

    st.info(
        "Project saving is planned for the next version. "
        "For the now, the main focus is debugging and pseudocode conversion."
    )

    st.markdown("### 🚀 PyGuide prototype includes")
    st.write("• Python syntax checking")
    st.write("• Beginner-friendly hints")
    st.write("• Suggested syntax corrections")
    st.write("• Runtime error explanations")
    st.write("• Basic logic-error detection")
    st.write("• Pseudocode → Python conversion")
    st.write("• Beginner-friendly coding chat")

st.markdown("---")
st.caption("PyGuide v2 • Free hackathon prototype • Built with Python + Streamlit")

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; font-size:14px;">
        <b>Team PyGuide</b><br><br>
        P Aishani Vardhan · Founder & Team Lead<br>
        Sannidhi Shetty · Co-Creator & Pitch Lead<br>
        B. Naga Harshitha · Developer<br>
        N. Harshitha · Developer
    </div>
    """,
    unsafe_allow_html=True
)