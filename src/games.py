""""Game Module Sucuri.

Classes neste módulo:
    - :py:class:`Game` A game for guessing a word.
    - :py:class:`Tux` A game for typing practice.
    - :py:class:`Cux` A game to join three or more figures.
    - :py:class:`WpCurses` A wrapper for the curses library.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    24.12
   |br| Classes Game (20).
   |br| Classes Tux and WpCurses (30).
   |br| Classes Cux (31).

|   **Open Source Notification:** This file is part of open source program **Suucurijuba**
|   **Copyright © 2024  Carlo Oliveira** <carlo@nce.ufrj.br>,
|   **SPDX-License-Identifier:** `GNU General Public License v3.0 or later <http:#is.gd/3Udt>`_.
|   `Labase <http:#labase.selfip.org/>`_ - `NCE <https:#portal.nce.ufrj.br>`_ - `UFRJ <https:#ufrj.br/>`_.
"""


class Game:
    def __init__(self):
        self.palavras = "cachorro soldado".split()  # lita de palavras
        self.letras = ""  # conjunto de letras já tentadas
        self.tentativas = 8
        self.boneco = "- -o -o- -o-_ -o-= -o-=- -o-=-_ -o-=-<".split()
        self.palavra = None  # a palavra que vai ser sorteada como enigma
        self.forca()  # executa o início da forca

    def forca(self):
        """Inicia o jogo da forca."""
        from random import choice
        self.palavra = choice(self.palavras)
        enigma = "_"*len(self.palavra)
        self.jogar(enigma)

    def jogar(self, enigma):
        """O laço principal do jogo que se repete a cada jogada recursivamente.

        :param enigma: O texto atual do enigma, marcando as incógnitas com "_".
        :return: None
        """
        forca = f"a forca está assim: {self.boneco[8-self.tentativas]}, os seus chutes foram: {self.letras}"
        print(forca)
        prompt = f"O enigma é {enigma}, escolha uma letra: "
        letra = input(prompt)
        self.letras += letra
        par = zip(enigma, self.palavra)
        """A função zip converte uma matriz axb numa bxa. O par ficaria [(_,s), (_,o),...]"""
        enigma = "".join([lp if lp in letra+le else "_" for le, lp in par])
        """le e lp são letras do enigma e da palavra. Gera lp se lp é le ou letra, senão "_"."""
        if "_" not in enigma:
            print("você acertou")
        elif self.tentativas <= 2:
            print(f"a forca ficou assim assim: {self.boneco[-1]}")  # [-1] é o fim da lista
            print("você perdeu")
        else:
            self.tentativas -= 1 if letra not in self.palavra else 0
            self.jogar(enigma)


from unicurses import initscr, clear, refresh, getch, endwin, mvaddstr
from unicurses import echo, nocbreak, newwin, wborder, wrefresh
from unicurses import noecho, cbreak, curs_set, keypad, start_color, init_pair, COLOR_BLACK, COLOR_YELLOW


class WpCurses:
    """Classe auxiliar para isolar a interface curses"""
    def __init__(self, hook=lambda *_: None) -> None:
        self.hook = hook
        self.std_scr = initscr()
        noecho()
        cbreak()
        curs_set(0)
        keypad(self.std_scr, True)
        start_color()
        init_pair(1, COLOR_YELLOW, COLOR_BLACK)  # used for the status bar
        clear()
        refresh()

    def window(self, height, width, row, col):
        win = newwin(height, width, row, col)
        wborder(win, 0, 0, 0, 0, 0, 0, 0, 0)
        wrefresh(win)
        return win

    def write(self, y, x, text) -> None:
        mvaddstr(y, x, text)

    def go(self, hook=None) -> None:
        self.hook = hook or self.hook
        self.hook(getch())

    def going(self, hook=None, hooked=None) -> None:
        self.hook = hook or self.hook
        k = getch()
        while self.hook(k):
            k = getch()
        # hooked(k) if hooked else self.ender(k)
        self.ender() if hooked(k) else None

    def ender(self, hook=None):
        self.hook = hook or self.hook
        k = getch()
        clear()
        refresh()
        nocbreak()
        keypad(self.std_scr, False)
        echo()
        endwin()
        self.hook(k)


