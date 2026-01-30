"""
tools/screens.py — Screenshot and OCR hook
"""
import mss
import mss.tools
from datetime import datetime
from pathlib import Path

def take_screenshot():
    Path("screenshots").mkdir(exist_ok=True)
    filename = f"screenshots/screen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        sct_img = sct.grab(monitor)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=filename)
    return filename