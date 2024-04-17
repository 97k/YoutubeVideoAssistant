import functools, time, traceback
from app.logger import get_logger

logger = get_logger(__name__)


def retry(
    retry_num: int = 3, retry_sleep_sec: int = 20, exit_if_not: Exception | None = None
):
    """
    retry help decorator.
    :param retry_num: the retry num; retry sleep sec
    :return: decorator
    """

    def decorator(func):
        """decorator"""
        # preserve information about the original function, or the func name will be "wrapper" not "func"
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """wrapper"""
            for attempt in range(retry_num):
                try:
                    return func(
                        *args, **kwargs
                    )  # should return the raw function's return value
                except Exception as err:  # pylint: disable=broad-except
                    logger.error(err)
                    logger.error(traceback.format_exc())
                    if exit_if_not and type(err) != exit_if_not:
                        logger.info(f"Breaking retry loop for {exit_if_not}")
                        return err
                    time.sleep(retry_sleep_sec)
                logger.error(f"Trying attempt {attempt+1} of {retry_num}")
            logger.error("func %s retry failed", func)
            raise Exception(f"Failed Request")

        return wrapper

    return decorator
