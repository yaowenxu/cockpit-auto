import os, yaml, logging, time
import logging.config
from constants import PROJECT_ROOT



class ResultsAndLogs(object):
    def __init__(self):
        self._logs_root_dir = os.path.join(PROJECT_ROOT, 'logs')
        self._img_url = None
        self.logger_conf = os.path.join(PROJECT_ROOT, 'logger.yml')
        self._logger_name = "results"
        self.logger_dict = self.conf_to_dict()
        self._current_log_path = "/tmp/logs"
        self._current_log_file = "/tmp/logs"
        self._current_date = self.get_current_date()
        self._current_time = self.get_current_time()

    @property
    def img_url(self):
        return self._img_url

    @img_url.setter
    def img_url(self, val):
        self._img_url = val

    @property
    def logger_name(self):
        return self._logger_name

    @logger_name.setter
    def logger_name(self, val):
        self._logger_name = val

    @property
    def current_log_path(self):
        return self._current_log_path

    @property
    def current_log_file(self):
        return self._current_log_file

    def get_current_date(self):
        return time.strftime("%Y-%m-%d", time.localtime())

    def get_current_time(self):
        return time.strftime("%H-%M-%S")

    def conf_to_dict(self):
        return yaml.load(open(self.logger_conf))

    def parse_img_url(self):
        #return self.img_url.split('/')[-2]
        return self.img_url

    def get_actual_logger(self, ks_name=''):
        log_file = os.path.join(PROJECT_ROOT, 'logs',
                                self._current_date,
                                self._current_time,
                                self.parse_img_url(), ks_name,
                                self.logger_name)
        if not os.path.exists(log_file):
            os.system("mkdir -p {0}".format(os.path.dirname(log_file)))

        self._current_log_path = os.path.dirname(log_file)
        self._current_log_file = log_file

        self.logger_dict['logging']['handlers']['logfile'][
            'filename'] = log_file

        logging.config.dictConfig(self.logger_dict['logging'])

    def del_existing_logs(self, ks_name=''):
        log_file = os.path.join(PROJECT_ROOT, 'logs',
                                self._current_date,
                                self._current_time,
                                self.parse_img_url(), ks_name)
        if os.path.exists(log_file):
            os.system('rm -rf {}/*'.format(log_file))


results_logs = ResultsAndLogs()
