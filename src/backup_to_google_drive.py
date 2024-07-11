import os
from pathlib import Path
import py_logging
import json
import requests

# set path and name
py_path = Path(__file__).parent
py_name = Path(__file__).stem
project_name = Path(__file__).parent.parent.stem
log_path = f"{py_path}/log"
log_name = py_name
logger_name = f"{project_name}_{py_name}"


# set logger
py_logging.remove_old_log(log_path=log_path, log_name=py_name)
log = py_logging.py_logger(
    "a", level="INFO", log_path=log_path, log_name=log_name, logger_name=logger_name
)


# Loading the access token and secret for line bot
with open(f"{str(py_path)}/config/line_bot_channel.json", encoding="utf-8") as f:
    channel_json = json.load(f)
    notify_token = channel_json["iu_server"]["notify_token"]


def main():
    update_status = os.system(
        "cp /home/qma/coding_program/qma_server/iu_server/db.sqlite3  /home/qma/mount/google_drive/backup_system/iu_server/"
    )
    if update_status == 0:
        msg = f"\n{project_name}'s db.sqlite3\nupdate success"
        line_notify(token=notify_token, msg=msg)
    else:
        msg = f"\n{project_name}'s db.sqlite3\nupdate fail"
        line_notify(token=notify_token, msg=msg)


def line_notify(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    payload = {"message": msg}
    requests.post(
        "https://notify-api.line.me/api/notify",
        headers=headers,
        params=payload,
        timeout=10,
    )


if __name__ == "__main__":
    main()
