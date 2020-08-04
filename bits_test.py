import re

line = "@badges=;bits=100;color=#D2691E;display-name=ev_brak;emotes=;id=63aa0ee2-5d1c-4fbb-9f2d-bdbcc87f1ea9;mod=0;room-id=68072575;subscriber=0;tmi-sent-ts=1494830731290;turbo=0;user-id=136533355;user-type= :ev_brak!v_brak@ev_brak.tmi.twitch.tv PRIVMSG #link_7777 :cheer100 Grats on affiliate!"

match = re.search('^@badges.*;bits=(.+?);.*display-name=(.+?);.*sent-ts=(.+?);.*PRIVMSG #link_7777\s+?:(.*)', line)
if match:
    message = "PRIVMSG #link_7777:" + match.group(2) + " thank you for the " + match.group(1) + " bits! Graphical widget coming soon.\r\n"
    print(message)

line = "@badges=premium/1;color=#3019B3;display-name=dwangoAC;emotes=;id=33d235a4-7736-40b3-9ba7-90642d1bf3b4;login=dwangoac;mod=0;msg-id=raid;msg-param-displayName=dwangoAC;msg-param-login=dwangoac;msg-param-profileImageURL=https://static-cdn.jtvnw.net/jtv_user_pictures/dwangoac-profile_image-2485e7aab13efd69-70x70.png;msg-param-viewerCount=25;room-id=68072575;subscriber=0;system-msg=25\sraiders\sfrom\sdwangoAC\shave\sjoined\n!;tmi-sent-ts=1527832945012;turbo=0;user-id=70067886;user-type= :tmi.twitch.tv USERNOTICE #link_7777"
#line = ":jtv!jtv@jtv.tmi.twitch.tv PRIVMSG link_7777 :dwangoAC is now hosting you for up to 12 viewers."

line = line[1:]
index2 = line.find("#link_7777")
meta = line[:index2]
data = line[index2+12:]

print(index2)
print(meta)
print(data)

meta_dict = dict(info.split('=') for info in meta.split(';'))

print(meta_dict)
