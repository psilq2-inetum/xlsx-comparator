# Python 3.9.13 NEED pandas / openpyxl / xlrd Si pb de VPN pour pip install
# pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org <nom-package>

import sys

import pandas as pd

from outputToFileAndConsole import OutputToFileAndConsole
from csv_comparator.csv_comparator import CsvComparator
from pathlib import Path
from csv import DictWriter
from csv_comparator.utils import comparer_lowercase, autorise_ecart

# LIGNES A SAUTER EN DEBUT DE FICHIER (POUR LES DEUX FICHIERS)
skip_line = 6


def compare_two_files(original, test):
    """
        Compare les noms des feuilles et les contenus (sheets) entre deux fichiers Excel.

        :param original: Chemin vers le fichier Excel original.
        :param test: Chemin vers le fichier Excel de test.
        """

    df1_sheet_names = pd.ExcelFile(original).sheet_names
    df2_sheet_names = pd.ExcelFile(test).sheet_names

    same_sheets(df1_sheet_names, df2_sheet_names, Path(original).name, Path(test).name)




def same_sheets(df1_sheet_names, df2_sheet_names, name1, name2):
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

        df1 = pd.read_excel(original_file, df1_sheet_names[i], skiprows=skip_line, header=None)
        df2 = pd.read_excel(test_file, df2_sheet_names[i], skiprows=skip_line, header=None)

        compare_sheet(df1.to_dict('records'), df2.to_dict('records'), df1_sheet_names[i], name1, name2)
        print('\n------------ Fin Feuille ---------------\n')
    output_manager.stop()


def compare_sheet(lines1, lines2, sheet_name, name1, name2):
    """
        Compare deux DataFrames et vérifie s'ils sont identiques.

        :param df1: Les lignes du premier fichier à comparer.
        :param df2: Les lignes du second fichier à comparer.
        """

    if is_same_dimension(lines1, lines2):
        
        evaluation_functions = {
            5: comparer_lowercase(),
            8: autorise_ecart(0.01),
            12: autorise_ecart(0.01),
            16: autorise_ecart(0.01), 
            17: autorise_ecart(0.01),
            18: autorise_ecart(0.01)
        }
        
        search_functions = {
            5: lambda x: x.lower()
        }
        
        # CHANGER ICI POUR COLUMNS_TO_EXCLUDE ET SEARCH_COLUMNS
        csv_comparator = CsvComparator(lines1, lines2, [0, 3], [1, 2, 5], evaluation_functions=evaluation_functions, search_functions=search_functions)
        
        valid, (len1, len2, _) = csv_comparator.compare_length()
        
        if not valid:
            print(f"Il n'y a pas le même nombre de lignes dans les deux fichiers: {len1} != {len2}")
            
        missing_lines_1 = csv_comparator.compare_lines_in_a()
        missing_lines_2 = csv_comparator.compare_lines_in_b()
        
        if len(missing_lines_1) > 0:
            print(f"Lignes en écart dans le premier fichier: {len(missing_lines_1)}")
            with open(Path("out") / f"missing_{name1}_{sheet_name}.csv", "w", encoding="utf-8-sig", newline="") as missing_1_out:
                fieldnames = list(range(len(missing_lines_1[0])))
                fieldnames.append("CAUSE")
                csv_writer = DictWriter(missing_1_out, fieldnames=fieldnames, delimiter=";")
                csv_writer.writerows(missing_lines_1)
            
        if len(missing_lines_2) > 0:
            print(f"Lignes en écart dans le deuxième fichier: {len(missing_lines_2)}")
            with open(Path("out") / f"missing_{name2}_{sheet_name}.csv", "w", encoding="utf-8-sig", newline="") as missing_2_out:
                fieldnames = list(range(len(missing_lines_2[0])))
                fieldnames.append("CAUSE")
                csv_writer = DictWriter(missing_2_out, fieldnames=fieldnames, delimiter=";")
                csv_writer.writerows(missing_lines_2)
        
        if len(missing_lines_1) == len(missing_lines_2) and len(missing_lines_1) == 0:
            print('Les deux feuilles sont identiques')


def is_same_dimension(lines1, lines2):
    if len(lines1) == 0 or len(lines2) == 0:
        print("L'un des deux tableaux est vide")
        return False
    if len(lines1[0]) != len(lines2[0]):
        print(f"Le nombre de colonnes n'est pas identiques : {len(lines1[0])} != {len(lines2[0])}")
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
