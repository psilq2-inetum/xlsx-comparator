class CsvSorter:
    
    def __init__(self, lines: list[dict], search_columns: list) -> None:
        self.lines = lines
        self.search_columns = search_columns
        
    def sort(self) -> list[dict]:
        return sorted(self.lines, key=lambda x: tuple(x[col] for col in (self.search_columns if len(self.search_columns) > 0 else self.lines[0].keys())))