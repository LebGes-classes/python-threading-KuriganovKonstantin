"""Модуль нормализатора статусов."""

from statuses import Status


class StatusNormalizer:
    """Класс нормализатора статусов."""

    def __init__(self, norm_statuses: dict = None) -> None:
        """Конструктор нормализатора статусов.

        Args:
            norm_statuses: Словарь, где статусу соответствует его нормализованная версия.
        """
        if not norm_statuses:
            self._norm_statuses = {
                'broken': Status.FAULTY, 'error': Status.FAULTY, 'faulty': Status.FAULTY,'needs_repair': Status.FAULTY,
                'maint_sched': Status.MAINTENANCE_SCHEDULED, 'maintenance': Status.MAINTENANCE_SCHEDULED,
                'maintenance_scheduled': Status.MAINTENANCE_SCHEDULED,
                'service_scheduled': Status.MAINTENANCE_SCHEDULED, 'scheduled_install': Status.MAINTENANCE_SCHEDULED,
                'ok': Status.OPERATIONAL, 'operational': Status.OPERATIONAL, 'working': Status.OPERATIONAL,
                'op': Status.OPERATIONAL,
                'planned': Status.PLANNED_INSTALLATION, 'to_install': Status.PLANNED_INSTALLATION,
                'planned_installation': Status.PLANNED_INSTALLATION
            }

    def normalize(self, status: str) -> str:
        """Метод нормализации статуса.

        Args:
            status: Статус, которому требуется нормализация.

        Returns:
            normalized_status: Исправленный статус.
        """

        clean_status = status.strip().lower()
        normalized_status = self._norm_statuses[clean_status].value

        return normalized_status