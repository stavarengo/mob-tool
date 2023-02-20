from dataclasses import dataclass

import flet as ft


@dataclass(frozen=True)
class GuiService:
    def show_message(self, message: str) -> None:
        def _main(page: ft.Page):
            def _close_window():
                page.window_close()

            def items():
                _items = [
                    ft.Icon(name=ft.icons.TIMER_SHARP, color=ft.colors.GREEN_400, size=65, expand=True),
                    ft.Text(
                        value=message,
                        style=ft.TextThemeStyle.DISPLAY_SMALL,
                        color=ft.colors.GREEN_400,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.ElevatedButton("Close window", on_click=lambda _: _close_window()),
                ]
                return [ft.Container(
                    content=item,
                    expand=True,
                    alignment=ft.alignment.center,
                ) for item in _items]

            page.add(
                ft.Row(
                    [ft.Column(
                        items(),
                        alignment=ft.MainAxisAlignment.CENTER,
                        expand=True,
                    )],
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )

            page.window_always_on_top = True

            page.on_keyboard_event = lambda e: _close_window() if e.key == 'Escape' else None

            page.update()

        ft.app(target=_main)
