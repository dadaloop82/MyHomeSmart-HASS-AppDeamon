import inspect
import traceback
import module.constant as CONSTANT


def LogError(self: any, text: str, die: bool = False):
    """Custom representation of an error message in the log

    Args:
        self (any):             The appDeamon HASS Api
        text (str):             Text message of error
        die (bool, optional):   If the program should terminate after this error. Defaults to False.
    """
    self.log("--------------------------------------------------------")
    self.error("[ ERROR ] in %s:%s \t\t %s" %
               (inspect.stack()[1][3], inspect.stack()[1][2], text))
    if die:
        self.log("%s was terminated due to a fatal exception." %
                 (CONSTANT.APP_NAME))
        self.log("--------------------------------------------------------")
        self.log(traceback.format_exc())
        # exit()
    self.log("--------------------------------------------------------")


def LogInfo(self, text):
    """Custom representation of an info message in the log

    Args:
        self (any):             The appDeamon HASS Api
        text (str):             Text message of error        
    """
    self.log(text)
