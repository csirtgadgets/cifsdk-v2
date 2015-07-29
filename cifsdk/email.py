from pyzmail import PyzMessage
from cifsdk.urls import extract_urls


def parse_message_urls(msg):
    m = PyzMessage.factory(msg)

    urls = set()
    if m.is_multipart():
        for p in m.mailparts:
            b = parse_message_part(p)
            if p.type == 'text/html':
                u = extract_urls(b, html=True)
                urls.update(u)
            if p.type == 'text/plain':
                u = extract_urls(b)
                urls.update(u)

    return urls


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
    msg = PyzMessage.factory(msg)
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
