import flet as ft
import time
import math
import threading

def main(page: ft.Page):
    page.title = "Clock & Compass App"
    page.theme_mode = ft.ThemeMode.DARK  # الوضع الداكن
    page.padding = 20

    # --- ساعة رقمية ---
    digital_clock = ft.Text(value="00:00:00", size=30, weight=ft.FontWeight.BOLD)
    
    def update_digital_clock():
        while True:
            digital_clock.value = time.strftime("%H:%M:%S")
            page.update()
            time.sleep(1)
    
    threading.Thread(target=update_digital_clock, daemon=True).start()

    # --- ساعة عقارب ---
    analog_clock = ft.Stack(width=200, height=200)

    clock_circle = ft.Container(
        width=200, height=200, bgcolor="black", border_radius=100
    )
    
    hour_hand = ft.Container(width=6, height=50, bgcolor="white", border_radius=3, top=50, left=97)
    minute_hand = ft.Container(width=4, height=70, bgcolor="gray", border_radius=2, top=30, left=98)
    second_hand = ft.Container(width=2, height=90, bgcolor="red", border_radius=1, top=10, left=99)
    
    analog_clock.controls.extend([clock_circle, hour_hand, minute_hand, second_hand])

    def update_analog_clock():
        while True:
            now = time.localtime()
            sec_angle = now.tm_sec * 6
            min_angle = now.tm_min * 6 + now.tm_sec * 0.1
            hour_angle = (now.tm_hour % 12) * 30 + now.tm_min * 0.5
            
            second_hand.rotate = sec_angle
            minute_hand.rotate = min_angle
            hour_hand.rotate = hour_angle

            page.update()
            time.sleep(1)

    threading.Thread(target=update_analog_clock, daemon=True).start()

    # --- بوصلة ---
    compass = ft.Stack(width=150, height=150)

    compass_circle = ft.Container(
        width=150, height=150, bgcolor="black", border_radius=75
    )

    needle = ft.Container(width=4, height=70, bgcolor="red", border_radius=2, top=40, left=73)

    compass.controls.extend([compass_circle, needle])

    def update_compass():
        while True:
            angle = (time.time() % 360)  # محاكاة دوران البوصلة
            needle.rotate = angle
            page.update()
            time.sleep(1)

    threading.Thread(target=update_compass, daemon=True).start()

    # --- زر القائمة الثلاثية ---
    def show_info(e):
        page.snack_bar = ft.SnackBar(ft.Text("Developed by Hasan"))
        page.snack_bar.open = True
        page.update()

    menu = ft.PopupMenuButton(
        items=[ft.PopupMenuItem(text="عن التطبيق", on_click=show_info)]
    )

    # --- تخطيط الصفحة ---
    page.add(
        ft.Row([menu], alignment=ft.MainAxisAlignment.END),
        ft.Column(
            [
                ft.Text("Digital Clock", size=20),
                digital_clock,
                ft.Text("Analog Clock", size=20),
                analog_clock,
                ft.Text("Compass", size=20),
                compass,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

ft.app(target=main)