class Tux:
    """Imita o jogo Tux typing para ensinar digitação rápida"""
    DY, DX, DR, WX, WY, WW, WC, MX = 21, 12, 20, 10, 20, 70, 5, 6

    def __init__(self, gui):
        self.palavras = PAL.split()  # lita de palavras
        self.letras = ""  # conjunto de letras já tentadas
        self.tentativas = Tux.WY  # número de mísseis disponíveis
        self.palavra = None  # o nome do cometa que cai
        self.chuva = 10  # número de meteoros nesta leva
        self.altura = Tux.WY - 2
        self.gui = gui
        self.gui.window(Tux.WY, Tux.WW, 0, Tux.WC)
        self.display = self.gui.window(3, Tux.WW, Tux.DR, Tux.WC)
        self.run_tux = self.tux
        self.tux(f"Você tem {self.tentativas} misseis para derrubar o meteoro, digitando o nome")
        # executa o início do tux typing

    def tux(self, texto=""):
        """Inicia o jogo do Tux."""
        from random import choice
        self.palavra = choice(self.palavras).lower()
        self.altura = Tux.WY - 2
        self.letras = ""  # conjunto de letras já tentadas
        if self.chuva == 0:
            self.atualiza(f"Você eliminou todos os meteoros, sobraram {self.tentativas} misseis", " "*61)
            self.run_tux = lambda *_: self.gui.ender(self.ender)
            return True
        self.chuva -= 1
        self.atualiza(texto)
        self.gui.going(self.atira, lambda *_: self.run_tux())
        return False

    def atira(self, k):
        def fim(texto=f"Fim do Jogo, você desistiu"):
            self.run_tux = lambda *_: self.gui.ender(self.ender)
            return self.atualiza(texto, limpa)
        limpa = " " * 61
        if chr(k) in "0":
            return fim()
        self.atualiza(limpa, limpa)
        self.altura -= 1
        if self.altura * self.tentativas == 0:
            return fim(f"Você perdeu, o meteoro {self.palavra} destruiu o planeta")
        p = palavra = self.letras + chr(k)
        vai = self.palavra.startswith(palavra)
        self.letras, palavra, self.tentativas = (p, p, self.tentativas) if vai else ("", limpa, self.tentativas-1)
        self.atualiza(palavra)
        if self.palavra == palavra:
            return self.atualiza(limpa, limpa)
        return True

    def atualiza(self, palavra, limpa=None):
        altura = Tux.WY - self.altura-1
        texto = limpa if limpa else f"{self.palavra} {self.altura}"
        self.gui.write(Tux.DY, Tux.DX, f"{palavra}")
        self.gui.write(Tux.DY, Tux.MX, f"M:{self.tentativas:3}")
        self.gui.write(altura, Tux.WX, texto)
        return limpa is None

    def ender(self, *_):
        print("Volte sempre para salvar o planeta...")


