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
#
# I have a dream:
# - make my life smarter without creating any automation!
#
# Ingredients:
# - Working instance of Home Assistant (https://www.home-assistant.io/)
# - Working addon appDeamon for HASS (https://github.com/AppDaemon/appdaemon)
# - Optional influxDB database - otherwise takes data from history (they are limited!)
#
# Operating idea:
# - Based on the analysis of the change of a certain switch
# - (set in configuration), the system analyzes the change of the sensors in that moment
# - So it creates a model, divided by periods (including seasons, etc. ..)
# - trying to guess their habits and if the conditions are similar, it proposes via Alexa
# - the activation of the switch, learning from the answers given.
# - If the probability of activation is very high,
# - the action could be performed automatically without any iteration with the user.
#
# Dependencies:
# - numpy (**installation are very slow, be patient!**)
# - pandas (**installation are very slow, be patient!**)
# - influxdb-client
# - sklearn

# from influxdb_client import InfluxDBClient

# python module imports
import hassapi as hass
import pytz
from datetime import datetime, timedelta
import pandas as pd
import os
from sklearn import model_selection
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from math import sqrt
"""
Constant and Variables
"""


class Constant:
    def __init__(self):
        self.DateTimeFormat = "%Y-%m-%d %H:%M:%S"
        self.DateTimeFormat_T = "%Y-%m-%dT%H:%M:%SZ"
        self.DateTimeFormat_TZ = "%Y-%m-%dT%H:%M:%S+00:00"
        self.DateTimeFormat_sTZ = "%Y-%m-%dT%H:%M:%S+00:00"
        self.DateTimeFormat_msTZ = "%Y-%m-%dT%H:%M:%S.%f+00:00"
        self.Time_short = "%H:%M"
        self.Path_Model = "models"
        self.Hemisphere = "north"
        self.UseInfluxDB = False
        self.UseHassBuildInDB = False
        self.Now = datetime.now()
        self.Currentfolder = os.path.dirname(os.path.abspath(__file__))

        self.EVENT_TIME = "time"
        self.EVENT_VALUE = "value"
        self.EVENT_DOMAIN = "domain"
        self.EVENT_ENTITYID = "entity_id"

        self.EVENT_TIME_HOUR = "hour"
        self.EVENT_TIME_MINUTE = "minute"

        self.EVENT_TIME_DAY = "day"
        self.EVENT_TIME_MONTH = "month"
        self.EVENT_TIME_YEAR = "year"

        self.EVENT_TIME_WEEKDAY = "weekday"
        self.EVENT_TIME_SEASON = "season"

        self.EVENT_TIME_WEEKOFYEAR = "weekofyear"
        self.EVENT_TIME_QUARTER = "quarter"
        self.EVENT_TIME_MONTHSTART = "monthstart"
        self.EVENT_TIME_MONTHEND = "monthend"

        self.influxDB_Qhistory = '''
                                from(bucket: "{bucket}")
                                |> range(start: {start}, stop: {stop})
                                |> filter(fn: (r) => r["domain"] == "{domain}")
                                |> filter(fn: (r) => r["entity_id"] == "{entity_id}")
                                |> filter(fn: (r) => r["_field"] == "{fieldtype}")
                                |> drop(columns:["_field", "_measurement", "friendly_name", "source","_start","_stop","domain","entity_id"])
                                |> sort(columns:["_time"])
                                |> yield(name: "mean")
                                '''

        self.dummy_cols = {'year': 'year',
                           'month': 'month',
                           'weekday': 'wday',
                           'quarter': 'qrtr',
                           'monthstart': 'm_start',
                           'monthend': 'm_end',
                           'season': 'season'}


"""
Config Class
"""


class Config:
    """
    Config Class:
                  - read the configuration
                  - set default config parameters
                  - set flag for UseInfluxDB
    """

    def __init__(self, hass, constant):
        self._hass = hass
        self._constant = constant

        self.configParms = self._hass.args["config"]
        self.currentConfig = {}
        self.useInfluxDB = False
        self.UseHassBuildInDB = False

        # default value of parameters
        self.defaultParams = {
            "historyday": 30,
            "timerangehistoryseconds": 0,
            "excludetimeslotpercentage": 30,
            "timezone": "Europe/Rome",
            "useinfluxdb": False
        }

        # read the config
        self.readConfig()

        # set the useInfluxDB flag
        if self.currentConfig["useinfluxdb"]:
            # setup the influxDB boolean
            self._constant.UseInfluxDB = True
        else:
          # setup the hassBuildin DB boolean
            self._constant.UseHassBuildInDB = True

    """
    Config Class:
                    read the configuration's value from apps.yaml
                    and apply default who key is missing
    """

    def readConfig(self) -> object:
        # set the current configuration
        self.currentConfig = self.configParms

        # set the default config value when missing
        for key, value in self.defaultParams.items():
            if not key in self.configParms:
                self.currentConfig[key] = value


