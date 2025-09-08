import pandas as pd
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config import FILES_FINANCES_MODULE_PATH
from general_functions import read_json

def total_value_expenses(expenses, start, end):
    """Calcula o valor total das despesas em um período específico.

    Filtra as despesas pelo intervalo de datas fornecido e retorna a soma dos valores.

    Args:
        expenses (list[dict]): Lista de despesas, cada uma contendo pelo menos 'date_time' e 'value'.
        start (datetime): Data inicial do período.
        end (datetime): Data final do período.

    Returns:
        float: Soma dos valores das despesas dentro do período.
    """
    df = pd.DataFrame(expenses)
    df['date_time'] = pd.to_datetime(df['date_time'], dayfirst=True, errors='coerce')

    df_filter = df[(df['date_time'].dt.date >= start.date()) & (df['date_time'].dt.date <= end.date())]
    total_value = df_filter["value"].sum()

    return total_value

def max_expense(expenses, start, end):
    """Retorna a maior despesa em um período.

    Filtra despesas pelo intervalo e retorna data, item e valor da maior.

    Args:
        expenses (list[dict]): Lista de despesas com 'date_time', 'item' e 'value'.
        start (datetime): Data inicial.
        end (datetime): Data final.

    Returns:
        tuple: (data_str, item, valor) da despesa.
    """

    df = pd.DataFrame(expenses)
    df['date_time'] = pd.to_datetime(df['date_time'], dayfirst=True, errors='coerce')

    df_filter = df[(df['date_time'].dt.date >= start.date()) & (df['date_time'].dt.date <= end.date())]
    max_expense_row = df_filter.sort_values('value', ascending=False).iloc[0]   

    return max_expense_row["date_time"].strftime('%d/%m/%Y'), max_expense_row["item"], max_expense_row["value"] 

def most_purchased(expenses, start, end):
    """Retorna o item mais comprado em um período.

    Filtra despesas pelo intervalo e identifica o item com maior quantidade.

    Args:
        expenses (list[dict]): Lista de despesas com 'date_time' e 'item'.
        start (datetime): Data inicial.
        end (datetime): Data final.

    Returns:
        tuple: (item, quantidade) mais comprado no período.
    """
        
    df = pd.DataFrame(expenses)
    df['date_time'] = pd.to_datetime(df['date_time'], dayfirst=True, errors='coerce')

    df_filter = df[(df['date_time'].dt.date >= start.date()) & (df['date_time'].dt.date <= end.date())]   
    most_purchased_row = df_filter["item"].value_counts().sort_values(ascending=False)

    for item, value in most_purchased_row.items():
        most_purchased = (item, value)
        return most_purchased

def average_value_expenses(expenses, start, end):
    """Calcula o gasto médio diário em um período.

    Filtra despesas pelo intervalo e retorna a média por dia.

    Args:
        expenses (list[dict]): Lista de despesas com 'date_time' e 'value'.
        start (datetime): Data inicial.
        end (datetime): Data final.

    Returns:
        float: Valor médio gasto por dia no período.
    """

    df = pd.DataFrame(expenses)
    df['date_time'] = pd.to_datetime(df['date_time'], dayfirst=True, errors='coerce')

    df_filter = df[(df['date_time'].dt.date >= start.date()) & (df['date_time'].dt.date <= end.date())]
    total_value = df_filter["value"].sum()

    num_days =  (end - start).days + 1

    if num_days == 0:
        return 0

    return round (total_value / num_days, 2)

def total_value_expenses_category(expenses, start, end):
    """Calcula o total gasto por categoria em um período.

    Filtra despesas pelo intervalo e retorna a soma dos valores por categoria.

    Args:
        expenses (list[dict]): Lista de despesas com 'date_time', 'category' e 'value'.
        start (datetime): Data inicial.
        end (datetime): Data final.

    Returns:
        list[tuple]: Lista de tuplas (categoria, valor_total) por categoria.
    """

    df = pd.DataFrame(expenses)
    df['date_time'] = pd.to_datetime(df['date_time'], dayfirst=True, errors='coerce')

    df_filter = df[(df['date_time'].dt.date >= start.date()) & (df['date_time'].dt.date <= end.date())]
    df_filter = df_filter.groupby("category")["value"].sum()
    
    items = []

    for category, value in df_filter.items():
        data = (category, value)
        items.append(data)
    
    return items

def expenses_full_report(period):
    """Gera um relatório completo de despesas para o período informado.

    Args:
        period (str): Período no formato 'dd/mm - dd/mm/aaaa'.

    Returns:
        str: Relatório com total, média, maior gasto, item mais comprado e gastos por categoria.
    """

    expenses = read_json(FILES_FINANCES_MODULE_PATH, "expenses.json")

    dates = period.split(" - ")
    start = dates[0]
    end = dates[1]
    
    start = pd.to_datetime(start, dayfirst=True)
    end = pd.to_datetime(end, dayfirst=True)

    total_value = total_value_expenses(expenses, start, end)
    value_max_expense = max_expense(expenses, start, end)
    counter_item = most_purchased(expenses, start, end)
    average_value = average_value_expenses(expenses, start, end)
    value_category = total_value_expenses_category(expenses, start, end)

    text = "*Métricas de Gastos*\n\n"

    if counter_item[1] > 1:
        text += f"*Mais comprado:*\n{counter_item[0]}: {counter_item[1]} vezes\n\n"

    text += f"*Maior gasto:*\nData: {value_max_expense[0]}\nItem: {value_max_expense[1]}\nValor: R${value_max_expense[2]}\n\n"
    text += "*Gasto por categoria:*\n"
    for item in value_category:
        text += f"{item[0]}: R$ {item[1]}\n"

    text += f"\n*Gasto médio por dia:* R$ {average_value}\n"
    text += f"*Gasto total:* R$ {total_value}\n\n"
    text += f"*Período: {period}*"

    return text.replace(".", ",")

