import pandas as pd
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config import FILES_STUDY_MODULE_PATH
from modules.study_module.functions_study import read_json


def study_time_total(registers, start, end):
    """Calcula o tempo total de estudo em um período.

    Args:
        registers (list[dict]): Registros de estudo com 'date_time' e 'duration'.
        start (datetime): Data inicial.
        end (datetime): Data final.

    Returns:
        int/float: Total de minutos estudados no período.
    """

    df = pd.DataFrame(registers)
    df['date_time'] = pd.to_datetime(df['date_time'], dayfirst=True, errors='coerce')

    df_filter = df[(df['date_time'].dt.date >= start.date()) & (df['date_time'].dt.date <= end.date())]
    time_total = df_filter["duration"].sum()

    return time_total

def study_time_average(registers, start, end):
    """Calcula o tempo médio diário de estudo em um período.

    Args:
        registers (list[dict]): Registros de estudo com 'date_time' e 'duration'.
        start (datetime): Data inicial.
        end (datetime): Data final.

    Returns:
        int: Média de minutos estudados por dia.
    """

    df = pd.DataFrame(registers)
    df['date_time'] = pd.to_datetime(df['date_time'], dayfirst=True, errors='coerce')

    df_filter = df[(df['date_time'].dt.date >= start.date()) & (df['date_time'].dt.date <= end.date())]
    time_total = df_filter["duration"].sum()

    num_days = df_filter['date_time'].dt.date.nunique()

    if num_days == 0:
        return 0

    return round(time_total / num_days)

def proportion_days_studied(registers, start, end):
    """Calcula a proporção de dias com estudo em um período.

    Args:
        registers (list[dict]): Registros de estudo com 'date_time' e 'duration'.
        start (datetime): Data inicial.
        end (datetime): Data final.

    Returns:
        float: Percentual de dias estudados no período, arredondado para 2 casas decimais.
    """

    df = pd.DataFrame(registers)
    df['date_time'] = pd.to_datetime(df['date_time'], dayfirst=True, errors='coerce')

    df_filter = df[(df['date_time'].dt.date >= start.date()) & (df['date_time'].dt.date <= end.date())]
    num_days = df_filter['date_time'].dt.date.nunique()
    difference_days = (end - start).days + 1

    proportion = (num_days / difference_days) * 100

    return round(proportion, 2)

def number_of_session(registers, start, end):
    """Conta o número de sessões de estudo em um período.

    Args:
        registers (list[dict]): Registros de estudo com 'date_time' e 'duration'.
        start (datetime): Data inicial.
        end (datetime): Data final.

    Returns:
        int: Quantidade de sessões registradas no período.
    """

    df = pd.DataFrame(registers)
    df['date_time'] = pd.to_datetime(df['date_time'], dayfirst=True, errors='coerce')

    df_filter = df[(df['date_time'].dt.date >= start.date()) & (df['date_time'].dt.date <= end.date())]
    
    return len(df_filter)

def longest_session(registers, start, end):
    """Retorna o dia com a sessão de estudo mais longa em um período.

    Args:
        registers (list[dict]): Registros de estudo com 'date_time' e 'duration'.
        start (datetime): Data inicial.
        end (datetime): Data final.

    Returns:
        tuple: Data (str, 'dd/mm/yyyy') e duração total (int/float) da sessão mais longa.
    """

    df = pd.DataFrame(registers)
    df['date_time'] = pd.to_datetime(df['date_time'], dayfirst=True, errors='coerce')
    df_filter = df[(df['date_time'].dt.date >= start.date()) & (df['date_time'].dt.date <= end.date())]

    total_per_day = df_filter.groupby(df_filter['date_time'].dt.date)['duration'].sum().reset_index()
    total_per_day.columns = ['date', 'total_duration']

    max_day = total_per_day.loc[total_per_day['total_duration'].idxmax()]

    date = max_day["date"].strftime('%d/%m/%Y')
    duration = max_day["total_duration"]
    
    return date, duration   

def study_time_total_for_subject(registers, start, end) -> list[tuple[str, int]]:
    """Calcula o tempo total de estudo por matéria em um período.

    Args:
        registers (list[dict]): Registros de estudo com 'date_time', 'duration' e 'subject'.
        start (datetime): Data inicial.
        end (datetime): Data final.

    Returns:
        list[tuple[str, int]]: Lista de tuplas (matéria, duração total em minutos).
    """

    df = pd.DataFrame(registers)
    df['date_time'] = pd.to_datetime(df['date_time'], dayfirst=True, errors='coerce')
    df_filter = df[(df['date_time'].dt.date >= start.date()) & (df['date_time'].dt.date <= end.date())]

    df_filter = df_filter.groupby("subject")["duration"].sum()
    items = []

    for subject, duration in df_filter.items():
        data = (subject, duration)
        items.append(data)
    
    return items

def study_full_report(period):
    """Gera um relatório completo de estudo para o período informado.

    Calcula métricas como número de sessões, média diária, proporção de dias estudados,
    dia mais intenso, tempo total por disciplina e tempo total geral.

    Args:
        period (str): Período no formato "dd/mm - dd/mm/aaaa".

    Returns:
        str: Texto formatado com todas as métricas de estudo.
    """
        
    registers = read_json(FILES_STUDY_MODULE_PATH, "registers.json")

    dates = period.split(" - ")
    start = dates[0]
    end = dates[1]
    
    start = pd.to_datetime(start, dayfirst=True)
    end = pd.to_datetime(end, dayfirst=True)

    time_total = study_time_total(registers, start, end)
    time_average = study_time_average(registers, start, end)
    proportion_days = proportion_days_studied(registers, start, end)
    number_session = number_of_session(registers, start, end)
    longest = longest_session(registers, start, end)
    time_total_for_subject = study_time_total_for_subject(registers, start, end)

    text = "*Métricas de Estudo*\n\n"
    text += f"*Número de sessões:* {number_session}\n"
    text += f"*Média de tempo por dia:* {time_average} minutos\n"
    text += f"*Proporção de dias estudados:* {proportion_days}%\n"
    text += f"*Dia mais intenso:* {longest[0]} | {longest[1]} minutos\n\n"

    text += "*Tempo total por disciplina:*\n"

    for subject, duration in time_total_for_subject:
        subject_escaped = subject.replace("-", "\\-").replace(".", "\\.").replace("(", "\\(").replace(")", "\\)").replace("!", "\\!")
        text += f"{subject_escaped}: {duration} minutos\n"

    text += f"*Total de tempo estudado:* {time_total} minutos\n"
    text += f"*Período: {period}*"

    return text
