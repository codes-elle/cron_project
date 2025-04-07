import logging
import time
from functools import wraps
from stats import update_stat

# Configure logging to write to job_logs.log in the project root.
logging.basicConfig(
    filename="job_logs.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)


def log_job(job_key, description, file_type=None):
    """
    Decorator to log job execution details and update stats.

    Args:
        job_key (str): Key used to update the job stats (should match the key in stats.json).
        description (str): Brief description of the job.
        file_type (str, optional): File type info if applicable.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            logging.info(f"Job Started: {job_key} - {description} - File type: {file_type or 'N/A'}")
            try:
                result = func(*args, **kwargs)
                elapsed = time.time() - start_time
                logging.info(f"Job Finished: {job_key} - Completed in {elapsed:.2f} seconds")
                update_stat(job_key, duration=elapsed, error=False)
                return result
            except Exception as e:
                elapsed = time.time() - start_time
                logging.error(f"Job Error: {job_key} - Error: {e} - Took {elapsed:.2f} seconds")
                update_stat(job_key, duration=elapsed, error=True)
                raise

        return wrapper

    return decorator
