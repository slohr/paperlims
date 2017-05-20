import re
import logging
import xlrd
import os
import errno
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)


def get_typical_timestamp():
  return datetime.now().strftime("%Y-%m-%d-%H%M")

def get_recursive_dict():
  recursive_default_dict = lambda: defaultdict(recursive_default_dict)
  return defaultdict(recursive_default_dict)

def NoneToString(string):
  if string is None:
    return ''
  return str(string)

def self_zip(list):
  return zip(list,list)


def float_convert(value):
  ret = None
  try:
    ret = float(value)
  except ValueError:
    ret = None
  return ret