import math
import flet as ft

from cards import create_card
from constants import (
    ACCENT_COLOR,
    BACKGROUND,
    CARD_HEIGHT,
    CARD_WIDTH,
    DROP_DISTANCE,
    SLOT_COLOR,
    SLOT_POSITIONS,
    SLOT_TOP,
    STACK_OFFSET,
    TEXT_COLOR,
)


class MonsterSolitaire:
    def __init__(self):
        self.page = None
        self.slots = []
        self.cards = []
        self.stack = None
        self.dragging_cards = []
        self.drag_origins = {}

    def make_slot(self, left):
        return ft.Container(
            width=CARD_WIDTH,
            height=CARD_HEIGHT,
            left=left,
            top=SLOT_TOP,
            border=ft.Border.all(2, "#56745E"),
            bgcolor=SLOT_COLOR,
            border_radius=5,
        )

    def create_cards(self):
        definitions = [
            (
                "VOLT", "⚡", 60, "ELECTRIC",
                ["#F5CE45", "#6E4B12", "#30220B", "#FFECA0", "#FFF4C9"],
                ["PIXEL SHOCK 10", "MAX LIGHTNING 30"],
            ),
            (
                "EMBER", "🔥", 70, "FIRE",
                ["#F07850", "#782F25", "#3C1510", "#FFC09A", "#FFE0CA"],
                ["EMBER 20", "FIRE BLAST 40"],
            ),
            (
                "AQUA", "💧", 60, "WATER",
                ["#58B8F5", "#174C83", "#102D50", "#C1E9FF", "#E0F5FF"],
                ["WATER SHOT 10", "WAVE CRASH 30"],
            ),
        ]

        self.cards = [
            create_card(self, *definition)
            for definition in definitions
        ]

        # Três cartas iniciam na mesma pilha.
        for index, card in enumerate(self.cards):
            card.left = SLOT_POSITIONS[0]
            card.top = SLOT_TOP + index * STACK_OFFSET

    def get_card_pile(self, selected):
        """
        Retorna a carta selecionada e as cartas visualmente abaixo dela
        na mesma coluna. A comparação usa posições de pilha, não índices
        globais dos controles.
        """
        pile = [
            card for card in self.cards
            if abs(card.left - selected.left) < 5
            and card.top >= selected.top - 1
        ]
        return sorted(pile, key=lambda card: card.top)

    def start_drag(self, event: ft.DragStartEvent):
        selected = event.control
        self.dragging_cards = self.get_card_pile(selected)

        self.drag_origins = {
            card: (card.left, card.top)
            for card in self.dragging_cards
        }

        # Mantém a ordem visual, colocando a pilha arrastada no topo.
        for card in self.dragging_cards:
            if card in self.stack.controls:
                self.stack.controls.remove(card)
                self.stack.controls.append(card)

        self.stack.update()

    def drag(self, event: ft.DragUpdateEvent):
        if not self.dragging_cards:
            return

        dx = event.local_delta.x
        dy = event.local_delta.y

        for card in self.dragging_cards:
            card.left = max(0, card.left + dx)
            card.top = max(0, card.top + dy)

        self.stack.update()

    def find_target_slot(self, reference_card):
        candidates = [
            (
                math.hypot(
                    reference_card.left - slot.left,
                    reference_card.top - slot.top,
                ),
                slot,
            )
            for slot in self.slots
        ]
        distance, slot = min(candidates, key=lambda item: item[0])
        return slot if distance <= DROP_DISTANCE else None

    def drop(self, event: ft.DragEndEvent):
        if not self.dragging_cards:
            return

        # Usa a carta que recebeu o gesto como referência ao destino.
        selected = event.control
        target = self.find_target_slot(selected)

        if target is None:
            self.restore_dragged_cards()
            self.finish_drag()
            return

        moving = set(self.dragging_cards)

        # Encontra cartas que já estão no slot de destino.
        destination_cards = [
            card for card in self.cards
            if card not in moving
            and abs(card.left - target.left) < 5
        ]

        # Empilha abaixo das cartas que já existem no destino.
        if destination_cards:
            base_top = max(card.top for card in destination_cards) + STACK_OFFSET
        else:
            base_top = target.top

        # Preserva os deslocamentos verticais entre as cartas arrastadas.
        first_card = self.dragging_cards[0]
        first_original_top = self.drag_origins[first_card][1]

        for card in self.dragging_cards:
            original_top = self.drag_origins[card][1]
            card.left = target.left
            card.top = base_top + (original_top - first_original_top)

        self.finish_drag()

    def restore_dragged_cards(self):
        for card, (left, top) in self.drag_origins.items():
            card.left = left
            card.top = top

    def finish_drag(self):
        self.dragging_cards = []
        self.drag_origins = {}
        self.stack.update()

    def build(self, page: ft.Page):
        self.page = page
        page.title = "Monster Solitaire"
        page.bgcolor = BACKGROUND
        page.padding = 20
        page.theme_mode = ft.ThemeMode.DARK

        self.slots = [
            self.make_slot(left)
            for left in SLOT_POSITIONS
        ]
        self.create_cards()

        self.stack = ft.Stack(
            width=510,
            height=300,
            controls=[*self.slots, *self.cards],
        )

        page.add(
            ft.Column(
                spacing=12,
                controls=[
                    ft.Text(
                        "MONSTER SOLITAIRE",
                        size=23,
                        weight=ft.FontWeight.BOLD,
                        color=ACCENT_COLOR,
                    ),
                    ft.Text(
                        "Arraste uma carta para mover ela e as cartas abaixo.",
                        size=13,
                        color=TEXT_COLOR,
                    ),
                    self.stack,
                    ft.Text(
                        "3 CARTAS • 3 ESPAÇOS • PILHAS ARRASTÁVEIS",
                        size=11,
                        color="#8DAA97",
                    ),
                ],
            )
        )
