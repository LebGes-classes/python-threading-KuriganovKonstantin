import threading
import pandas as pd
import time
import asyncio
from medical_device_processor import DeviceAnalyzer
from normalizer import StatusNormalizer


class ThreadedDeviceAnalyzer(DeviceAnalyzer):
    """Класс анализа медицинского оборудования с многопоточностью."""

    def __init__(self, df: pd.DataFrame) -> None:
        """Инициализация/конструктор класса.

        Args:
            df: Датафрейм медицинского оборудования.
        """

        super().__init__(df)

    def save_warranty_report(self):
        """Сохранение отчёта по гарантии."""

        df = self.get_df()

        report = df[df['warranty_until'] > '2026-04-24']
        report.to_excel('warranty_report.xlsx', index=False)
        print("Поток: Отчет по гарантии сохранен.")

    def save_worst_clinics(self):
        """Геттер худших клиник.

        Returns:
            worst_clinics: Худшие клиники.
        """

        df = self.get_df()

        worst_clinics = df.groupby('clinic_name')['issues_reported_12mo'].sum().sort_values(ascending=False).reset_index()
        worst_clinics.to_excel('problem_clinics.xlsx', index=False)

        print("Поток: Клиники с проблемами сохранены.")

    def save_calibration_report(self):
        """Модуль, сохраняющий отчёт по калибровке.

            Returns:
                calibration_date_analyze_output: Текстовый анализ дат последней калибровки.
        """

        stats = self.get_calibration_stats()

        with open('calibration_report.txt', 'w', encoding='utf-8') as f:
            f.write(stats)

        print("Поток: Отчет по калибровке сохранен.")

    def save_pivot_table(self):
        """Метод, сохраняющий сводную таблицу по клиникам и оборудованию.

            Returns:
                df.pivot_table: Сводная таблица по клиникам и оборудованию.
        """

        pivot_table = self.get_clinic_pivot()
        pivot_table.to_excel('clinic_pivot.xlsx')

        print("Поток: Сводная таблица сохранена.")