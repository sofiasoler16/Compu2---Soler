
# ==============================
# File: processor/screenshot.py
# ==============================
import os
import time
from typing import Tuple, Optional

# Selenium es opcional; si no está disponible, devolvemos None con gracia

def _try_imports():
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        from selenium.webdriver.firefox.options import Options as FirefoxOptions
        from selenium.webdriver.common.by import By
        return webdriver, ChromeOptions, FirefoxOptions
    except Exception:
        return None, None, None


def _chrome_driver(headless=True):
    webdriver, ChromeOptions, _ = _try_imports()
    if not webdriver:
        return None
    try:
        opts = ChromeOptions()
        if headless:
            opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--disable-dev-shm-usage")
        drv = webdriver.Chrome(options=opts)
        return drv
    except Exception:
        return None


def _firefox_driver(headless=True):
    webdriver, _, FirefoxOptions = _try_imports()
    if not webdriver:
        return None
    try:
        opts = FirefoxOptions()
        if headless:
            opts.add_argument("-headless")
        drv = webdriver.Firefox(options=opts)
        return drv
    except Exception:
        return None


def take_screenshot_png(url: str, viewport: Tuple[int, int] = (1280, 800), timeout: int = 15) -> Optional[bytes]:
    """Devuelve PNG bytes de la página renderizada o None si no se pudo."""
    drv = _chrome_driver(headless=True) or _firefox_driver(headless=True)
    if drv is None:
        return None
    try:
        drv.set_page_load_timeout(timeout)
        drv.set_window_size(*viewport)
        t0 = time.perf_counter()
        drv.get(url)
        # Pequeña espera para contenido dinámico
        time.sleep(1.0)
        png = drv.get_screenshot_as_png()
        _ = time.perf_counter() - t0
        return png
    finally:
        try:
            drv.quit()
        except Exception:
            pass