"""
HassIO history manager (build-in history and influxDB )
"""


class predictionUtil:
    """
    predictionUtil Class:
                      - if UseInfluxDB are true, load the PIP module (must be added in appDeamon!)
                      - setup the connection
                      - do a query for test
    """

    def __init__(self, hass, constant, config, utility):
        self._hass = hass
        self._utility = utility
        self._constant = constant
        self._config = config

        self.influxDB_client = None
        self.InfluxDB_module = None
        self.influxDB_queryapi = None
        self.influxDB_config = None

        if constant.UseInfluxDB:
            # using influDB

            try:
                # import the module
                influxbModule = __import__("influxdb_client")
                self.InfluxDB_module = influxbModule.InfluxDBClient
            except:
                self._hass.log(
                    "InfluxDB enabled but library are not loaded in AppDeamon, fallback to HASS history (limited!)", level="WARNING")
                self._constant.UseInfluxDB = False
                self._constant.UseHassBuildInDB = True

            try:
                # set the influxDB config
                self.influxDB_config = self._config.currentConfig['influxdb']
                self.influxDB_client = self.InfluxDB_module(
                    url=self.influxDB_config['url'], token=self.influxDB_config['token'], org=self.influxDB_config['org'])
            except:
                self._hass.log(
                    "InfluxDB is enabled but not configured correctly, fallback to HASS history (limited!)", level="WARNING")
                self._constant.UseInfluxDB = False
                self._constant.UseHassBuildInDB = True

    """
    predictionUtil Class:
                        Get history with actived module (HASS build-in or influxDB)
                        > kwargs  (dict arguments)  arguments (ex: start=[dt], end=[dt])
    """

    def getHistory(self, kwargs) -> pd:

        pd_result = pd.DataFrame()

        if self._constant.UseInfluxDB:
            self._hass.log(
                f"Asking influxDb for < {kwargs['entityid'] if 'entityid' in kwargs else ''} > history")
            # using influxDB
            q = self._constant.influxDB_Qhistory.format(
                bucket=self.influxDB_config['bucket'],
                start=kwargs['start'].strftime(
                    self._constant.DateTimeFormat_T) if 'start' in kwargs else self._constant.Now.strftime(
                    self._constant.DateTimeFormat_T),
                stop=kwargs['stop'].strftime(
                    self._constant.DateTimeFormat_T) if 'stop' in kwargs else self._constant.Now.strftime(
                    self._constant.DateTimeFormat_T),
                domain=kwargs['entityid'].split(
                    ".")[0] if 'entityid' in kwargs else "*",
                entity_id=kwargs['entityid'].split(
                    ".")[1] if 'entityid' in kwargs else "*",
                fieldtype="state" if kwargs['entityid'].split(".")[0] in ["switch", "person", "binary_sensor"] else "value")

            # get Pandas results
            # print(q)
            pd_result = self.influxDB_client.query_api().query_data_frame(
                q).rename(columns={
                    '_value': self._constant.EVENT_VALUE, '_time': self._constant.EVENT_TIME}).assign(
                **{self._constant.EVENT_ENTITYID: kwargs['entityid'] if 'entityid' in kwargs else ""}).set_index(self._constant.EVENT_TIME)

            pd_result.rename(columns={
                '_value': self._constant.EVENT_VALUE, '_time': self._constant.EVENT_TIME})

        if self._constant.UseHassBuildInDB:
            self._hass.log(
                f"Asking Hass(build-in History) for < {kwargs['entityid'] if 'entityid' in kwargs else ''} > history")

            # using HassBuildInDB
            hasshistory = self._hass.get_history(entity_id=kwargs['entityid'] if 'entityid' in kwargs else "*", start_time=kwargs['start']
                                                 if 'start' in kwargs else self._constant.Now, end_time=kwargs['stop'] if 'stop' in kwargs else self._constant.Now)[0]

            # convert last_changed to datetime
            for h in hasshistory:
                h['last_changed'] = datetime.strptime(
                    h['last_changed'], self._constant.DateTimeFormat_msTZ if "." in h['last_changed'] else self._constant.DateTimeFormat_sTZ)

            # get dataFrame results
            df_result = pd.DataFrame(hasshistory, columns=[
                'last_changed', 'state', 'entity_id']).rename(columns={
                    'state': self._constant.EVENT_VALUE,
                    'last_changed': self._constant.EVENT_TIME,
                    'entity_id': self._constant.EVENT_ENTITYID}).set_index(self._constant.EVENT_TIME)

            # convert it to Pandas and rename useful fields
            if not df_result.empty:
                pd_result = df_result

        if not pd_result.empty:

          # split the #time
            pd_result[self._constant.EVENT_TIME_HOUR] = pd_result.index.hour
            pd_result[self._constant.EVENT_TIME_MINUTE] = pd_result.index.minute
            pd_result[self._constant.EVENT_TIME_DAY] = pd_result.index.day
            pd_result[self._constant.EVENT_TIME_HOUR] = pd_result.index.hour
            pd_result[self._constant.EVENT_TIME_MONTH] = pd_result.index.month
            pd_result[self._constant.EVENT_TIME_YEAR] = pd_result.index.year
            pd_result[self._constant.EVENT_TIME_QUARTER] = pd_result.index.quarter
            pd_result[self._constant.EVENT_TIME_MONTHSTART] = pd_result.index.is_month_start
            pd_result[self._constant.EVENT_TIME_MONTHEND] = pd_result.index.is_month_end
            pd_result[self._constant.EVENT_TIME_WEEKDAY] = pd_result.index.day_of_week
            pd_result[self._constant.EVENT_TIME_SEASON] = pd_result.index.to_series().apply(
                lambda x:  self._utility.getSeasonByDate(x))

            # get first datatime
            first_DT = pd_result.index[0]
            last_DT = pd_result.index[-1]

            # print(pd_result.iloc[1])

        return (pd_result, first_DT, last_DT)

    """
    setSituations Class:
                        Combine the based entity id with baseswitch entity id and search situations
                        > masterPD  (pandas)  pandasObject Master (baseSwitch)
                        > slavePD  (pandas)  pandasObject SlavePD (basedOnSwitch)
    """

    def setSituations(self, masterPD, slavePD) -> pd:
        if slavePD.empty or masterPD.empty:
            return False
        slaveEntityID = slavePD.iloc[1][self._constant.EVENT_ENTITYID]
        masterEntityID = masterPD.iloc[1][self._constant.EVENT_ENTITYID]

        self._hass.log(
            f"Combine < {masterEntityID} > with < {slaveEntityID} > and search situations")

        masterPD[slaveEntityID] = masterPD.index.to_series().apply(
            lambda x:  slavePD.iloc[slavePD.index.get_loc(x, method='nearest')]['value'])

        return masterPD

    def createDummyEncoding(self, pdObject) -> pd:

        ret = pdObject
        for dummycols_key in self._constant.dummy_cols.keys():
            ret = pd.get_dummies(ret, columns=[dummycols_key], drop_first=True,
                                 prefix=self._constant.dummy_cols[dummycols_key])
        return ret


