import logging
from django.template import RequestContext

from core import constants

logger = logging.getLogger(__name__)

def environment(request):
    logger.debug("Inside Context Processor constants")
    request_context = RequestContext(request)
    object = request_context.get("object",otherwise="NotSet")
    return {
        'constants':constants,
        'object':object
    }