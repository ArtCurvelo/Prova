import flet as ft
from constants import CARD_WIDTH, CARD_HEIGHT


def create_card(game, name, creature, hp, element, colors, attacks):
    """Cria uma carta arrastável e associa os eventos ao controlador do jogo."""
    return ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=5,
        on_pan_start=game.start_drag,
        on_pan_update=game.drag,
        on_pan_end=game.drop,
        content=ft.Container(
            width=CARD_WIDTH,
            height=CARD_HEIGHT,
            padding=5,
            bgcolor=colors[0],
            border=ft.Border.all(3, colors[1]),
            border_radius=5,
            content=ft.Column(
                spacing=3,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                name,
                                size=10,
                                weight=ft.FontWeight.BOLD,
                                color=colors[2],
                            ),
                            ft.Text(
                                f"{hp} HP",
                                size=9,
                                weight=ft.FontWeight.BOLD,
                                color=colors[2],
                            ),
                        ],
                    ),
                    ft.Container(
                        height=65,
                        bgcolor=colors[3],
                        border=ft.Border.all(2, colors[1]),
                        alignment=ft.Alignment.CENTER,
                        content=ft.Text(creature, size=35),
                    ),
                    ft.Text(
                        element,
                        size=8,
                        weight=ft.FontWeight.BOLD,
                        color=colors[2],
                    ),
                    ft.Container(
                        padding=3,
                        bgcolor=colors[4],
                        border=ft.Border.all(1, colors[1]),
                        content=ft.Column(
                            spacing=4,
                            controls=[
                                ft.Text(
                                    attacks[0],
                                    size=8,
                                    color=colors[2],
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    attacks[1],
                                    size=8,
                                    color=colors[2],
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        ),
    )
