# Personal PC Agent (Windows 11) — Starter PoC

Summary
- Local-first, modular personal agent for Windows 11.
- PoC supports: simulated voice input, TTS replies, open website, open app, take screenshot, click, toggle Wi‑Fi, basic hardware/software health checks.
- Safety: denies destructive commands by default (no delete/registry writes).

Quick start (PoC mode)
1. Install Python 3.10+ and pip.
2. Create & activate virtual env:
   - python -m venv venv
   - venv\Scripts\activate
3. Install dependencies:
   - pip install -r requirements.txt
4. Run:
   - python main.py
5. PoC usage:
   - For now the agent prompts you to type commands (simulate speech). Example commands:
     - "open website github.com"
     - "open notepad"
     - "take screenshot"
     - "click"
     - "wifi off"
     - "wifi on"
     - "health check"

Notes & next steps
- Replace the simulated STT with whisper.cpp, Vosk, or cloud Whisper for live speech.
- Replace the simple intent classifier with an LLM planner (OpenAI or local Llama) for complex multi-step commands.
- Add Playwright for robust web automation and pywinauto/WinAppDriver for precise native app control.
- Admin-required actions (wifi toggle via netsh, Defender queries) will ask for elevation — be careful.

Security & safety
- The PoC contains a safety policy that blocks keywords like delete, format, registry edits.
- Always review requests requiring admin rights. Audit logs are written to logs/audit.log.

If you want, I can:
- Scaffold a full GitHub repo with these files.
- Add Whisper/LLM integration (cloud or local).
- Add Playwright and WinAppDriver modules for more robust automation.