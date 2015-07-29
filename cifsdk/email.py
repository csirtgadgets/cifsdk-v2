import pyzmail
import logging
from pprint import pprint


def parse_message_urls(msg):
    msg = pyzmail.PyzMessage.factory(msg)

    body = []
    if msg.is_multipart():
        for part in msg.mailparts:
            body.append(parse_message_part(part))
    else:
        body.append(parse_message_part(msg))

        #
        # if msg.get_default_type() == "text/plain":
        #     body = msg.get_payload()
        # elif msg.get_default_type() == "text/html":
        #     body = msg.get_payload()
        # else:
        #     # not sure a non mulitpart message has anything be text/plain and text/html
        #     print("WARNING: unhandled default.type", msg.get_default_type())

    return body


def parse_message_part(part):
    try:
        charset = part.charset
    except AttributeError:
        charset = None

    try:
        type = part.type
    except AttributeError:
        type = part.get_default_type()

    if type == "text/plain":
        if charset:
            # return the decoded unicode string
            return part.get_payload().decode(part.charset)
        else:
            # return the str, but decode it first
            return part.get_payload(decode=True)

    # same questions as above but for 'text/html'
    elif type == "text/html":
        payload = part.get_payload()

        if charset:
            payload = payload.decode(part.charset)

        return payload

    elif type == 'application/octet-stream':
        payload = part.get_payload()

    elif type == 'message/rfc822':
        payload = part.get_payload()

    else:
        raise RuntimeError('uhandled part type: {}'.format(type))

    return payload


def parse_message(msg):
    body = []

    if msg.is_multipart():
        for part in msg.mailparts:
            body.append(parse_message_part(part))
    else:
       
        if msg.get_default_type() == "text/plain":
            body = msg.get_payload(decode=True)
        elif msg.get_default_type() == "text/html":
            body = msg.get_payload(decode=True)
        else:
            # not sure a non mulitpart message has anything be text/plain and text/html
            print("WARNING: unhandled default.type", msg.get_default_type())

    return body
