import logging
from logging.handlers import TimedRotatingFileHandler
import time
from functools import wraps
from stats import update_stat

# Create and configure a logger for the project
logger = logging.getLogger("cron_project")
logger.setLevel(logging.INFO)

# Set up a TimedRotatingFileHandler: rotate at midnight, keep 1 days worth of logs (change as needed).
handler = TimedRotatingFileHandler("job_logs.log", when="midnight", interval=1, backupCount=1)
formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def log_job(job_key, description, file_type=None):
    """
    Decorator to log job execution details.

    Wraps a job function so when it's called, it logs:
    1. Job start with a timestamp.
    2. Job end with the execution duration.
    3. Any exceptions that occur along with an error message.
    Also updates the statistics for that job using update_stat()

    Args:
        job_key (str): Key used to update the job stats (should match the key in stats.json).
        description (str): Brief description of the job.
        file_type (str, optional): File type info if applicable.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            logger.info(f"Job Started: {job_key} - {description} - File type: {file_type or 'N/A'}")
            try:
                result = func(*args, **kwargs)
                elapsed = time.time() - start_time
                logger.info(f"Job Finished: {job_key} - Completed in {elapsed:.2f} seconds")
                #Update stats with the duration and mark as successful (error=False)
                update_stat(job_key, duration=elapsed, error=False)
                return result
            except Exception as e:
                elapsed = time.time() - start_time
                logger.error(f"Job Error: {job_key} - Error: {e} - Took {elapsed:.2f} seconds")
                #Update stats with the duration and mark as having an error (error=True)
                update_stat(job_key, duration=elapsed, error=True)
                raise
        return wrapper
    return decorator
