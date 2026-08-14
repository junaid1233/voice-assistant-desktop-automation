"""
BluePilot — Bluexech product UI.

Market-ready control center with Run/Stop, English/Urdu mode,
quick commands, and social branding.
"""

from __future__ import annotations

import threading
import webbrowser
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

from app.config import Config
from app.assistant.assistant import Assistant
from app.commands.router import CommandRouter
from app.utils.logger import logger
from app.ui import theme as T


ROOT = Path(__file__).resolve().parents[2]
STATIC = ROOT / "static"
ICONS = ROOT / "assets" / "icons"


class AssistantUI:
    """BluePilot product control center."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(f"{T.PRODUCT_NAME} — a {T.COMPANY} product")
        self.root.geometry("920x720")
        self.root.minsize(820, 640)
        self.root.configure(bg=T.BG)

        self.assistant: Assistant | None = None
        self.worker: threading.Thread | None = None
        self.router = CommandRouter()
        self.language = tk.StringVar(value="en" if Config.LANGUAGE == "en" else "ur")
        self.status_var = tk.StringVar(value="Ready")
        self.pulse_on = False

        self._photos: list[ImageTk.PhotoImage] = []  # keep refs

        self._build_styles()
        self._build_layout()
        self._append_activity("Welcome to BluePilot. Choose a language, then press Run.")
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._tick_pulse()

        # Window icon
        icon_path = STATIC / "bluexech-icon.png"
        if icon_path.exists():
            try:
                self.root.iconphoto(True, tk.PhotoImage(file=str(icon_path)))
            except Exception:
                pass

    # ------------------------------------------------------------------ styles
    def _build_styles(self) -> None:
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure("Root.TFrame", background=T.BG)
        style.configure("Card.TFrame", background=T.CARD)
        style.configure("Elevated.TFrame", background=T.BG_ELEVATED)
        style.configure("Hero.TLabel", background=T.BG, foreground=T.TEXT, font=T.FONT_DISPLAY)
        style.configure("Headline.TLabel", background=T.BG, foreground=T.TEXT, font=T.FONT_HEADLINE)
        style.configure("Muted.TLabel", background=T.BG, foreground=T.TEXT_MUTED, font=T.FONT_BODY)
        style.configure("CardTitle.TLabel", background=T.CARD, foreground=T.TEXT, font=("Segoe UI Semibold", 12))
        style.configure("CardMuted.TLabel", background=T.CARD, foreground=T.TEXT_MUTED, font=T.FONT_SMALL)
        style.configure("Status.TLabel", background=T.CARD, foreground=T.TEAL_SOFT, font=("Segoe UI Semibold", 13))
        style.configure("By.TLabel", background=T.BG, foreground=T.TEAL_SOFT, font=("Segoe UI Semibold", 10))

    # ------------------------------------------------------------------ layout
    def _build_layout(self) -> None:
        shell = ttk.Frame(self.root, style="Root.TFrame", padding=24)
        shell.pack(fill="both", expand=True)

        self._build_header(shell)
        self._build_hero(shell)

        body = ttk.Frame(shell, style="Root.TFrame")
        body.pack(fill="both", expand=True, pady=(18, 0))
        body.columnconfigure(0, weight=3)
        body.columnconfigure(1, weight=2)

        left = ttk.Frame(body, style="Root.TFrame")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        right = ttk.Frame(body, style="Root.TFrame")
        right.grid(row=0, column=1, sticky="nsew")

        self._build_controls(left)
        self._build_status(left)
        self._build_activity(left)
        self._build_quick(right)
        self._build_how(right)
        self._build_tips(right)
        self._build_footer(shell)

    def _build_header(self, parent: ttk.Frame) -> None:
        header = ttk.Frame(parent, style="Root.TFrame")
        header.pack(fill="x")

        brand = ttk.Frame(header, style="Root.TFrame")
        brand.pack(side="left")

        logo_path = STATIC / "bluexech-logo.png"
        if logo_path.exists():
            img = Image.open(logo_path).convert("RGBA")
            img = img.resize((48, 48), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self._photos.append(photo)
            tk.Label(brand, image=photo, bg=T.BG, bd=0).pack(side="left", padx=(0, 12))

        titles = ttk.Frame(brand, style="Root.TFrame")
        titles.pack(side="left")
        ttk.Label(titles, text=T.PRODUCT_NAME, style="Headline.TLabel").pack(anchor="w")
        ttk.Label(titles, text=f"by {T.COMPANY}", style="By.TLabel").pack(anchor="w")

        social = ttk.Frame(header, style="Root.TFrame")
        social.pack(side="right")
        for key, label, url in T.SOCIAL:
            self._social_button(social, key, label, url).pack(side="left", padx=6)

    def _social_button(self, parent: ttk.Frame, key: str, label: str, url: str) -> ttk.Frame:
        """Large branded icon + caption."""
        wrap = ttk.Frame(parent, style="Root.TFrame")
        icon_path = ICONS / f"{key}.png"

        def open_link(_event=None, u=url):
            webbrowser.open(u)

        if icon_path.exists():
            img = Image.open(icon_path).convert("RGBA").resize((44, 44), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self._photos.append(photo)
            btn = tk.Label(
                wrap,
                image=photo,
                bg=T.BG,
                cursor="hand2",
                bd=0,
            )
            btn.pack()
            btn.bind("<Button-1>", open_link)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=T.CARD))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=T.BG))
        else:
            btn = tk.Button(
                wrap,
                text=label[:1],
                command=open_link,
                bg=T.CARD,
                fg=T.TEXT,
                relief="flat",
                width=4,
                height=2,
                cursor="hand2",
            )
            btn.pack()

        tk.Label(
            wrap,
            text=label,
            bg=T.BG,
            fg=T.TEXT_MUTED,
            font=("Segoe UI", 8),
            cursor="hand2",
        ).pack(pady=(4, 0))
        wrap.bind("<Button-1>", open_link)
        for child in wrap.winfo_children():
            child.bind("<Button-1>", open_link)
        return wrap

    def _build_hero(self, parent: ttk.Frame) -> None:
        hero = ttk.Frame(parent, style="Root.TFrame")
        hero.pack(fill="x", pady=(22, 0))
        ttk.Label(hero, text=T.PRODUCT_NAME, style="Hero.TLabel").pack(anchor="w")
        ttk.Label(hero, text=T.TAGLINE, style="Headline.TLabel").pack(anchor="w", pady=(6, 0))
        ttk.Label(hero, text=T.SUPPORT, style="Muted.TLabel", wraplength=760).pack(anchor="w", pady=(8, 0))
        ttk.Label(
            hero,
            text="Local productivity assistant · Not an unrestricted AI agent",
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(6, 0))

    def _build_controls(self, parent: ttk.Frame) -> None:
        card = ttk.Frame(parent, style="Card.TFrame", padding=18)
        card.pack(fill="x", pady=(0, 12))
        ttk.Label(card, text="Assistant controls", style="CardTitle.TLabel").pack(anchor="w")

        ttk.Label(
            card,
            text="Language locks for the whole session. Pick mode, then Run.",
            style="CardMuted.TLabel",
        ).pack(anchor="w", pady=(4, 0))

        row = ttk.Frame(card, style="Card.TFrame")
        row.pack(fill="x", pady=(14, 0))

        # Language segmented control
        lang_wrap = ttk.Frame(row, style="Card.TFrame")
        lang_wrap.pack(side="left")

        self.en_chip = tk.Button(
            lang_wrap,
            text="English",
            command=lambda: self._set_language("en"),
            relief="flat",
            bd=0,
            cursor="hand2",
            font=T.FONT_BUTTON,
            padx=14,
            pady=8,
        )
        self.en_chip.pack(side="left", padx=(0, 6))

        self.ur_chip = tk.Button(
            lang_wrap,
            text="اردو",
            command=lambda: self._set_language("ur"),
            relief="flat",
            bd=0,
            cursor="hand2",
            font=T.FONT_BUTTON,
            padx=14,
            pady=8,
        )
        self.ur_chip.pack(side="left")
        self._paint_language_chips()

        btns = ttk.Frame(row, style="Card.TFrame")
        btns.pack(side="right")

        self.run_btn = tk.Button(
            btns,
            text="Run Assistant",
            command=self.start_assistant,
            bg=T.TEAL,
            fg=T.WHITE,
            activebackground=T.TEAL_DEEP,
            activeforeground=T.WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=T.FONT_BUTTON,
            padx=18,
            pady=10,
        )
        self.run_btn.pack(side="left", padx=(0, 8))

        self.stop_btn = tk.Button(
            btns,
            text="Stop",
            command=self.stop_assistant,
            bg=T.CARD_ALT,
            fg=T.TEXT,
            activebackground=T.LINE,
            activeforeground=T.WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=T.FONT_BUTTON,
            padx=18,
            pady=10,
            state="disabled",
        )
        self.stop_btn.pack(side="left")

    def _build_status(self, parent: ttk.Frame) -> None:
        card = ttk.Frame(parent, style="Card.TFrame", padding=18)
        card.pack(fill="x", pady=(0, 12))
        top = ttk.Frame(card, style="Card.TFrame")
        top.pack(fill="x")
        ttk.Label(top, text="Status", style="CardTitle.TLabel").pack(side="left")
        self.pulse = tk.Canvas(top, width=12, height=12, bg=T.CARD, highlightthickness=0)
        self.pulse.pack(side="right")
        self.pulse_dot = self.pulse.create_oval(2, 2, 10, 10, fill=T.TEXT_MUTED, outline="")
        ttk.Label(card, textvariable=self.status_var, style="Status.TLabel").pack(anchor="w", pady=(10, 0))

    def _build_activity(self, parent: ttk.Frame) -> None:
        card = ttk.Frame(parent, style="Card.TFrame", padding=18)
        card.pack(fill="both", expand=True)
        ttk.Label(card, text="Activity", style="CardTitle.TLabel").pack(anchor="w")
        self.log = tk.Text(
            card,
            height=14,
            bg=T.BG,
            fg=T.TEXT,
            insertbackground=T.TEXT,
            relief="flat",
            font=T.FONT_MONO,
            wrap="word",
            bd=0,
            padx=10,
            pady=10,
        )
        self.log.pack(fill="both", expand=True, pady=(10, 0))
        self.log.configure(state="disabled")

    def _build_quick(self, parent: ttk.Frame) -> None:
        card = ttk.Frame(parent, style="Card.TFrame", padding=18)
        card.pack(fill="x", pady=(0, 12))
        ttk.Label(card, text="Quick commands", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(
            card,
            text="Click to run instantly, or say them aloud after Run.",
            style="CardMuted.TLabel",
        ).pack(anchor="w", pady=(4, 10))

        wrap = ttk.Frame(card, style="Card.TFrame")
        wrap.pack(fill="x")
        for i, (label, command) in enumerate(T.QUICK_COMMANDS):
            btn = tk.Button(
                wrap,
                text=label,
                command=lambda c=command, l=label: self._run_quick(c, l),
                bg=T.BG,
                fg=T.TEXT,
                activebackground=T.TEAL,
                activeforeground=T.WHITE,
                relief="flat",
                bd=0,
                cursor="hand2",
                font=T.FONT_SMALL,
                padx=10,
                pady=8,
            )
            btn.grid(row=i // 2, column=i % 2, sticky="ew", padx=4, pady=4)
        wrap.columnconfigure(0, weight=1)
        wrap.columnconfigure(1, weight=1)

    def _build_how(self, parent: ttk.Frame) -> None:
        card = ttk.Frame(parent, style="Card.TFrame", padding=18)
        card.pack(fill="x", pady=(0, 12))
        ttk.Label(card, text="How it works", style="CardTitle.TLabel").pack(anchor="w")
        steps = [
            "1. Pick English or اردو",
            "2. Press Run Assistant",
            "3. Speak a clear command — or use quick chips",
        ]
        for step in steps:
            ttk.Label(card, text=step, style="CardMuted.TLabel").pack(anchor="w", pady=(6, 0))

    def _build_tips(self, parent: ttk.Frame) -> None:
        card = ttk.Frame(parent, style="Card.TFrame", padding=18)
        card.pack(fill="both", expand=True)
        ttk.Label(card, text="Language tips", style="CardTitle.TLabel").pack(anchor="w")
        tip = (
            "EN: Open Cursor · Create new folder · Open my LinkedIn profile · Exit\n\n"
            "UR: کرسر کھولو · نیا فولڈر بناؤ · میرا لنکڈان کھولو · بند کرو\n\n"
            "Roman: cursor kholo · folder banao · mera linkedin kholo · band karo"
        )
        tk.Label(
            card,
            text=tip,
            bg=T.CARD,
            fg=T.TEXT_MUTED,
            justify="left",
            anchor="nw",
            font=T.FONT_SMALL,
            wraplength=280,
        ).pack(fill="both", expand=True, pady=(8, 0))

    def _build_footer(self, parent: ttk.Frame) -> None:
        footer = ttk.Frame(parent, style="Root.TFrame")
        footer.pack(fill="x", pady=(16, 0))

        left = ttk.Frame(footer, style="Root.TFrame")
        left.pack(side="left")
        ttk.Label(left, text="Built by Muhammad Junaid", style="Muted.TLabel").pack(anchor="w")
        ttk.Label(left, text="Full-Stack Developer & AI Engineer · Bluexech", style="Muted.TLabel").pack(anchor="w")

        right = ttk.Frame(footer, style="Root.TFrame")
        right.pack(side="right")
        for key, label, url in T.SOCIAL:
            chip = ttk.Frame(right, style="Root.TFrame")
            chip.pack(side="left", padx=6)
            icon_path = ICONS / f"{key}.png"
            if icon_path.exists():
                img = Image.open(icon_path).convert("RGBA").resize((28, 28), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self._photos.append(photo)
                lbl = tk.Label(chip, image=photo, bg=T.BG, cursor="hand2", bd=0)
                lbl.pack(side="left", padx=(0, 6))
                lbl.bind("<Button-1>", lambda e, u=url: webbrowser.open(u))
            tk.Button(
                chip,
                text=label,
                command=lambda u=url: webbrowser.open(u),
                bg=T.BG,
                fg=T.TEAL_SOFT,
                activebackground=T.BG,
                activeforeground=T.WHITE,
                relief="flat",
                bd=0,
                cursor="hand2",
                font=("Segoe UI Semibold", 9),
            ).pack(side="left")

    # ------------------------------------------------------------------ helpers
    def _paint_language_chips(self) -> None:
        lang = self.language.get()
        if lang == "en":
            self.en_chip.configure(bg=T.TEAL, fg=T.WHITE, activebackground=T.TEAL_DEEP)
            self.ur_chip.configure(bg=T.BG, fg=T.TEXT, activebackground=T.CARD_ALT)
        else:
            self.ur_chip.configure(bg=T.TEAL, fg=T.WHITE, activebackground=T.TEAL_DEEP)
            self.en_chip.configure(bg=T.BG, fg=T.TEXT, activebackground=T.CARD_ALT)

    def _set_language(self, lang: str) -> None:
        self.language.set(lang)
        Config.set_language(lang)
        self._paint_language_chips()
        label = "English" if lang == "en" else "اردو"
        welcome = (
            "English mode is on. Welcome. How can I help you?"
            if lang == "en"
            else "اردو موڈ آن ہے۔ خوش آمدید۔ میں آپ کی کیا مدد کر سکتا ہوں؟"
        )
        self._append_activity(f"Language → {label}")
        self._append_activity(f"BluePilot: {welcome}")

        # If assistant is running, switch live + speak welcome in that language
        if self.assistant and self.assistant.running:
            threading.Thread(
                target=lambda: self.assistant.switch_language(lang),
                daemon=True,
            ).start()
        else:
            # Preview voice welcome even before Run
            def _preview() -> None:
                try:
                    from app.speech.speaker import Speaker
                    Speaker().speak(welcome)
                except Exception:
                    logger.exception("Language preview speech failed.")

            threading.Thread(target=_preview, daemon=True).start()

    def _append_activity(self, message: str) -> None:
        stamp = datetime.now().strftime("%H:%M:%S")
        self.log.configure(state="normal")
        self.log.insert("end", f"[{stamp}] {message}\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _ui(self, fn) -> None:
        self.root.after(0, fn)

    def _tick_pulse(self) -> None:
        status = self.status_var.get().lower()
        listening = "listen" in status or status == "running"
        color = T.TEAL_SOFT if listening and self.pulse_on else (T.TEAL if listening else T.TEXT_MUTED)
        self.pulse.itemconfigure(self.pulse_dot, fill=color)
        self.pulse_on = not self.pulse_on
        self.root.after(500, self._tick_pulse)

    def _run_quick(self, command: str, label: str) -> None:
        self._append_activity(f"Quick: {label}")
        try:
            # If assistant is running, speak path via processor; else execute directly
            if self.assistant and self.assistant.running:
                response = self.assistant.processor.process(command)
            else:
                response = self.router.handle(command)
            self._append_activity(f"BluePilot: {response}")
            # Speak via a short-lived speaker only when assistant not owning mixer heavily
            if self.assistant and self.assistant.running:
                threading.Thread(
                    target=lambda: self.assistant.speaker.speak(response),
                    daemon=True,
                ).start()
        except Exception:
            logger.exception("Quick command failed.")
            self._append_activity("Quick command failed.")

    # ------------------------------------------------------------------ run/stop
    def start_assistant(self) -> None:
        if self.worker and self.worker.is_alive():
            return

        Config.set_language(self.language.get())
        self.run_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        # Language chips stay enabled for live English/Urdu welcome switch
        self.en_chip.configure(state="normal")
        self.ur_chip.configure(state="normal")
        self.status_var.set("Starting...")
        self._append_activity(
            f"Starting BluePilot ({'English' if Config.LANGUAGE == 'en' else 'Urdu'})..."
        )

        def on_status(msg: str) -> None:
            self._ui(lambda: self.status_var.set(msg))

        def on_heard(text: str) -> None:
            self._ui(lambda: self._append_activity(f"You: {text}"))

        def on_reply(text: str) -> None:
            self._ui(lambda: self._append_activity(f"BluePilot: {text}"))

        def worker() -> None:
            try:
                self.assistant = Assistant(
                    on_status=on_status,
                    on_heard=on_heard,
                    on_reply=on_reply,
                )
                self.assistant.run()
            except Exception:
                logger.exception("UI worker failed.")
                self._ui(lambda: self._append_activity("Assistant crashed. Check logs/."))
                self._ui(lambda: self.status_var.set("Error"))
            finally:
                self._ui(self._reset_controls)

        self.worker = threading.Thread(target=worker, daemon=True)
        self.worker.start()

    def stop_assistant(self) -> None:
        if self.assistant and self.assistant.running:
            self._append_activity("Stop requested...")
            self.assistant.stop()
            self.status_var.set("Stopping...")
        else:
            self._reset_controls()

    def _reset_controls(self) -> None:
        self.run_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.en_chip.configure(state="normal")
        self.ur_chip.configure(state="normal")
        if self.status_var.get() != "Error":
            self.status_var.set("Stopped")
        self._append_activity("BluePilot stopped.")

    def _on_close(self) -> None:
        if self.assistant and self.assistant.running:
            self.assistant.stop()
        self.root.destroy()

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    Config.set_language(Config.LANGUAGE)
    AssistantUI().run()


if __name__ == "__main__":
    main()
