import inspect
import traceback
import module.constant as CONSTANT


def error(self: any, text: str, die: bool = False):
    """Custom representation of an error message in the log

    Args:
        self (any):             The appDeamon HASS Api
        text (str):             Text message of error
        die (bool, optional):   If the program should terminate after this error. Defaults to False.
    """
    info(self,
         "################################################################")
    self.error("ERROR in %s:%s - [ %s ]" %
               (inspect.stack()[1][3], inspect.stack()[1][2], text))
    if die:
        info(self, "################################################################")
        info(self, "due to this error, %s cannot continue and must be restarted." %
             (CONSTANT.APP_NAME))
        info(self, "################################################################")
    info(self, "== Traceback ==")
    info(self, traceback.format_exc())

    if die:
        exit()


def info(self, text):
    """Custom representation of an info message in the log

    Args:
        self (any):             The appDeamon HASS Api
        text (str):             Text message of error        
    """
    self.log(text)
