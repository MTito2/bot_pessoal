import pandas as pd
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config import FILES_FINANCES_MODULE_PATH
from modules.finances_module.functions_finances import read_json

def total_value_expenses(expenses, start, end):
    df = pd.DataFrame(expenses)
    df['date_time'] = pd.to_datetime(df['date_time'], dayfirst=True, errors='coerce')

    df_filter = df[(df['date_time'].dt.date >= start.date()) & (df['date_time'].dt.date <= end.date())]
    total_value = df_filter["value"].sum()

    return total_value

def max_expense(expenses, start, end):
    df = pd.DataFrame(expenses)
    df['date_time'] = pd.to_datetime(df['date_time'], dayfirst=True, errors='coerce')

    df_filter = df[(df['date_time'].dt.date >= start.date()) & (df['date_time'].dt.date <= end.date())]
    max_expense_row = df_filter.sort_values('value', ascending=False).iloc[0]   

    return max_expense_row["date_time"].strftime('%d/%m/%Y'), max_expense_row["item"], max_expense_row["value"] 

def most_purchased(expenses, start, end):
    df = pd.DataFrame(expenses)
    df['date_time'] = pd.to_datetime(df['date_time'], dayfirst=True, errors='coerce')

    df_filter = df[(df['date_time'].dt.date >= start.date()) & (df['date_time'].dt.date <= end.date())]   
    most_purchased_row = df_filter["item"].value_counts().sort_values(ascending=False)

    #Itera sobre as linhas de contagem de itens do maior para o menor
    for item, value in most_purchased_row.items():
        most_purchased = (item, value)
        return most_purchased # Page somente a primeira linha

def average_value_expenses(expenses, start, end):
    df = pd.DataFrame(expenses)
    df['date_time'] = pd.to_datetime(df['date_time'], dayfirst=True, errors='coerce')

    df_filter = df[(df['date_time'].dt.date >= start.date()) & (df['date_time'].dt.date <= end.date())]
    total_value = df_filter["value"].sum()

    num_days =  (end - start).days + 1

    if num_days == 0:
        return 0

    return round (total_value / num_days, 2)

def total_value_expenses_category(expenses, start, end):
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
    expenses_path = FILES_FINANCES_MODULE_PATH / "expenses.json"
    expenses = read_json(expenses_path)

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
    text += f"*Mais comprado:*\n{counter_item[0]}: {counter_item[1]} vezes\n\n"
    text += f"*Maior gasto:*\nData: {value_max_expense[0]}\nItem: {value_max_expense[1]}\nValor: R${value_max_expense[2]}\n\n"


    text += "*Gasto por categoria:*\n"
    for item in value_category:
        text += f"{item[0]}: R$ {item[1]}\n"

    text += f"\n*Gasto médio por dia:* R$ {average_value}\n"
    text += f"*Gasto total:* R$ {total_value}\n"

    return text.replace(".", ",")

