import asyncio
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from run import main


class TaskManager:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._scheduler = BackgroundScheduler()
        self._scheduler.add_job(main, 'cron', minute='*')

    def run(self):
        try:
            self.logger.info('STARTING')
            self._start()
        except (KeyboardInterrupt, SystemExit):
            pass
        finally:
            self._stop()

    def _start(self):
        if not self._scheduler.running:
            self._scheduler.start()
        asyncio.get_event_loop().run_forever()

    def _stop(self):
        if self._scheduler.running:
            self._scheduler.shutdown()


if __name__ == '__main__':

    logger = logging.getLogger(__name__)

    tm = TaskManager()

    logger.info('STARTING TASK MANAGER')

    tm.run()
