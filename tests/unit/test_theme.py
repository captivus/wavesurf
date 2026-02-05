"""Tests for wavesurf._theme."""

from __future__ import annotations

import pytest

from wavesurf._theme import DARK, LIGHT, Theme, ThemeRegistry, themes


class TestBuiltInThemes:
    def test_dark_exists(self):
        assert DARK is not None
        assert DARK.background == "#1a1a2e"

    def test_light_exists(self):
        assert LIGHT is not None
        assert LIGHT.background == "#f8f8fc"

    def test_themes_are_frozen(self):
        with pytest.raises(AttributeError):
            DARK.background = "red"  # type: ignore[misc]


class TestWaveformOverrides:
    def test_returns_waveform_fields_only(self):
        theme = Theme(
            wave_color=["#aaa", "#bbb"],
            progress_color=["#ccc", "#ddd"],
            cursor_color="#eee",
            bar_width=3,
            bar_gap=2,
            bar_radius=3,
            height=80,
            background="#1a293d",
        )
        overrides = theme.waveform_overrides()
        assert "wave_color" in overrides
        assert "progress_color" in overrides
        assert "height" in overrides
        # Non-waveform fields should be absent
        assert "background" not in overrides
        assert "border" not in overrides
        assert "font_family" not in overrides

    def test_none_values_excluded(self):
        theme = Theme(wave_color="#aaa")  # other waveform fields default to None
        overrides = theme.waveform_overrides()
        assert "wave_color" in overrides
        assert "bar_width" not in overrides


class TestThemeReplace:
    def test_replace_returns_new_instance(self):
        new_theme = DARK.replace(background="#000000")
        assert new_theme.background == "#000000"
        assert DARK.background == "#1a1a2e"  # original unchanged

    def test_replace_preserves_other_fields(self):
        new_theme = DARK.replace(background="#000000")
        assert new_theme.wave_color == DARK.wave_color
        assert new_theme.height == DARK.height


class TestCustomTheme:
    def test_create_custom(self):
        custom = Theme(
            wave_color="#ff0000",
            progress_color="#00ff00",
            background="#333333",
            play_button_style="minimal",
        )
        assert custom.wave_color == "#ff0000"
        assert custom.play_button_style == "minimal"


class TestThemeRegistry:
    def test_builtin_themes_registered(self):
        assert "dark" in themes
        assert "light" in themes
        assert themes["dark"] is DARK
        assert themes["light"] is LIGHT

    def test_default_is_dark(self):
        assert themes.default == "dark"

    def test_names(self):
        assert "dark" in themes.names()
        assert "light" in themes.names()

    def test_register_and_get(self):
        registry = ThemeRegistry()
        custom = Theme(wave_color="#ff0000", background="#000")
        registry.register(name="custom", theme=custom)
        assert registry.get(name="custom") is custom
        assert registry["custom"] is custom

    def test_setitem(self):
        registry = ThemeRegistry()
        custom = Theme(wave_color="#ff0000")
        registry["my-theme"] = custom
        assert registry["my-theme"] is custom

    def test_contains(self):
        registry = ThemeRegistry()
        custom = Theme(wave_color="#ff0000")
        registry.register(name="test", theme=custom)
        assert "test" in registry
        assert "nonexistent" not in registry

    def test_register_rejects_non_theme(self):
        registry = ThemeRegistry()
        with pytest.raises(TypeError, match="Expected a Theme"):
            registry.register(name="bad", theme={"color": "red"})  # type: ignore[arg-type]

    def test_get_unknown_raises(self):
        registry = ThemeRegistry()
        with pytest.raises(KeyError, match="Unknown theme"):
            registry.get(name="nonexistent")

    def test_enable(self):
        registry = ThemeRegistry()
        custom = Theme(wave_color="#ff0000")
        registry.register(name="dark", theme=DARK)
        registry.register(name="custom", theme=custom)
        registry.enable(name="custom")
        assert registry.default == "custom"

    def test_enable_unknown_raises(self):
        registry = ThemeRegistry()
        with pytest.raises(KeyError):
            registry.enable(name="nonexistent")

    def test_resolve_none_returns_default(self):
        registry = ThemeRegistry()
        registry.register(name="dark", theme=DARK)
        assert registry.resolve(theme=None) is DARK

    def test_resolve_string(self):
        registry = ThemeRegistry()
        registry.register(name="light", theme=LIGHT)
        assert registry.resolve(theme="light") is LIGHT

    def test_resolve_theme_object_passthrough(self):
        registry = ThemeRegistry()
        custom = Theme(wave_color="#ff0000")
        assert registry.resolve(theme=custom) is custom
