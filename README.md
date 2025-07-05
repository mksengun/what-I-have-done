# What I Have Done

A command-line tool that fetches your Git commit history for the last 30 days, sends it to the OpenAI API, and prints a visually rich, retro-style monthly development report in your terminal.

---

## 🚀 Features

- **Auto-fetch logs**: Retrieves commits by your Git user for the specified period.
- **AI-powered analysis**: Generates insights on:
  - Which feature took how many days
  - The most refactored feature
  - The biggest problem areas
  - Your time allocation breakdown
- **Retro terminal UI**: Outputs ASCII-art boxes, borders, and emojis for a classic, three-dimensional look.

---

## 🛠 Prerequisites

- **Node.js 12+** (for npm installation)
- **Python 3.7+** (required for the tool to run)
- `git` installed and available in your `PATH`
- An **OpenAI API key** (create one at https://platform.openai.com)

---

## ⚙️ Installation

### Option 1: Install via npm (Recommended)

```bash
npm install -g what-i-have-done
```

### Option 2: Install from source

1. **Clone this repository**
   ```bash
   git clone https://github.com/mksengun/what-I-have-done.git
   cd what-I-have-done
   ```

2. **Install dependencies**
   ```bash
   pip3 install requests
   ```

3. **Make the script executable** (optional)
   ```bash
   chmod +x what-I-have-done.py
   ```

---

## 🔧 Configuration

You can provide your OpenAI API key in two ways:

1. **Environment variable** (default):
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```

2. **Command-line argument** (overrides environment variable):
   Add `--api-key YOUR_OPENAI_KEY` when running the script.

---

## 🚀 Usage

### If installed via npm:

```bash
# Basic usage (uses environment variable):
what-i-have-done

# With inline API key:
what-i-have-done --api-key YOUR_OPENAI_KEY
```

### If running from source:

```bash
# Basic (uses environment variable):
python3 what-I-have-done.py

# With inline API key:
python3 what-I-have-done.py --api-key YOUR_OPENAI_KEY
```

### Example Commands

```bash
# Generate report using environment variable
what-i-have-done

# Generate report with inline API key
what-i-have-done --api-key sk-ABC123xyz
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

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Open a pull request or issue on GitHub.

---

## 📄 License

Distributed under the [MIT License](LICENSE).

*Made with ❤️ by Mustafa using ChatGPT*
