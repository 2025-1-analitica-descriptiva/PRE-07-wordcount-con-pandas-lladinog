"""Taller evaluable"""

import glob
import os

import pandas as pd #type: ignore

def load_input(input_directory):
    """
    Lee los archivos de texto en la carpeta input/ y almacena el contenido 
    en un DataFrame de pandas. Cada linea del archivo de texto debe ser 
    una entradad del DataFrame
    """
    files=glob.glob(f"{input_directory}/*")
    dataframes = [
        pd.read_csv(
            file,
            header=None,
            delimiter="\t",
            names=["line"],
            index_col=None,
        )
        for file in files
    ]

    df = pd.concat(dataframes, ignore_index=True)
    return df

def clean_text(dataframe):
    """
    Elimina la puntuación y convierte el texto a minúsculas.
    """
    dataframe=dataframe.copy()
    dataframe["line"] = dataframe["line"].str.lower()
    dataframe["line"] = (
        dataframe["line"]
        .str.replace(",", " ")
        .str.replace(".", " ")
        )
    return dataframe


def count_words(dataframe):
    """
    Cuenta la cantidad de palabras en cada línea del DataFrame y agrega 
    una nueva columna con el conteo.
    """
    dataframe=dataframe.copy()
    dataframe["line"] = dataframe["line"].str.split()
    dataframe = dataframe.explode("line")
    dataframe = dataframe.groupby("line").size().reset_index(name="count")
    return dataframe


def save_output(dataframe, output_directory):
    """
    Guarda el DataFrame en un archivo CSV en la carpeta output/.
    """
    if os.path.exists(output_directory):
        files = glob.glob(f"{output_directory}/*")
        for file in files:
            os.remove(file)
        os.rmdir(output_directory)
    os.makedirs(output_directory, exist_ok=True)

    dataframe.to_csv(
        f"{output_directory}/part-00000",
        sep="\t",
        index=False,
        header=False,
        
    )

def create_marker(output_directory):
    """
    Crea un archivo llamado _SUCCESS.txt en la carpeta output/ para indicar que el
    trabajo se ha completado con éxito.
    """
    with open(f"{output_directory}/_SUCCESS", "w", encoding="utf-8") as f:
        f.write("")


# Escriba la función job, la cual orquesta las funciones anteriores.
#
def run_job(input_directory, output_directory):
    """Job"""
    dataframe = load_input(input_directory)
    dataframe = clean_text(dataframe)
    dataframe = count_words(dataframe)
    save_output(dataframe, output_directory)
    create_marker(output_directory)

if __name__ == "__main__":

    run_job(
        "files/input",
        "files/output",
    )
