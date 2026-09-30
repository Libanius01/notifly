"""Notification Vault: Kivy UI. Shows notifications saved by NotifListener.java
and lets you switch recording on/off per app."""
import colorsys
import json
import os
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import NoTransition, Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.switch import Switch
from kivy.uix.textinput import TextInput
from kivy.utils import escape_markup, platform

Window.clearcolor = (0, 0, 0, 1)

CATEGORIES = ["All", "Messages", "Mail", "Social", "Banking", "Other"]
BASE_HUES = {"All": 210, "Messages": 150, "Mail": 35,
             "Social": 280, "Banking": 190, "Other": 0}
KEYWORDS = {
    "Messages": ["whatsapp", "telegram", "signal", "messaging", "mms", "sms", "viber"],
    "Mail": ["gm", "mail", "outlook", "yahoo"],
    "Social": ["instagram", "facebook", "twitter", "tiktok", "snapchat", "reddit", "linkedin"],
    "Banking": ["bank", "pay", "wallet", "finance", "papara", "enpara"],
}
DARK = (0.13, 0.13, 0.13, 1)


def category_of(pkg):
    p = pkg.lower()
    for cat, words in KEYWORDS.items():
        if any(w in p for w in words):
            return cat
    return "Other"


def data_dir():
    if platform == "android":
        from jnius import autoclass
        ctx = autoclass("org.kivy.android.PythonActivity").mActivity
        return ctx.getFilesDir().getAbsolutePath()
    return os.path.dirname(os.path.abspath(__file__))


def log_path():
    return os.path.join(data_dir(), "notifications.jsonl")


def blocked_path():
    return os.path.join(data_dir(), "blocked.txt")   # read by NotifListener.java


def read_blocked():
    try:
        with open(blocked_path(), encoding="utf-8") as f:
            return {l.strip() for l in f if l.strip()}
    except OSError:
        return set()


def write_blocked(blocked):
    try:
        with open(blocked_path(), "w", encoding="utf-8") as f:
            f.write("\n".join(sorted(blocked)) + "\n")
    except OSError:
        pass


def installed_apps():
    """Returns [(label, package)] for apps that have a launcher icon."""
    if platform != "android":   # sample data for testing on a computer
        return [("WhatsApp", "com.whatsapp"), ("Gmail", "com.google.android.gm"),
                ("Instagram", "com.instagram.android"), ("Chrome", "com.android.chrome"),
                ("My Bank", "com.example.bank")]
    from jnius import autoclass
    act = autoclass("org.kivy.android.PythonActivity").mActivity
    pm = act.getPackageManager()
    me = act.getPackageName()
    lst = pm.getInstalledApplications(0)
    apps = []
    for i in range(lst.size()):
        ai = lst.get(i)
        pkg = ai.packageName
        if pkg == me or pm.getLaunchIntentForPackage(pkg) is None:
            continue
        apps.append((pm.getApplicationLabel(ai).toString(), pkg))
    apps.sort(key=lambda a: a[0].lower())
    return apps


def open_access_settings():
    if platform != "android":
        return
    from jnius import autoclass
    Intent = autoclass("android.content.Intent")
    act = autoclass("org.kivy.android.PythonActivity").mActivity
    act.startActivity(Intent("android.settings.ACTION_NOTIFICATION_LISTENER_SETTINGS"))


def rgb(hue):
    return colorsys.hsv_to_rgb((hue % 360) / 360.0, 0.5, 0.4) + (1,)


class Item(Label):
    def __init__(self, **kw):
        super().__init__(size_hint_y=None, halign="left", valign="top", markup=True, **kw)
        self.bind(width=lambda *_: setattr(self, "text_size", (self.width - 16, None)))
        self.bind(texture_size=lambda *_: setattr(self, "height", self.texture_size[1] + 18))


def dark_button(text, **kw):
    return Button(text=text, background_normal="", background_color=DARK, **kw)


