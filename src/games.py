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
   |br| Classe Game (20).
   |br| Classes Tux and WpCurses (30).
   |br| Classe Cux (31).
   |br| Aprimora e documenta a Classe Cux (31).

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
        self.hook, self.go = hook, False
        self.std_scr = initscr()
        noecho()
        cbreak()
        curs_set(0)
        keypad(self.std_scr, True)
        start_color()
        init_pair(1, COLOR_YELLOW, COLOR_BLACK)  # used for the status bar
        clear()
        refresh()

    def set_interval(self, template, timing:float):
        this=self
        this.write(1, 77, "0")

        class Interval:
            def __init__(self):
                self.template = template
                self.timing = timing
                self._timer = None
                self.is_running = False
                self.cnt = 1
                self.start()

            def _run(self):
                self.is_running = False
                this.write(1,77, f"{self.cnt}")
                self.cnt += 1
                # self.__enter__()
                self.template(self)

            def start(self):
                from threading import Timer
                if not self.is_running:
                    self._timer = Timer(self.timing, self._run)
                    self._timer.start()
                    self.is_running = True
                return self

            def stop(self, exception_type, exception_value, exception_traceback):
                # Exception handling here
                self._timer.cancel()
                self.is_running = False
        return Interval()

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
        self.palavra = self.disparo = None  # o nome do cometa que cai
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
        self.gui.set_interval(self.disparar,1)
        self.gui.going(self.atira, lambda *_: self.run_tux())

        return False

    def disparar(self, timer):
        altura = Tux.WY - self.altura-1
        limpa = " " * 61
        texto = limpa
        self.gui.write(altura, Tux.WX, texto)
        self.altura -= 1
        altura = Tux.WY - self.altura-1
        texto = f"{self.palavra} {self.altura}"
        self.gui.write(altura, Tux.WX, texto)
        if self.altura <= 0:
            timer.stop(None, None, None)
        if self.chuva >= 0:
            timer.start()

    def atira(self, k):
        def fim(texto=f"Fim do Jogo, você desistiu"):
            self.run_tux = lambda *_: self.gui.ender(self.ender)
            return self.atualiza(texto, limpa)
        limpa = " " * 61
        if chr(k) in "0":
            return fim()
        self.atualiza(limpa, limpa)
        # self.altura -= 1
        if self.altura * self.tentativas == 0:
            return fim(f"Você perdeu, o meteoro {self.palavra} destruiu o planeta")
        self.disparo = p = palavra = self.letras + chr(k)
        vai = self.palavra.startswith(palavra)
        self.letras, palavra, self.tentativas = (p, p, self.tentativas) if vai else ("", limpa, self.tentativas-1)
        self.atualiza(palavra)
        if self.palavra == palavra:
            return self.atualiza(limpa, limpa)
        return True

    def atualiza(self, palavra=None, limpa=None):
        altura = Tux.WY - self.altura-1
        palavra = palavra or self.disparo
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
    CW, MM, MP, DZ, DC = 10, MX+12, MX+5, 11, DX+14
    MAX_COUNT = 190

    def __init__(self, gui):
        from re import compile
        self.pattern = compile("AAA+|EEE+|III+|OOO+|UUU+")
        self.num = "-0123456789\n"  # para testar letras quando forem coordenadas
        self.run_cux = self.cux  # run_cux vai inicialmente ser cux
        self.pontos = 0
        self.estoque = "".join([kind for _ in range(3) for kind in "AEIOU"])
        self.pilhas = self.cria_pilhas()
        self.letras = ""  # código para buscar as letras a serem movidas
        self.movidos = 0  # número de letras movidas
        self.gui = gui
        self.gui.window(Cux.WY, Cux.WW, 0, Cux.WC)
        self.display = self.gui.window(3, Cux.WW, Cux.DR, Cux.WC)
        for _ in range(Cux.MAX_COUNT):
            self.pilhas = self.cria_pilhas()
            if not self.verificar(self.pilhas):
                break
        self.atualiza("Escreva uma sequencia seguida de + o -")
        self.cux()  # executa o início do tux typing

    def cria_pilhas(self):
        """
        Cria as pilhas sorteando letras do estoque.
        :return: Matriz de pilhas.
        """
        from random import sample
        return ["".join(sample(self.estoque, Cux.CW)) for _ in range(Cux.CW)]

    def cux(self):
        """Inicia o jogo do Cux. Usa o loop de chamada da GUI"""
        self.gui.going(self.move, lambda *_: self.run_cux())

    def atualiza(self, palavra, limpa=None) -> bool:
        """ Atualiza a tela com a matriz e a matriz invertida.
        :param limpa: Mensagem de saída do aplicativo.
        :param palavra: Mensagem para imprimir na linha de display.
        :return: True se não é mensagem final.
        """
        ilhas = zip(*self.pilhas)
        [self.gui.write(5+row, Cux.DX, letras) for row, letras in enumerate(self.pilhas)]
        [self.gui.write(5+row, Cux.DC, "".join(letras)) for row, letras in enumerate(ilhas)]
        self.gui.write(Cux.DY, Cux.MX, f"M:{self.movidos:3} P:{self.pontos:04} {palavra} {' '*(49-len(palavra))}")
        return limpa is None

    def verificar(self, pilhas) -> list:
        """ Usa expressão regular para ver se tem três ou mais tipos iguais consecutivos.

        :param pilhas: A matriz de palavras a verificar.
        :return: Lista de pares individuais de letras pertencentes aos consecutivos.
        """
        rx = [(mx.start(), mx.end()) for mx in self.pattern.finditer(" ".join(pilhas))]
        """ Acha os marcadores de início e fim dos iguais consecutivos na horizontal."""
        pilhas = ["".join(letras) for letras in zip(*pilhas)]
        """ Inverte a matriz de letras."""
        ry = [(mx.start(), mx.end()) for mx in self.pattern.finditer(" ".join(pilhas))]
        """ Acha os marcadores de início e fim dos iguais consecutivos na vertical."""
        rmv = [(x//Cux.DZ, x % Cux.DZ) for rgx in ry for x in range(*rgx)]
        rmv += [(x % Cux.DZ, x // Cux.DZ) for rgx in rx for x in range(*rgx)]
        """ Expande as sequências em pares ordenados para cada letra participante."""
        rmv = list(set(rmv))
        rmv = sorted(rmv)
        return rmv  # retorna os pares em ordem crescente para que o pop funcione.

    def remove(self, hits):
        """ Remove as letras que estão marcadas por pertencer a grupos de iguais.

        :param hits: Coordenadas das letras a serem removidas.
        :return: None
        """
        from random import sample
        pilhas = [sample(self.estoque, Cux.CW)+list(letras) for letras in zip(*self.pilhas)]
        """Aumenta cada pilha para que novas letras sejam inseridas ao remover uma letra."""
        [pilhas[col].pop(row-Cux.CW) for col, row in hits]
        """ Remove e rotaciona a pilha para cada letra. Posição é contada a partir da direita"""
        pilhas = [col[-Cux.CW:] for col in pilhas]
        """ Recorta as pilhas no tamanho certo, removendo a pilha extra não rotacionada."""
        self.pilhas = ["".join(letras) for letras in zip(*pilhas)]

    def move(self, k):
        """
        Movimenta uma letra escolhida como um código de coordenada X.Y.(H, V)
        ou como uma busca de uma string dentro das pilhas AEIOU(-, =).
        O "-" indica que a primeira letra da busca é trocada e "=" a última letra.

        :param k: Letra recebida do input do usuário.
        :return: False se o usuário escolheu terminar, True se continua.
        """
        def fim(texto=f"Fim do Jogo, você desistiu"):
            """Executa a finalização da interface gráfica."""
            self.run_cux = lambda *_: self.gui.ender(self.ender)
            return self.atualiza(texto, limpa)
        
        def mover(ix_, string_):
            """ Move uma letra da matriz indicada pelo índice.

            :param ix_: Índice da letra que vai ser trocada com a próxima.
            :param string_: Representa as matrizes de pilhas horizontais e verticais.
            :return: None
            """
            self.movidos += 1
            ix_ += 0 if lk in self.num else len(self.letras) - 2
            string_ = list(string_)
            string_[ix_], string_[ix_ + 1] = string_[ix_ + 1], string_[ix_]
            string_ = "".join(string_)
            string_ = string_[:110] if ix_ < 110 else " ".join(
                ["".join(letras) for letras in zip(*string_[110:].split())])
            self.pilhas = [row for row in string_.split()]
            while oxy := self.verificar(self.pilhas):
                self.pontos += len(oxy)
                self.remove(oxy) if oxy else None

        END, GO, CODE, BAD, FOUND, SKIP = "END, GO, CODE, BAD, FOUND, SKIP".split(", ")
        lk, lt, ix, limpa = chr(k), self.letras, -1, " " * 61
        string = " ".join(self.pilhas) + " " + " ".join(["".join(letras) for letras in zip(*self.pilhas)])
        """Concatena uma string com as linhas e outra com as colunas."""
        st = CODE if (len(lt) == 5) and (lt[-2] == ".") else FOUND if (ix := string.find(self.letras)) > -1 else SKIP
        """Diferencia os dois modos de especificar a letra que move. 0.0.0: CODE, AEIOU: FOUND"""
        st = BAD if (st == CODE) and not (lt[0]+lt[2]+lt[4]).isnumeric() else st
        """Valida o modo code que deve conter apenas algarismos."""
        st = END if lk in "q" else GO if lk not in "+-=\n" else st
        """Testa se termina ou continua."""

        match st:
            case "END":  # END
                return fim()
            case "GO" | "SKIP":  # GO
                self.letras += lk.upper()
                self.atualiza(self.letras)
                return True
            case "BAD":  # BAD
                self.letras = ""
                return True
            case "CODE":  # CODE
                ix = (lambda a, b, c: int(c)*110+int(a)*11 + int(b))(*self.letras.split("."))
                mover(ix, string)
            case "FOUND":  # FOUND
                mover(ix, string)
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
    tux = Tux(WpCurses())
