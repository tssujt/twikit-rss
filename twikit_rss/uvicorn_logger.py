from logging import Filter, LogRecord

from twikit_rss.app import app


class HealthCheckFilter(Filter):
    def filter(self, record: LogRecord) -> bool:
        health_path = str(app.url_path_for("health_check"))
        return not record.args or health_path not in str(record.args)
