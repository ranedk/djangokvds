from django.conf import settings
from django.http import HttpResponseServerError
import logging

# logging # {{{
def create_logger(name=None):
    if name is None:
        name = settings.APP_DIR.namebase
    logger = logging.getLogger(name)
    hdlr = logging.FileHandler(
        settings.APP_DIR.joinpath("%s.log" % name)
    )
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    return logger

logger = create_logger()
# }}}

# SimpleExceptionHandler www.djangosnippets.org/snippets/650/ # {{{
class SimpleExceptionHandler:
    def process_exception(self, request, exception):
        import sys, traceback
        (exc_type, exc_info, tb) = sys.exc_info()
        response = "%s\n" % exc_type.__name__
        response += "%s\n\n" % exc_info
        response += "TRACEBACK:\n"    
        for tb in traceback.format_tb(tb):
            response += "%s\n" % tb
        logger.exception(exception)    
        if not settings.DEBUG: return
        if not request.is_ajax(): return
        return HttpResponseServerError(response)
# }}}
