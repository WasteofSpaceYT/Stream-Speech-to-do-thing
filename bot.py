import logging
import sys

from irc.bot import SingleServerIRCBot

# config
HOST = 'irc.twitch.tv'
PORT = 6667
USERNAME = 'WasteofCode'
PASSWORD = 'oauth:#'  # http://www.twitchapps.com/tmi/
CHANNEL = '#wasteofspacety'
poopwords = []

def _get_logger():
    logger_name = 'Beffrey'
    logger_level = logging.DEBUG
    log_line_format = '%(asctime)s | %(name)s - %(levelname)s : %(message)s'
    log_line_date_format = '%Y-%m-%dT%H:%M:%SZ'
    logger_ = logging.getLogger(logger_name)
    logger_.setLevel(logger_level)
    logging_handler = logging.StreamHandler(stream=sys.stdout)
    logging_handler.setLevel(logger_level)
    logging_formatter = logging.Formatter(log_line_format, datefmt=log_line_date_format)
    logging_handler.setFormatter(logging_formatter)
    logger_.addHandler(logging_handler)
    return logger_

logger = _get_logger()


class Beffrey(SingleServerIRCBot):

    VERSION = '1.0.0'

    def __init__(self, host, port, nickname, password, channel):
        logger.debug('Beffrey.__init__ (VERSION = %r)', self.VERSION)
        SingleServerIRCBot.__init__(self, [(host, port, password)], nickname, nickname)
        self.channel = channel
        self.viewers = []

    def on_welcome(self, connection, event):
        logger.debug('Beffrey.on_welcome')
        connection.join(self.channel)
        connection.privmsg(event.target, 'Hello world!')

    def on_join(self, connection, event):
        logger.debug('Beffrey.on_join')
        nickname = self._parse_nickname_from_twitch_user_id(event.source)
        self.viewers.append(nickname)
        print(nickname)

        if nickname.lower() == connection.get_nickname().lower():
            True

    def on_part(self, connection, event):
        logger.debug('Beffrey.on_part')
        nickname = self._parse_nickname_from_twitch_user_id(event.source)
        print(nickname)
        self.viewers.remove(nickname)

    def on_pubmsg(self, connection, event):
        logger.debug('Beffrey.on_pubmsg')
        message = event.arguments[0]
        if(message.startswith("!") == True):
            splitmessage = message.split('!')
            splitmessage.remove('')
            word = splitmessage[0]
            with open('commands.txt', 'r') as commandlist:
                command = commandlist.readlines()
            if(command.__contains__(word) == False):
                poopwords.append(word.lower())
                with open('blacklist.txt', 'a') as blacklist:
                    if(blacklist.reallines().__contains__(word) == False):
                        blacklist.writelines(word.lower() + " ")
        
            
        
            
        
        logger.debug('message = %r', message)
        message_parts = message.split(":", 1)
        if len(message_parts) > 1 and message_parts[0].lower() == connection.get_nickname().lower():
            self.do_command(event, message_parts[1].strip())

    def do_command(self, event, command):
        logger.debug('Beffrey.do_command (command = %r)', command)

        if command == "version":
            version_message = 'Version: %s' % self.VERSION
            self.connection.privmsg(event.target, version_message)
        if command == "count_viewers":
            num_viewers = len(self.viewers)
            num_viewers_message = 'Viewer count: %d' % num_viewers
            self.connection.privmsg(event.target, num_viewers_message)
        elif command == 'exit':
            self.die(msg="")
        else:
            logger.error('Unrecognized command: %r', command)

    @staticmethod
    def _parse_nickname_from_twitch_user_id(user_id):
        # nickname!username@nickname.tmi.twitch.tv
        return user_id.split('!', 1)[0]


def main():
    my_bot = Beffrey(HOST, PORT, USERNAME, PASSWORD, CHANNEL)
    my_bot.start()


if __name__ == '__main__':
    main()