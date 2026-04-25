"""Модуль c данными."""

from enum import Enum


class Status(Enum):
    """Разрешённые статусы."""

    PLANNED_INSTALLATION = 'planned_installation'
    OPERATIONAL = 'operational'
    MAINTENANCE_SCHEDULED = 'maintenance_scheduled'
    FAULTY = 'faulty'


class ColumnsWithDates(Enum):
    """Наименования столбцов с датами."""

    INSTALL_DATE = 'install_date'
    WARRANTY_UNTIL = 'warranty_until'
    LAST_CALIBRATION_DATE = 'last_calibration_date'
    LAST_SERVICE_DATE = 'last_service_date'