"""
Utility Class
"""


class Utility:
    """
      Utility Class:   Init
    """

    def __init__(self, hass, constant):
        self._hass = hass
        self._constant = constant

    """
    Utility Class:
                      Calculate the datetime difference and return the datetime object
                      > dtobj     (datetime object) the datetime context
                      > **kwargs  (dict arguments)  arguments (ex: minutes=1)
    """

    def dateTimeDiffernce(self, dtobj, **kwargs) -> datetime:
        return dtobj - timedelta(**kwargs)

    """
    Utility Class:
                      Detects if the datetime string contains a timezone notation
                      and converts the string to a datetime object
                      > dtstring    (string) the datetime context
    """

    def stringToDateTime(self, dtstring) -> datetime:
        if "." in dtstring:
            dtstring = datetime.strptime(
                dtstring, self._constant.DateTimeFormat_msTZ).strftime(self._constant.DateTimeFormat)
        dtstring = self._hass.parse_utc_string(dtstring)
        dtstring = datetime.utcfromtimestamp(dtstring)
        return dtstring

    """
    Utility Class:
                      Convert datetime object in ISO with timezone
                      > dtobj     (datetime object) the datetime context
    """

    def dateTimeToIsoTimezone(self, dtobj) -> datetime:
        return dtobj.replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")

    """
    Utility Class:
                      Transorm the datetime in date in midnight
                      > dtobj     (datetime object) the datetime context
    """

    def dateTimeToMidnight(self, dtobj) -> datetime:
        return dtobj.replace(hour=0, minute=0, second=00)

    """
    Utility Class:
                      Get season number (0/4)
                      > dtobj     (datetime object) the datetime context
    """

    def getSeasonByDate(self, dtobj):
        md = dtobj.month * 100 + dtobj.day
        if ((md > 320) and (md < 621)):
            s = 0  # spring
        elif ((md > 620) and (md < 923)):
            s = 1  # summer
        elif ((md > 922) and (md < 1223)):
            s = 2  # fall
        else:
            s = 3  # winter
        if not self._constant.Hemisphere == 'north':
            s = (s + 2) % 3
        return s


