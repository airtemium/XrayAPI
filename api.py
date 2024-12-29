import requests
from repo.xray.exception import XRayAPIException
from repo.xray.routes import  XRayAPIRoutes
import random
from repo.xray.settings import XRayInboundSettings
from repo.xray.client import XRayClient
from repo.xray.inbound import XRayInbound
from urllib.parse import urlparse, parse_qs, quote_plus
import uuid
import datetime
import time
import json

class XRayAPI:
    __api_url = None
    __cookie = None
    __username = None
    __password = None
    __is_logged = False

    def __init__(self, api_url, username, password):
        self.__api_url = api_url
        self.__username = username
        self.__password = password

    @property
    def api_host(self):
        if not self.__api_url:
            return None

        parsed_url = urlparse(self.__api_url)

        return parsed_url.hostname

    def login(self):
        if not self.__api_url or len(self.__api_url) == 0:
            raise XRayAPIException("API URL can't be empty or nullable")

        if not self.__username:
            raise XRayAPIException("Param username can't be empty or nullable")

        if not self.__password:
            raise XRayAPIException("Param password can't be empty or nullable")

        url = f"{self.__api_url}{XRayAPIRoutes.LOGIN.value}"

        data = {
            "username": self.__username,
            "password": self.__password
        }

        try:
            resp = requests.post(url, json=data, headers={
                "Content-Type": "application/json"
            }, verify=False, timeout=15)

            ret = resp.json()
            if not ret:
                raise XRayAPIException("API Response is not valid")

            success = ret.get('success', False)

            if not success:
                raise XRayAPIException("Username or password incorrect")

            self.__cookie = resp.cookies.get_dict()

            self.__is_logged = True
        except requests.exceptions.HTTPError as err:
            print("Http Error:", err)
            raise err
        except requests.exceptions.ConnectionError as err:
            print("Error Connecting:", err)
            raise err
        except requests.exceptions.Timeout as err:
            print("Timeout Error:", err)
            raise err
        except requests.exceptions.RequestException as err:
            print("Request error:", err)
            raise err

    @property
    def cookie(self):
        return self.__cookie

    def new_cert(self):
        if not self.__is_logged:
            raise XRayAPIException("You must login first")

        if len(self.__cookie) == 0:
            raise XRayAPIException("Invalid creds")

        url = f"{self.__api_url}{XRayAPIRoutes.NEW_CERT.value}"

        try:
            resp = requests.post(url, cookies=self.__cookie, json={}, headers={
                "Content-Type": "application/json"
            }, verify=False, timeout=15)

            if not resp:
                raise XRayAPIException("API Response is not valid")

            if resp.status_code != 200:
                raise XRayAPIException("API Response is not valid")

            ret = resp.json()

            if not ret:
                raise XRayAPIException("API Response is not valid")

            success = ret.get('success', False)

            if not success:
                raise XRayAPIException("Username or password incorrect")

            #{'success': True, 'msg': '', 'obj': {'privateKey': 'mHiz_gac5vyOFUmpyliwr2W7z4jxlRaJ1zXGWXhmIgk', 'publicKey': 'CTMEvq3QV5blGrayK520q3VZ91k2lmv3l0OJE18AkXM'}}
            # print(ret)

            obj = ret.get('obj', {})

            privateKey = obj.get('privateKey', None)
            publicKey = obj.get('publicKey', None)

            if not privateKey or not publicKey:
                raise XRayAPIException("API Response is not valid")

            return {
                "private": privateKey,
                "public": publicKey,
            }
        except requests.exceptions.HTTPError as err:
            print("Http Error:", err)
            raise err
        except requests.exceptions.ConnectionError as err:
            print("Error Connecting:", err)
            raise err
        except requests.exceptions.Timeout as err:
            print("Timeout Error:", err)
            raise err
        except requests.exceptions.JSONDecodeError as err:
            print("DEcode error:", err)
            raise err
        except requests.exceptions.RequestException as err:
            print("Request error:", err)
            raise err

    def random_short_ids(self):
        return self.__random_short_ids__()

    def __random_short_ids__(self):
        seq = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        lengths = [2, 4, 6, 8, 10, 12, 14, 16]
        random.shuffle(lengths)

        short_ids = []
        for length in lengths:
            short_id = ''.join(random.choice(seq[:16]) for _ in range(length))
            short_ids.append(short_id)

        return short_ids

    def __random_lower_and_num__(self, length):
        seq = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        return ''.join(random.choice(seq[:16]) for _ in range(0, length))

    def get_sub_port(self):
        if not self.__is_logged:
            raise XRayAPIException("You must login first")

        if len(self.__cookie) == 0:
            raise XRayAPIException("Invalid creds")

        url = f"{self.__api_url}{XRayAPIRoutes.GET_SETTINGS.value}"

        try:
            resp = requests.get(url, cookies=self.__cookie, headers={
                "Content-Type": "application/json"
            }, verify=False, timeout=15)

            if not resp:
                raise XRayAPIException("API Response is not valid")

            if resp.status_code != 200:
                raise XRayAPIException("API Response is not valid")

            ret = resp.json()

            if not ret:
                raise XRayAPIException("API Response is not valid")

            success = ret.get('success', False)

            if not success:
                raise XRayAPIException("Username or password incorrect")

            # print(ret)

            settings = ret.get('obj', [])

            subPort = settings.get('subPort', 2096)

            return subPort
        except requests.exceptions.HTTPError as err:
            print("Http Error:", err)
            raise err
        except requests.exceptions.ConnectionError as err:
            print("Error Connecting:", err)
            raise err
        except requests.exceptions.Timeout as err:
            print("Timeout Error:", err)
            raise err
        except requests.exceptions.JSONDecodeError as err:
            print("DEcode error:", err)
            raise err
        except requests.exceptions.RequestException as err:
            print("Request error:", err)
            raise err

    def add_additional_client(self, inbound_id, client_name, port, protocol, network, security, private_cert, public_cert, fingerprint, spiderX, shortIds, sni="store.steampowered.com", expiry_in_days=0, limit_of_ip=1):
        print("** add_additional_client 1")

        if not self.__is_logged:
            print("** add_additional_client 2")
            raise XRayAPIException("You must login first")

        if len(self.__cookie) == 0:
            print("** add_additional_client 3")
            raise XRayAPIException("Invalid creds")

        url = f"{self.__api_url}{XRayAPIRoutes.ADD_CLIENT.value}"

        try:
            expiry_ts = 0

            if expiry_in_days > 0:
                orig_date = datetime.datetime.fromtimestamp(time.time())
                new_date = orig_date + datetime.timedelta(days=expiry_in_days)
                expiry_ts = int(new_date.timestamp()) * 1000

            client_id = str(uuid.uuid4())
            client_email = self.__random_lower_and_num__(12)
            client_sub_id = self.__random_lower_and_num__(16)
            flow = "xtls-rprx-vision"

            settings = {
                "clients": [
                    {
                        "id": client_id,
                        "flow": flow,
                        "email": client_email,
                        "limitIp": limit_of_ip,
                        "totalGB": 0,
                        "expiryTime": expiry_ts,
                        "enable": True,
                        "tgId": "",
                        "subId": client_sub_id,
                        "reset": 0
                    }
                ]
            }

            new_client = {
                "settings": json.dumps(settings),
                "id": inbound_id
            }

            resp = requests.post(url, cookies=self.__cookie, json=new_client, headers={
                "Content-Type": "application/json"
            }, verify=False, timeout=15)

            if not resp:
                print("** add_additional_client 4")
                raise XRayAPIException("API Response is not valid")

            if resp.status_code != 200:
                print("** add_additional_client 5")
                raise XRayAPIException("API Response is not valid")

            ret = resp.json()

            success = ret.get('success', False)

            if not success:
                msg = ret.get('msg', "")

                print("** add_additional_client 5.1")
                raise XRayAPIException(msg)

            print(ret)

            # obj = ret.get('obj', {})
            #
            # if not obj:
            #     print("** add_additional_client 6")
            #     raise XRayAPIException("API Response is not valid")
            #
            # id = obj.get('id', 0)

            new_client = XRayClient({
                "email": client_email,
                "enable": True,
                "expiryTime": expiry_ts,
                "flow": flow,
                "id": client_id,
                "subId": client_sub_id,
            }, {
                "down": 0,
                "up": 0
            },
            XRayInboundSettings(self.api_host, port, client_name, protocol, network, security, private_cert, public_cert, fingerprint, spiderX, sni, shortIds))

            return {
                "inbound_id": inbound_id,
                "sub_id": client_sub_id,
                "client_id": client_id,
                "client_email": client_email,
                "key": new_client.client_key,
                "expiry_ts": expiry_ts
            }


            #{"success":true,"msg":"Client(s) added Successfully","obj":null}
        except requests.exceptions.HTTPError as err:
            print("Http Error:", err)
            raise err
        except requests.exceptions.ConnectionError as err:
            print("Error Connecting:", err)
            raise err
        except requests.exceptions.Timeout as err:
            print("Timeout Error:", err)
            raise err
        except requests.exceptions.JSONDecodeError as err:
            print("DEcode error:", err)
            raise err
        except requests.exceptions.RequestException as err:
            print("Request error:", err)
            raise err

    def quick_add_client(self, client_name, limit_in_gb=0, expiry_in_days=0, sni="store.steampowered.com", limit_of_ip=1):
        if not self.__is_logged:
            raise XRayAPIException("You must login first")

        if len(self.__cookie) == 0:
            raise XRayAPIException("Invalid creds")

        url = f"{self.__api_url}{XRayAPIRoutes.ADD_INBOUND.value}"

        try:
            if limit_in_gb > 0:
                limit_in_gb = limit_in_gb * 1024 * 1024 * 1024

            expiry_ts = 0

            if expiry_in_days > 0:
                orig_date = datetime.datetime.fromtimestamp(time.time())
                new_date = orig_date + datetime.timedelta(days=expiry_in_days)
                expiry_ts = int(new_date.timestamp()) * 1000

            print("*** quick_add_client")
            print(f"days {expiry_in_days}")
            print(f"expiry_ts {expiry_ts}")

            client_name = client_name.replace('-', '_')
            new_port = random.randint(21578, 65531)
            client_id = str(uuid.uuid4())
            client_email = self.__random_lower_and_num__(12)
            client_sub_id = self.__random_lower_and_num__(16)
            flow = "xtls-rprx-vision"
            network = "tcp"
            security = "reality"
            fingerprint = "chrome"
            spiderX = "/"
            shortIds = self.__random_short_ids__()
            protocol = "vless"

            # return {
            #
            # }

            new_cert = self.new_cert()

            settings = {
                "clients": [
                    {
                        "id": client_id,
                        "flow": flow,
                        "email": client_email,
                        "limitIp": limit_of_ip,
                        "totalGB": 0,
                        "expiryTime": expiry_ts,
                        "enable": True,
                        "tgId": "",
                        "subId": client_sub_id,
                        "reset": 0
                    }],
                "decryption": "none",
                "fallbacks": []
            }



            streamSettings = {
                "network": network,
                "security": security,
                "externalProxy": [],
                "realitySettings": {
                    "show": False,
                    "xver": 0,
                    "dest": f"{sni}:443",
                    "serverNames": [sni],
                    "privateKey": new_cert['private'],
                    "minClient": "",
                    "maxClient": "",
                    "maxTimediff": 0,
                    "shortIds": shortIds,
                    "settings": {
                        "publicKey": new_cert['public'],
                        "fingerprint": fingerprint,
                        "serverName": "",
                        "spiderX": spiderX
                    }
                },
                "tcpSettings": {
                    "acceptProxyProtocol": False,
                    "header": {
                        "type": "none"
                    }
                }
            }

            sniffing = {
                "enabled": False,
                "destOverride": ["http", "tls", "quic", "fakedns"],
                "metadataOnly": False,
                "routeOnly": False
            }

            allocate = {
                'strategy': 'always',
                'refresh': 5,
                'concurrency': 3
            }

            data = {
                "up": 0,
                "down": 0,
                "total": limit_in_gb,
                "remark": client_name,
                "enable": True,
                "expiryTime": expiry_ts,
                "listen": "",
                "port": new_port,
                "protocol": protocol,
                "settings": json.dumps(settings),
                "streamSettings": json.dumps(streamSettings),
                "sniffing": json.dumps(sniffing),
                "allocate": json.dumps(allocate),
            }

            # print(data)

            resp = requests.post(url, cookies=self.__cookie, json=data, headers={
                "Content-Type": "application/json"
            }, verify=False, timeout=15)

            if not resp:
                raise XRayAPIException("API Response is not valid")

            if resp.status_code != 200:
                raise XRayAPIException("API Response is not valid")

            ret = resp.json()

            success = ret.get('success', False)

            if not success:
                msg = ret.get('msg', "")
                raise XRayAPIException(msg)

            obj = ret.get('obj', {})

            if not obj:
                raise XRayAPIException("API Response is not valid")

            id = obj.get('id', 0)

            new_client = XRayClient({
                "email": client_email,
                "enable": True,
                "expiryTime": expiry_ts,
                "flow": flow,
                "id": client_id,
                "subId": client_sub_id,
            }, {
                "down": 0,
                "up": 0
            },
            XRayInboundSettings(self.api_host, new_port, client_name, protocol, network, security, new_cert['private'], new_cert['public'], fingerprint, spiderX, sni, shortIds))

            return {
                "inbound_id": id,
                "client_id": client_id,
                "client_email": client_email,
                "key": new_client.client_key,
                "expiry_ts": expiry_ts,
                "sub_id": client_sub_id,
                "inbound": {
                    "port": new_port,
                    "client_name": client_name,
                    "protocol": protocol,
                    "network": network,
                    "security": security,
                    "fingerprint": fingerprint,
                    "spiderX": spiderX,
                    "short_ids": shortIds,
                    "public_cert": new_cert['public'],
                    "private_cert": new_cert['private'],
                }
            }
        except requests.exceptions.HTTPError as err:
            print("Http Error:", err)
            raise err
        except requests.exceptions.ConnectionError as err:
            print("Error Connecting:", err)
            raise err
        except requests.exceptions.Timeout as err:
            print("Timeout Error:", err)
            raise err
        except requests.exceptions.JSONDecodeError as err:
            print("DEcode error:", err)
            raise err
        except requests.exceptions.RequestException as err:
            print("Request error:", err)
            raise err

    def update_inbound(self, inbound_id, inbound: XRayInbound, add_days, save_traffic_limit=False):
        if not self.__is_logged:
            raise XRayAPIException("You must login first")

        if len(self.__cookie) == 0:
            raise XRayAPIException("Invalid creds")

        url = f"{self.__api_url}{XRayAPIRoutes.UPDATE_INBOUND.value}/{inbound_id}"

        expired_time = inbound.expired_time
        download = inbound.download
        upload = inbound.upload
        total = inbound.total
        port = inbound.port
        protocol = inbound.protocol

        if (expired_time / 1000) < int(time.time()):
            orig_date = datetime.datetime.fromtimestamp(int(time.time()))
        else:
            orig_date = datetime.datetime.fromtimestamp(expired_time / 1000)

        new_date = orig_date + datetime.timedelta(days=add_days)
        expiry_ts = int(new_date.timestamp()) * 1000

        inboundSettings = inbound.settings

        try:
            settings = {
                "clients": [
                    {
                        "id": x.client_id,
                        "flow": x.flow,
                        "email": x.email,
                        "limitIp": x.limitIp,
                        "totalGB": x.totalGB,
                        "expiryTime": expiry_ts,
                        "enable": x.is_enabled,
                        "tgId": "",
                        "subId": x.client_sub_id,
                        "reset": 0
                    } for x in inbound.clients],
                "decryption": "none",
                "fallbacks": []
            }

            streamSettings = {
                "network": inboundSettings.network,
                "security": inboundSettings.security,
                "externalProxy": [],
                "realitySettings": {
                    "show": False,
                    "xver": 0,
                    "dest": f"{inboundSettings.sni}:443",
                    "serverNames": [inboundSettings.sni],
                    "privateKey": inboundSettings.private_key,
                    "minClient": "",
                    "maxClient": "",
                    "maxTimediff": 0,
                    "shortIds": inboundSettings.short_ids,
                    "settings": {
                        "publicKey": inboundSettings.public_key,
                        "fingerprint": inboundSettings.fingerprint,
                        "serverName": "",
                        "spiderX": inboundSettings.spider_x
                    }
                },
                "tcpSettings": {
                    "acceptProxyProtocol": False,
                    "header": {
                        "type": "none"
                    }
                }
            }

            sniffing = {
                "enabled": False,
                "destOverride": ["http", "tls", "quic", "fakedns"],
                "metadataOnly": False,
                "routeOnly": False
            }

            allocate = {
                'strategy': 'always',
                'refresh': 5,
                'concurrency': 3
            }

            data = {
                "up": upload,
                "down": download,
                "total": total if save_traffic_limit else 0,
                "remark": inbound.inbound_label,
                "enable": True,
                "expiryTime": expiry_ts,
                "listen": "",
                "port": port,
                "protocol": protocol,
                "settings": json.dumps(settings),
                "streamSettings": json.dumps(streamSettings),
                "sniffing": json.dumps(sniffing),
                "allocate": json.dumps(allocate),
            }

            print(data)


            resp = requests.post(url, cookies=self.__cookie, json=data, headers={
                "Content-Type": "application/json"
            }, verify=False, timeout=15)

            if not resp:
                print("** update_inbound 4")
                raise XRayAPIException("API Response is not valid")

            if resp.status_code != 200:
                print("** update_inbound 5")
                raise XRayAPIException("API Response is not valid")

            return int(expiry_ts / 1000)
        except requests.exceptions.HTTPError as err:
            print("Http Error:", err)
            raise err
        except requests.exceptions.ConnectionError as err:
            print("Error Connecting:", err)
            raise err
        except requests.exceptions.Timeout as err:
            print("Timeout Error:", err)
            raise err
        except requests.exceptions.JSONDecodeError as err:
            print("DEcode error:", err)
            raise err
        except requests.exceptions.RequestException as err:
            print("Request error:", err)
            raise err

    def get_inbound_by_id(self, inbound_id):
        if not self.__is_logged:
            raise XRayAPIException("You must login first")

        if len(self.__cookie) == 0:
            raise XRayAPIException("Invalid creds")

        url = f"{self.__api_url}{XRayAPIRoutes.GET_INBOUND.value}/{inbound_id}"

        try:
            resp = requests.get(url, cookies=self.__cookie, headers={
                "Content-Type": "application/json"
            }, verify=False, timeout=15)

            if not resp:
                raise XRayAPIException("API Response is not valid")

            if resp.status_code != 200:
                raise XRayAPIException("API Response is not valid")

            ret = resp.json()

            if not ret:
                raise XRayAPIException("API Response is not valid")

            success = ret.get('success', False)

            if not success:
                raise XRayAPIException("Username or password incorrect")

            inbound = ret.get('obj', {})

            return XRayInbound(inbound, self.api_host)

        except requests.exceptions.HTTPError as err:
            print("Http Error:", err)
            raise err
        except requests.exceptions.ConnectionError as err:
            print("Error Connecting:", err)
            raise err
        except requests.exceptions.Timeout as err:
            print("Timeout Error:", err)
            raise err
        except requests.exceptions.JSONDecodeError as err:
            print("DEcode error:", err)
            raise err
        except requests.exceptions.RequestException as err:
            print("Request error:", err)
            raise err

    def get_inbounds_list(self):
        if not self.__is_logged:
            raise XRayAPIException("You must login first")

        if len(self.__cookie) == 0:
            raise XRayAPIException("Invalid creds")

        url = f"{self.__api_url}{XRayAPIRoutes.INBOUNDS_LIST.value}"

        try:
            resp = requests.get(url, cookies=self.__cookie, headers={
                "Content-Type": "application/json"
            }, verify=False, timeout=15)

            if not resp:
                raise XRayAPIException("API Response is not valid")

            if resp.status_code != 200:
                raise XRayAPIException("API Response is not valid")

            ret = resp.json()

            if not ret:
                raise XRayAPIException("API Response is not valid")

            success = ret.get('success', False)

            if not success:
                raise XRayAPIException("Username or password incorrect")

            # print(ret)

            inbounds = ret.get('obj', [])

            return [
                XRayInbound(i, self.api_host) for i in inbounds
            ]
        except requests.exceptions.HTTPError as err:
            print("Http Error:", err)
            raise err
        except requests.exceptions.ConnectionError as err:
            print("Error Connecting:", err)
            raise err
        except requests.exceptions.Timeout as err:
            print("Timeout Error:", err)
            raise err
        except requests.exceptions.JSONDecodeError as err:
            print("DEcode error:", err)
            raise err
        except requests.exceptions.RequestException as err:
            print("Request error:", err)
            raise err