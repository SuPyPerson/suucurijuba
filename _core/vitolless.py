""""Module Vitoless - Vitollino Headless.
class Container:
Classes neste módulo:
    - :py:class:`Head` Add all stuff to head section.
    - :py:function:`main` Set DOM hooks.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    25.01
   |br| Classes Head, Pane (09).

|   **Open Source Notification:** This file is part of open source program **Suucurijuba**
|   **Copyright © 2025  Carlo Oliveira** <carlo@nce.ufrj.br>,
|   **SPDX-License-Identifier:** `GNU General Public License v3.0 or later <http:#is.gd/3Udt>`_.
|   `Labase <http:#labase.activufrj.nce.ufrj.br/>`_ - `NCE <https:#portal.nce.ufrj.br>`_ - `UFRJ <https:#ufrj.br/>`_.
"""


class Coisa:
    def __init__(self, nome, descreve):
        """Inicializa uma instância de Coisa com nome e descrição."""
        self.nome = nome
        self.descreve = descreve

    def descrever(self):
        """Retorna a descrição da coisa."""
        return [self.nome, self.descreve]
    
    
class Cena(Coisa):
    def __init__(self, nome, descreve):
        """Initialize an empty container for objects."""
        super().__init__(nome, descreve)
        self.items = []

    def todos(self, opera):
        """Run an operation for all items in the container."""
        def para_todos(*args, **kwargs):
            items = self.items[:]
            [opera(*args, **kwargs) for _ in items]
        return para_todos

    def acolhe(self, item):
        """Add an object to the container."""
        self.items.append(item)

    def dispensa(self, item):
        """Remove an object from the container."""
        if item in self.items:
            self.items.remove(item)

    def move(self, cena, coisa=None):
        """Move an object from the container."""
        coisa = coisa or self.items[-1]
        cena.acolhe(coisa)
        self.dispensa(coisa)

    @property
    def itens(self):
        """Retrieve all objects in the container."""
        return self.items

    def encontra(self, name):
        """Find an object in the container by its name."""
        return next((item for item in self.items if item.nome == name), None)
    def __getitem__(self, param1):
        return self.items[param1]
    def __setitem__(self, param1, param2):
        self.items[param1] = param2
    def __delitem__(self, param1):
        del self.items[param1]
    def __len__(self):
        return len(self.items)
    def __contains__(self, param1):
        return True if param1 in self.items else False


def test():
    pass
from unittest import TestCase
class TestVitolless(TestCase):
    def coisa_to_cena(self, coisa, cena):
        cena = Cena(cena.capitalize(), f"Uma cena de {cena}")
        coisa = Coisa(coisa.capitalize(), f"Qualquer {coisa} vermelha")
        return cena, coisa
    def test_coisa_to_cena(self):
        cena, coisa = self.coisa_to_cena("bola", "praia")
        self.assertIsInstance(cena, Cena)
        self.assertIsInstance(coisa, Coisa)
        self.assertEqual(cena.nome, "Praia")
        self.assertEqual(coisa.nome, "Bola")
        self.assertEqual(cena.descreve, "Uma cena de praia")
        self.assertEqual(coisa.descreve, "Qualquer bola vermelha")
        cena.acolhe(coisa)
        self.assertIn(coisa, cena)
        self.assertEqual(cena.encontra("Bola"), coisa)
    def test_coisa_from_cena(self):
        parque = Cena("Parque", "Uma cena no parque")
        cena, coisa = self.coisa_to_cena("bola", "praia")
        cena.acolhe(coisa)
        self.assertIn(coisa, cena)
        self.assertEqual(cena.encontra("Bola"), coisa)
        cena.move(parque)
        self.assertIn(coisa, parque)
        self.assertNotIn(coisa, cena)
    def test_coisas_from_cena(self):
        parque = Cena("Parque", "Uma cena no parque")
        cena, coisa = self.coisa_to_cena("bola", "praia")
        balde = Coisa("Balde", "Qualquer balde verde")
        cena.acolhe(coisa)
        cena.acolhe(balde)
        self.assertIn(balde, cena)
        self.assertEqual(cena.encontra("Balde"), balde)
        cena.todos(cena.move(parque))
        # (cena.move(parque))
        # (cena.move(parque))
        self.assertIn(coisa, parque)
        self.assertNotIn(coisa, cena)
        self.assertIn(balde, parque)
        self.assertNotIn(balde, cena)

        
if __name__ == '__main__':
    import unittest
    unittest.main()

        