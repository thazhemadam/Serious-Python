# -*- coding: utf-8 -*-
"""
Created on Tue May 28 08:23:32 2019

@author: user
"""

# SMTP protocol is used for sending mails
# This dictates how mails should be formatted, encrypted etc
# Python smtplib simplefies this into a few functions
# we can use IMAP/POP3 for receiving mails
# so let us start by connecting to gmail
# the server for smtp for gmail is smtp.gmail.com
# the port at which almost all mail servers listen
# is 587
import smtplib
smtpObj = smtplib.SMTP('smtp.gmail.com',587)
# so there is a method to connect SMTP , what is the object
type(smtpObj)
# This guy is needed for logging, sending mails
# dont try this just yet
# smtpObj = smtplib.SMTP_SSL('smtp.gmail.com',465)
# Say namaste to google mama using ehlo()
smtpObj.ehlo()
# Better to encrypt stuff that you send by using TLS
# Transport Layer Security is used for authenticatio, privacy
# and a widely used protocol
# so let us become James Bond
smtpObj.starttls()
# Largely uses the public key - private key exchange for secure communication
# to prevent man in the middle attackes
# Let us try a  login to gmail
smtpObj.login('katharguppe33@gmail.com','2306-srini')
# if you get an authentiction error then google for letting less
# secure app access your gmail
smtpObj.sendmail('katharguppe33@gmail.com ', 'srinivasks@pes.edu ',r'Subject: \nDear Prof, You seem to love cricket and am therefore send a few crickets\(keech keech\) by courier. Sincerely,keetch...keetck')
smtpObj.quit()
# so you now know how to send mails automaticallys
# Let us complete receiving mails and then try something
# Internet Message Access Protocol and POP3 is used for receiving mails

#!/usr/bin/python

#import smtplib

#sender = 'from@fromdomain.com'
#receivers = ['to@todomain.com']

#message = """From: From Person <from@fromdomain.com>
#To: To Person <to@todomain.com>
#Subject: SMTP e-mail test

#This is a test e-mail message.
#"""
# See the format of this message
#try:
#   smtpObj = smtplib.SMTP('localhost')
#   smtpObj.sendmail(sender, receivers, message)         
#   print "Successfully sent email"
#except SMTPException:
#   print "Error: unable to send email"
#"""