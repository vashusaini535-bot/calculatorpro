"""
MathMaster Pro - Android / mobile version (Kivy)
Entry point for Buildozer. It reuses every solver from mathmaster_pro.py,
so keep both files in the same folder.

Test on PC:  pip install kivy  &&  python main.py
Build APK :  buildozer -v android debug
"""
from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.resources import resource_find
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

import mathmaster_pro as mm

Window.clearcolor = (0.055, 0.067, 0.125, 1)
Window.softinput_mode = "below_target"          # keyboard never hides the field

MONO = resource_find("data/fonts/RobotoMono-Regular.ttf") or "Roboto"
FG, MUTED = (0.91, 0.92, 0.97, 1), (0.55, 0.58, 0.74, 1)
ACCENT, DARK, FIELD = (0.486, 0.612, 1, 1), (0.05, 0.07, 0.13, 1), (0.13, 0.16, 0.28, 1)

# Roboto (Kivy's default font) lacks some symbols, so swap them for safe ones.
SAFE = {"⁴⁄₃": "4/3", "■": ">> ", "✔": "OK ", "⚠": "! ", "✓": "(ok)", "→": "->", "²": "^2", "³": "^3",
        "⁴": "^4", "⁄": "/", "₀": "0", "₁": "1", "₂": "2", "₃": "3", "ₙ": "n", "√": "sqrt ", "≥": ">=",
        "≤": "<=", "∑": "Sum", "Σ": "Sum", "⅓": "1/3", "⅔": "2/3", "…": "...", "−": "-", "·": "*",
        "≈": "~", "\u0304": "", "≠": "!="}


def clean(text):
    for k, v in SAFE.items():
        text = text.replace(k, v)
    return text


class MathApp(App):
    title = "MathMaster Pro"

    def build(self):
        self.specs = {t["name"]: t for t in mm.TABS}
        self.inputs, self.history, self.spec = [], [], None

        root = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(8))
        menu = Spinner(text=mm.TABS[0]["name"], values=list(self.specs), size_hint_y=None,
                       height=dp(52), background_color=ACCENT, color=DARK, font_size=dp(17))
        menu.bind(text=lambda s, t: self.load(t))
        root.add_widget(menu)

        scroll = ScrollView()
        self.body = BoxLayout(orientation="vertical", spacing=dp(8), size_hint_y=None,
                              padding=(0, dp(6), 0, dp(40)))
        self.body.bind(minimum_height=self.body.setter("height"))
        scroll.add_widget(self.body)
        root.add_widget(scroll)

        self.load(mm.TABS[0]["name"])
        return root

    # ---------------------------------------------------------- helpers
    @staticmethod
    def label(text, size, color, mono=False, bold=False):
        lb = Label(text=text, font_size=size, color=color, size_hint_y=None,
                   halign="left", valign="top", bold=bold)
        if mono:
            lb.font_name = MONO
        lb.bind(width=lambda w, v: setattr(w, "text_size", (v, None)),
                texture_size=lambda w, v: setattr(w, "height", v[1] + dp(6)))
        return lb

    def load(self, name):
        spec = self.spec = self.specs[name]
        self.inputs = []
        self.body.clear_widgets()
        self.body.add_widget(self.label(clean(spec["title"]), dp(19), FG, bold=True))
        if spec.get("hint"):
            self.body.add_widget(self.label(clean(spec["hint"]), dp(13), MUTED))

        for f in spec["fields"]:
            self.body.add_widget(self.label(clean(f[0]), dp(13), MUTED))
            if len(f) > 2:
                w = Spinner(text=f[1], values=f[2], size_hint_y=None, height=dp(46),
                            background_color=FIELD, font_size=dp(15))
            else:
                w = TextInput(text=f[1], multiline=False, write_tab=False, size_hint_y=None,
                              height=dp(46), font_size=dp(17), background_color=FIELD,
                              foreground_color=(1, 1, 1, 1), cursor_color=(1, 1, 1, 1))
                w.bind(on_text_validate=self.solve)
            self.body.add_widget(w)
            self.inputs.append(w)

        row = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        row.add_widget(Button(text="Solve", bold=True, background_normal="", background_color=ACCENT,
                              color=DARK, on_release=self.solve))
        row.add_widget(Button(text="Reset", background_normal="", background_color=FIELD,
                              on_release=self.reset))
        self.body.add_widget(row)

        self.body.add_widget(self.label("SOLUTION", dp(12), (0.72, 0.58, 0.96, 1), bold=True))
        self.out = self.label("Tap Solve to see the step-by-step answer.", dp(14), FG, mono=True)
        self.body.add_widget(self.out)

    def reset(self, *_):
        for w, f in zip(self.inputs, self.spec["fields"]):
            w.text = f[1]
        self.history = []
        self.out.text = ""

    def solve(self, *_):
        vals = [w.text for w in self.inputs]
        try:
            res = self.spec["fn"](vals)
        except ZeroDivisionError:
            res = "⚠ Division by zero is not allowed."
        except Exception as e:
            res = f"⚠ {e}"
        if isinstance(res, tuple):          # (text, graph data) - graph is desktop-only
            res = res[0]
        is_error = res.startswith("⚠")
        res = clean(res)
        if self.spec.get("append") and not is_error:
            self.history.append(f"{vals[0]}  =  {res}")
            self.out.text = "\n".join(self.history[-30:])
        else:
            self.out.text = res


if __name__ == "__main__":
    MathApp().run()
