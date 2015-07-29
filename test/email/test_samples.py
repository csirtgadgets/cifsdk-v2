from cifsdk.urls import extract_urls
from cifsdk.email import parse_message_part
from pyzmail import PyzMessage
import os
from pprint import pprint

SAMPLES = 'samples/email'

# not quite finished
def test_email_urls():
    pass

# def test_email_urls():
#     pass
#     for file in os.listdir(SAMPLES):
#         urls = set()
#         file = os.path.join(SAMPLES, file)
#         print file
#         with open(file) as f:
#             m = PyzMessage.factory(f.read())
#
#             urls = set()
#             if m.is_multipart():
#                 for p in m.mailparts:
#                     b = parse_message_part(p)
#                     if p.type == 'text/html':
#                         u = extract_urls(b, html=True)
#                         urls.update(u)
#                     if p.type == 'text/plain':
#                         u = extract_urls(b)
#                         urls.update(u)
#                     if p.type == 'application/octet-stream':
#                         u = extract_urls(b, html=True)
#                         if u:
#                             urls.update(u)
#
#             else:
#                 b = parse_message_part(m)
#                 urls = extract_urls(m)