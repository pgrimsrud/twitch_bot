import re

line = "@badges=;bits=100;color=#D2691E;display-name=ev_brak;emotes=;id=63aa0ee2-5d1c-4fbb-9f2d-bdbcc87f1ea9;mod=0;room-id=68072575;subscriber=0;tmi-sent-ts=1494830731290;turbo=0;user-id=136533355;user-type= :ev_brak!v_brak@ev_brak.tmi.twitch.tv PRIVMSG #link_7777 :cheer100 Grats on affiliate!"

match = re.search('^@badges.*;bits=(.+?);.*display-name=(.+?);.*sent-ts=(.+?);.*PRIVMSG #link_7777\s+?:(.*)', line)
if match:
    message = "PRIVMSG #link_7777:" + match.group(2) + " thank you for the " + match.group(1) + " bits! Graphical widget coming soon.\r\n"
    print(message)
