# Project Structure

## 📁 **Current Organization**

```
workflow-automation/
│
├── README.md                       # Main documentation
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
│
├── src/                           # Core source code
│   ├── __init__.py
│   ├── adaptive_planner.py        # AI workflow planning (GPT-4o)
│   ├── adaptive_executor.py       # Multi-strategy execution engine
│   ├── perception.py              # State detection & visual marks
│   ├── config.py                  # Platform configurations
│   └── utils.py                   # Report generation utilities
│
├── tests/                         # Test scripts
│   ├── __init__.py
│   ├── test_youtube.py            # YouTube workflows (2)
│   ├── test_linear.py             # Linear workflows (3)
│   ├── test_wikipedia.py          # Wikipedia workflows (1)
│   └── main_adaptive.py           # General test runner
│
├── dataset/                       # Generated workflow outputs
│   ├── youtube_search_python/
│   │   ├── README.md              # Step-by-step guide
│   │   ├── step_01.png            # Clean screenshots
│   │   ├── step_01_debug.png      # With element markers
│   │   └── ...
│   ├── linear_create_issue/
│   │   └── ...
│   └── [other workflows]/
│
└── data/                          # Browser data (gitignored)
    └── user_data/                 # Chromium profile (login sessions)
```

---

## 📂 **Folder Descriptions**

### **`src/` - Core System**
The main automation engine.

| File | Purpose | Lines | Key Features |
|------|---------|-------|--------------|
| **`adaptive_planner.py`** | AI workflow planning | 237 | GPT-4o planning, vision feedback, selector discovery |
| **`adaptive_executor.py`** | Execution engine | 333 | Multi-strategy fallbacks, self-healing, verification |
| **`perception.py`** | State detection | 93 | Content hashing, visual mark injection |
| **`config.py`** | App configurations | 98 | Minimal context per platform |
| **`utils.py`** | Utilities | 19 | Markdown report generation |

**Total:** ~780 lines of core logic

---

### **`tests/` - Test Suites**
Platform-specific test scripts.

| File | Platform | Workflows | Features |
|------|----------|-----------|----------|
| **`test_youtube.py`** | YouTube | 2 | Search, navigation |
| **`test_linear.py`** | Linear | 3 | Create issue, filters, navigation |
| **`test_wikipedia.py`** | Wikipedia | 1 | Search |
| **`main_adaptive.py`** | Generic | - | Flexible test runner |

**Total:** 5 distinct workflows across 2-3 platforms

---

### **`dataset/` - Generated Outputs**
All workflow captures and documentation.

Each workflow run creates:
```
dataset/[platform]_[workflow_name]/
├── README.md              # Complete step-by-step guide
├── step_01.png            # Clean screenshot (user view)
├── step_01_debug.png      # Debug view with element markers
├── step_02.png
├── step_02_debug.png
└── ...
```

**Example:**
- `dataset/youtube_search_python/` - 10 screenshots + README
- `dataset/linear_create_issue/` - 16 screenshots + README

---

### **`data/` - Browser Profiles**
Persistent browser data for login sessions.

```
data/user_data/
├── Default/
│   ├── Cookies              # Session cookies
│   ├── Login Data           # Saved credentials (encrypted)
│   ├── Local Storage/       # App data
│   └── ...
```

**Purpose:** 
- Saves login sessions between runs
- No need to re-authenticate
- Gitignored for security

---

## 🔧 **Key Files**

### **Root Level**

| File | Purpose |
|------|---------|
| `README.md` | Main documentation, setup, usage |
| `requirements.txt` | Python dependencies (playwright, openai, dotenv) |
| `.gitignore` | Excludes dataset/, data/, __pycache__ |
| `LOOM_SCRIPT.md` | Video demonstration script |
| `PROJECT_STRUCTURE.md` | This documentation |

### **Configuration**

