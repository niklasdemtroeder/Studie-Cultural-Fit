import os
import streamlit.components.v1 as components

_RELEASE = True

if _RELEASE:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend", "dist")
    _component_func = components.declare_component(
        "swipe_component",
        path=build_dir,
    )
else:
    _component_func = components.declare_component(
        "swipe_component",
        url="http://localhost:5173",
    )

def swipe_component(items=None, mode="swipe", key=None):
    return _component_func(
        items=items or [],
        mode=mode,
        key=key,
        default={},
    )