# time_utils.py

from datetime import datetime
import pytz

class TimeUtils:
    @staticmethod
    def get_current_time(timezone: str) -> str:
        """
        Obtém a hora atual no fuso horário especificado e retorna como string.
        
        Args:
            timezone (str): O fuso horário desejado (ex: 'America/Sao_Paulo').
        
        Returns:
            str: A hora atual no fuso horário especificado, formatada como 'dd/mm/yyyy HH:MM:SS'.
        """
        local_tz = pytz.timezone(timezone)
        local_time = datetime.now(local_tz)
        return local_time.strftime('%d/%m/%Y %H:%M:%S')

    @staticmethod
    def convert_timestamp_to_brazilian_format(timestamp: float, timezone: str) -> str:
        """
        Converte um timestamp para o formato brasileiro de data e hora no fuso horário especificado.
        
        Args:
            timestamp (float): O timestamp Unix a ser convertido.
            timezone (str): O fuso horário desejado (ex: 'America/Sao_Paulo').
        
        Returns:
            str: O timestamp convertido para o formato 'dd/mm/yyyy HH:MM:SS'.
        """
        local_tz = pytz.timezone(timezone)
        local_time = datetime.fromtimestamp(timestamp, local_tz)
        return local_time.strftime('%d/%m/%Y %H:%M:%S')

    @staticmethod
    def get_time_components(timestamp: float, timezone: str) -> dict:
        """
        Converte um timestamp para um dicionário com os componentes de data e hora no formato brasileiro.
        
        Args:
            timestamp (float): O timestamp Unix a ser convertido.
            timezone (str): O fuso horário desejado (ex: 'America/Sao_Paulo').
        
        Returns:
            dict: Dicionário com os componentes de data e hora {'dia', 'mes', 'ano', 'hora', 'minuto', 'segundo'}.
        """
        local_tz = pytz.timezone(timezone)
        local_time = datetime.fromtimestamp(timestamp, local_tz)
        return {
            'dia': local_time.day,
            'mes': local_time.month,
            'ano': local_time.year,
            'hora': local_time.hour,
            'minuto': local_time.minute,
            'segundo': local_time.second
        }
