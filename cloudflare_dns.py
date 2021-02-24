#!/usr/bin/env python3
# coding = utf-8
import requests
import argparse
import logging

cf_id = "cloudflare account id(mail)"
cf_key = "global api key"
zone_id = "domain zone id"
zone_name = 'domain zone name'

def list_record(name=''):
    global record
    params = {'name': f'{name}.{zone_name}'} if name else {'per_page': 100}
    resp = requests.get(base_url, headers=headers, params=params)
    for msg in resp.json()['result']:
        print(eval(print_msg))
        if name:
            record = eval(print_msg)
            return msg['id']


def new_record(name, content, record_id, record_type='A'):
    data = {'type': record_type, 'name': name, 'content': content}
    if record_id:
        msg = requests.put(f'{base_url}/{record_id}',
                           headers=headers,
                           json=data).json()['result']
        print('Changed to')
        logging.info(f'update: {eval(print_msg)}')
    else:
        msg = requests.post(base_url, headers=headers,
                            json=data).json()['result']
        print('New record:')
        logging.info(f'create: {eval(print_msg)}')
    print(eval(print_msg))


def delete_record(record_id):
    if record_id:
        msg = requests.delete(f'{base_url}/{record_id}', headers=headers)
        if msg.json()['success']:
            print('Deleted')
            logging.info(f'delete: {record}')
    else:
        print(f'Record not found: {name}')


def get_parser():
    parser = argparse.ArgumentParser(
        description="Manipulate DNS records on cloudflare")
    parser.add_argument('-n', '--name')
    parser.add_argument('-c', '--content')
    parser.add_argument('-t', '--type', default='A')
    parser.add_argument('-d', '--delete', action="store_true")
    return parser


if __name__ == '__main__':
    logging.basicConfig(filename='/var/log/cloudflare_dns.log',
                        encoding='utf-8',
                        format='%(levelname)s %(asctime)s %(message)s',
                        level=logging.INFO)
    print_msg = """f'{msg["name"]} {msg["type"]} {msg["content"]}'"""
    base_url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'
    headers = {
        'X-Auth-Email': cf_id,
        'X-Auth-Key': cf_key,
        'Content-Type': 'application/json'
    }
    args = get_parser().parse_args()
    name = args.name
    content = args.content
    record_type = args.type
    delete = args.delete
    if name and delete:
        delete_record(list_record(name))
    elif name and content:
        new_record(name, content, list_record(name), record_type)
    else:
        list_record(name)
