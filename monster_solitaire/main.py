import flet as ft
from game import MonsterSolitaire


def main(page: ft.Page):
    game = MonsterSolitaire()
    game.build(page)


if __name__ == "__main__":
    ft.run(main)
