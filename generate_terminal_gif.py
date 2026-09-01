#!/usr/bin/env python3
"""Generate a terminal-style about GIF for the profile README."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 900, 340
BG = (15, 23, 42)
PANEL = (30, 41, 59)
TEXT = (226, 232, 240)
MUTED = (148, 163, 184)
GREEN = (52, 211, 153)
CYAN = (34, 211, 238)
RED = (248, 113, 113)
YELLOW = (250, 204, 21)

LINES = [
    ("prompt", "~ % whoami"),
    ("output", "Yashwanth Devulapally"),
    ("blank", ""),
    ("prompt", "~ % cat about.txt"),
    ("output", "Student engineer building AI-powered automation,"),
    ("output", "backend systems, and cloud infrastructure."),
    ("output", "DevOps · n8n · AI/ML · cybersecurity · full-stack."),
    ("blank", ""),
    ("prompt", "~ % cat status.txt"),
    ("output", "B.Tech CSE (AI & ML) @ GRIET"),
    ("output", "AI and Automations Intern @ ParityBit Security"),
    ("blank", ""),
    ("prompt", "~ % _"),
]

FRAMES_PER_LINE = 4
FRAME_MS = 120


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf" if bold else "/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_frame(visible_count: int) -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    title_font = load_font(16, bold=True)
    mono_font = load_font(18)

    draw.rounded_rectangle((20, 20, WIDTH - 20, HEIGHT - 20), radius=14, fill=PANEL)

    for i, color in enumerate([RED, YELLOW, GREEN]):
        draw.ellipse((42 + i * 24, 36, 56 + i * 24, 50), fill=color)

    draw.text((90, 32), "yashwanth@dev ~ zsh", font=title_font, fill=MUTED)

    y = 78
    line_height = 24
    visible = 0

    for kind, text in LINES:
        if visible >= visible_count:
            break
        if kind == "blank":
            y += line_height // 2
            visible += 1
            continue

        if kind == "prompt":
            color = CYAN
        else:
            color = TEXT

        draw.text((42, y), text, font=mono_font, fill=color)
        y += line_height
        visible += 1

    return img


def main() -> None:
    out = Path(__file__).resolve().parent / "assets" / "about_yashwanth.gif"
    out.parent.mkdir(parents=True, exist_ok=True)

    frames: list[Image.Image] = []
    durations: list[int] = []

    for i in range(1, len(LINES) + 1):
        frame = draw_frame(i)
        for _ in range(FRAMES_PER_LINE):
            frames.append(frame.copy())
            durations.append(FRAME_MS)

    for _ in range(18):
        frames.append(draw_frame(len(LINES)))
        durations.append(FRAME_MS)

    frames[0].save(
        out,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=True,
    )
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
