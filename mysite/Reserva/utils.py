from datetime import datetime

def formatar_data(data_str):
    
    dias_da_semana = ["Domingo", "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado"]
    meses_do_ano = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    
    # Converte a string de data para um objeto datetime
    data = datetime.strptime(data_str, "%Y-%m-%d")
    
    # Extrai o dia da semana, dia do mês, mês e ano
    dia_semana = dias_da_semana[data.weekday()]
    dia_mes = data.day
    mes = meses_do_ano[data.month - 1]
    ano = data.year
    
    # Retorna a data formatada
    return f"{dia_semana}, {str(dia_mes).zfill(2)} de {mes} de {ano}"
