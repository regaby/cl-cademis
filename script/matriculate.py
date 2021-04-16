import xmlrpc.client
import csv
import time
import configparser
import sys

CONFIG = configparser.ConfigParser()
CONFIG.read('xmlrpc.conf')

HOST = CONFIG['local']['HOST']
PORT = int(CONFIG['local']['PORT'])
USER = CONFIG['local']['USER']
PASS = CONFIG['local']['PASS']
DB = CONFIG['local']['DB']

INPUT_FILE = 'matriculate_debt.csv'

URL = 'http://%s:%d/xmlrpc/common' % (HOST, PORT)
SOCK = xmlrpc.client.ServerProxy(URL)
UID = SOCK.login(DB, USER, PASS)

print("Logged in as %s (UID:%d)" % (USER, UID))
URL = 'http://%s:%d/xmlrpc/object' % (HOST, PORT)
SOCK = xmlrpc.client.ServerProxy(URL)

CSV_FILE = csv.reader(open(INPUT_FILE, 'rt'), delimiter=';')
next(CSV_FILE)
MODEL_NAME = 'res.partner'
cont = 0
creations = 0
updates = 0
START_TIME = time.time()

for line in CSV_FILE:
    cont += 1
    matricula = line[0]
    name = line[1]
    state = line[4]

    args = [('matricula_number', '=', name)]

    partner_id = SOCK.execute(DB, UID, PASS, MODEL_NAME, 'search', args)
    contract_type = {
        'name': name,
        'matricula_number': matricula,
        'state': state,
    }
    sys.stdout.write("\rLoading Concept: #%s" % cont)
    sys.stdout.flush()
    if not partner_id:
        reg_id = SOCK.execute(DB, UID, PASS, MODEL_NAME, 'create', contract_type)
#         # print("Creating Concept #%s" % cont)
        creations += 1
    else:
        reg_id = SOCK.execute(DB, UID, PASS, MODEL_NAME, 'write', partner_id, contract_type)
        # print("Updating Concept #%s" % cont)
        updates += 1
#
print("\nElapsed time: %.2f seg." % (time.time() - START_TIME))
print("%d records created, %d records updated\n" % (creations, updates))
