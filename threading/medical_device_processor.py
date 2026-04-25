"""Модуль анализа медицинского оборудования."""

import pandas as pd
import statuses as st


class DeviceAnalyzer:
    """Класс анализа медицинского оборудования."""

    def __init__(self, df: pd.DataFrame) -> None:
        """Инициализация/конструктор класса.

        Args:
            df: Датафрейм медицинского оборудования.
        """
        self.__df = df

    def get_df(self) -> pd.DataFrame:
        """Геттер датафрейма.

        Returns:
            df: Датафрейм медицинского оборудования.
        """

        return self.__df

    def set_df(self, new_df) -> None:
        """Геттер датафрейма.

        Args:
            new_df: Датафрейм медицинского оборудования.
        """

        self.__df = new_df

    def normalize_dates(self) -> None:
        """Нормализатор дат."""

        for col in st.ColumnsWithDates:
            self.__df[col.value] = pd.to_datetime(self.__df[col.value], format='mixed', dayfirst=False, errors='coerce')

    def get_calibration_stats(self) -> str:
        """Модуль, считающий отчёт по калибровке.

        Returns:
            calibration_date_analyze_output: Текстовый анализ дат последней калибровки.
        """
        amount_of_wrong_cal_dates = (
            len(self.__df[
                    self.__df[
                        st.ColumnsWithDates.LAST_CALIBRATION_DATE.value] < self.__df[
                        st.ColumnsWithDates.INSTALL_DATE.value]]))
        amount_of_empty_cal_dates = self.__df[st.ColumnsWithDates.LAST_CALIBRATION_DATE.value].isnull().sum()
        amount_of_right_cal_dates = len(self.__df) - amount_of_empty_cal_dates - amount_of_wrong_cal_dates

        calibration_date_analyze_output = (
            f'\nКоличество неверных дат последней калибровки: {amount_of_wrong_cal_dates}'
            f'\nКоличество пустых дат последней калибровки: {amount_of_empty_cal_dates}'
            f'\nКоличество правильных дат последней калибровки: {amount_of_right_cal_dates}'
        )

        return calibration_date_analyze_output

    def get_clinic_pivot(self):
        """Геттер сводной таблицы по клиникам и оборудованию.

        Returns:
            df.pivot_table: Сводная таблица по клиникам и оборудованию.
        """

        return self.__df.pivot_table(
            index='clinic_name',
            columns='model',
            values='device_id',
            aggfunc='count',
            fill_value=0
        )

    def get_worst_clinics(self):
        """Геттер худших клиник.

        Returns:
            worst_clinics: Худшие клиники.
        """

        clinics = self.__df.groupby('clinic_id')['issues_reported_12mo'].sum()
        worst_clinics = clinics[clinics == clinics.max()]

        return worst_clinics
