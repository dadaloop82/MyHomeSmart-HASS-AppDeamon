
# Json python library
import json


def getConfigValue(self: any, key: str) -> str:
    """_summary_

    Args:
        self (any):       The appDeamon HASS Api
        key (str):        The key to check to return the value

    Returns:
        (str):            The value from key in appDeamon Config
    """
    _config = self.args['config']
    if not key in _config:
        return False
    return _config[key]


def parseDictValueForSqlite(v: dict) -> str:
    """parse the Values of Dict for sqlLite compatibility

    Args:
        v (dict):     the dict to parse

    Returns:
        str:          the string with values parsed
    """
    try:
        return ','.join([
            "'"+str(json.dumps(x))+"'" if isinstance(x, dict)
            else "'"+str(x)+"'" for x in v.values()])
    except:
        return None
