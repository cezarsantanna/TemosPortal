#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import logging.handlers
import inotify.adapters
from os import rename
from time import sleep
from utils.parser.mailparser import MailParser
from utils.parser.officetrack import parserOfficeTrack as parseOT
from utils.parser.servicenow import parserServiceNow as parseSN
from daemonize import Daemonize

pid = '/tmp/mail_monitor.pid'

logdirfile = '/var/log/temosportal/abastece/mail_monitor.log'

mon_dir = '/opt/abastece/Maildir/new'

# Criando o log da aplicação
logger = logging.getLogger('Mail_Monitor')
logger.setLevel(logging.DEBUG)

# Definido a Rotação do Arquivo de Log 
logfile = logging.handlers.TimedRotatingFileHandler(
    logdirfile,
    when='midnight',
    interval = 1,
    backupCount=7,
    encoding='utf-8',
)
logfile.setLevel(logging.DEBUG)

# Definindo o Formato do Log
formatter = logging.Formatter(
    '%(asctime)s %(name)s|%(levelname)s|%(message)s',
    '%Y/%m/%d %H:%M:%S'
)

# Atribuindo o formato ao arquivo de log
logfile.setFormatter(formatter)

# Adicionando o arquivo de log ao logger
logger.addHandler(logfile)
keep_fds = [logfile.stream.fileno()]
print(keep_fds)


#Testando o Arquivo de Log
def test_log():
    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')


def parsemail(_mailfile):
    source = _mailfile
    mail = MailParser()
    mail.parse_from_file(_mailfile)
    if mail.X_Original_To_ == 'officetrack@temos.online':
        destination = parseOT(_mailfile, mail)
        rename(source, destination)
    elif mail.X_Original_To_ == 'servicenow@temos.online':
        destination = parseSN(_mailfile, mail)
        rename(source, destination)
    else:
        destination = source.replace('/new/', '/Others/not_parsed/')
        rename(source, destination)
    #print(len(parser.attachments_list))
    #print(type(mail.attachments_list[0]))
    #print(parser.attachments_list[0].keys())
    #print(parser.attachments_list[0]['filename'])
    #print(parser.attachments_list[0]['content_transfer_encoding'])
    #print(parser.attachments_list[0]['mail_content_type'])
    #print(parser.attachments_list[0]['payload'])


# Função Principal
def main():
    while True:
        try:
            i = inotify.adapters.Inotify()
            i.add_watch(bytes(mon_dir.encode('utf-8'), ))
            for event in i.event_gen():
                if event is not None:
                    (header, type_names, watch_path, filename) = event
                    #if 'IN_CREATE' in event[1] and len(filename.decode('utf-8')):
                    if 'IN_CLOSE_WRITE' in event[1] and len(filename.decode('utf-8')):
                        logger.info("WATCH-PATH=[%s] FILENAME=[%s]",
                            watch_path.decode('utf-8'), filename.decode('utf-8'))
                        mailfile = ('%s/%s') % (watch_path.decode('utf-8'), filename.decode('utf-8'))
                        parsemail(mailfile)
        except KeyboardInterrupt:
            i.remove_watch(bytes(mon_dir.encode('utf-8'), ))
            break
        except:
            logger.error("Mailfile %s, can't be parsed" % mailfile.replace('/new/', '/Errors/'))
            destination = mailfile.replace('/new/', '/Errors/')
            rename(mailfile,  destination)
            pass
        finally:
            i.remove_watch(bytes(mon_dir.encode('utf-8'), ))



if __name__ == '__main__':
    daemon = Daemonize(
        app='mail_monitor',
        pid=pid,
        action=main,
        keep_fds=keep_fds
    )
    #daemon.start()
    main()