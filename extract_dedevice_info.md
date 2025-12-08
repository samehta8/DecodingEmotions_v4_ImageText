# Option B: UA parsing + tiny JS signals (Streamlit Community Cloud friendly)
#
# requirements.txt:
#   streamlit
#   user-agents
#   ua-parser
#   streamlit_js_eval
#
# Notes:
# - UA-only can misclassify some iPads as macOS; adding touchpoints + viewport width helps.
# - JS values can be None on first render; we guard with defaults.

import streamlit as st
from user_agents import parse
from streamlit_js_eval import streamlit_js_eval


def classify_device(ua_raw: str, inner_width: int | None, max_touch_points: int | None) -> dict:
    ua = parse(ua_raw or "")

    # Base classification from UA
    device_type = (
        "tablet" if ua.is_tablet else
        "smartphone" if ua.is_mobile else
        "laptop/desktop" if ua.is_pc else
        "unknown"
    )

    os_family = ua.os.family          # e.g., 'Windows', 'Mac OS X', 'iOS', 'Android', 'Linux'
    browser_family = ua.browser.family

    # Heuristic: iPad-as-Mac often appears as macOS in UA, but has touchpoints > 0.
    # Viewport width can help avoid labeling large touch-enabled desktops as tablets.
    w = inner_width if inner_width is not None else 10_000
    touch = max_touch_points if max_touch_points is not None else 0

    if device_type == "laptop/desktop" and os_family in {"Mac OS X", "macOS"}:
        if touch > 0 and w <= 1366:
            device_type = "tablet (likely iPad)"

    return {
        "device_type": device_type,
        "os": os_family,
        "browser": browser_family,
        "window_innerWidth": inner_width,
        "maxTouchPoints": max_touch_points,
        "user_agent": ua_raw,
    }


st.title("Device / OS detection (UA + JS)")

# UA from Streamlit context headers
ua_raw = st.context.headers.get("User-Agent", "")

# Tiny JS signals (best-effort; may be None briefly)
inner_width = streamlit_js_eval(js_expressions="window.innerWidth", key="win_w")
max_touch_points = streamlit_js_eval(js_expressions="navigator.maxTouchPoints", key="touch_pts")

info = classify_device(ua_raw, inner_width, max_touch_points)

st.subheader("Detected info")
st.json(info)

