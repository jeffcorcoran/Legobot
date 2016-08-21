import ssl

import irc.client
import irc.connection
import irc.bot
import threading
from Lego import Lego

class IRCBot(threading.Thread, irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, baseplate, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        threading.Thread.__init__(self)
        self.channel = channel
        self.baseplate = baseplate

    def connect(self, *args, **kwargs):
        factory = irc.connection.Factory(wrapper=ssl.wrap_socket)
        self.connection.connect('irc.sithmail.com', 6697, 'TheOperative', connect_factory=factory)
        self.connection.join("#social")

    def on_pubmsg(self, c, e):
        text = e.arguments[0]
        metadata = {"source": self}
        message = {"text": text, "metadata": metadata}
        self.baseplate.tell(message)

    def run(self):
        self._connect()
        super(irc.bot.SingleServerIRCBot, self).start()


class IRCLego(Lego):
    def __init__(self, channel, nickname, server, baseplate, lock, port=6667):
        super().__init__(baseplate, lock)
        self.botThread = IRCBot(channel, nickname, server, baseplate, port)

    def on_start(self):
        self.botThread.start()

    def listening_for(self, message):
        return (str(self.botThread) != str(message['metadata']['source']))

    def on_failure(self, exception_type, exception_value, traceback):
        print(exception_type)
        print(exception_value)

    def handle(self, message):
        self.botThread.connection.privmsg("#social", message['text'])