""""Module Aventura Sucuri.

Classes neste módulo:
    - :py:class:`Head` Add all stuff to head section.
    - :py:function:`main` Set DOM hooks.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    24.12
   |br| Classes Head, Pane (10).

|   **Open Source Notification:** This file is part of open source program **Pynoplia**
|   **Copyright © 2024  Carlo Oliveira** <carlo@nce.ufrj.br>,
|   **SPDX-License-Identifier:** `GNU General Public License v3.0 or later <http:#is.gd/3Udt>`_.
|   `Labase <http:#labase.selfip.org/>`_ - `NCE <https:#portal.nce.ufrj.br>`_ - `UFRJ <https:#ufrj.br/>`_.
"""


class Head:
    def __init__(self):
        import tomllib
        self.zonas = {}
        self.locais = {}
        self.objetos = {}
        self.verbos = {}
        self.mestre = []
        self.owner = "__MAIN__"
        self.container = self.mestre

        with open("adv.toml", "rb") as f:
            data = tomllib.load(f)
            self.parse(data)
        print(self.zonas)
        print(self.locais)
        print(self.mestre)
        print(self.objetos)
        print(self.verbos)

    def parse(self, data, owner=None):
        owner = owner or self.mestre
        # if not isinstance(data, dict):
        match data:
            case str() as var:
                # print(data)
                return data
        for key, value in data.items():
            # print(key, self.parse(value))
            match key.lower()[0]:
                case "z":
                    self.zona(value, key)
                case "i":
                    self.iniciar(value)
                case "l":
                    self.local(value, key)
                case "d":
                    self.descreve(value)
                case "o":
                    self.objeto(value, key)
                case "v":
                    self.verbo(value, key)
                case "f":
                    self.fecha(value, key)
                case "b":
                    self.bastou(value)
                case "n":
                    self.negou(value)

    def iniciar(self, data):
        print(data)

    def zona(self, data, owner):
        self.container.append(owner)
        # self.mestre.append(owner)
        self.owner = owner
        self.zonas[owner] = []
        self.container = self.zonas[owner]
        self.parse(data)

    def local(self, data, owner):
        self.container.append(owner)
        self.owner = owner
        self.locais[owner] = []
        self.container = self.locais[owner]
        self.parse(data)

    def descreve(self, data):
        self.container.append(data)

        print(data)

    def objeto(self, data, owner):
        self.container.append(owner)
        self.owner = owner
        self.objetos[owner] = []
        self.container = self.objetos[owner]
        self.parse(data)

    def verbo(self, data, owner):
        self.container.append(owner)
        self.owner = owner
        self.verbos[owner] = []
        self.container = self.verbos[owner]
        self.parse(data)
        pass

    def fecha(self, data, key):
        self.container.append(data)

        print(data)

    def bastou(self, data):
        self.container.append(data)

    def negou(self, data):
        self.container.append(data)


def main():
    """Main function."""
    Head()


if __name__ == '__main__':
    main()
