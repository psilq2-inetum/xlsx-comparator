# Python 3.9.13 NEED pandas / openpyxl / xlrd Si pb de VPN pour pip install
# pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org <nom-package>

import sys

import pandas as pd

from outputToFileAndConsole import OutputToFileAndConsole

skip_line = 5


def compare_two_files(original, test):
    """
        Compare les noms des feuilles et les contenus (sheets) entre deux fichiers Excel.

        :param original: Chemin vers le fichier Excel original.
        :param test: Chemin vers le fichier Excel de test.
        """

    try:

        df1_sheet_names = pd.ExcelFile(original).sheet_names
        df2_sheet_names = pd.ExcelFile(test).sheet_names

        same_sheets(df1_sheet_names, df2_sheet_names)

    except Exception as e:
        print("Erreur : ", str(e))


def same_sheets(df1_sheet_names, df2_sheet_names):
    """
        Vérifie si les feuilles de deux fichiers Excel sont identiques.

        :param df1_sheet_names: Liste des noms de feuilles dans le premier fichier Excel.
        :param df2_sheet_names: Liste des noms de feuilles dans le deuxième fichier Excel.

        :raise Si le nombre de feuilles diffère entre les deux fichiers ou si les noms des feuilles est diffèrent.
        """

    if len(df1_sheet_names) != len(df2_sheet_names):
        raise ValueError(f'Le nombre de feuille est différent entre les 2 fichiers : {len(df1_sheet_names)} != '
                         f'{len(df2_sheet_names)}')
    output_manager.start()
    for i in range(len(df1_sheet_names)):
        print('\n------------ Nouvelle Feuille ---------------\n')
        print(f'Comparasion des feuilles : {df1_sheet_names[i]} et {df1_sheet_names[i]}')

        if df1_sheet_names[i] != df2_sheet_names[i]:
            print('Les noms ne sont pas identiques.')
            continue
            # raise ValueError(f"Le nom des feuilles est différent : {df1_sheet_names[i]} != {df2_sheet_names[i]} à "f"l\'index {i}")

        df1 = pd.read_excel(original_file, df1_sheet_names[i])
        df2 = pd.read_excel(test_file, df2_sheet_names[i])

        compare_sheet(df1, df2)
        print('\n------------ Fin Feuille ---------------\n')
    output_manager.stop()


def compare_sheet(df1, df2):
    """
        Compare deux DataFrames et vérifie s'ils sont identiques.

        :param df1: Le premier DataFrame à comparer.
        :param df2: Le deuxième DataFrame à comparer.

        :raise Si les DataFrames ne sont pas identiques.
        """

    df1 = df1.iloc[skip_line:]  # Ignorer les premières lignes du DataFrame
    df2 = df2.iloc[skip_line:]

    if is_same_matrice(df1, df2):
        if not df1.equals(df2):
            differences = df1[df1 != df2]
            print(f"Les deux feuilles ne sont pas identiques :\n {differences}")
            # raise ValueError(f"Les deux feuilles ne sont pas identiques :\n {differences}")
        print('Les deux feuilles sont identiques')


def is_same_matrice(df1, df2):
    if df1.shape[1] != df2.shape[1]:
        print(f"Le nombre colonnes n'est pas identiques : {df1.shape[0]} != {df2.shape[0]}")
        # raise ValueError(f"Le nombre colonnes n'est pas identiques :\n {df1.shape[0]} != {df2.shape[0]}")
        return False
    if df1.shape[0] != df2.shape[0]:
        print(f"Le nombre de lignes n'est pas identiques : {df1.shape[0]} != {df2.shape[0]}")
        # raise ValueError(f"Le nombre de lignes n'est pas identiques :\n {df1.shape[0]} != {df2.shape[0]}")
        return False
    return True


def get_files_value():
    """
       Cette fonction récupère les noms de fichiers à partir des arguments de la ligne de commande.
       :return str: Nom du fichier original.xlsx et str: Nom du fichier test.xlsx
       """

    if len(sys.argv) != 3:
        raise ValueError("Usage: python script.py original.xlsx test.xlsx")
    return sys.argv[1], sys.argv[2]


if __name__ == '__main__':
    original_file, test_file = get_files_value()
    output_manager = OutputToFileAndConsole(original_file + '.txt')

    compare_two_files(original_file, test_file)
