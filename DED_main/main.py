import time
import webbrowser
import os
import sys
import threading
import http.server
import socketserver
import tkinter as tk
from pynput import keyboard, mouse
from fatigue_model import calculate_exhaustion

print("✅ Real laptop monitoring started...")
print("🔹 Demo mode: alert after 2 minutes")
print("🔹 Press Ctrl + Q to stop monitoring safely\n")

# ---------------- STATE ----------------
typing_count = 0
mouse_count = 0
start_time = time.time()
alert_shown = False
running = True
ctrl_pressed = False

# ---------------- POPUP ----------------
def start_local_server():
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", 8000), handler) as httpd:
        httpd.serve_forever()

def show_toy_popup():
    path = os.path.abspath("toy_popup.html")
    webbrowser.open_new(f"file://{path}")

# ---------------- INPUT LISTENERS ----------------
def on_key_press(key):
    global typing_count, running, ctrl_pressed
    typing_count += 1

    if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
        ctrl_pressed = True

    if key == keyboard.KeyCode.from_char('q') and ctrl_pressed:
        print("\n🛑 Monitoring stopped by user (Ctrl + Q)")
        running = False
        return False

def on_key_release(key):
    global ctrl_pressed
    if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
        ctrl_pressed = False

def on_mouse_click(x, y, button, pressed):
    global mouse_count
    if pressed:
        mouse_count += 1

keyboard.Listener(
    on_press=on_key_press,
    on_release=on_key_release
).start()

mouse.Listener(on_click=on_mouse_click).start()

# ---------------- MAIN LOOP ----------------
while running:
    elapsed_seconds = int(time.time() - start_time)
    screen_time = elapsed_seconds // 60  # minutes

    exhaustion_score = calculate_exhaustion(
        screen_time, typing_count, mouse_count
    )

    print(
        f"Time:{screen_time}m | Typing:{typing_count} | "
        f"Mouse:{mouse_count} | Exhaustion:{exhaustion_score}"
    )

    # 🔔 DEMO ALERT (2 minutes)
    if screen_time >= 2 and not alert_shown:
        show_toy_popup()
        alert_shown = True

        print("\n⏹ Demo complete: 2 minutes reached.")
        running = False
        break

    time.sleep(5)

print("✅ Program exited cleanly.")
sys.exit()