class Cux:
    """Imita o jogo tipo Candy Crush"""
    DY, DX, DR, WX, WY, WW, WC, MX = 21, 12, 20, 10, 20, 70, 5, 6

    def __init__(self, gui):
        from re import compile
        self.pattern = compile("AAA+|EEE+|III+|OOO+|UUU+")
        self.run_cux = self.cux
        self.pontos = 0
        estoque = []
        _ = [estoque.extend([kind]*3) for kind in "AEIOU"]
        self.estoque = "".join(estoque)
        self.pilhas = self.cria_pilhas()
        self.letras = ""  # conjunto de letras já tentadas
        self.movidos = 0  # número de meteoros nesta leva
        self.altura = Cux.WY - 2
        self.gui = gui
        self.gui.window(Cux.WY, Cux.WW, 0, Cux.WC)
        self.display = self.gui.window(3, Cux.WW, Cux.DR, Cux.WC)
        self.oxy = []
        for _ in range(190):
            self.pilhas = self.cria_pilhas()
            self.oxy = self.verificar(self.pilhas)
            if len(self.oxy) <= 0:
                break
        # self.atualiza(" ".join(f"{a}{b}" for a, b in self.oxy))
        self.atualiza("Escreva uma sequencia seguida de + o -")
        self.cux()
        # executa o início do tux typing

    def cria_pilhas(self):
        from random import sample
        return ["".join(sample(self.estoque, 10)) for _ in range(10)]

    def cux(self):
        self.gui.going(self.move, lambda *_: self.run_cux())

    def atualiza(self, palavra, limpa=None):
        ilhas = zip(*self.pilhas)
        [self.gui.write(5+row, Cux.DX, letras) for row, letras in enumerate(self.pilhas)]
        [self.gui.write(5+row, Cux.DX+14, "".join(letras)) for row, letras in enumerate(ilhas)]
        self.gui.write(Cux.DY, Cux.MX+12, f" "*49)
        self.gui.write(Cux.DY, Cux.MX+12, f"{palavra}")
        self.gui.write(Cux.DY, Cux.MX, f"M:{self.movidos:3}")
        self.gui.write(Cux.DY, Cux.MX+4, f"P:{self.pontos:04}")
        return limpa is None

    def verificar(self, pilhas):
        rx = [(mx.start(), mx.end()) for mx in self.pattern.finditer(" ".join(pilhas))]
        pilhas = ["".join(letras) for letras in zip(*pilhas)]
        ry = [(mx.start(), mx.end()) for mx in self.pattern.finditer(" ".join(pilhas))]
        rmv = [(x//11, x % 11) for rgx in ry for x in range(*rgx)]
        rmv += [(x % 11, x // 11) for rgx in rx for x in range(*rgx)]
        rmv = list(set(rmv))
        rmv = sorted(rmv)
        return rmv

    def remove(self, hits):
        from random import sample
        pilhas = [sample(self.estoque, 10)+list(letras) for letras in zip(*self.pilhas)]
        [pilhas[col].pop(row-10) for col, row in hits]
        pilhas = [col[-10:] for col in pilhas]
        self.pilhas = ["".join(letras) for letras in zip(*pilhas)]

    def move(self, k):
        def fim(texto=f"Fim do Jogo, você desistiu"):
            self.run_cux = lambda *_: self.gui.ender(self.ender)
            return self.atualiza(texto, limpa)
        limpa = " " * 61
        if chr(k) in "0":
            return fim()

        lk = chr(k)
        if lk not in "+-=":
            self.letras += lk.upper()
            self.atualiza(self.letras)
            return True
        string = " ".join(self.pilhas)
        ix = string.find(self.letras)
        if ix > -1:
            self.movidos += 1
            ix += 0 if lk in "-" else len(self.letras)-2
            string = list(string)
            string[ix], string[ix+1] = string[ix+1], string[ix]
            string = "".join(string)
            self.pilhas = [row for row in string.split()]
            self.letras = ""
            while oxy := self.verificar(self.pilhas):
                self.pontos += len(oxy)
                self.remove(oxy) if oxy else None
            self.atualiza(" ".join(f"{a}{b}" for a, b in oxy))
        self.letras = ""
        self.atualiza(self.letras)
        return True

    def ender(self, *_):
        print("Volte sempre para salvar o planeta...")


PAL = """Axioma
Azulejo
Blitz
Catarro
Crespo
Cripta
Duplex
Girar
Haicai
Hera
Indigno
Intrigante
Jazz
Linfa
Marfim
Psique
Quartzo
Quiz
Quorum
Tonto
Torpor
Valsa
Vaporizar
Vertiginoso
Vicissitude
Xilofone"""

if __name__ == '__main__':
    """Esta fórmula é chavão em python para só executar se for main e não se for importado"""
    # game = Game()
    # tux = Tux(WpCurses())
    tux = Cux(WpCurses())
