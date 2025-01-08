"""Web Worker script."""

# In web workers, "window" is replaced by "self".
from browser import bind, self

@bind(self, "message")
def message(evt):
    """Handle a message sent by the main script.
    evt.data is the message body.
    """
    try:
        result = int(evt.data[0]) * int(evt.data[1])-1
        workerResult = f'Result: {result}'
        # Send a message to the main script.
        # In the main script, it will be handled by the function passed as the
        # argument "onmessage" of create_worker().
        self.send(workerResult)
    except ValueError:
        self.send('Please write two numbers')
