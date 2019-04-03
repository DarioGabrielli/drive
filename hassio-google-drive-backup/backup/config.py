import os.path
import json
import logging
from .logbase import LogBase
from typing import Dict, List, Tuple, Any, Optional

HASSIO_OPTIONS_FILE = '/data/options.json'

DEFAULTS = {
    "max_snapshots_in_hassio": 4,
    "max_snapshots_in_google_drive": 4,
    "hassio_base_url": "http://hassio/",
    "ha_base_url": "http://hassio/homeassistant/api/",
    "path_separator": "/",
    "port": 1627,
    "days_between_snapshots": 3,

    # how many hours after startup the server will wait before starting a new snapshot automatically
    "hours_before_snapshot": 1,
    "folder_file_path": "/data/folder.dat",
    "credentials_file_path": "/data/credentials.dat",
    "seconds_between_refreshes": 60 * 60,  # once per hour, refresh everythin regardless
    "seconds_between_directory_checks": 10,
    "verbose": False,
    "use_ssl": False,
    "certfile": "/ssl/fullchain.pem",
    "keyfile": "/ssl/privkey.pem",
    "require_login": False,
    "backup_directory": "/backup",
    "snapshot_stale_minutes": 60 * 3,
    "ha_bearer": "",
    "snapshot_time_of_day": ""
}


class Config(LogBase):

    def __init__(self, file_paths: List[str] = [], extra_config: Dict[str, any] = {}):
        self.config: Dict[str, Any] = DEFAULTS
        for config_file in [HASSIO_OPTIONS_FILE, ""]:
            if os.path.isfile(config_file):
                with open(config_file) as file_handle:
                    self.config.update(json.load(file_handle))
        for config_file in file_paths:
            if os.path.isfile(config_file):
                with open(config_file) as file_handle:
                    self.info("Loading config from " + config_file)
                    self.config.update(json.load(file_handle))

        self.config.update(extra_config)
        self.info("Loaded config:")
        self.info(json.dumps(self.config, sort_keys=True, indent=4))
        if self.verbose():
            self.setConsoleLevel(logging.DEBUG)
        else:
            self.setConsoleLevel(logging.INFO)
        gen_config = self.getGenerationalConfig()
        if gen_config:
            self.info("Generationl backup config:")
            self.info(json.dumps(gen_config, sort_keys=True, indent=4))

    def maxSnapshotsInHassio(self) -> int:
        return int(self.config['max_snapshots_in_hassio'])

    def maxSnapshotsInGoogleDrive(self) -> int:
        return int(self.config['max_snapshots_in_google_drive'])

    def hassioBaseUrl(self) -> str:
        return str(self.config['hassio_base_url'])

    def haBaseUrl(self) -> str:
        return str(self.config['ha_base_url'])

    def pathSeparator(self) -> str:
        return str(self.config['path_separator'])

    def port(self) -> int:
        return int(self.config['port'])

    def daysBetweenSnapshots(self) -> float:
        return float(self.config['days_between_snapshots'])

    def hoursBeforeSnapshot(self) -> float:
        return float(self.config['hours_before_snapshot'])

    def folderFilePath(self) -> str:
        return str(self.config['folder_file_path'])

    def credentialsFilePath(self) -> str:
        return str(self.config['credentials_file_path'])

    def secondsBetweenRefreshes(self) -> int:
        return int(self.config['seconds_between_refreshes'])

    def secondsBetweenDirectoryChecks(self) -> float:
        return float(self.config['seconds_between_directory_checks'])

    def verbose(self) -> bool:
        return bool(self.config['verbose'])

    def useSsl(self) -> bool:
        return bool(self.config['use_ssl'])

    def certFile(self) -> str:
        return str(self.config['certfile'])

    def keyFile(self) -> str:
        return str(self.config['keyfile'])

    def requireLogin(self) -> bool:
        return bool(self.config['require_login'])

    def backupDirectory(self) -> str:
        return str(self.config['backup_directory'])

    def snapshotStaleMinutes(self) -> float:
        return float(self.config['snapshot_stale_minutes'])

    def haBearer(self) -> str:
        return str(self.config['ha_bearer'])

    def snapshotTimeOfDay(self) -> Optional[str]:
        if len(str(self.config['snapshot_time_of_day'])) > 0:
            return str(self.config['snapshot_time_of_day'])
        return None

    def getGenerationalConfig(self) -> Optional[Dict[str, Any]]:
        if 'generational_days' not in self.config and 'generational_weeks' not in self.config and 'generational_months' not in self.config and 'generational_years' not in self.config: 
            return None
        base = {
            'days': 0,
            'weeks': 0,
            'months': 0,
            'years': 0,
            'day_of_week': 'mon',
            'day_of_month': 1,
            'day_of_year': 1
        }
        if 'generational_days' in self.config:
            base['days'] = self.config['generational_days']
        if 'generational_weeks' in self.config:
            base['weeks'] = self.config['generational_weeks']
        if 'generational_months' in self.config:
            base['months'] = self.config['generational_months']
        if 'generational_years' in self.config:
            base['years'] = self.config['generational_years']
        if 'generational_day_of_week' in self.config:
            base['day_of_week'] = self.config['generational_day_of_week']
        if 'generational_day_of_month' in self.config:
            base['day_of_month'] = self.config['generational_day_of_month']
        if 'generational_day_of_year' in self.config:
           base['day_of_year'] =  self.config['generational_day_of_year']
        return base
