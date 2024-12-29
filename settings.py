class XRayInboundSettings:
    __api_host: None
    __port: None
    __remark: None
    __protocol: None
    __network: None
    __security: None
    __public_key: None
    __private_key: None
    __fingerprint: None
    __spider_x: None
    __sni: None
    __short_ids: []

    def __init__(self, api_host, port, remark, protocol, network, security, private_key, public_key, fingerprint, spider_x, sni, short_ids):
        self.__api_host = api_host
        self.__port = port
        self.__remark = remark
        self.__protocol = protocol
        self.__network = network
        self.__security = security
        self.__public_key = public_key
        self.__private_key = private_key
        self.__fingerprint = fingerprint
        self.__spider_x = spider_x
        self.__sni = sni
        self.__short_ids = short_ids

    @property
    def api_host(self):
        return self.__api_host

    @property
    def short_ids(self):
        return self.__short_ids

    @property
    def fingerprint(self):
        return self.__fingerprint

    @property
    def sni(self):
        return self.__sni

    @property
    def spider_x(self):
        return self.__spider_x

    @property
    def public_key(self):
        return self.__public_key

    @property
    def private_key(self):
        return self.__private_key

    @property
    def security(self):
        return self.__security

    @property
    def remark(self):
        return self.__remark

    @property
    def protocol(self):
        return self.__protocol

    @property
    def network(self):
        return self.__network

    @property
    def port(self):
        return self.__port