from Lego import Lego
from Message import *
import json

class PrintTips(Lego):
    def __init__(self, baseplate, lock, tips_file='tips.json'):
        super().__init__(baseplate, lock)
        self.tips_file = tips_file

    def listening_for(self, message):
        return message['text'].split()[0] == '!printtips'

    def handle(self, message):
        with open(self.tips_file, mode='r') as f:
            json_str = f.read()
            print(json_str)
            try:
                tips = json.loads(json_str)
            except:
                print('Failed to read in printtips')
                tips = {}
            for tip in tips:
                metadata = Metadata(source=self, dest=message['metadata']['source']).__dict__
                message = Message(text=(str(tip) + ': ' + str(tips[tip])), metadata=metadata).__dict__
                self.baseplate.tell(message)
