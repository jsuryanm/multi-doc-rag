import sys 
import traceback
from typing import Optional,cast

class DocumentPortalException(Exception):
    def __init__(self, error_message,error_details: Optional[object]=None):
        
        if isinstance(error_message,BaseException):
            norm_msg = str(error_message)
        else:
            norm_msg = str(error_message)

            