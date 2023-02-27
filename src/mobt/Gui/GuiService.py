from dataclasses import dataclass

import flet as ft


@dataclass(frozen=True)
class GuiService:
    def show_message(self, message: str, color: str = ft.colors.GREEN_400, on_show: callable = None) -> None:
        def _main(page: ft.Page):
            def _close_window(e: ft.ControlEvent):
                if isinstance(e, ft.KeyboardEvent) and e.key != 'Escape':
                    return

                page.window_close()

            def items():
                _items = [
                    ft.Text(
                        value=message,
                        style=ft.TextThemeStyle.DISPLAY_SMALL,
                        color=color,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.ElevatedButton("Close window", on_click=_close_window),
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

            page.on_keyboard_event = _close_window

            page.update()
            if on_show:
                on_show()

        ft.app(target=_main)
