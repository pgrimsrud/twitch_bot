import hexchat
import re
import smtplib

__module_name__ = "srl_bot"
__module_version__ = "1.0"
__module_description__ = "send srl emails"

def sendmail(message):
    try:
        smtp_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        smtp_ssl.ehlo()
        smtp_ssl.login("phillip.grimsrud@gmail.com","Redacted password")
        smtp_ssl.sendmail("phillip.grimsrud@gmail.com","phillip.grimsrud@gmail.com","Subject: srl_bot race detection\n\n " + message)
        smtp_ssl.close()
        print("email sent")
    except:
        error = sys.exc_info()[0]
        print("email NOT sent: " + error)
    
def messageHandler(word, word_eol, userdata):
    if re.match(".*zelda2hacks.*",word[1]):
        #print(word[0] + " said " + word[1])
        sendmail(word[0] + " " + word[1])
        #hexchat.command("say z2hacks said " + word[0] + "!")
    return hexchat.EAT_NONE

#def timerHandler(userdata):
#    hexchat.command("say C-3PO: I am C-3PO, human-cyborg relations (!c3po)")
#    return 1

#hexchat.hook_timer(1800000, timerHandler)
hexchat.hook_print("Channel Message", messageHandler)
hexchat.hook_print("Your Message", messageHandler)
