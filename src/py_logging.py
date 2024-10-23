# -*- coding: utf-8 -*-
# 2024_1015 v10 modify the date format
import logging
import time
import datetime
from pathlib import Path

# set path and name
py_path = Path(__file__).parent
py_name = Path(__file__).stem
project_path = Path(__file__).parent.parent
project_name = Path(__file__).parent.stem
log_path = f"{project_path}/log"
log_name = f"{project_name}_{py_name}"
logger_name = f"{project_name}_{py_name}"
config_path = f"{project_path}/config"


def py_logger(
    write_mode="a",
    level="DEBUG",
    log_path="here",
    log_name="file_name",
    logger_name="root",
    file_console="both",
):
    """Use logger,
    log = py_logger("w","INFO",log_path,log_name,logger_name)

    Args:
            write_mode (str, optional): w for write, a for attached. Defaults to "a".
            level (str, optional): debug, info, warning, error, critical. Defaults to "DEBUG".
            log_path (str, optional): path to save log file. Defaults to "here".
            file_name (str, optional): file name of log. Defaults to "file_name".
            file_console (str, optional): both, file, console, none. Defaults to "both".

    Returns:
            class:'logging.RootLogger'
    """
    if log_path == "here":
        log_path = f"{Path(__file__).parent}/log"
    Path(log_path).mkdir(exist_ok=True)
    logger = logging.getLogger(logger_name)
    level_mode = logging.getLevelName(f"{level.upper()}")
    logger.setLevel(level_mode)
    formatter = logging.Formatter(
        "[%(levelname).1s %(asctime)s %(module)s %(lineno)4d] %(message)s",
        datefmt="%m%d_%H:%M:%S",
    )

    if file_console == "both" or file_console == "console":
        # this is for console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level_mode)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    if file_console == "both" or file_console == "file":
        # this is for log file
        log_date = datetime.datetime.now().strftime("%Y_%m%d")
        if log_name == "file_name":
            log_name = f"{Path(__file__).stem}"
        else:
            log_name = f"{log_name}"
        file_handler = logging.FileHandler(
            f"{log_path}/{log_date}_{log_name}.log", f"{write_mode}", "utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        print(f"{logger_name} at {log_path}/{log_date}_{log_name}.log")
    else:
        pass
    return logger


def get_logger():
    logger = logging.getLogger()
    return logger


def close_log(arg_logger):
    handlers = arg_logger.handlers[:]
    for handler in handlers:
        handler.close()
        arg_logger.removeHandler(handler)


def remove_old_log(log_path="here", log_name="None"):
    if log_path == "here":
        log_path = str(Path(__file__).parent)
    else:
        log_path = str(log_path)
    if log_name == "None":
        log_name = ""
    else:
        log_name = str(log_name)
    path_list = sorted(Path(log_path).glob("*.log"))
    today_ts = time.mktime(time.strptime(str(datetime.date.today()), "%Y-%m-%d"))
    for logger in path_list:
        old_log_name = Path(logger).stem[10:]
        if old_log_name == log_name:
            log_date = Path(logger).stem[0:9]
            log_ts = time.mktime(time.strptime(log_date, "%Y_%m%d"))
            if (today_ts - log_ts) > 60 * 60 * 24 * 3:
                Path(logger).unlink()
                print("remove", Path(logger).name)


if __name__ == "__main__":
    # set logger
    remove_old_log(log_path=log_path, log_name=py_name)
    log = py_logger(
        "w", level="DEBUG", log_path=log_path, log_name=log_name, logger_name=logger_name
    )
    # log = py_logger("w","INFO",log_path,log_name,logger_name)

    # log test
    log.debug(f"{__name__} start, logger_name = {logger_name}")

    # close log
    close_log(log)

    log = get_logger()
