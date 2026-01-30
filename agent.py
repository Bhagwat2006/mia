"""
agent/agent.py — Intent classification, policy checks, orchestration
"""
import re
import logging
import subprocess
from tools import automation, wifi, screens, health

DANGEROUS_PATTERNS = re.compile(r'\b(delete|format|remove registry|registry edit|rm -rf|format disk|wipe|uninstall)\b', re.I)

class Agent:
    def __init__(self):
        self.logger = logging.getLogger("agent")
        self.logger.setLevel(logging.INFO)

    def log(self, level, msg):
        logging.info(msg)

    def classify_intent(self, text: str):
        t = text.lower()
        if DANGEROUS_PATTERNS.search(t):
            return ("dangerous", None)
        if "open website" in t or "open site" in t or t.startswith("open ") and ("http" in t or "." in t.split()[-1]):
            # extract last token as URL if present
            token = t.split()[-1]
            return ("open_website", token)
        if "open" in t and ("notepad" in t or "chrome" in t or "edge" in t or "app" in t):
            return ("open_app", t)
        if "screenshot" in t or "screen" in t:
            return ("screenshot", None)
        if "click" in t or "press" in t:
            return ("click", None)
        if t in ("wifi on", "wifi off") or "wifi" in t:
            return ("wifi", t)
        if "health" in t or "status" in t or "diagnostic" in t:
            return ("health_check", None)
        if "volume" in t or "brightness" in t:
            return ("media_control", t)
        return ("unknown", None)

    def handle_input(self, text: str):
        self.log("info", f"User input: {text}")
        intent, param = self.classify_intent(text)
        if intent == "dangerous":
            self.log("warning", f"Blocked dangerous request: {text}")
            return "I will not perform that dangerous operation."
        if intent == "open_website":
            target = param or text
            self.log("info", f"Open website: {target}")
            automation.open_website(target)
            return f"Opening website {target}"
        if intent == "open_app":
            self.log("info", f"Open app request: {text}")
            started = automation.open_app(text)
            return f"Opening app: {started}"
        if intent == "screenshot":
            path = screens.take_screenshot()
            return f"Screenshot saved to {path}"
        if intent == "click":
            automation.click_current()
            return "Clicked at current mouse position."
        if intent == "wifi":
            if "off" in text:
                ok = wifi.set_wifi(False)
                return "Wi‑Fi turned off." if ok else "Failed to turn Wi‑Fi off (need admin)."
            else:
                ok = wifi.set_wifi(True)
                return "Wi‑Fi turned on." if ok else "Failed to turn Wi‑Fi on (need admin)."
        if intent == "health_check":
            report = health.basic_health_report()
            return report
        if intent == "media_control":
            return "Media control not implemented yet in PoC."
        return "I didn't understand. I can open websites, apps, screenshot, click, toggle wifi, or run a health check."
