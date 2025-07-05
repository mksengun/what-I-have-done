# What I Have Done

A command-line tool that fetches your Git commit history for a configurable period (default: last 30 days), sends it to the OpenAI API, and prints a visually rich, retro-style monthly development report in your terminal.

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

- **Python 3.7+**
- `git` installed and available in your `PATH`
- An **OpenAI API key** (create one at https://platform.openai.com)

---

## ⚙️ Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/your-username/what-I-have-done.git
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

Run the script from your project directory:

```bash
# Basic (uses environment variable):
python3 what-I-have-done.py

# With inline API key and custom period:
python3 what-I-have-done.py --api-key YOUR_OPENAI_KEY
```

### Example One-Liner

```bash
python3 what-I-have-done.py --api-key sk-ABC123xyz
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
