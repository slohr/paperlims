import re
import logging
import xlrd
from django.core.files import File
from core.models import Project, DataFile


from django.db import transaction

import core.utils

logger = logging.getLogger(__name__)

def map_header_row(header_row):
  header_map = dict()
  index = 0
  for cell in header_row:
    logger.debug("{0} {1}".format(index,cell.value))
    header_map[cell.value] = index
    index += 1
  return header_map


@transaction.atomic
def process_data_file(user,data_file):
  logging.debug("inside process_data_file {0}".format(data_file.file.name))
  workbook = xlrd.open_workbook(file_contents = data_file.file.read())
  worksheet = workbook.sheet_by_index(0)
  num_rows = worksheet.nrows - 1
  curr_row = 0

  header_map = map_header_row(worksheet.row(0))

  logger.debug(header_map)
  while curr_row < num_rows:
    curr_row += 1
    row = worksheet.row(curr_row)
    logger.debug(row)