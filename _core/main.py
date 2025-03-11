""""Main Module Sucuri.

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
# from browser import bind, document, worker

# Create a web worker, identified by a script id in this page.


class Head:
    def __init__(self, br, wk):
        self.dom = br
        self.conta = 0
        self.aumenta = 1
        app = br.document["app"]
        self.btn = br.html.BUTTON(f"conta {self.conta}")
        self.stp = br.html.BUTTON(f"Para")
        _ = app <= self.btn
        _ = app <= self.stp
        # self.btn.bind("click", self.contou)
        self.stp.bind("click", self.parou)
        # x = self.dom.worker.create_worker("prime_worker", self.on_ready, self.onmessage)
        x = wk.create_worker("prime_worker", self.on_ready, self.onmessage)
        print("init", self.aumenta, x)

    def parou(self, *args):
        self.conta += 1
        self.btn.text = f"conta {self.conta}"

    def contou(self, *args):
        self.conta += 1
        self.btn.text = f"conta {self.conta}"

    def onmessage(self, e):
        """Handles the messages sent by the worker."""
        # result.text = e.data
        self.conta = e.data
        self.btn.text = f"conta {self.conta}"

    def on_ready(self, my_worker):
        print("on_ready", self.aumenta, my_worker)

        @self.dom.bind(self.btn, "click")
        def change(evt):
            """Called when the value in one of the input fields changes."""
            print(self.conta, self.aumenta)
            # Send a message (here a list of values) to the worker
            my_worker.send(self.aumenta)


def adder():

    from browser import bind, document, worker
    print("Create Worker")

    result = document.select_one('.result')
    inputs = document.select("input")

    def onmessage(e):
        """Handles the messages sent by the worker."""
        result.text = e.data

    def onready(myWorker):

        @bind(inputs, "change")
        def change(evt):
            """Called when the value in one of the input fields changes."""
            # Send a message (here a list of values) to the worker
            print("Worker ready", [x.value for x in inputs])
            myWorker.send([x.value for x in inputs])

    # Create a web worker, identified by a script id in this page.
    worker.create_worker("prime_worker", onready, onmessage)
    print(" Worker Created")



def main(br=0, wk=0):
    """Main function."""
    # Head(br, wk)
    adder()
