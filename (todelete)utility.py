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

# python module imports
import datetime
import pytz
import os

# variables
datetime = datetime.datetime


class Utility:
  print("utility")

# class CurrentModel:
#     def __init__(self):
#        # set Variables
#        # {bt} = data about baseentity
#        # {bo} = data about basedOnEntities
#         self.currentModel = {'bt': {}, 'bo': {}}

#     def getCurrentModel(self):
#         return self.currentModel


# def getCurrentDatetime():
#     return datetime.now(pytz.timezone(configGet("timezone"))).replace(tzinfo=None)


# def getCurrentFolder():
#     return os.path.dirname(os.path.abspath(__file__))


# def convertdatatime(datatimeString):
#     if "." in datatimeString:
#         datatimeString = datetime.strptime(
#             datatimeString, ALT_DATETIME_FORMAT).strftime(DATETIME_FORMAT)
#     a = hass.parse_utc_string(datatimeString)
#     b = datetime.utcfromtimestamp(a)
#     return b


# def getdifferncedate(date, keytime, value):
#     if keytime == 'days':
#         return date - datetime.timedelta(days=value)
#     return None


# def stringisnumber(string):
#     try:
#         float(string)
#         return True
#     except:
#         return False


# def setifnotexist(objvar, key, initvalue):
#     if key in objvar:
#         return objvar
#     objvar[key] = initvalue
#     return objvar


# def roundDateByMinutes(dt, delta):
#     return (dt + (datetime.datetime.min - dt) % delta).replace(year=1900, month=1, day=1, second=0, microsecond=00)


# def getSeasonByDate(date):
#     md = date.month * 100 + date.day
#     if ((md > 320) and (md < 621)):
#         s = 0  # spring
#     elif ((md > 620) and (md < 923)):
#         s = 1  # summer
#     elif ((md > 922) and (md < 1223)):
#         s = 2  # fall
#     else:
#         s = 3  # winter
#     if not CONST_HEMISPHERE == 'north':
#         s = (s + 2) % 3
#     return s
