import logging

from plataforma.serializers import ProfileSerializer
from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
from socketio.mixins import BroadcastMixin
from socketio.sdjango import namespace
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.utils.datetime_safe import time
from django.utils.html import strip_tags
from plataforma.models import *
from django.utils import timezone
import json


def message(self, msg):
    room = get_object_or_404(Room, name=msg["room"])
    if room:
        user_from = Profile.objects.get(user__username=msg["user_from"])
        MessageInstEvent.objects.create(room=room, user_from=user_from, msg=msg["message"],
                                        date_pub=timezone.now(), type="message_int_event")

        msg["message"] = strip_tags(msg["message"])
        msg["name"] = msg["user_from"]
        msg["image"] = user_from.image.url
        self.emit_to_room(self.room, 'message', msg)
        for item in room.users.all():
            read = True if item.active == True else False
            MessageInstEvent.objects.create(room=room, user_from=user_from, user_to=item, msg=msg["message"],
                                            date_pub=timezone.now(), type="message_int_event", readed=read)
    else:
        profile = Profile.objects.get(user__username=msg["user_from"])
        self.sendMessage(profile.socketsession, 'message', {"error": "Room not exits"})


def call(self, msg):
    profile = Profile.objects.get(user__username=msg["user_to"])
    room = RoomCall.objects.get(name=msg['room'])
    serializer = ProfileSerializer(room.users.all(), many=True)
    users = json.dumps(serializer.data)
    profile_from = Profile.objects.get(user__username=msg["user_from"])
    self.sendMessage(profile_from.socketsession, 'message',
                     {"action": "user_list", "room": room.name, "user_from": msg["user_from"], "users": users})
    if profile:

        self.sendMessage(profile.socketsession, 'message',
                         {"action": "call_join_request", "user_from": msg["user_from"],
                          "user_to": msg["user_to"],
                          'avatar': profile.image.url, "room": room.name})

    else:
        profile = Profile.objects.get(user__username=msg["user_from"])
        self.sendMessage(profile.socketsession, 'message',
                         {"action": "call_failed", "message": "No connected sockets exist"})


def callaccept(self, msg):
    room = RoomCall.objects.get(name=msg['room'])
    serializer = ProfileSerializer(room.users.all(), many=True)
    users = json.dumps(serializer.data)
    profile = Profile.objects.get(user__username=msg["user_from"])

    self.sendMessage(profile.socketsession, 'message',
                     {"action": "user_list", "room": room.name, "user_from": msg["user_from"], "users": users})
    for item in room.users.all():
        self.sendMessage(item.socketsession, 'message',
                         {"action": "join", "room": room.name, "user_from": msg["user_from"], "users": users})


def speaking(self, msg):
    room = RoomCall.objects.get(name=msg['room'])

    for item in room.users.all():
        self.sendMessage(item.socketsession, 'message',
                         {"action": "speaking", "room": room.name, "user_from": msg["user_from"],
                          'avatar': item.image.url})


def muted(self, msg):
    room = RoomCall.objects.get(name=msg['room'])

    for item in room.users.all():
        self.sendMessage(item.socketsession, 'message',
                         {"action": "muted", "room": room.name, "user_from": msg["user_from"]
                          })


def unmuted(self, msg):
    room = RoomCall.objects.get(name=msg['room'])

    for item in room.users.all():
        self.sendMessage(item.socketsession, 'message',
                         {"action": "unmuted", "room": room.name, "user_from": msg["user_from"]
                          })


def calldecline(self, msg):
    room = RoomCall.objects.get(name=msg['room'])

    self.broadcast_event('message', {"action": "call_decline", "user_from": msg["user_from"], "room": room.name})


def offer(self, msg):
    room = RoomCall.objects.get(name=msg['room'])
    profile = Profile.objects.get(user__username=msg["user_to"])

    print 'Sending offer to: ' + profile.user.username + " " + profile.socketsession
    self.sendMessage(profile.socketsession, 'message', {
        'action': "offer",
        'offer': msg['offer'],
        'user_from': msg["user_from"],
        "room": room.name,

    })


def answer(self, msg):
    room = RoomCall.objects.get(name=msg['room'])
    profile = Profile.objects.get(user__username=msg["user_to"])

    print 'Sending answer to: ' + profile.user.username + " " + profile.socketsession
    self.sendMessage(profile.socketsession, 'message', {
        'action': "answer",
        'answer': msg['answer'],
        'user_from': msg["user_from"],
        "room": room.name,

    })


def candidate(self, msg):
    room = RoomCall.objects.get(name=msg['room'])
    profile = Profile.objects.get(user__username=msg["user_to"])
    print 'candidate' + msg["user_to"]

    print 'Sending offer to: ' + profile.user.username + " " + profile.socketsession
    self.sendMessage(profile.socketsession, 'message', {
        'action': "candidate",
        'candidate': msg['candidate'],
        'user_from': msg["user_from"],
        "room": room.name,

    })


def leave(self, msg):
    self.broadcast_event('message', {
        'action': "leave",
        'user_from': msg["user_from"]

    })


optionchannel = {'message': message,
                 'call': call,
                 'callaccept': callaccept,
                 'calldecline': calldecline,
                 'offer': offer,
                 'answer': answer,
                 'candidate': candidate,
                 'leave': leave,
                 'speaking': speaking,
                 'muted': muted,
                 'unmuted': unmuted,
                 }


@namespace('/chat')
class ChatNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
    nicknames = []

    # self.socket.server.sockets.get_socket
    def initialize(self):
        self.logger = logging.getLogger("socketio.chat")
        self.log("Socketio session started")

    def log(self, message):
        self.logger.info("[{0}] {1}".format(self.socket.sessid, message))

    def on_subcribe(self, data):
        self.room = data['room']
        self.join(data['room'])
        return True

    def on_unsubcribe(self, data):
        self.leave(data['room'])
        return True

    def on_join(self, data):
        user = data['user']
        profile = Profile.objects.get(user__username=user)
        profile.socketsession = self.socket.sessid
        profile.save()
        self.sendMessage(self.socket.sessid, 'connected', {"action": "connected", "message": profile.user.username})
        return True

    def on_message(self, msg):

        if msg['action'] == "message":
            user_from = Profile.objects.get(user__username=msg["user_from"])
            if user_from:
                profile = Profile.objects.get(user__username=msg["user_to"])
                read = True if profile.active == True else False
                message = MessageInstEvent.objects.create(user_to=profile, user_from=user_from,
                                                          msg=msg["message"],
                                                          type="message_int_event", readed=read)
                msg["action"] = "message"
                msg["user_to"] = profile.user.username
                msg["user_from"] = user_from.user.username
                msg["image"] = user_from.image.url
                msg["date_pub"] = str(message.date_pub.isoformat())
                self.sendMessage(profile.socketsession, 'message', msg)

        return True

    def on_messagechanel(self, msg):
        print 'inchannel'
        action = msg['action']
        func = optionchannel.get(action, lambda: "nothing")
        func(self, msg)

        return True

    def sendMessage(self, sessid, event, *args):
        socket = self.socket.server.get_socket(sessid)
        if socket:
            pkt = dict(type="event",
                       name=event,
                       args=args,
                       endpoint=self.ns_name)
            socket.send_packet(pkt)
