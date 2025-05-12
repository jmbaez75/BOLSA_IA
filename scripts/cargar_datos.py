import os
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Función para obtener los tickers del S&P 500 desde Wikipedia
def obtener_tickers_sp500_wiki():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Buscar la tabla de tickers
    table = soup.find('table', {'class': 'wikitable'})
    tickers = []

    # Recorremos las filas de la tabla para obtener los tickers
    for row in table.find_all('tr')[1:]:  # Ignoramos el encabezado y recorremos las filas
        ticker = row.find_all('td')[0].text.strip()
        tickers.append(ticker)

    return tickers

# Función para obtener los datos de balance financiero de los tickers
def obtener_datos_balance(tickers):
    datos_balance = []

    for ticker in tickers:
        print(f"Obteniendo datos de balance para {ticker}...")
        try:
            accion = yf.Ticker(ticker)
            balance = accion.financials

            if not balance.empty:
                balance_ultimos_5 = balance.iloc[:, :5]  # Últimos 5 años

                # Crear un diccionario por cada ticker
                fila_anual = {"Ticker": ticker}

                for fila in balance_ultimos_5.index:
                    for columna in balance_ultimos_5.columns:
                        nombre_columna = fila.replace(" ", "_").replace("/", "_")
                        valor = balance_ultimos_5.at[fila, columna]

                        # Asignar el valor del parámetro con el año correspondiente
                        fila_anual[f"{nombre_columna} {columna.year}"] = valor

                # Obtener los años extremos
                años_disponibles = [col.year for col in balance_ultimos_5.columns]
                primer_año = min(años_disponibles)
                último_año = max(años_disponibles)

                fecha_inicio = f"{primer_año}-01-01"
                fecha_abril = f"{último_año}-04-01"

                try:
                    historial = accion.history(start=fecha_inicio, end=f"{último_año}-04-15")

                    if not historial.empty:
                        # Precio 1 enero del primer año
                        if fecha_inicio in historial.index:
                            precio_inicio = historial.loc[fecha_inicio]["Close"]
                        else:
                            precio_inicio = historial.loc[historial.index >= fecha_inicio].iloc[0]["Close"]

                        # Precio 1 abril del último año
                        if fecha_abril in historial.index:
                            precio_abril = historial.loc[fecha_abril]["Close"]
                        else:
                            precio_abril = historial.loc[historial.index >= fecha_abril].iloc[0]["Close"]

                        fila_anual[f"Precio_1_Enero_{primer_año}"] = precio_inicio
                        fila_anual[f"Precio_1_Abril_{último_año}"] = precio_abril
                        fila_anual["Rentabilidad"] = (precio_abril - precio_inicio) / precio_inicio
                    else:
                        print(f"No hay histórico disponible para {ticker} entre {fecha_inicio} y {fecha_abril}")
                except Exception as e:
                    print(f"Error obteniendo precios para {ticker}: {e}")


                # Añadir la fila con los valores de todos los parámetros para ese ticker
                datos_balance.append(fila_anual)

            else:
                print(f"No se encontraron datos de balance para {ticker}.")
        except Exception as e:
            print(f"Error al obtener datos para {ticker}: {e}")

    # Convertir la lista de diccionarios en un DataFrame
    df_balance = pd.DataFrame(datos_balance)

    # Reorganizar las columnas para que cada parámetro tenga los años correspondientes
    df_balance = df_balance.set_index("Ticker")
    return df_balance

# Función para guardar los datos en un archivo CSV
def guardar_datos(df_balance):
    # Verifica si la carpeta 'datos' existe, si no la crea
    carpeta = './datos'
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    # Guarda el DataFrame en un archivo CSV dentro de la carpeta 'datos'
    df_balance.to_csv(os.path.join(carpeta, 'datos_balance.csv'), index=True, sep=';', decimal='.')

if __name__ == "__main__":
    # Obtener los tickers del S&P 500 desde Wikipedia
    tickers_sp500_wiki = obtener_tickers_sp500_wiki()

    # Obtener los datos del balance
    df_balance = obtener_datos_balance(tickers_sp500_wiki)

    # Guardar los datos en un archivo CSV
    guardar_datos(df_balance)
