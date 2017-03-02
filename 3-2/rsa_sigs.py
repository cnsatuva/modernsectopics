from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from Crypto.PublicKey import RSA
import logging

class Notary(LineReceiver):
    def __init__(self):
        self.delimiter = '\n'
        self.name = None
        self.key = RSA.generate(2048)
        self.signed_messages = [0, 1]
        self.state = 'GETNAME'
        logging.info('new connection')

    def connectionMade(self):
        self.sendLine("Hey it's your pal Elon Musk. What's your name?")

    def handle_GETNAME(self, name):
        self.name = name
        self.sendLine('Welcome, %s! Here is my public key:' % name)
        logging.info('welcome %s' % name)
        self.sendLine('e = %s' % self.key.e)
        self.sendLine('n = %s' % self.key.n)
        self.signed_messages.append(n - 1)  # (-1)^e = -1
        self.sendLine('Want a signature?')
        self.state = 'GOTNAME'

    def sign(self, message):
        logging.info('signing %s' % message)
        try:
            message = long(message)
        except ValueError as e:
            # invalid literal
            self.sendLine('Your message should be a number')
            logging.warning(str(e))
            return
        if message == 1337:
            self.sendLine('Haha nice try')
            return

        try:
            ''' From the docs:
            "Attention: this function performs the plain, primitive RSA
            decryption (textbook). In real applications, you always need
            to use proper cryptographic padding, and you should not
            directly sign data with this method. Failure to do so may
            lead to security vulnerabilities. It is recommended to use
            modules Crypto.Signature.PKCS1_PSS or
            Crypto.Signature.PKCS1_v1_5 instead."
            But I like my crypto like I like my Vibrams '''
            sig = self.key.sign(message, None)[0]
        except ValueError as e:
            # Ciphertext too large
            self.sendLine(str(e))
            logging.warning(str(e))
            return

        self.signed_messages.append(message)
        self.sendLine(str(sig))

    def verify(self, message, sig):
        logging.info('verify %s, %s' % (message, sig))
        try:
            message = long(message)
        except ValueError as e:
            # invalid literal
            self.sendLine('Your message should be a number')
            logging.warning(str(e))
            return

        try:
            sig = long(sig)
        except ValueError as e:
            # invalid literal
            self.sendLine('Your signature should be a number')
            logging.warning(str(e))
            return

        if self.key.verify(message, (sig, None)):
            if message in self.signed_messages:
                self.sendLine('Yep that checks out')
                logging.info('valid signature')
            else:
                if message == 1337:
                    self.sendLine('Wow if I signed this for you, you can come to Mars whenever you like.')
                    logging.info('selective forgery by %s' % self.name)
                else:
                    self.sendLine("How'd you get this signature? I'm gonna have to ban you from Mars.")
                    logging.info('existential forgery by %s' % self.name)
        else:
            self.sendLine('No way is that my signature')
            logging.info('bad signature')

    def lineReceived(self, line):
        if self.state == 'GETNAME':
            self.handle_GETNAME(line)
        else:
            logging.info('received command: %s' % line)
            command = line.split(' ')

            if command[0] == 'sign':
                if len(command) != 2:
                    self.sendLine('Usage: sign <message>')
                    return
                self.sign(command[1])

            elif command[0] == 'verify':
                if len(command) != 3:
                    self.sendLine('Usage: verify <message> <signature>')
                    return
                self.verify(command[1], command[2])

            else: # help
                self.sendLine('Usage:')
                self.sendLine('sign <message>')
                self.sendLine('verify <message> <signature>')



def main():
    logging.basicConfig(filename='rsa.log', level=logging.DEBUG)

    # Create the server
    f = Factory()
    f.protocol = Notary
    reactor.listenTCP(1977, f)
    reactor.run()

if __name__ == '__main__': main()
