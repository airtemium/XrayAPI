from repo.xray.settings import XRayInboundSettings
from urllib.parse import urlparse, parse_qs, quote_plus

class XRayClient:
    #{'email': 'lbb8soc7', 'enable': True, 'expiryTime': 0, 'flow': 'xtls-rprx-vision', 'id': 'd7de8f9a-d562-4f54-bad0-4305c19c136a',
    # 'limitIp': 0, 'reset': 0, 'subId': 's40dknig0i5dybtb', 'tgId': '', 'totalGB': 0}
    #{'id': 4, 'inboundId': 4, 'enable': True, 'email': 'fqzyv098', 'up': 188907, 'down': 449282, 'expiryTime': 0, 'total': 0, 'reset': 0}

    __email: None
    __enabled: False
    __expired_time: 0
    __flow: None
    __id: None
    __sub_id: None
    __upload: 0
    __download: 0
    __limitIp: 0
    __totalGB: 0
    __setting: None

    def __init__(self, obj, stat_obj, settings: XRayInboundSettings):
        self.__setting = settings
        self.__email = obj.get('email', None)
        self.__enabled = obj.get('enable', False)
        self.__expired_time = obj.get('expiryTime', 0)
        self.__limitIp = obj.get('limitIp', 0)
        self.__totalGB = obj.get('totalGB', 0)
        self.__flow = obj.get('flow', None)
        self.__id = obj.get('id', None)
        self.__sub_id = obj.get('subId', None)

        if stat_obj:
            self.__download = stat_obj.get("down", 0)
            self.__upload = stat_obj.get("up", 0)

    @property
    def client_sub_id(self) -> str:
        return self.__sub_id

    @property
    def client_key(self) -> str:
        if not self.__setting:
            return None

        protocol = self.__setting.protocol
        port = self.__setting.port
        api_host = self.__setting.api_host
        security = self.__setting.security
        network = self.__setting.network
        public_key = self.__setting.public_key
        fingerprint = self.__setting.fingerprint
        short_ids = self.__setting.short_ids
        spider_x = self.__setting.spider_x
        sni = self.__setting.sni
        remark = self.__setting.remark

        if not protocol:
            return None

        if not spider_x:
            return None

        id = self.client_id
        sid = self.__sub_id
        email = self.__email
        flow = self.__flow

        if not id:
            return None

        if not port:
            return None

        if not api_host:
            return None

        if not security:
            return None

        if not network:
            return None

        if not public_key:
            return None

        if not fingerprint:
            return None

        if not sni:
            return None

        if not flow:
            return flow

        if not short_ids or len(short_ids) == 0:
            return None

        if not remark or not email:
            return None

        url_data = []
        url_data.append(f"{protocol}://")
        url_data.append(f"{id}@")
        url_data.append(api_host)
        url_data.append(f":{port}")
        url_data.append("?")
        url_data.append(f"type={network}")
        url_data.append(f"&security={security}")
        url_data.append(f"&pbk={public_key}")
        url_data.append(f"&fp={fingerprint}")
        url_data.append(f"&sni={sni}")
        url_data.append(f"&sid={short_ids[0]}")
        url_data.append(f"&spx={quote_plus(spider_x)}")
        url_data.append(f"&flow={flow}")
        url_data.append(f"#{remark}-{email}")

        return ''.join(url_data)

        # return vless://
        # 1a6c96c0-99fb-4cd8-a822-84233072e530@
        # fn1.silvervpn.ru
        # :13925
        # ?type=tcp
        # &security=reality
        # &pbk=CGyfMGzZZSO7h1JXBnkbbEuL-S7dFxiiFvwTqCrbZn8
        # &fp=random
        # &sni=vk.com
        # &sid=e1a3c5b4ce
        # &spx=%2F
        # &flow=xtls-rprx-vision
        # #qwerty-fqzyv098

    @property
    def client_id(self):
        return self.__id

    @property
    def limitIp(self):
        return self.__limitIp

    @property
    def totalGB(self):
        return self.__totalGB

    @property
    def email(self):
        return self.__email

    @property
    def flow(self):
        return self.__flow


    @property
    def is_enabled(self):
        return self.__enabled