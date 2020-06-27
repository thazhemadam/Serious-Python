# -*- coding: utf-8 -*-
"""
Created on Tue May 28 09:48:39 2019

@author: user
"""

import imapclient
imapObj = imapclient.IMAPClient('imap.gmail.com', ssl=True)
imapObj.login('seriouspython6@gmail.com ', 'sp@12345')
imapObj.select_folder('INBOX', readonly=True)
messages = imapObj.search(['FROM','no-reply@accounts.google.com']) 
print("%d messages from our best friend" % len(messages))
# fetch gets you data and the id of the message
# fetch(message_set, message_parts) , message_parts are ENVELOPE, BODY, FLAGS etc

for msgid, data in imapObj.fetch(messages, ['ENVELOPE']).items():
    envelope = data[b'ENVELOPE']
    print('ID #%d: "%s" received %s' % (msgid, envelope.subject.decode(), envelope.date))
"""rawMessages = imapObj.fetch([40041], ['BODY[]', 'FLAGS'])
import pyzmail36
message = pyzmail36.PyzMessage.factory(rawMessages[40041]['BODY[]'])
message.get_subject()
message.get_addresses('from')
message.get_addresses('to')
message.get_addresses('cc')
message.get_addresses('bcc')
message.text_part != None
message.text_part.get_payload().decode(message.text_part.charset)
message.html_part != None
message.html_part.get_payload().decode(message.html_part.charset)
imapObj.logout() "