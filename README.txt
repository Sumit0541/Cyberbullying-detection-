CyberShield AI — Privacy-First Cyberbullying Detection (educational demo)

RUN:
1. Extract the ZIP.
2. Open Command Prompt in the extracted CyberShield_AI folder.
3. Install dependencies: python -m pip install -r requirements.txt
4. Train the model: python train_model.py
5. Start website: python app.py
6. Open http://127.0.0.1:5000 in your browser.

Python IDLE:
- Open train_model.py in IDLE and press F5 once.
- Then open app.py in IDLE and press F5.
- Open http://127.0.0.1:5000 in your browser.

IMPORTANT:
- The included dataset is tiny and only for demonstrating the workflow.
- Model scores are not proof that bullying occurred.
- Keyword matching can miss context, sarcasm, spelling variants and languages.
- Messages are not saved to a database by this demo; the app processes them in memory.
- Do not enter real sensitive/private messages in a classroom demo.
- Blocking and reporting are recommendations only; this app does not access social platforms.
