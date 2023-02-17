from dataclasses import dataclass

import flet as ft


@dataclass(frozen=True)
class GuiService:
    def show_message(self, message: str) -> None:
        def _main(page: ft.Page):
            text = ft.Text(value=message, style=ft.TextThemeStyle.DISPLAY_LARGE, color=ft.colors.GREEN_400)
            page.controls.append(
                ft.Row([
                    ft.Icon(name=ft.icons.TIMER_SHARP, color=ft.colors.GREEN_400, size=65),
                ], alignment=ft.MainAxisAlignment.CENTER)
            )
            page.controls.append(
                ft.Row([
                    text,
                ], alignment=ft.MainAxisAlignment.CENTER)
            )
            page.window_always_on_top = True

            page.add(
                ft.ElevatedButton("Close window", on_click=lambda _: page.window_close()),
            )

            page.update()

        ft.app(target=_main)
