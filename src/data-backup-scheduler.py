import logging
import time

import schedule

from git_tool import commit_db_if_changed

logger = logging.getLogger(__name__)


def schedule_loop():
    """Schedule the periodic tasks."""
    schedule.every().hour.at(":00").do(commit_db_if_changed)
    logger.info("Scheduled hourly commit of DB if changed")
    while True:
        schedule.run_pending()
        time.sleep(1)


def get_scheduled_jobs():
    """Get the scheduled jobs for logging."""
    return [repr(job) for job in schedule.get_jobs()]
