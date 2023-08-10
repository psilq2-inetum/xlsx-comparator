import sys


class OutputToFileAndConsole:
    def __init__(self, filename):
        self.filename = filename
        self.original_stdout = sys.stdout
        self.output_file = open(self.filename, 'a')  # 'a' pour append (ajouter à la fin)

    def start(self):
        filtered_stdout = FilteredTee(self.original_stdout, self.output_file)
        sys.stdout = filtered_stdout

    def stop(self):
        sys.stdout = self.original_stdout
        self.output_file.close()


class FilteredTee:
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        if not obj.startswith("Warning:"):  # Exclure les lignes commençant par "Warning:"
            for f in self.files:
                f.write(obj)

    def flush(self):
        for f in self.files:
            f.flush()


output_manager = OutputToFileAndConsole('sortie_print.txt')
