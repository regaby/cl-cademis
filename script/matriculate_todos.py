import xmlrpc.client
import csv
import time
import configparser
import sys

def search_create_or_write(model, args, dicc):
    register_id = SOCK.execute(DB, UID, PASS, model, 'search', args)
    if register_id:
        reg_id = SOCK.execute(DB, UID, PASS, model, 'write', register_id, dicc)
        # updates += 1
    else:
        register_id = SOCK.execute(DB, UID, PASS, model, 'create', dicc)
        register_id = [register_id]
        # creations += 1
    return register_id[0]

CONFIG = configparser.ConfigParser()
CONFIG.read('xmlrpc.conf')

HOST = CONFIG['local']['HOST']
PORT = int(CONFIG['local']['PORT'])
USER = CONFIG['local']['USER']
PASS = CONFIG['local']['PASS']
DB = CONFIG['local']['DB']

INPUT_FILE = 'matriculate_todos.csv'

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

country = SOCK.execute(DB, UID, PASS, 'res.country', 'search', [('name', '=', 'Argentina')])[0]
state = SOCK.execute(DB, UID, PASS, 'res.country.state', 'search', [('name', '=', 'Misiones')])[0]
matricula_ant = False

for line in CSV_FILE:
    #print ('line',line)
    if line[0] == 'matricula':
        continue
    cont += 1
    matricula = line[0]
    if matricula == matricula_ant:
        continue
    matricula_ant = matricula
    street = line[3]
    street_number = line[4]
    street_floor = line[5]
    street_depto = line[6]
    city = line[7]
    circuns = line[16]

    args = [('name', '=', city)]
    city_val = {
        'name': city,
        'country_id': country,
        'state_id': state,
    }
    city_id = search_create_or_write('res.city', args, city_val)

    args = [('name', '=', circuns)]
    circuns_val = {
        'name': circuns,
    }
    department_id = search_create_or_write('res.partner.department', args, circuns_val)

    args = [('matricula_number', '=', matricula)]
    partner_id = SOCK.execute(DB, UID, PASS, MODEL_NAME, 'search', args)
    partner_val = {
        'street': street,
        'street_number': street_number,
        'street_floor': street_floor,
        'street_depto': street_depto,
        'street_number': street_number,
        'city_id': city_id,
        'country_id': country,
        'state_id': state,
        'department_id': department_id,

    }
    sys.stdout.write("\rLoading Concept: #%s" % cont)
    sys.stdout.flush()
    if not partner_id:
        reg_id = SOCK.execute(DB, UID, PASS, MODEL_NAME, 'create', partner_val)
#         # print("Creating Concept #%s" % cont)
        creations += 1
    else:
        reg_id = SOCK.execute(DB, UID, PASS, MODEL_NAME, 'write', partner_id, partner_val)
        # print("Updating Concept #%s" % cont)
        updates += 1
#
print("\nElapsed time: %.2f seg." % (time.time() - START_TIME))
print("%d records created, %d records updated\n" % (creations, updates))
