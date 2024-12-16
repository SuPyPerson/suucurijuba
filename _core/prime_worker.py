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
# In web workers, "window" is replaced by "self".
from browser import bind, self


@bind(self, "message")
def message(evt):
    """Handle a message sent by the main script.
    evt.data is the message body.
    """
    try:
        result = int(evt.data)+2
        workerResult = f'{result}'
        # Send a message to the main script.
        # In the main script, it will be handled by the function passed as the
        # argument "onmessage" of create_worker().
        self.send(workerResult)
        # self.send(result)
    # except ValueError:
    except Exception as e:
        self.send('11111')