class Vault(App):
    def build(self):
        self.title = "Notification Vault"
        self.filter = None
        self.hues = dict(BASE_HUES)
        self.entries = []
        self.last_sig = None
        self.clear_armed = False
        self.blocked = read_blocked()
        self.apps = None

        self.sm = ScreenManager(transition=NoTransition())
        self.sm.add_widget(self.build_log_screen())
        self.sm.add_widget(self.build_apps_screen())
        Clock.schedule_interval(lambda dt: self.refresh(), 2)
        self.refresh(force=True)
        return self.sm

    # ---------- log screen ----------
    def build_log_screen(self):
        screen = Screen(name="log")
        root = BoxLayout(orientation="vertical", padding=12, spacing=10)
        root.add_widget(Label(text="Notification Vault", size_hint_y=None,
                              height=40, font_size="20sp"))

        grid = GridLayout(cols=3, spacing=10, size_hint_y=None)
        grid.bind(width=lambda w, v: setattr(w, "height", ((v - 20) / 3) * 2 + 10))
        self.tiles = {}
        for name in CATEGORIES:
            t = Button(text=name, background_normal="", background_down="",
                       background_color=rgb(self.hues[name]), halign="center",
                       font_size="15sp")
            t.bind(on_release=lambda _b, n=name: self.press(n))
            self.tiles[name] = t
            grid.add_widget(t)
        root.add_widget(grid)

        self.list = GridLayout(cols=1, spacing=8, size_hint_y=None)
        self.list.bind(minimum_height=self.list.setter("height"))
        sv = ScrollView()
        sv.add_widget(self.list)
        root.add_widget(sv)

        row = BoxLayout(size_hint_y=None, height=52, spacing=10)
        apps_btn = dark_button("Apps")
        apps_btn.bind(on_release=lambda *_: self.show("apps"))
        access = dark_button("Grant access")
        access.bind(on_release=lambda *_: open_access_settings())
        self.clear_btn = dark_button("Clear log")
        self.clear_btn.bind(on_release=self.clear)
        for b in (apps_btn, access, self.clear_btn):
            row.add_widget(b)
        root.add_widget(row)
        screen.add_widget(root)
        return screen

    def press(self, name):
        self.hues[name] = (self.hues[name] + 14) % 360   # slight colour shift
        self.tiles[name].background_color = rgb(self.hues[name])
        self.filter = None if name == "All" else name
        self.refresh(force=True)

    def clear(self, *_):
        if not self.clear_armed:
            self.clear_armed = True
            self.clear_btn.text = "Tap again to confirm"
            Clock.schedule_once(self.disarm, 3)
            return
        try:
            os.remove(log_path())
        except OSError:
            pass
        self.disarm()
        self.refresh(force=True)

    def disarm(self, *_):
        self.clear_armed = False
        self.clear_btn.text = "Clear log"

    def load(self):
        out = []
        try:
            with open(log_path(), encoding="utf-8") as f:
                for line in f:
                    try:
                        out.append(json.loads(line))
                    except ValueError:
                        pass
        except OSError:
            pass
        return out

    def refresh(self, force=False):
        try:
            sig = (os.path.getsize(log_path()), self.filter)
        except OSError:
            sig = (0, self.filter)
        if not force and sig == self.last_sig:
            return
        self.last_sig = sig
        self.entries = self.load()
        for e in self.entries:
            e["cat"] = category_of(e.get("pkg", ""))

        for name, tile in self.tiles.items():
            n = len(self.entries) if name == "All" else sum(e["cat"] == name for e in self.entries)
            tile.text = "%d\n%s" % (n, name)

        shown = [e for e in self.entries if not self.filter or e["cat"] == self.filter]
        self.list.clear_widgets()
        if not shown:
            self.list.add_widget(Item(text="[color=777777]Nothing logged here yet. Grant "
                                           "notification access, then wait for a notification.[/color]"))
        for e in reversed(shown[-300:]):
            when = datetime.fromtimestamp(e.get("time", 0) / 1000).strftime("%d %b %H:%M")
            who = e.get("app") or e.get("pkg", "")
            self.list.add_widget(Item(text="[color=888888]%s  %s[/color]\n[b]%s[/b]\n%s\n%s" % (
                when, escape_markup(who), escape_markup(e.get("title", "")),
                escape_markup(e.get("text", "")), "")))

    # ---------- apps screen ----------
    def build_apps_screen(self):
        screen = Screen(name="apps")
        root = BoxLayout(orientation="vertical", padding=12, spacing=10)

        top = BoxLayout(size_hint_y=None, height=48, spacing=10)
        back = dark_button("Back", size_hint_x=None, width=90)
        back.bind(on_release=lambda *_: self.show("log"))
        top.add_widget(back)
        top.add_widget(Label(text="Apps to record", font_size="18sp"))
        root.add_widget(top)

        self.search = TextInput(hint_text="Search apps", multiline=False,
                                size_hint_y=None, height=44,
                                background_color=(0.1, 0.1, 0.1, 1),
                                foreground_color=(1, 1, 1, 1),
                                cursor_color=(1, 1, 1, 1),
                                hint_text_color=(0.5, 0.5, 0.5, 1))
        self.search.bind(text=lambda *_: self.build_rows())
        root.add_widget(self.search)

        bulk = BoxLayout(size_hint_y=None, height=44, spacing=10)
        all_on = dark_button("All on")
        all_on.bind(on_release=lambda *_: self.set_visible(True))
        all_off = dark_button("All off")
        all_off.bind(on_release=lambda *_: self.set_visible(False))
        bulk.add_widget(all_on)
        bulk.add_widget(all_off)
        root.add_widget(bulk)

        self.app_box = GridLayout(cols=1, spacing=4, size_hint_y=None)
        self.app_box.bind(minimum_height=self.app_box.setter("height"))
        sv = ScrollView()
        sv.add_widget(self.app_box)
        root.add_widget(sv)
        screen.add_widget(root)
        return screen

    def show(self, name):
        if name == "apps" and self.apps is None:
            self.apps = installed_apps()
            self.build_rows()
        self.sm.current = name

    def visible(self):
        q = self.search.text.lower().strip()
        return [(l, p) for l, p in (self.apps or [])
                if not q or q in l.lower() or q in p.lower()]

    def build_rows(self):
        self.app_box.clear_widgets()
        for label, pkg in self.visible():
            row = BoxLayout(size_hint_y=None, height=60, spacing=8)
            lab = Label(text="%s\n[size=11sp][color=777777]%s[/color][/size]" % (
                escape_markup(label), escape_markup(pkg)),
                markup=True, halign="left", valign="middle")
            lab.bind(size=lambda w, _: setattr(w, "text_size", w.size))
            sw = Switch(active=pkg not in self.blocked, size_hint_x=None, width=110)
            sw.bind(active=lambda _s, v, p=pkg: self.set_recording(p, v))
            row.add_widget(lab)
            row.add_widget(sw)
            self.app_box.add_widget(row)

    def set_recording(self, pkg, on):
        if on:
            self.blocked.discard(pkg)
        else:
            self.blocked.add(pkg)
        write_blocked(self.blocked)

    def set_visible(self, on):
        for _label, pkg in self.visible():
            if on:
                self.blocked.discard(pkg)
            else:
                self.blocked.add(pkg)
        write_blocked(self.blocked)
        self.build_rows()


if __name__ == "__main__":
    Vault().run()
