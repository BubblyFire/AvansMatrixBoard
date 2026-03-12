_state = {"type": "idle", "label": ""}
_slideshow_state = {"running": False, "folder": "", "interval": 5.0, "current": ""}


def set_now_playing(type: str, label: str = "") -> None:
    """Update what is currently being displayed (e.g. type="image", label="cat.png")."""
    _state["type"] = type
    _state["label"] = label


def get_now_playing() -> dict:
    """Return a copy of the current display state (safe to serialise as JSON)."""
    return dict(_state)


def set_slideshow_state(**kwargs) -> None:
    """Merge keyword arguments into the slideshow state dict (e.g. running=True, current="img.png")."""
    _slideshow_state.update(kwargs)


def get_slideshow_state() -> dict:
    """Return a copy of the current slideshow state (safe to serialise as JSON)."""
    return dict(_slideshow_state)
