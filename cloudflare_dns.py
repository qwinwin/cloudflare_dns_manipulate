#!/usr/bin/env python3
# coding = utf-8
import httpx
import argparse
from loguru import logger


def list_record(name='', record_type=''):
    req_name = f'{name}.{zone_name}' if name != '@' else f'{zone_name}'
    params = {'name': f'{req_name}'} if name else {'per_page': 100}
    params['type'] = record_type
    resp = httpx.get(base_url, headers=headers, params=params)
    msgs = []
    count = 0
    if name:
        for msg in resp.json()['result']:
            if msg['name'] == req_name:
                msgs.append(msg)
                print(f"{count}: {eval(req_msg)}")
                count += 1
    else:
        for msg in resp.json()['result']:
            print(eval(req_msg))
    return msgs


def new_record(name, content, msgs, record_type='', proxied=False):
    data = {
        'type': record_type,
        'name': name,
        'content': content,
        'proxied': proxied
    }
    if msgs and not multi:
        option = int(input("choose the option: ")) if len(msgs) > 1 else 0
        msg = msgs[option]
        old_msg = eval(req_msg)
        msg = httpx.put(f'{base_url}/{msg["id"]}', headers=headers,
                        json=data).json()['result']
        print('Changed to')
        logger.info(f"CHANGED | {old_msg} -> {eval(req_msg)}")
    else:
        msg = httpx.post(base_url, headers=headers, json=data).json()['result']
        logger.info(f"NEW | {eval(req_msg)}")
        print('New record:')
    print(eval(req_msg))


def delete_record(msgs):
    if msgs:
        option = int(input("choose the option: ")) if len(msgs) > 1 else 0
        msg = msgs[option]
        if httpx.delete(f'{base_url}/{msg["id"]}',
                        headers=headers).json()['success']:
            print('Deleted')
            logger.info(f'DELETED | {eval(req_msg)}')
    else:
        print(f'Record not found: {name}')


def get_parser():
    parser = argparse.ArgumentParser(
        description="Manipulate DNS records hosted on cloudflare")
    parser.add_argument('-n', '--name')
    parser.add_argument('-c', '--content')
    # parser.add_argument('-t', '--type', default='A')
    parser.add_argument('-t', '--type')
    parser.add_argument('-z', '--zone', default=0)
    parser.add_argument('-d', '--delete', action="store_true")
    parser.add_argument('-m', '--multi', action="store_true")
    parser.add_argument('-p', '--proxied', action="store_true")
    return parser


if __name__ == '__main__':
    cf_id = "cloudflare account id(mail)"
    cf_key = "global api key"
    zone_info = [{
        'name': 'name1',
        'id': 'xxxx'
    }, {
        'name': 'name2',
        'id': 'xxxx'
    }]
    logger.remove(handler_id=None)
    logger.add('/var/log/cloudflare_dns.log',
               format="{time:YYYY-MM-DD HH:mm:ss} | {message}")
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
    multi = args.multi
    proxied = args.proxied
    zone_num = int(args.zone)
    zone_name, zone_id = zone_info[zone_num]['name'], zone_info[zone_num]['id']
    req_msg = """f'{msg["name"]} {msg["type"]} {msg["content"]}'"""
    base_url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'

    if name and delete:
        delete_record(list_record(name, record_type))
    elif name and content:
        new_record(name, content, list_record(name, record_type), record_type,
                   proxied)
    else:
        list_record(name, record_type)
