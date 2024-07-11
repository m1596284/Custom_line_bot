from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
import os
import sys
from pathlib import Path
from src.py_logging import py_logger, remove_old_log
from datetime import datetime

# set path and name
py_path = Path(__file__).parent
py_name = Path(__file__).stem
project_name = Path(__file__).parent.stem
log_path = f"{py_path}/log"
log_name = py_name
logger_name = f"{project_name}_{py_name}"

# remove_old_log(log_path=log_path, log_name=py_name)
log = py_logger(
    write_mode="a",
    level="INFO",
    log_path=log_path,
    log_name=log_name,
    logger_name=logger_name,
)


def show(request):
    log.info("okok, show")
    file_path = "/home/qma/Downloads/1100816.pdf"
    with open(file_path, 'rb') as f:
        pdf_content = f.read()
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=file.pdf'
    return response