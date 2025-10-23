# F8 Blog Review – Automation

Run locally:
```bash
python -m venv .venv
# Windows: .\.venv\Scripts\activate
pip install -r requirements.txt
pytest -q --html=report.html --self-contained-html