class HassPredictSwitch(hass.Hass):
    def initialize(self):
        self.log("Starting new instance, initialization ...", level="INFO")
        _constant = Constant()
        _config = Config(self, _constant)
        _utility = Utility(self, _constant)
        _predictionUtil = predictionUtil(self, _constant, _config, _utility)

        Config_predictsEvents = _config.currentConfig['predictsevents']
        if not Config_predictsEvents:
            self.log(
                "No event to predict specified in the configuration, please refer to apps.yaml of appDeamon", level="WARNING")
        else:

            # cycle for predictEventKey
            for predictEventKey in list(Config_predictsEvents.keys()):

                # get event Detail Configuration
                predictEventDetailConfig = Config_predictsEvents[predictEventKey]

                if not "base_switch" in predictEventDetailConfig:
                    self.log(
                        f"< {predictEventKey} > not have the base_switch key configured, please refer to apps.yaml of appDeamon", level="WARNING")
                else:
                    Config_predictsEventBaseSwitch = predictEventDetailConfig["base_switch"]
                    Config_daysHistory = _config.currentConfig['historyday']

                    (pdHistoryDM, firstDT, lastDT) = _predictionUtil.getHistory({
                        'start': _utility.dateTimeToMidnight(_utility.dateTimeDiffernce(_constant.Now, days=Config_daysHistory)),
                        'stop': _constant.Now,
                        'entityid': Config_predictsEventBaseSwitch
                    })

                    if pdHistoryDM.empty:
                        self.log(
                            f"history of {Config_predictsEventBaseSwitch} using {'influxDB' if _constant.UseInfluxDB else 'HASS Build-In History'} did not produce any results", level="WARNING")
                    else:
                        self.log(
                            f"Getting {len(pdHistoryDM)} history's item of < {Config_predictsEventBaseSwitch} > from {firstDT}")

                        # cycle the basedon Entity and get history
                        for predictEventKey_basedon in list(predictEventDetailConfig['basedon']):

                            (pdbasedonHistoryDM, firstDT, lastDT) = _predictionUtil.getHistory({
                                'start': _utility.dateTimeToMidnight(_utility.dateTimeDiffernce(_constant.Now, days=Config_daysHistory)),
                                'stop': _constant.Now,
                                'entityid': predictEventKey_basedon
                            })

                            if pdbasedonHistoryDM.empty:
                                self.log(
                                    f"history of {predictEventKey_basedon} using {'influxDB' if _constant.UseInfluxDB else 'HASS Build-In History'} did not produce any results", level="WARNING")
                            else:
                                self.log(
                                    f"Getting {len(pdbasedonHistoryDM)} history's item of < {predictEventKey_basedon} > from {firstDT}")

                                # combine the data
                                pdHistoryDM = _predictionUtil.setSituations(
                                    pdHistoryDM, pdbasedonHistoryDM)

                pdHistoryDM = _predictionUtil.createDummyEncoding(pdHistoryDM)

                

                # .get_dummies(pdHistoryDM, columns=['month'], drop_first=True, prefix='month').get_dummies(pdHistoryDM, columns=['weekday'], drop_first=True, prefix='wday').get_dummies(pdHistoryDM, columns=['quarter'], drop_first=True, prefix='qrtr')

                # !! Debug !!
                # pdHistoryDM.to_csv(os.path.join(
                #     _constant.Currentfolder, f"{predictEventKey}.csv"), sep='\t', encoding='utf-8')
