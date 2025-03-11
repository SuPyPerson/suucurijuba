"""Lantean Module Sucuri.

Classes neste módulo:
    - :py:class:`Head` Add all stuff to head section.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    25.03
   |br| Classes Head (11).

|   **Open Source Notification:** This file is part of open source program **Suucurijuba**
|   **Copyright © 2025  Carlo Oliveira** <carlo@nce.ufrj.br>,
|   **SPDX-License-Identifier:** `GNU General Public License v3.0 or later <http:#is.gd/3Udt>`_.
|   `Labase <http:#labase.github.io/>`_ - `NCE <https:#portal.nce.ufrj.br>`_ - `UFRJ <https:#ufrj.br/>`_.
"""


class Head:
    def __init__(self, br, ht):
        def go(*_):
            ob.value = ib.value
        self.dom = br
        dc = br.document.body
        _ = dc <= (ib:=ht.TEXTAREA(cols=80, rows=60))
        _ = dc <= (ob:=ht.TEXTAREA("lantean", cols=80, rows=60, style=dict(fontFamily="anquietas")))
        bt = ht.BUTTON("GO")
        bt.bind("click", go)
        _ = dc <= bt
        style = ht.STYLE()
        style.textContent = self.add_face()

        # Append the <style> element to the <head> of the document
        _ = br.document.head <= style

    def add_face(self):
        _ = self
        font_face_rule = """
        @font-face {
            font-family: anquietas;
            src: url('/css/anquietas.ttf');
        
            font-weight: normal;
            font-style: normal;
        }
        """
        return font_face_rule

        # Create a <style> element and add the @font-face rule


def main(br=None, wk=None):
    """Main function."""
    Head(br, wk)
