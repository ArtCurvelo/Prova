# Monster Solitaire

Protótipo de Solitário em Python com Flet, dividido em módulos.

## Estrutura

- `main.py`: ponto de entrada do aplicativo.
- `game.py`: tabuleiro, pilhas, arraste e encaixe.
- `cards.py`: componente visual das cartas.
- `constants.py`: tamanhos, posições e cores.
- `requirements.txt`: dependência do projeto.

## Executar no Windows

Abra o terminal nesta pasta e execute:

```powershell
py -m pip install -r requirements.txt
py main.py
```

Se estiver usando um ambiente virtual, ative-o antes de instalar as dependências.

## Controles

- Arraste uma carta para mover essa carta e todas as cartas abaixo dela.
- Solte perto de um dos três espaços para encaixar a pilha.
- Se soltar longe dos espaços, a pilha retorna à posição anterior.

Este é um protótipo visual; as regras completas de um jogo de Solitário ainda não foram implementadas.
