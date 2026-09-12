import streamlit as st
import ast
import subprocess
import sys
import re
import base64
import builtins
import difflib

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
# Styling — ORIGINAL DESIGN
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
        0% { transform: translate3d(0, -10vh, 0) rotate(0deg); }
        25% { transform: translate3d(18px, 28vh, 0) rotate(80deg); }
        50% { transform: translate3d(-15px, 55vh, 0) rotate(180deg); }
        75% { transform: translate3d(20px, 82vh, 0) rotate(270deg); }
        100% { transform: translate3d(-10px, 110vh, 0) rotate(360deg); }
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

    .suggestion-box {
        background: #102957;
        border: 2px solid #b7ff26;
        border-radius: 12px;
        padding: 14px;
        margin-top: 14px;
    }

    .suggestion-title {
        color: #b7ff26;
        font-weight: 800;
        font-family: Consolas, "Courier New", monospace;
        font-size: 16px;
    }

    .suggestion-subtitle {
        color: #dceeff;
        margin-top: 5px;
        font-size: 14px;
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

    textarea {
        font-family: Consolas, "Courier New", monospace !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Falling clovers — ORIGINAL
# ============================================================

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

# ============================================================
# Python execution
# ============================================================

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


# ============================================================
# Syntax explanation
# ============================================================

def explain_syntax_error(error):
    message = str(getattr(error, "msg", "")).lower()

    if "'(' was never closed" in message or "was never closed" in message:
        return (
            "A bracket, parenthesis or curly brace was opened but Python "
            "could not find its closing partner."
        )

    if "expected ':'" in message:
        return (
            "Python expected a colon (:). Statements such as if, elif, else, "
            "for, while, def, class, try and with normally need a colon at the end."
        )

    if "expected an indented block" in message:
        return (
            "Python found the start of a block, but the code inside that "
            "block is missing or is not indented."
        )

    if "unexpected indent" in message:
        return (
            "This line has more indentation than Python expects. "
            "Check the spaces at the beginning of the line."
        )

    if "unindent does not match" in message:
        return (
            "The indentation does not match the surrounding block. "
            "Use consistent indentation, normally 4 spaces."
        )

    if "unterminated string" in message or "eol while scanning string" in message:
        return (
            "A string was started with a quote, but Python could not find "
            "the matching closing quote."
        )

    if "invalid syntax" in message:
        return (
            "Python could not understand the structure of this line. "
            "Check brackets, quotes, commas, operators and colons."
        )

    return (
        "Python found a syntax problem. Check the highlighted line and "
        "the line immediately before it."
    )


# ============================================================
# Runtime explanation
# ============================================================

def explain_runtime_error(error_text):
    text = (error_text or "").lower()

    if "nameerror" in text:
        return (
            "Python cannot find the variable, function or name you used. "
            "Make sure it is defined before use and check its spelling."
        )

    if "typeerror" in text:
        return (
            "Python received a value of the wrong type. For example, "
            "text and a number cannot always be combined directly."
        )

    if "valueerror" in text:
        return (
            "Python received the right kind of object, but the value itself "
            "is not acceptable for this operation."
        )

    if "indexerror" in text:
        return (
            "You tried to access a list or sequence position that does not "
            "exist. Check the valid index range."
        )

    if "keyerror" in text:
        return (
            "You tried to access a dictionary key that does not exist. "
            "Check the key or use .get()."
        )

    if "attributeerror" in text:
        return (
            "The object does not have the attribute or method you tried to "
            "use. Check the object's type and spelling."
        )

    if "zerodivisionerror" in text:
        return (
            "A number is being divided by zero. Check the denominator "
            "before performing the division."
        )

    if "modulenotfounderror" in text:
        return (
            "Python could not find the module you tried to import. "
            "Check the module name and installation."
        )

    if "importerror" in text:
        return (
            "Python found the module, but it could not import the requested item."
        )

    if "filenotfounderror" in text:
        return (
            "Python tried to open a file that does not exist at the specified path."
        )

    if "recursionerror" in text:
        return (
            "A function kept calling itself too deeply. Check its stopping condition."
        )

    if "indentationerror" in text:
        return (
            "Python found an indentation problem. Make sure lines in the "
            "same block use consistent indentation."
        )

    return (
        "Your program encountered a runtime error. Read the final line of "
        "the error first; it usually tells you what went wrong."
    )


# ============================================================
# Undefined-name analysis
# ============================================================

PYTHON_BUILTINS = set(dir(builtins)) | {
    "True", "False", "None", "NotImplemented", "Ellipsis"
}


def _bound_names_in_target(target):
    names = set()
    if isinstance(target, ast.Name):
        names.add(target.id)
    elif isinstance(target, (ast.Tuple, ast.List)):
        for elt in target.elts:
            names.update(_bound_names_in_target(elt))
    elif isinstance(target, ast.Starred):
        names.update(_bound_names_in_target(target.value))
    return names


def collect_global_definitions(tree):
    """Names that exist in the program/module namespace."""
    defined = set()

    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                defined.update(_bound_names_in_target(target))
        elif isinstance(node, ast.AnnAssign):
            defined.update(_bound_names_in_target(node.target))
        elif isinstance(node, ast.AugAssign):
            defined.update(_bound_names_in_target(node.target))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            defined.add(node.name)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                defined.add(alias.asname or alias.name.split(".")[0])
        elif isinstance(node, ast.For):
            defined.update(_bound_names_in_target(node.target))
        elif isinstance(node, ast.With):
            for item in node.items:
                if item.optional_vars:
                    defined.update(_bound_names_in_target(item.optional_vars))

    return defined


def find_undefined_names(code):
    """Find likely NameError variables without flagging Python builtins."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return []

    module_defined = collect_global_definitions(tree)
    findings = []

    # Make a conservative visitor. This focuses on names referenced at module
    # level, which catches the judge-demo case print(y) without pretending
    # static analysis can prove every dynamic Python program.
    class Analyzer(ast.NodeVisitor):
        def __init__(self, outer_defined):
            self.scope_stack = [set(outer_defined)]
            self.in_function = 0
            self.local_names_stack = []

        def current_defined(self):
            result = set()
            for scope in self.scope_stack:
                result.update(scope)
            return result

        def visit_Name(self, node):
            if isinstance(node.ctx, ast.Load):
                name = node.id
                if (
                    name not in self.current_defined()
                    and name not in PYTHON_BUILTINS
                ):
                    findings.append((name, getattr(node, "lineno", None)))
            elif isinstance(node.ctx, ast.Store):
                self.scope_stack[-1].add(node.id)

        def visit_Import(self, node):
            for alias in node.names:
                self.scope_stack[-1].add(alias.asname or alias.name.split(".")[0])

        def visit_ImportFrom(self, node):
            for alias in node.names:
                self.scope_stack[-1].add(alias.asname or alias.name)

        def visit_FunctionDef(self, node):
            # Function name is already visible in current scope.
            self.scope_stack[-1].add(node.name)

            local_defs = set()
            for arg in node.args.posonlyargs:
                local_defs.add(arg.arg)
            for arg in node.args.args:
                local_defs.add(arg.arg)
            for arg in node.args.kwonlyargs:
                local_defs.add(arg.arg)
            if node.args.vararg:
                local_defs.add(node.args.vararg.arg)
            if node.args.kwarg:
                local_defs.add(node.args.kwarg.arg)

            # Defaults are evaluated in outer scope.
            for default in node.args.defaults:
                self.visit(default)
            for default in node.args.kw_defaults:
                if default:
                    self.visit(default)

            self.scope_stack.append(local_defs)
            for child in node.body:
                self.visit(child)
            self.scope_stack.pop()

        visit_AsyncFunctionDef = visit_FunctionDef

        def visit_ClassDef(self, node):
            self.scope_stack[-1].add(node.name)
            for base in node.bases:
                self.visit(base)
            for keyword in node.keywords:
                self.visit(keyword.value)
            self.scope_stack.append(set(module_defined))
            for child in node.body:
                self.visit(child)
            self.scope_stack.pop()

    Analyzer(module_defined).visit(tree)

    unique = []
    seen = set()
    for name, line in findings:
        if name not in seen:
            seen.add(name)
            unique.append((name, line))

    return unique


def nearest_defined_name(code, missing):
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return None

    defined = sorted(collect_global_definitions(tree))
    matches = difflib.get_close_matches(missing, defined, n=1, cutoff=0.55)
    return matches[0] if matches else None


def replace_name_safely(code, wrong, right):
    candidate = re.sub(rf"\b{re.escape(wrong)}\b", right, code)
    try:
        ast.parse(candidate)
        return candidate
    except SyntaxError:
        return None


# ============================================================
# Syntax correction / suggestion box
# ============================================================

def auto_close_delimiter(code):
    pairs = {"(": ")", "[": "]", "{": "}"}
    reverse = {v: k for k, v in pairs.items()}
    stack = []
    quote = None
    escaped = False

    for ch in code:
        if escaped:
            escaped = False
            continue
        if ch == "\\":
            escaped = True
            continue
        if quote:
            if ch == quote:
                quote = None
            continue
        if ch in ("'", '"'):
            quote = ch
        elif ch in pairs:
            stack.append(ch)
        elif ch in reverse:
            if stack and stack[-1] == reverse[ch]:
                stack.pop()
            else:
                return None

    if quote or not stack:
        return None

    candidate = code + "".join(pairs[x] for x in reversed(stack))
    try:
        ast.parse(candidate)
        return candidate
    except SyntaxError:
        return None


def add_missing_colons(code):
    lines = []
    changed = False
    pattern = re.compile(
        r"^(\s*)(if|elif|else|for|while|def|class|try|except|finally|with|match|case)\b"
    )

    for line in code.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and pattern.match(line):
            if not stripped.endswith(":"):
                line = line.rstrip() + ":"
                changed = True
        lines.append(line)

    if not changed:
        return None

    candidate = "\n".join(lines)
    try:
        ast.parse(candidate)
        return candidate
    except SyntaxError:
        return None


def fix_common_mistakes(code):
    candidates = []

    fixed = auto_close_delimiter(code)
    if fixed:
        candidates.append(fixed)

    fixed = add_missing_colons(code)
    if fixed:
        candidates.append(fixed)

    # t(...) -> input(...) beginner typo
    fixed = re.sub(
        r"(^|\n)(\s*[A-Za-z_]\w*\s*=\s*)t(\s*\()",
        r"\1\2input\3",
        code,
    )
    if fixed != code:
        try:
            ast.parse(fixed)
            candidates.append(fixed)
        except SyntaxError:
            pass

    # Combined fixes
    working = code
    for _ in range(3):
        new = add_missing_colons(working) or working
        new = auto_close_delimiter(new) or new
        if new == working:
            break
        working = new

    if working != code:
        try:
            ast.parse(working)
            candidates.append(working)
        except SyntaxError:
            pass

    for candidate in candidates:
        try:
            ast.parse(candidate)
            if candidate != code:
                return candidate
        except SyntaxError:
            pass

    return None


# ============================================================
# Logic checker
# ============================================================


# Backward-compatible name used by the UI
suggest_syntax_correction = fix_common_mistakes


def check_logic(code):
    results = []

    lines = code.splitlines()

    for i, line in enumerate(lines, 1):
        if re.search(r"\bif\s+\w+\s*=\s*[^=]", line):
            results.append({
                "title": "Possible condition error",
                "message": (
                    "A single = assigns a value. If you want to compare values "
                    "inside an if statement, you normally need ==."
                ),
                "line": i,
            })

        if re.search(r"\btotal\s*=\s*price\s*\*\s*quantity\b", line):
            results.append({
                "title": "Possible accumulation error",
                "message": (
                    "If this is inside a loop, = replaces the previous total. "
                    "You may need += to keep adding each item."
                ),
                "line": i,
            })

    if re.search(r"\baverage\s*=", code) and not re.search(r"\btotal\s*/\s*count\b", code):
        results.append({
            "title": "Possible average calculation issue",
            "message": "An average normally needs the total divided by the number of values.",
            "line": None,
        })

    return results


def suggest_logic_correction(code, results):
    lines = code.splitlines()

    for result in results:
        line_no = result.get("line")
        if line_no and 1 <= line_no <= len(lines):
            line = lines[line_no - 1]

            if "condition" in result["title"].lower():
                lines[line_no - 1] = re.sub(
                    r"(\bif\s+\w+)\s*=\s*",
                    r"\1 == ",
                    line,
                )

            elif "accumulation" in result["title"].lower():
                indent = line[:len(line) - len(line.lstrip())]
                lines[line_no - 1] = indent + "total += price * quantity"

    if any("average" in x["title"].lower() for x in results):
        for i, line in enumerate(lines):
            if re.match(r"^\s*average\s*=", line):
                indent = line[:len(line) - len(line.lstrip())]
                lines[i] = indent + "average = total / count"
                break

    candidate = "\n".join(lines)
    try:
        ast.parse(candidate)
        return candidate
    except SyntaxError:
        return None


# ============================================================
# Pseudocode validation
# ============================================================

def normalize_pseudocode(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not text:
        return ""

    lines = [x.strip() for x in text.splitlines() if x.strip()]

    # Recover common pasted one-line pseudocode.
    if len(lines) == 1:
        s = lines[0]
        keywords = [
            "END FUNCTION", "END WHILE", "END FOR", "END IF", "END LOOP",
            "ELSE IF", "START", "END", "ELSE", "IF", "FOR", "WHILE",
            "REPEAT", "FUNCTION", "RETURN", "BREAK", "CONTINUE", "PASS",
            "INPUT", "READ", "OUTPUT", "DISPLAY", "PRINT", "SET", "STORE",
            "ASSIGN", "ADD", "SUBTRACT", "MULTIPLY", "DIVIDE",
        ]
        for keyword in sorted(keywords, key=len, reverse=True):
            s = re.sub(
                rf"\s+(?={re.escape(keyword)}\b)",
                "\n",
                s,
                flags=re.IGNORECASE,
            )
        lines = [x.strip() for x in s.splitlines() if x.strip()]

    return "\n".join(lines)


def check_pseudocode(text):
    normalized = normalize_pseudocode(text)
    lines = [x.strip() for x in normalized.splitlines() if x.strip()]

    if not lines:
        return {"error": "Please enter pseudocode first.", "normalized": normalized}

    if lines[0].upper() != "START":
        return {
            "error": "Pseudocode must start with START.",
            "hint": "Put START as the first non-empty line.",
            "normalized": normalized,
        }

    if lines[-1].upper() != "END":
        return {
            "error": "Your pseudocode is missing the final END.",
            "hint": f"The last instruction is: {lines[-1]}",
            "normalized": normalized,
        }

    stack = []

    for i, line in enumerate(lines[1:-1], start=2):
        u = line.upper().strip()

        if u == "START":
            return {"error": f"START is in the wrong position on line {i}.", "normalized": normalized}

        if u == "END":
            return {"error": f"END appears too early on line {i}.", "normalized": normalized}

        if u.startswith("IF "):
            condition = line[3:].strip()
            if not condition or condition == ":":
                return {"error": f"IF is incomplete on line {i}.", "hint": "Example: IF age >= 18", "normalized": normalized}
            if line.rstrip().endswith(":"):
                return {"error": f"Do not use a Python colon on pseudocode line {i}.", "hint": "Write IF age >= 18, not IF age >= 18:", "normalized": normalized}
            stack.append(("IF", i))
            continue

        if u.startswith("ELSE IF "):
            if not stack or stack[-1][0] != "IF":
                return {"error": f"ELSE IF on line {i} has no matching IF.", "normalized": normalized}
            continue

        if u == "ELSE":
            if not stack or stack[-1][0] != "IF":
                return {"error": f"ELSE on line {i} has no matching IF.", "normalized": normalized}
            continue

        if u.startswith("FOR "):
            if u == "FOR":
                return {"error": f"FOR is incomplete on line {i}.", "normalized": normalized}
            stack.append(("FOR", i))
            continue

        if u.startswith("WHILE "):
            if len(u) <= 6:
                return {"error": f"WHILE is incomplete on line {i}.", "normalized": normalized}
            stack.append(("WHILE", i))
            continue

        if u.startswith("REPEAT"):
            if not re.match(r"REPEAT\s+.+\s+TIMES?$", u):
                return {
                    "error": f"REPEAT is incomplete on line {i}.",
                    "hint": "Example: REPEAT 5 TIMES",
                    "normalized": normalized,
                }
            stack.append(("REPEAT", i))
            continue

        if u.startswith("FUNCTION "):
            if not re.match(r"FUNCTION\s+[A-Za-z_]\w*\s*\(.*\)$", line, re.I):
                return {
                    "error": f"FUNCTION is incomplete on line {i}.",
                    "hint": "Example: FUNCTION add(a, b)",
                    "normalized": normalized,
                }
            stack.append(("FUNCTION", i))
            continue

        if u in {"END IF", "ENDIF"}:
            if not stack or stack[-1][0] != "IF":
                return {"error": f"END IF on line {i} does not match the current block.", "normalized": normalized}
            stack.pop()
            continue

        if u in {"END FOR", "ENDFOR"}:
            if not stack or stack[-1][0] != "FOR":
                return {"error": f"END FOR on line {i} does not match the current block.", "normalized": normalized}
            stack.pop()
            continue

        if u in {"END WHILE", "ENDWHILE"}:
            if not stack or stack[-1][0] != "WHILE":
                return {"error": f"END WHILE on line {i} does not match the current block.", "normalized": normalized}
            stack.pop()
            continue

        if u in {"END REPEAT", "ENDREPEAT", "END LOOP", "ENDLOOP"}:
            if not stack or stack[-1][0] not in {"REPEAT"}:
                return {"error": f"End marker on line {i} does not match the current block.", "normalized": normalized}
            stack.pop()
            continue

        if u in {"END FUNCTION", "ENDFUNCTION"}:
            if not stack or stack[-1][0] != "FUNCTION":
                return {"error": f"END FUNCTION on line {i} does not match the current block.", "normalized": normalized}
            stack.pop()
            continue

        # Reject empty commands.
        for key in ["INPUT", "READ", "TAKE", "OUTPUT", "DISPLAY", "PRINT", "SET", "STORE", "ASSIGN", "ADD", "SUBTRACT", "MULTIPLY", "DIVIDE", "RETURN"]:
            if u == key:
                return {
                    "error": f"Incomplete {key} statement on line {i}.",
                    "hint": "Add the value or operation required by the instruction.",
                    "normalized": normalized,
                }

    if stack:
        block, start_line = stack[-1]
        expected = {
            "IF": "END IF",
            "FOR": "END FOR",
            "WHILE": "END WHILE",
            "REPEAT": "END REPEAT",
            "FUNCTION": "END FUNCTION",
        }[block]
        return {
            "error": f"{block} started on line {start_line} was not closed.",
            "hint": f"Add {expected} before the final END.",
            "normalized": normalized,
        }

    return {"error": None, "normalized": normalized}


# ============================================================
# Pseudocode converter
# ============================================================

def convert_pseudocode(text):
    normalized = normalize_pseudocode(text)
    lines = [x.strip() for x in normalized.splitlines() if x.strip()]

    output = []
    notes = []
    indent = 0

    for i, original in enumerate(lines, 1):
        u = original.upper().strip()

        if u in {"START", "END"}:
            continue

        # Closers
        if u in {
            "END IF", "ENDIF", "END FOR", "ENDFOR", "END WHILE", "ENDWHILE",
            "END REPEAT", "ENDREPEAT", "END LOOP", "ENDLOOP",
            "END FUNCTION", "ENDFUNCTION",
        }:
            indent = max(0, indent - 1)
            continue

        # ELSE IF
        if u.startswith("ELSE IF "):
            indent = max(0, indent - 1)
            output.append("    " * indent + "elif " + original[8:].strip() + ":")
            indent += 1
            notes.append(f"Line {i}: ELSE IF → elif")
            continue

        # ELSE
        if u == "ELSE":
            indent = max(0, indent - 1)
            output.append("    " * indent + "else:")
            indent += 1
            notes.append(f"Line {i}: ELSE → else")
            continue

        # IF
        if u.startswith("IF "):
            output.append("    " * indent + "if " + original[3:].strip() + ":")
            indent += 1
            notes.append(f"Line {i}: IF → if")
            continue

        # FOR variable FROM start TO end
        m = re.match(r"FOR\s+([A-Za-z_]\w*)\s+FROM\s+(.+?)\s+TO\s+(.+)$", original, re.I)
        if m:
            var, start, end = m.groups()
            output.append("    " * indent + f"for {var} in range({start}, ({end}) + 1):")
            indent += 1
            notes.append(f"Line {i}: FOR FROM TO → range()")
            continue

        # FOR variable IN iterable
        m = re.match(r"FOR\s+([A-Za-z_]\w*)\s+IN\s+(.+)$", original, re.I)
        if m:
            var, seq = m.groups()
            output.append("    " * indent + f"for {var} in {seq}:")
            indent += 1
            notes.append(f"Line {i}: FOR IN → for")
            continue

        # WHILE
        if u.startswith("WHILE "):
            output.append("    " * indent + "while " + original[6:].strip() + ":")
            indent += 1
            notes.append(f"Line {i}: WHILE → while")
            continue

        # REPEAT n TIMES
        m = re.match(r"REPEAT\s+(.+?)\s+TIMES?$", original, re.I)
        if m:
            count = m.group(1).strip()
            output.append("    " * indent + f"for _ in range({count}):")
            indent += 1
            notes.append(f"Line {i}: REPEAT → for/range")
            continue

        # FUNCTION name(args)
        m = re.match(r"FUNCTION\s+([A-Za-z_]\w*)\s*\((.*?)\)$", original, re.I)
        if m:
            name, args = m.groups()
            output.append("    " * indent + f"def {name}({args}):")
            indent += 1
            notes.append(f"Line {i}: FUNCTION → def")
            continue

        # INPUT
        m = re.match(r"(?:INPUT|READ|TAKE)\s+(.+)$", original, re.I)
        if m:
            var = m.group(1).strip()
            if re.fullmatch(r"[A-Za-z_]\w*", var):
                output.append("    " * indent + f"{var} = input()")
            else:
                output.append("    " * indent + f"input({var})")
            notes.append(f"Line {i}: INPUT → input()")
            continue

        # OUTPUT/DISPLAY/PRINT
        m = re.match(r"(?:OUTPUT|DISPLAY|PRINT)\s+(.+)$", original, re.I)
        if m:
            value = m.group(1).strip()
            output.append("    " * indent + f"print({value})")
            notes.append(f"Line {i}: OUTPUT/DISPLAY → print()")
            continue

        # SET / STORE / ASSIGN
        m = re.match(r"(?:SET|STORE|ASSIGN)\s+([A-Za-z_]\w*)\s*=\s*(.+)$", original, re.I)
        if m:
            var, value = m.groups()
            output.append("    " * indent + f"{var} = {value}")
            notes.append(f"Line {i}: SET → assignment")
            continue

        # ADD
        m = re.match(r"ADD\s+(.+?)\s+AND\s+(.+)$", original, re.I)
        if m:
            a, b = m.groups()
            output.append("    " * indent + f"result = {a} + {b}")
            notes.append(f"Line {i}: ADD → +")
            continue

        # SUBTRACT a FROM b
        m = re.match(r"SUBTRACT\s+(.+?)\s+FROM\s+(.+)$", original, re.I)
        if m:
            a, b = m.groups()
            output.append("    " * indent + f"result = {b} - {a}")
            notes.append(f"Line {i}: SUBTRACT FROM → -")
            continue

        # MULTIPLY
        m = re.match(r"MULTIPLY\s+(.+?)\s+(?:BY|AND)\s+(.+)$", original, re.I)
        if m:
            a, b = m.groups()
            output.append("    " * indent + f"result = {a} * {b}")
            notes.append(f"Line {i}: MULTIPLY → *")
            continue

        # DIVIDE
        m = re.match(r"DIVIDE\s+(.+?)\s+BY\s+(.+)$", original, re.I)
        if m:
            a, b = m.groups()
            output.append("    " * indent + f"result = {a} / {b}")
            notes.append(f"Line {i}: DIVIDE BY → /")
            continue

        # RETURN/BREAK/CONTINUE/PASS
        if re.match(r"RETURN\s+.+", original, re.I):
            output.append("    " * indent + "return " + original[6:].strip())
            notes.append(f"Line {i}: RETURN → return")
            continue

        if u == "BREAK":
            output.append("    " * indent + "break")
            continue

        if u == "CONTINUE":
            output.append("    " * indent + "continue")
            continue

        if u == "PASS":
            output.append("    " * indent + "pass")
            continue

        # IMPORT
        if u.startswith("IMPORT "):
            output.append("    " * indent + original[7:].strip())
            notes.append(f"Line {i}: IMPORT → import")
            continue

        # Direct Python escape
        if u.startswith("PYTHON:"):
            output.append("    " * indent + original.split(":", 1)[1].strip())
            notes.append(f"Line {i}: PYTHON → direct Python")
            continue

        # Comments
        if original.startswith("#"):
            output.append("    " * indent + original)
            continue

        # Unknown instruction — deliberately mark it instead of silently saying converted.
        output.append("    " * indent + f"# TODO: review pseudocode: {original}")
        notes.append(f"Line {i}: unrecognised instruction — review required")

    generated = "\n".join(output).strip()

    if not generated:
        return "", "No convertible instructions were found."

    try:
        ast.parse(generated)
    except SyntaxError as error:
        return (
            generated,
            "Generated Python still needs review near line "
            f"{getattr(error, 'lineno', '?')}."
        )

    return generated, "\n".join(notes)


# ============================================================
# Code explanation
# ============================================================

def explain_code(code):
    if not code.strip():
        return "There is no code in the editor yet. Paste some Python code first."

    try:
        tree = ast.parse(code)
    except SyntaxError as error:
        return (
            f"Python found a syntax problem around line {getattr(error, 'lineno', '?')}.\n\n"
            f"{explain_syntax_error(error)}"
        )

    explanations = []

    undefined = find_undefined_names(code)
    if undefined:
        explanations.append(
            "• Possible undefined name(s): " + ", ".join(f"`{n}`" for n, _ in undefined)
        )

    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    explanations.append(f"• `{target.id}` is created and assigned a value.")

        elif isinstance(node, ast.If):
            explanations.append("• `if` checks a condition and chooses which block should run.")
            if node.orelse:
                explanations.append("• `else`/another branch provides an alternate path.")

        elif isinstance(node, (ast.For, ast.While)):
            explanations.append("• This is a loop, so Python repeats a block of instructions.")

        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            explanations.append(f"• `{node.name}()` is a function that groups reusable instructions.")

        elif isinstance(node, ast.Return):
            explanations.append("• `return` sends a value back from a function.")

        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            explanations.append("• This imports a module or tool the program can use.")

        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Name) and node.value.func.id == "print":
                explanations.append("• `print()` displays information in the output.")
            elif isinstance(node.value.func, ast.Name) and node.value.func.id == "input":
                explanations.append("• `input()` gets text from the user.")

    if not explanations:
        explanations.append("• The code is syntactically valid, but this prototype does not have a special explanation for every Python construct.")

    return "\n".join(explanations)


# ============================================================
# Chat
# ============================================================

def chat_response(question, code):
    q = question.lower().strip()

    if not q:
        return "Type a question first."

    if any(x in q for x in ["explain my code", "explain this code", "what does my code do", "explain my program"]):
        return explain_code(code)

    if any(x in q for x in ["correct my code", "fix my code", "give me the correct code", "show correct code"]):
        try:
            ast.parse(code)
        except SyntaxError as error:
            correction = suggest_syntax_correction(code)
            if correction:
                return f"### Correct Code\n\n{correction}"
            return explain_syntax_error(error)

        undefined = find_undefined_names(code)
        if undefined:
            name, line = undefined[0]
            nearest = nearest_defined_name(code, name)
            if nearest:
                candidate = replace_name_safely(code, name, nearest)
                if candidate:
                    return f"`{name}` may be a typo. I found `{nearest}` already defined.\n\n```python\n{candidate}\n```"
            return f"`{name}` is not defined. Define it before using it."

        logic = check_logic(code)
        if logic:
            corrected = suggest_logic_correction(code, logic)
            if corrected:
                return f"{logic[0]['message']}\n\n```python\n{corrected}\n```"
            return logic[0]["message"]

        return "I did not find a problem that this prototype can safely auto-correct."

    if "nameerror" in q or "undefined" in q:
        return "A NameError means Python cannot find the name you used. Make sure the variable or function is defined before it is used."

    if "syntax" in q or "colon" in q:
        return "A syntax error means Python cannot understand the structure of the code. Check brackets, quotes, indentation, commas and colons."

    if "indent" in q:
        return "Indentation tells Python which lines belong to the same block. Use consistent indentation, usually 4 spaces."

    if "loop" in q:
        return "A loop repeats instructions. `for` commonly iterates through a sequence; `while` repeats while a condition is true."

    if "input" in q:
        return "`input()` gets text from the user. Use `int(input())` when you need an integer."

    if "print" in q:
        return "`print()` displays information in the program output."

    return "Ask about Python syntax, runtime errors, variables, lists, conditions, loops, functions, input, output, or your code."


# ============================================================
# Header — ORIGINAL logo, fixed HTML rendering
# ============================================================

try:
    with open("pyguide_logo.png", "rb") as f:
        logo_base64 = base64.b64encode(f.read()).decode()

    header_html = f'''
<div class="pyguide-title" style="display:flex; align-items:center; gap:15px;">
    <img src="data:image/png;base64,{logo_base64}" width="60">
    <span>PyGuide</span>
</div>
'''

    st.markdown(header_html, unsafe_allow_html=True)

except FileNotFoundError:
    st.markdown(
        '<div class="pyguide-title">PyGuide</div>',
        unsafe_allow_html=True,
    )

st.markdown(
    '<div class="pyguide-subtitle">Interactive Debugging Assistant</div>',
    unsafe_allow_html=True,
)


# ============================================================
# Main navigation — ORIGINAL TABS
# ============================================================

tab1, tab2, tab3 = st.tabs(
    [" AI Debugger", " Pseudocode → Python", " Projects"]
)


# ============================================================
# AI DEBUGGER
# ============================================================

with tab1:
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Your Python Code")

        code = st.text_area(
            "Code editor",
            value="",
            placeholder="Try: print(y)",
            height=430,
            label_visibility="collapsed",
            key="code_editor_v3",
        )

    with col2:
        st.markdown("### PyGuide Assistant")

        st.info(
            "PyGuide checks syntax, possible undefined names, runtime errors, "
            "and common logic mistakes."
        )

        analyze_col, logic_col, run_col = st.columns(3)

        with analyze_col:
            analyze = st.button(
                " Analyze",
                use_container_width=True,
                key="analyze_button_v3",
            )

        with logic_col:
            logic = st.button(
                " Check Logic",
                use_container_width=True,
                key="logic_button_v3",
            )

        with run_col:
            run = st.button(
                "▶️ Run",
                use_container_width=True,
                key="run_button_v3",
            )

        # ====================================================
        # ANALYZE
        # ====================================================
        if analyze:
            if not code.strip():
                st.warning("Please enter some Python code first.")
            else:
                try:
                    ast.parse(code)
                except SyntaxError as error:
                    st.error(" Syntax Error")

                    line = getattr(error, "lineno", "?")
                    column = getattr(error, "offset", "?")

                    st.markdown(
                        f'''<div class="error-box">
                        <b>Problem:</b> {error.msg}<br>
                        <b>Line:</b> {line} &nbsp;
                        <b>Position:</b> {column}
                        </div>''',
                        unsafe_allow_html=True,
                    )

                    st.markdown("###  Simple Explanation")
                    st.write(explain_syntax_error(error))

                    correction = suggest_syntax_correction(code)

                    if correction:
                        st.markdown(
                            '''<div class="suggestion-box">
                            <div class="suggestion-title">✓ SUGGESTION BOX — FULL FIX PREVIEW</div>
                            <div class="suggestion-subtitle">Only a syntactically valid corrected program is shown here.</div>
                            </div>''',
                            unsafe_allow_html=True,
                        )
                        st.code(correction, language="python")
                    else:
                        st.info(
                            "PyGuide found the error, but it cannot safely generate a complete automatic correction for this particular mistake."
                        )

                else:
                    undefined = find_undefined_names(code)

                    if undefined:
                        name, line = undefined[0]
                        st.error(" Undefined Name Detected")

                        st.markdown(
                            f'''<div class="error-box">
                            <b>Problem:</b> <code>{name}</code> is used but has not been defined.<br>
                            <b>Line:</b> {line or "unknown"}
                            </div>''',
                            unsafe_allow_html=True,
                        )

                        st.markdown("###  Simple Explanation")
                        st.write(
                            f"Python does not know what `{name}` means yet. "
                            "Define it before using it, or check whether you meant another variable name."
                        )

                        nearest = nearest_defined_name(code, name)

                        if nearest:
                            candidate = replace_name_safely(code, name, nearest)
                        else:
                            candidate = None

                        st.markdown(
                            '''<div class="suggestion-box">
                            <div class="suggestion-title">✓ SUGGESTION BOX — FULL FIX PREVIEW</div>
                            <div class="suggestion-subtitle">PyGuide only suggests a name replacement when it finds a likely existing variable.</div>
                            </div>''',
                            unsafe_allow_html=True,
                        )

                        if candidate:
                            st.code(candidate, language="python")
                            st.caption(f"Suggested correction: `{name}` → `{nearest}`")
                        else:
                            st.info(
                                f"No safe replacement was found for `{name}`. "
                                f"Define `{name}` before using it."
                            )

                    else:
                        logic_results = check_logic(code)

                        if logic_results:
                            st.warning(f" {logic_results[0]['title']}")

                            st.markdown(
                                f'''<div class="hint-box"><b>Hint:</b> {logic_results[0]["message"]}</div>''',
                                unsafe_allow_html=True,
                            )

                            corrected = suggest_logic_correction(
                                code,
                                logic_results,
                            )

                            if corrected:
                                st.markdown(
                                    '''<div class="suggestion-box">
                                    <div class="suggestion-title">✓ SUGGESTION BOX — FULL FIX PREVIEW</div>
                                    <div class="suggestion-subtitle">PyGuide corrected the detected logic pattern.</div>
                                    </div>''',
                                    unsafe_allow_html=True,
                                )
                                st.code(corrected, language="python")

                        else:
                            st.success(" No basic syntax or undefined-name error found.")
                            st.markdown(
                                '''<div class="success-box">
                                Your code passed syntax and undefined-name checks.
                                </div>''',
                                unsafe_allow_html=True,
                            )

        # ====================================================
        # CHECK LOGIC
        # ====================================================
        elif logic:
            if not code.strip():
                st.warning("Please enter some Python code first.")
            else:
                try:
                    ast.parse(code)
                except SyntaxError as error:
                    st.error(" Fix the syntax error first.")
                    st.write(explain_syntax_error(error))
                else:
                    undefined = find_undefined_names(code)

                    if undefined:
                        st.error(" Undefined name(s) found")
                        for name, line in undefined:
                            st.write(
                                f"`{name}` on line {line or '?'} is used before PyGuide can find a definition."
                            )
                    else:
                        results = check_logic(code)

                        if results:
                            for result in results:
                                st.warning(f" {result['title']}")
                                st.write(result["message"])

                            corrected = suggest_logic_correction(code, results)

                            if corrected:
                                st.markdown(
                                    '''<div class="suggestion-box">
                                    <div class="suggestion-title">✓ SUGGESTION BOX — FULL FIX PREVIEW</div>
                                    </div>''',
                                    unsafe_allow_html=True,
                                )
                                st.code(corrected, language="python")
                        else:
                            st.success(" No common logic error detected.")
                            st.write("Try Run to test the program with Python itself.")
                            
        # ====================================================
        # RUN
        # ====================================================
        elif run:
            if not code.strip():
                st.warning("Please enter some Python code first.")
            else:
                try:
                    ast.parse(code)
                except SyntaxError as error:
                    st.error(" The program cannot run because it contains a syntax error.")
                    st.write(explain_syntax_error(error))
                else:
                    undefined = find_undefined_names(code)

                    if undefined:
                        st.error(" Cannot run: undefined name(s)")
                        for name, line in undefined:
                            st.write(
                                f"`{name}` is used on line {line or '?'} but is not defined."
                            )
                    elif re.search(r"\binput\s*\(", code):
                        st.info(
                            "This program uses input(). Use Analyze for code checking, "
                            "or run this kind of program in your normal Python environment."
                        )
                    else:
                        stdout, stderr, returncode = run_python_code(code)

                        if returncode == 0:
                            st.success(" Program finished successfully.")
                            if stdout.strip():
                                st.markdown("### Output")
                                st.code(stdout, language="text")
                            else:
                                st.info("The program ran successfully but printed no output.")
                        else:
                            error_text = stderr.strip() or stdout.strip() or "Unknown runtime error."
                            st.error(" Runtime Error")

                            st.markdown(
                                f'''<div class="error-box"><b>Problem:</b><br>{error_text}</div>''',
                                unsafe_allow_html=True,
                            )

                            st.markdown("###  Simple Explanation")
                            st.write(explain_runtime_error(error_text))

                            name_match = re.search(
                                r"name ['\"]([^'\"]+)['\"] is not defined",
                                error_text,
                            )

                            if name_match:
                                missing = name_match.group(1)
                                nearest = nearest_defined_name(code, missing)

                                if nearest:
                                    candidate = replace_name_safely(code, missing, nearest)
                                    if candidate:
                                        st.markdown(
                                            '''<div class="suggestion-box">
                                            <div class="suggestion-title">✓ SUGGESTION BOX — FULL FIX PREVIEW</div>
                                            <div class="suggestion-subtitle">Likely variable spelling correction.</div>
                                            </div>''',
                                            unsafe_allow_html=True,
                                        )
                                        st.code(candidate, language="python")

                            with st.expander("Technical error"):
                                st.code(error_text, language="text")

    st.markdown("</div>", unsafe_allow_html=True)

    # ========================================================
    # Chatbox — ORIGINAL FEATURE
    # ========================================================
    st.markdown("###  Ask PyGuide")

    question = st.text_input(
        "Ask a question about Python or your code",
        placeholder="Example: Why is print(y) wrong?",
        key="chat_question_v3",
    )

    if st.button("Send", key="send_chat_v3"):
        if question.strip():
            answer = chat_response(question, code)

            st.markdown(
                '<div class="info-box">',
                unsafe_allow_html=True,
            )
            st.markdown(answer)
            st.markdown("</div>", unsafe_allow_html=True)

            q_lower = question.lower()

            if (
                ("if" in q_lower and "else" in q_lower)
                or "conditional" in q_lower
                or "condition" in q_lower
            ):
                st.markdown("### Visual Explanation")
                st.markdown(
                    """
```text
START
  ↓
Check condition
  ↙       ↘
TRUE     FALSE
 ↓          ↓
IF block  ELSE block
  ↘       ↙
     ↓
    END
```
                    """
                )

            elif "loop" in q_lower or "for loop" in q_lower or "while loop" in q_lower:
                st.markdown("### Visual Explanation")
                st.markdown(
                    """
```text
START
  ↓
Check loop condition
  ↙       ↘
TRUE     FALSE
 ↓          ↓
Run code   END
 ↓
Repeat
 ↺
```
                    """
                )
        else:
            st.warning("Type a question first.")


# ============================================================
# PSEUDOCODE → PYTHON
# ============================================================

with tab2:
    st.markdown("##  Convert Pseudocode to Python")

    st.write(
        "Write your logic in simple pseudocode. PyGuide validates START, END, "
        "block endings and supported instructions before converting."
    )

    pseudocode = st.text_area(
        "Pseudocode",
        height=280,
        placeholder="""START
INPUT length
INPUT width
SET area = length * width
OUTPUT area
END""",
        key="pseudocode_input_v3",
    )

    if st.button(
        " Convert to Python",
        use_container_width=True,
        key="convert_button_v3",
    ):
        if not pseudocode.strip():
            st.warning("Please enter pseudocode first.")
        else:
            validation = check_pseudocode(pseudocode)

            if validation["error"]:
                st.error(" Pseudocode Error")
                st.write(validation["error"])

                if validation.get("hint"):
                    st.markdown(
                        f'''<div class="hint-box"><b>Hint:</b> {validation["hint"]}</div>''',
                        unsafe_allow_html=True,
                    )
            else:
                normalized = validation["normalized"]

                if normalized != pseudocode.strip():
                    st.caption("PyGuide normalized the pasted pseudocode before checking it.")

                python_code, explanation = convert_pseudocode(normalized)

                st.markdown("###  Python Code")
                st.code(python_code, language="python")

                try:
                    ast.parse(python_code)
                    st.success(" Generated Python passed syntax validation.")
                except SyntaxError:
                    st.warning(" Generated Python still needs review.")

                st.markdown("### How PyGuide mapped it")
                st.write(explanation)


# ============================================================
# PROJECTS — ORIGINAL FEATURE (without team names)
# ============================================================

with tab3:
    st.markdown("##  Projects")

    st.info(
        "Project saving is planned for the next version. "
        "For now, the main focus is debugging and pseudocode conversion."
    )

    st.markdown("### PyGuide prototype includes")
    st.write("• Python syntax checking")
    st.write("• Undefined-name detection")
    st.write("• Beginner-friendly hints")
    st.write("• Suggested syntax corrections")
    st.write("• Runtime error explanations")
    st.write("• Basic logic-error detection")
    st.write("• Pseudocode → Python conversion")
    st.write("• Beginner-friendly coding chat")

st.markdown("---")
st.caption("PyGuide v2 • Free hackathon prototype • Built with Python + Streamlit")
