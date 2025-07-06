# Git Analyzer (What I Have Done)

A modern command-line tool that fetches your Git commit history, sends it to the OpenAI API, and generates a visually rich, retro-style monthly development report in your terminal.

---

## 🚀 Features

- **Auto-fetch logs**: Retrieves commits by your Git user for the specified period.
- **AI-powered analysis**: Generates insights on:
  - Which feature took how many days
  - The most refactored feature
  - The biggest problem areas
  - Your time allocation breakdown
- **Retro terminal UI**: Outputs ASCII-art boxes, borders, and emojis for a classic, three-dimensional look.
- **Modern Python packaging**: Built with modern Python packaging standards and comprehensive testing
- **Multiple installation methods**: Install via pip, npm, or from source

---

## 🛠 Prerequisites

- **Python 3.8+** (required for the tool to run)
- `git` installed and available in your `PATH`
- An **OpenAI API key** (create one at https://platform.openai.com)

---

## ⚙️ Installation

### Option 1: Install via pip (Recommended)

```bash
pip install git-analyzer
```

### Option 2: Install via npm (Legacy Support)

```bash
npm install -g what-i-have-done
```

**Note:** The `-g` flag installs the package globally, making the `what-i-have-done` command available system-wide.

### Option 3: Install from source

1. **Clone this repository**
   ```bash
   git clone https://github.com/mksengun/what-I-have-done.git
   cd what-I-have-done
   ```

2. **Install the package**
   ```bash
   pip install -e .
   ```

3. **For development (install with dev dependencies)**
   ```bash
   pip install -e ".[dev]"
   ```

---

## 🔧 Configuration

You can provide your OpenAI API key in two ways:

1. **Environment variable** (recommended):
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```

2. **Command-line argument** (overrides environment variable):
   Add `--api-key YOUR_OPENAI_KEY` when running the command.

---

## 🚀 Usage

### If installed via pip:

```bash
# Basic usage (uses environment variable):
git-analyzer --since 1.month

# With inline API key:
git-analyzer --since 1.month --api-key YOUR_OPENAI_KEY

# Different time periods:
git-analyzer --since 2.weeks
git-analyzer --since 7.days
```

### If installed via npm (legacy):

```bash
# Basic usage (uses environment variable):
what-i-have-done --since 1.month

# With inline API key:
what-i-have-done --since 1.month --api-key YOUR_OPENAI_KEY
```

### If running from source:

```bash
# Using the modern CLI:
python -m src.git_analyzer.cli --since 1.month

# Using the legacy script (for backward compatibility):
python what_I_have_done.py --since 1.month
```

### Example Commands

```bash
# Generate report for the last month
git-analyzer --since 1.month

# Generate report for the last 2 weeks  
git-analyzer --since 2.weeks

# Generate report with inline API key
git-analyzer --since 1.month --api-key sk-ABC123xyz

# Legacy npm command
what-i-have-done --since 1.month
```

---

## 🧪 Development

### Setting up development environment

```bash
# Clone the repository
git clone https://github.com/mksengun/what-I-have-done.git
cd what-I-have-done

# Install in development mode with all dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html

# Format code
black src tests
isort src tests

# Lint code
flake8 src tests

# Type checking
mypy src
```

### Project Structure

```
git-analyzer/
├── src/
│   └── git_analyzer/
│       ├── __init__.py
│       ├── cli.py              # Main CLI entry point
│       ├── commands/           # Command modules
│       │   ├── __init__.py
│       │   └── monthly_report.py
│       ├── core/               # Analysis logic
│       │   ├── __init__.py
│       │   ├── git_parser.py
│       │   └── analyzer.py
│       └── utils/              # Helper functions
│           ├── __init__.py
│           └── helpers.py
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_cli.py
│   ├── test_git_parser.py
│   └── test_analyzer.py
├── pyproject.toml              # Modern Python packaging
├── .github/workflows/          # CI/CD
│   └── main.yml
└── README.md
```

---

## 📊 Sample Output

```text
+------------------------------------------------------+   
| 🚀 Feature Durations                                 |   
+------------------------------------------------------+   
| • Unified Game Architecture : 12 days               |   
+------------------------------------------------------+   
| • Lesson Module Integration : 1 day                  |   
+------------------------------------------------------+   

+------------------------------------------------------+   
| 🔍 Analysis                                          |   
+------------------------------------------------------+   
| • Most refactored feature: Unified Game Architecture |   
| • Top problem area: Game state synchronization       |   
+------------------------------------------------------+   
```

---

## 🔄 Backward Compatibility

This modernized version maintains full backward compatibility with the original script:

- The original `what_I_have_done.py` script still works exactly as before
- The same command-line interface (`--since`, `--api-key`) is preserved
- Both pip and npm installation methods are supported
- Existing workflows and scripts will continue to work unchanged

The new modular architecture provides better maintainability and testing while preserving all existing functionality.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Open a pull request or issue on GitHub.

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_cli.py -v
```

### Code Quality

This project uses modern Python tooling:
- **Black** for code formatting
- **isort** for import sorting  
- **flake8** for linting
- **mypy** for type checking
- **pytest** for testing

---

## 📄 License

Distributed under the [MIT License](LICENSE).

*Made with ❤️ by Mustafa using ChatGPT*
