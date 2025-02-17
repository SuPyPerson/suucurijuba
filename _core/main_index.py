""""Configure Sucuri from Brython.

Classes neste módulo:
    - :py:class:`Head` Add all stuff to head section.
    - :py:function:`initial` Set DOM hooks.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    24.10
   |br| Classes Head, Pane (26).

|   **Open Source Notification:** This file is part of open source program **Pynoplia**
|   **Copyright © 2024  Carlo Oliveira** <carlo@nce.ufrj.br>,
|   **SPDX-License-Identifier:** `GNU General Public License v3.0 or later <http:#is.gd/3Udt>`_.
|   `Labase <http:#labase.selfip.org/>`_ - `NCE <https:#portal.nce.ufrj.br>`_ - `UFRJ <https:#ufrj.br/>`_.
"""
from browser import window, document, alert, html, timer


class Head:
    """Add all stuff to head section"""
    # SL = "editor lecture fa6.6.all.min darcula mermaid.min darcula.min prism-funky.min".split()
    GM = None
    SL = "fa6.6.all.min darcula darcula.min prism-funky.min accordion_style lecture editor".split()
    STLIB = (f"/_core/css/{st}.css" for st in SL)
    HEAD = document.head
    BODY = document.body
    J1 = "ace1.36.2.min mode1.36.2-python.min.js theme-1.36.2gruvbox.min ext1.36.2-language_tools.min"
    J2 = "external-script.min docsify.min accordion.index docsify-sidebar-collapse.min"
    SCT = (f"/_lib/{st}.js" for st in J1.split())
    SCB = (f"/_lib/{st}.js" for st in J2.split())
    git = "https://raw.githubusercontent.com/SuPyPerson/SuPyPerson.github.io/"
    PATH = dict(i="jaie24", o="sbce", f="guia", n="snct", k="pyjr", c="snct/guia", q="pyjr/guia",
                    j=git + "jaie24/jaie24/", p=git + "sbce/sbce", g=git + "jaie24/guia", m=git + "snct/snct",
                    l=git + "pyjr"
                    )
    REL = dict(i="JAIE24", o="SBCE", f="JAIE Guia", n="SNCT", k="Py Jr.", c="SNCT Guia",
               j="JAIE24/", p="SBCE", g="JAIE Guia", m="SNCT", l="Py Jr.", q="Agentes Guia")
    G = dict(a="Agentes da Escola", p="Help Pet", d="Descarte de Medicamentos", r="Recicla")

    def __init__(self, ln=html.LINK, st=html.SCRIPT):
        def append(child, node=self.HEAD):
            _ = node <= child

        window.docBasePath = "snct"
        # [append(st(src=hr)) for hr in self.SCT]
        # [append(ln(rel="stylesheet", href=hr)) for hr in self.STLIB]
        # append(st(src="/_lib/main_index.js"), self.BODY)
        # self.scripter()
        # timer.set_timeout(self.scripter, 50)
        # timer.set_timeout(self.pos_scripter, 90)
        # timer.set_timeout(self.poster_scripter, 900)

    def scripter(self, st=html.SCRIPT, *_):
        def append(child, node=self.HEAD):
            _ = node <= child

        append(st(src="/_lib/ga.min.js"), self.BODY)

    def pos_scripter(self, st=html.SCRIPT, *_):
        def append(child, node=self.HEAD):
            _ = node <= child

        [append(st(src=hr), self.BODY) for hr in self.SCB]

    def poster_scripter(self, st=html.SCRIPT, *_):
        def append(child, node=self.HEAD):
            _ = node <= child

        append(st(src="/_lib/prism-python.min.js"), self.BODY)

    def game_page(self):
        self.BODY.html = ""
        jogo = html.DIV(id="_jogo_")
        _ = self.BODY <= jogo
        _ = self.BODY <= html.DIV(html.SPAN("version:", Class="curversion"),
                                  style="position:absolute; top:650px; left:2px; height: 10px;")

    def gamer(self):
        self.game_page() if self.GM else None
        match self.GM:
            case "a":
                from age.main import main
                main()
            case "p":
                import pet.main
            case "r":
                import rec.main
            case "d":
                import des.main


def initial(h):
    from browser import window, document, alert, html, timer
    from browser.session_storage import storage

    def clipboard_show(bt):
        btp = bt.parent.previousSibling
        # storage[PLB] = btp.text
        window.navigator.clipboard.writeText(btp.text)

    try:
        sw.SPR = window.__SP_RELEASE__
    except Exception as e:
        queryString = window.location.search
        urlParams = window.URLSearchParams.new(queryString)
        sw.SPR = urlParams.get('rel') or "k"
        Head.GM = urlParams.get('g') or None
        sw.HOST = window.location.origin
        window.__SP_RELEASE__ = Head.PATH[sw.SPR]
    print("urlParams.get('rel')", sw.SPR)
    h.gamer() if Head.GM else None

    window.__widget__ = show
    window.__did_got__ = build
    window.__copy_clip__ = clipboard_show
    title = Head.REL[sw.SPR]
    title = Head.G[Head.GM] if Head.GM is not None else title
    document.title = f"SuucuriJuba {title}"


def main():
    h = Head()
    # initial(h)
    document.title = f"SuucuriJuba"


if __name__ == '__main__':
    main()
