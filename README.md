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
- **Multiple Report Templates**: Choose from different perspectives:
  - **Developer**: Technical focus on code quality and refactoring
  - **Manager**: Business focus on deliverables and productivity
  - **Technical Debt**: Analysis of maintenance and improvement areas
  - **Productivity**: Personal productivity patterns and trends
- **Flexible Output Formats**: 
  - **Terminal**: Classic retro ASCII art style
  - **Markdown**: Clean, structured markdown format
  - **JSON**: Structured data format for integration
- **Smart Time Presets**: Use convenient presets like `yesterday`, `this-week`, `last-sprint`
- **Enhanced Filtering**: Exclude merge commits and focus on meaningful changes

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

**Note:** The `-g` flag installs the package globally, making the `what-i-have-done` command available system-wide.

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

### Basic Usage

```bash
# Basic usage with default settings (terminal output, developer template)
what-i-have-done --since 1.month --api-key YOUR_API_KEY

# Using environment variable for API key
export OPENAI_API_KEY="your-api-key"
what-i-have-done --since 1.month
```

### Time Period Options

```bash
# Use convenient presets
what-i-have-done --since yesterday
what-i-have-done --since this-week
what-i-have-done --since last-sprint

# Or use custom periods
what-i-have-done --since "2.weeks"
what-i-have-done --since "1.month"
```

### Report Templates

```bash
# Developer-focused report (default)
what-i-have-done --since 1.month --template developer

# Manager-focused report
what-i-have-done --since 1.month --template manager

# Technical debt analysis
what-i-have-done --since 1.month --template technical-debt

# Productivity analysis
what-i-have-done --since 1.month --template productivity
```

### Output Formats

```bash
# Terminal output with ASCII art (default)
what-i-have-done --since 1.month --format terminal

# Markdown format
what-i-have-done --since 1.month --format markdown

# JSON format for integration
what-i-have-done --since 1.month --format json
```

### Advanced Options

```bash
# Exclude merge commits from analysis
what-i-have-done --since 1.month --exclude-merges

# Combine multiple options
what-i-have-done --since last-sprint --template manager --format markdown --exclude-merges
```

### If running from source:

```bash
# Basic (uses environment variable):
python3 what-I-have-done.py --since 1.month

# With all options:
python3 what-I-have-done.py --since this-week --template productivity --format json --exclude-merges --api-key YOUR_API_KEY
```

### Example Commands

```bash
# Quick daily standup report
what-i-have-done --since yesterday --template developer

# Weekly manager report
what-i-have-done --since this-week --template manager --format markdown

# Sprint retrospective
what-i-have-done --since last-sprint --template technical-debt --exclude-merges

# Personal productivity review
what-i-have-done --since 1.month --template productivity --format json
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

## 🎯 Report Templates

Choose from different report perspectives to match your needs:

### 📋 Developer Template (default)
- **Focus**: Technical aspects and code quality
- **Sections**: Feature development, refactoring patterns, technical problems, code quality improvements
- **Best for**: Daily standups, technical reviews, personal development tracking

### 👔 Manager Template  
- **Focus**: Business deliverables and productivity
- **Sections**: Key deliverables, time allocation, productivity patterns, potential blockers, collaboration metrics
- **Best for**: Team reports, sprint reviews, stakeholder updates

### 🔧 Technical Debt Template
- **Focus**: Code maintenance and improvement opportunities
- **Sections**: Hotspot analysis, refactoring efforts, maintenance areas, technical improvements
- **Best for**: Architecture reviews, technical debt planning, code quality assessments

### 📈 Productivity Template
- **Focus**: Personal productivity patterns and trends
- **Sections**: Activity patterns, peak productivity periods, commit consistency, focus areas
- **Best for**: Personal retrospectives, productivity optimization, work-life balance analysis

---

## 🎨 Output Formats

### Terminal (Default)
Classic retro ASCII art with boxes, borders, and emojis for a nostalgic terminal experience.

### Markdown
Clean, structured markdown format perfect for documentation, wikis, and reports.

### JSON
Structured data format ideal for integration with other tools, dashboards, or automated workflows.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Open a pull request or issue on GitHub.

---

## 📄 License

Distributed under the [MIT License](LICENSE).

*Made with ❤️ by Mustafa using ChatGPT*
