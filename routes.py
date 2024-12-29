from enum import Enum

class XRayAPIRoutes(Enum):
    LOGIN = '/login'
    INBOUNDS_LIST = '/panel/api/inbounds/list'
    NEW_CERT = '/server/getNewX25519Cert'
    ADD_INBOUND = '/panel/api/inbounds/add'
    ADD_CLIENT = '/panel/inbound/addClient'
    GET_INBOUND = '/panel/api/inbounds/get'
    UPDATE_INBOUND = '/panel/inbound/update'
    GET_SETTINGS = '/panel/setting/all'