#  _    _                                               _              _
# | |  | |                          /\           (_)   | |            | |
# | |__| | ___  _ __ ___   ___     /  \   ___ ___ _ ___| |_ __ _ _ __ | |_
# |  __  |/ _ \| '_ ` _ \ / _ \   / /\ \ / __/ __| / __| __/ _` | '_ \| __|
# | |  | | (_) | | | | | |  __/  / ____ \\__ \__ \ \__ \ || (_| | | | | |_
# |_|  |_|\___/|_| |_| |_|\___| /_/    \_\___/___/_|___/\__\__,_|_| |_|\__|
#    ___                                  _ _   _
#   / _ \_____      _____ _ __  __      _(_) |_| |__
#  / /_)/ _ \ \ /\ / / _ \ '__| \ \ /\ / / | __| '_ \
# / ___/ (_) \ V  V /  __/ |     \ V  V /| | |_| | | |
# \/    \___/ \_/\_/ \___|_|      \_/\_/ |_|\__|_| |_|
# /\_/\___  _   _ _ __    / __\___  _ __ | |_ _ __ ___ | | / \
# \_ _/ _ \| | | | '__|  / /  / _ \| '_ \| __| '__/ _ \| |/  /
#  / \ (_) | |_| | |    / /__| (_) | | | | |_| | | (_) | /\_/
#  \_/\___/ \__,_|_|    \____/\___/|_| |_|\__|_|  \___/|_\/
#
# Github:
# https://github.com/dadaloop82/HASS_AppDeamon_SwitchPredictor

# Constant
class Constant:
    print("constant")

    CONST_HEMISPHERE = "north"
    DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S+00:00"
    ALT_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f+00:00"
    ONPERIOD_DATETIME_FORMAT = "%H:%M"
    MODELPATH = "models"
    CONFIG_PARMS = [
        {"historyday": {"default": 30}},
        {"timerangehistoryseconds": {"default": 0}},
        {"mergeonperiodminutes": {"default": 15}},
        {"roundtimeevents": {"default": 15}},
        {"excludetimeslotpercentage": {"default": 30}},
        {"timezone": {"default": "Europe/Rome"}}
    ]
