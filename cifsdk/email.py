import pyzmail
import logging
from pprint import pprint

def parse_message_part(part):
    #Data available in each part:
    # http://www.magiksys.net/pyzmail/api/pyzmail.parse.MailPart-class.html

    #print("charset:", part.charset)
    #print("content_id:", part.content_id)
    #print("description:", part.description)
    #print("disposition:", part.disposition)
    #print("filename:", part.filename)
    #print("is body:", part.is_body)
    #print("part:", part.part) #entire message
    #print("sanitized_filename:", part.sanitized_filename)
    #print("type:", part.type)

    # Step 1: if part.type text/plain and has a characther set, try to decode
    # with character set.
    # pyzmail will try to do some charcter set decoding for you, not sure
    # how this applies to .decode() below
    # https://github.com/aspineux/pyzmail/blob/master/pyzmail/pyzmail/parse.py#L487
    #
    # Q1: when if ever should this be used:
    #   body, _ = pyzmail.decode_text(body, charset, None)
    #   is this the same as '.decode(part.charset))'?
    # Step 2: if we don't have character set, try without? Is this sane?

    try:
        if part.type == "text/plain":
            if part.charset:
                # return the decoded unicode string
                return part.get_payload().decode(part.charset)
            else:
                # return the str, but decode it first
                return part.get_payload(decode=True)

        # same questions as above but for 'text/html'
        elif part.type == "text/html":
            if part.charset:
                return part.get_payload().decode(part.charset)  # decode the unicode
            else:
                return part.get_payload(decode=True)
    except AttributeError:
        if part.get_default_type().startswith('text/'):
            return part.get_payload(decode=True)
        else:
            raise RuntimeError('unhandled type: {}'.format(part.get_default_type()))

    # there are many types you might find here:
    # multipart/alternative
    # message/rfc822
    # multipart/signed
    # multipart mixed
    # application/pgp-signature
    # multipart/digest
    # others??
    #
    # Q1: do we need to handle them individually or treat the all the same?
    #
    # fact 1: this needs to be a recursive function back to pyzmail
    #   something like:
    #       zmail = pyzmail.PyzMessage(part)
    #       a = msg_to_dict(zmail)
    #
    # fact 2: for each attachment the part may have, if they are text/html
    # parts we need to send them back through pyzmail to be parsed. think
    # forwarded phishing email to phish@ren-isac.net. Do we need to think
    # about based64 encoded attachments that could be plain text? Does something
    # already handle that for us?
    #
    # If the attachment is a binary (.zip, .scr, .exe) we should not send
    # it back through pyzmail but we should store it??
    #
    # Q2: what's the correct way to identify and parse out attachments?
    # ?  if len(msg.mailparts) > 1:?
    # ? if bool(content_disposition and dispositions[0].lower() == "attachment"):
    #   see: lan_lewis_example.parser.txt example

    else:
        raise RuntimeError('uhandled part type: {}'.format(part.type))

def parse_message(msg):
    d = {}
    msg_body = ''
    msg = pyzmail.PyzMessage.factory(msg)

    # put message headers into dictionary
    msg_headers = {}
    for header in msg.keys():
        value = msg.get_decoded_header(header)
        try:
            msg_headers[header].append(value)
        except:
            msg_headers[header] = [value]

    # check to see if the email is multipart
    # if so, go through each part
    body = []
    if msg.is_multipart():
        for part in msg.mailparts:
            body.append(parse_message_part(part))
    else:

        #Data available in each message:
        #print("charset:", msg.get_charset())
        #print("charsets:", msg.get_charsets())
        #print("content_charset:", msg.get_content_charset())
        #print("content_maintype:", msg.get_content_maintype())
        #print("content_subtype:", msg.get_content_subtype())
        #print("content_type:", msg.get_content_type())
        #print("default_type:", msg.get_default_type())
        #print("filename:", msg.get_filename())

        # Q1 sometimes msg.get_charset() has a charset value
        #
        # Q2 sometimes msg.get_charsets() is an array with one or more?
        #    charsets in the array
        #
        # Q3 someimes you'll try to decode it with the charset but
        #    it throws a unicode error
        #    mail pile seems to have addressed this:
        #    https://github.com/mailpile/Mailpile/blob/master/mailpile/mailutils.py#L668
        #
        # So with all the ways to decode messages, what's the best way?
        #
        # if msg.get_default_type() == "text/plain":
        #     print("get_payload-1:", msg.get_payload(decode=True))
        # elif msg.get_default_type() == "text/html":
        #     print("get_payload-2:", msg.get_payload(decode=True))
        # else:
        #     # not sure a non mulitpart message has anything be text/plain and text/html
        #     print("WARNING: unhandled default.type", msg.get_default_type())

        body.append(parse_message_part(msg))
    return body
