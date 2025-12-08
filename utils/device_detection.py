"""
Device detection utility using User-Agent parsing and JavaScript signals.

This module provides comprehensive device, OS, and browser detection for
collecting metadata alongside user ratings.
"""
import streamlit as st
from user_agents import parse
from streamlit_js_eval import streamlit_js_eval


def get_device_info() -> dict:
    """
    Detect device type, OS, and browser information using User-Agent parsing
    and JavaScript signals (window dimensions and touch capabilities).

    Returns:
        dict: Device information containing:
            - device_type: str - "smartphone", "tablet", "laptop/desktop", or "unknown"
            - os: str - Operating system family (e.g., "Windows", "iOS", "Android")
            - os_version: str - Operating system version
            - browser: str - Browser family (e.g., "Chrome", "Safari", "Firefox")
            - browser_version: str - Browser version
            - window_innerWidth: int|None - Browser window width in pixels
            - window_innerHeight: int|None - Browser window height in pixels
            - maxTouchPoints: int|None - Maximum number of simultaneous touch points
            - screen_width: int|None - Physical screen width in pixels
            - screen_height: int|None - Physical screen height in pixels
            - user_agent: str - Raw User-Agent string
    """
    # Get User-Agent from Streamlit context headers
    ua_raw = st.context.headers.get("User-Agent", "")

    # Get JavaScript signals (best-effort; may be None on first render)
    inner_width = streamlit_js_eval(js_expressions="window.innerWidth", key="device_win_w")
    inner_height = streamlit_js_eval(js_expressions="window.innerHeight", key="device_win_h")
    max_touch_points = streamlit_js_eval(js_expressions="navigator.maxTouchPoints", key="device_touch_pts")
    screen_width = streamlit_js_eval(js_expressions="window.screen.width", key="device_screen_w")
    screen_height = streamlit_js_eval(js_expressions="window.screen.height", key="device_screen_h")

    # Parse User-Agent
    ua = parse(ua_raw or "")

    # Base classification from UA
    device_type = (
        "tablet" if ua.is_tablet else
        "smartphone" if ua.is_mobile else
        "laptop/desktop" if ua.is_pc else
        "unknown"
    )

    os_family = ua.os.family  # e.g., 'Windows', 'Mac OS X', 'iOS', 'Android', 'Linux'
    os_version = ua.os.version_string
    browser_family = ua.browser.family
    browser_version = ua.browser.version_string

    # Heuristic: iPad-as-Mac detection
    # iPads with iOS 13+ often appear as macOS in UA, but have touch capabilities
    # Viewport width helps avoid labeling large touch-enabled desktops as tablets
    w = inner_width if inner_width is not None else 10_000
    touch = max_touch_points if max_touch_points is not None else 0

    if device_type == "laptop/desktop" and os_family in {"Mac OS X", "macOS"}:
        if touch > 0 and w <= 1366:
            device_type = "tablet (likely iPad)"

    return {
        "device_type": device_type,
        "os": os_family,
        "os_version": os_version,
        "browser": browser_family,
        "browser_version": browser_version,
        "window_innerWidth": inner_width,
        "window_innerHeight": inner_height,
        "maxTouchPoints": max_touch_points,
        "screen_width": screen_width,
        "screen_height": screen_height,
        "user_agent": ua_raw,
    }


def get_device_info_cached() -> dict:
    """
    Get device information with session state caching.

    Device info is collected once per session and cached to avoid
    repeated JavaScript evaluations.

    Returns:
        dict: Device information (same format as get_device_info())
    """
    if 'device_info' not in st.session_state:
        st.session_state.device_info = get_device_info()

    return st.session_state.device_info
