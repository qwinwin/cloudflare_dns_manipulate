#!/usr/bin/env python
# coding = utf-8
import requests
import re
import sys
cf_id = "your id|mail"
cf_key = "your key"
zone_id = "domain zone id"
base_url = "https://api.cloudflare.com/client/v4/zones/" + zone_id + "/dns_records"
headers = {
    "X-Auth-Email": cf_id,
    "X-Auth-Key": cf_key,
    "Content-Type": "application/json"
}


def list_record(*name):
    list_url = base_url + "?per_page=100"
    resp = requests.get(list_url, headers=headers)
    for i in range(100):
        try:
            jsons = resp.json()["result"][i]
            get_msg = jsons["name"], jsons["type"], jsons["content"], jsons[
                "id"]
            if len(name) > 0 and re.match(
                    str(jsons["name"]).split('.')[0], str(name[0]), re.I):
                print(get_msg)
                return jsons["id"]
                break
            elif len(name) == 0:
                print(get_msg)
            i += 1
        except Exception:
            break


def create_record(name, content, record_type="A"):
    data = {
        "type": record_type,
        "name": name,
        "content": content,
        "ttl": 120,
        "priority": 10
    }
    create = requests.post(base_url, headers=headers, json=data)
    print("New Record:")
    print(create.content)


def delete_record(record_id):
    try:
        modify_url = base_url + "/" + record_id
        delete = requests.delete(modify_url, headers=headers)
        print(delete.content)
        print("Deleted")
    except Exception:
        print("Record Not Found")


if __name__ == "__main__":
    try:
        action = sys.argv[1]
        name = sys.argv[2]
        if action == "del":
            delete_record(list_record(name))
        elif action == "get":
            list_record(name)
        else:
            name = sys.argv[1]
            content = sys.argv[2]
            delete_record(list_record(name))
            try:
                record_type = sys.argv[3]
                create_record(name, content, record_type=record_type)
            except Exception:
                create_record(name, content)
    except Exception:
        list_record()
