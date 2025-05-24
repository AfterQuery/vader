# VADER: A Human-Evaluated Benchmark for Vulnerability Assessment, Detection, Explanation, and Remediation

**Official GitHub Repo: https://github.com/AfterQuery/vader**  
**Hugging Face Dataset: https://huggingface.co/datasets/AfterQuery/vader**  

---

VADER is a **human-evaluated benchmark** designed to measure how well large language models (LLMs) handle real-world software vulnerabilities. It contains **174 real-world vulnerability cases** (curated from open-source repositories) covering four tasks:

- Vulnerability identification and classification (CWE)
- Root-cause explanation
- Patch (remediation)
- Test plan generation

These cases span **15+ programming languages** (e.g. JavaScript, Python, Go, C/C++, PHP, etc.) and often include **multi-file context**, mimicking real-world development environments.

---

## 📌 Key Features

- ✅ **174 Real-World Vulnerabilities**: Verified and annotated by experienced security experts.
- 🛠️ **Multi-Stage Evaluation**: Assessment, detection, explanation, remediation, and testing.
- 🌐 **Languages**: JavaScript, Python, PHP, Go, TypeScript, C/C++, HTML/CSS, Shell, Solidity, Java, Ruby, and more.
- 🧠 **Human Scoring Rubric**: Grounded in real cybersecurity practices. Scores weighted 50% toward remediation quality.
- 📊 **Multi-File Scenarios**: Over 75% of examples include multiple files or languages.
- 🚨 **Severity-Aware**: 61% of examples are "High" or "Critical" severity.

---

## 📦 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/AfterQuery/vader.git
cd vader
pip install -r requirements.txt