| File | What It Stores |
|------|----------------|
| `src/config.py` | Platform contexts (URLs, selectors, notes) |
| `.env` | API keys (not in repo) |

---

## 🎯 **How Files Work Together**

### **Workflow Execution Flow:**

```
1. User runs test:
   tests/test_youtube.py
   
2. Test imports from src/:
   → adaptive_planner.py (plans workflow)
   → adaptive_executor.py (executes steps)
   → perception.py (detects state changes)
   → utils.py (generates report)
   
3. Executor uses:
   → config.py (gets platform selectors)
   → data/user_data/ (browser profile)
   
4. Outputs saved to:
   → dataset/youtube_search_python/
      - README.md
      - step_*.png
```

---

## 🚀 **Running the System**

### **From Project Root:**
```bash
# YouTube test
python tests/test_youtube.py

# Linear test
python tests/test_linear.py

# View outputs
open dataset/
```

### **From Tests Directory:**
```bash
cd tests
python test_youtube.py
# Outputs still go to ../dataset/
```

---

## 📊 **File Statistics**

| Category | Files | Lines of Code |
|----------|-------|---------------|
| **Core (`src/`)** | 5 | ~780 |
| **Tests (`tests/`)** | 4 | ~300 |
| **Docs** | 2 | ~600 |
| **Config** | 1 | ~100 |
| **Total Code** | 10 | ~1,180 |

---

## 🗂️ **What's Gitignored**

From `.gitignore`:
```
# Python
__pycache__/
*.pyc

# Environment
.env

# Project Data
dataset/          # Generated outputs (too large)
data/user_data/   # Login sessions (sensitive)

# OS
.DS_Store
```

---

## 📦 **For Submission**

### **Include:**
- ✅ `src/` - All core code
- ✅ `tests/` - Test scripts
- ✅ `README.md` - Documentation
- ✅ `requirements.txt` - Dependencies
- ✅ `.gitignore` - Ignore rules
- ✅ `LOOM_SCRIPT.md` - Demo guide
- ✅ Sample from `dataset/` (1-2 workflows)

### **Exclude:**
- ❌ `data/user_data/` - Contains login info
- ❌ `__pycache__/` - Python bytecode
- ❌ `.env` - API keys
- ❌ Most of `dataset/` - Too large (just include samples)

---

## 🔄 **Adding a New Platform**

### **1. Update `src/config.py`**
```python
MY_APP_CONTEXT = {
    "base_url": "https://myapp.com",
    "common_selectors": {
        "search_box": "input[type='search']",
    },
    "notes": "Brief description"
}
```

### **2. Create `tests/test_myapp.py`**
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import config
from adaptive_planner import AdaptivePlanner
from adaptive_executor import AdaptiveExecutor
from utils import generate_markdown_report

# ... test code
```

### **3. Run**
```bash
python tests/test_myapp.py
# Outputs → dataset/myapp_workflow/
```

---

## 🎯 **Key Design Decisions**

### **Why This Structure?**

1. **Separation of Concerns**
   - `src/` = core logic
   - `tests/` = platform tests
   - `dataset/` = outputs
   
2. **Easy to Navigate**
   - Clear folder names
   - Logical grouping
   - Minimal nesting

3. **Git-Friendly**
   - Sensitive data gitignored
   - Large outputs gitignored
   - Only code tracked

4. **Extensible**
   - Add platforms without changing core
   - New tests just import from `src/`
   - Modular components

---

## 📖 **Quick Reference**

| Need to... | Go to... |
|------------|----------|
| **Understand the system** | `README.md` |
| **Add a platform** | `src/config.py` + new test file |
| **Run a test** | `python tests/test_[platform].py` |
| **View outputs** | `dataset/` folder |
| **Debug selectors** | Check `step_*_debug.png` screenshots |
| **Understand code** | Comments in `src/` files |
| **Record demo** | Follow `LOOM_SCRIPT.md` |

---

**Clean, organized, and ready for submission!** ✅
