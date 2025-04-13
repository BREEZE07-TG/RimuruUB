from pyrogram import Client
import config as c
import logging

FORMAT = "[UB]:%(message)s"

logging.basicConfig(level=logging.INFO,handlers=[logging.FileHandler('logs.txt'),
                                                 logging.StreamHandler()],format=FORMAT)

app = Client(c.string_session,
             api_id=c.api_id,
             api_hash=c.api_hash,
             plugins=dict(root='module'))
