from repo.xray.settings import XRayInboundSettings
from repo.xray.exception import XRayAPIException
import json
from repo.xray.client import XRayClient
import time

class XRayInbound:
    __obj: None
    __inbound_id: None
    __enabled: False
    __expired_time: 0
    __upload: 0
    __download: 0
    __total: 0
    __inbound_label: None
    __port: 0
    __protocol: None
    __clients: []

    __network: None
    __security: None

    __private_key: None
    __public_key: None
    __fingerprint: None
    __spider_x: None
    __sni: None
    __short_ids: []

    __api_host: None

    def __init__(self, obj, api_host):
        if type(obj) is not dict:
            raise XRayAPIException("XRayClient init params incorrect")

        self.__api_host = api_host

        self.__obj = obj
        self.__parse_obj__()

    def __parse_obj__(self):
        self.__inbound_id = self.__obj.get("id", None)
        self.__enabled = self.__obj.get("enable", False)
        self.__expired_time = self.__obj.get("expiryTime", 0)
        self.__inbound_label = self.__obj.get("remark", None)
        self.__download = self.__obj.get("down", 0)
        self.__total = self.__obj.get("total", 0)
        self.__upload = self.__obj.get("up", 0)
        self.__protocol = self.__obj.get("protocol", None)
        self.__port = self.__obj.get("port", 0)

        self.__parse_settings__()
        self.__parse_clients__()

    def __parse_settings__(self):
        stream_settings = self.__obj.get("streamSettings", None)

        if not stream_settings:
            return

        stream_settings_dict = json.loads(stream_settings)

        self.__network = stream_settings_dict.get('network', 'tcp')
        self.__security = stream_settings_dict.get('security', None)

        if self.__security and self.__security == "reality":
            #{'show': False, 'xver': 0, 'dest': 'vk.com:443', 'serverNames': ['vk.com'],
            # 'privateKey': 'QLdk46IU9RKzHThE7VGygnewIgTQ3DMH223tvnVWtGo', 'minClient': '',
            # 'maxClient': '', 'maxTimediff': 0, 'shortIds': ['e1a3c5b4ce', '40', 'ea0da99a2cb56f90', '0a3c3dc3825c', '48f67567', 'b3e478', 'cc74a1e4189fd9', 'f0e9'],
            # 'settings': {'publicKey': 'CGyfMGzZZSO7h1JXBnkbbEuL-S7dFxiiFvwTqCrbZn8', 'fingerprint': 'random', 'serverName': '', 'spiderX': '/'}}

            if not 'realitySettings' in stream_settings_dict:
                return

            reality_settings = stream_settings_dict.get('realitySettings', {})

            self.__private_key = reality_settings.get('privateKey', None)

            # self.__public_key: None
            # self.__fingerprint: None
            # self.__spider_x: None
            # self.__sni: None
            #
            servers = reality_settings.get('serverNames', [])

            if len(servers) > 0:
                self.__sni = servers[0]

            self.__short_ids = reality_settings.get('shortIds', [])

            #
            #
            if 'settings' in reality_settings:
                settings = reality_settings.get('settings', {})

                self.__public_key = settings.get('publicKey', None)
                self.__fingerprint = settings.get('fingerprint', None)
                self.__spider_x = settings.get('spiderX', None)

            # print(stream_settings_dict['realitySettings'])

    def __parse_clients__(self):
        print("*** __parse_clients__ 1")

        settings = self.__obj.get("settings", None)

        if not settings:
            print("*** __parse_clients__ 2")
            return

        clientStats = self.__obj.get('clientStats', [])

        # if not clientStats:
        #     print("*** __parse_clients__ 3")
        #     return

        settings_dict = json.loads(settings)

        self.__clients = []

        if 'clients' in settings_dict:
            print("*** __parse_clients__ 4")

            for client in settings_dict['clients']:

                stat = None
                if clientStats:
                    stat = list(filter(lambda x: x['email'] == client['email'], clientStats))

                    stat = stat[0] if len(stat) > 0 else None

                self.__clients.append(XRayClient(client, stat, self.settings))

    @property
    def settings(self) -> XRayInboundSettings:
        # print(f"*** XRayInboundSettings INIT: api_host - {self.__api_host}, port - {self.__port}, network - {self.__network}, security - {self.__security}, PVK - {self.__private_key}, PBK - {self.__public_key}")
        # return None

        if not self.__api_host or not self.__port or not self.__protocol or not self.__network or not self.__security or not self.__private_key or not self.__public_key or not self.__fingerprint or not self.__spider_x or not self.__inbound_label or not self.__sni:
            return None

        # return None
        #
        return XRayInboundSettings(self.__api_host, self.__port, self.__inbound_label, self.__protocol,
                                   self.__network, self.__security, self.__private_key, self.__public_key,
                                   self.__fingerprint, self.__spider_x, self.__sni, self.__short_ids
                                   )

    @property
    def client_count(self):
        return len(self.__clients)

    @property
    def clients(self) -> [XRayClient]:
        return self.__clients

    @property
    def inbound_label(self):
        return self.__inbound_label

    @property
    def inbound_id(self):
        return self.__inbound_id

    @property
    def expired_time(self):
        return self.__expired_time

    @property
    def download(self):
        return self.__download

    @property
    def upload(self):
        return self.__upload

    @property
    def total(self):
        return self.__total

    @property
    def port(self):
        return self.__port

    @property
    def protocol(self):
        return self.__protocol

    @property
    def is_enabled(self):
        if self.__enabled and self.__expired_time == 0:
            return True

        if self.__expired_time > 0 and (self.__expired_time / 1000) > int(time.time()):
            return True

        return False