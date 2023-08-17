from csv_comparator.utils import print_avancement
from csv_comparator.csv_sorter import CsvSorter
import bisect

class LineComparator:
    
    def __init__(self, columns_to_exclude: [list,None] = None, evalutation_functions: [dict, None] = None) -> None:
        self.columns_to_exclude = columns_to_exclude if columns_to_exclude != None else []
        self.evalutation_functions = evalutation_functions if evalutation_functions != None else {}
        
    def compare(self, a: dict, b: dict) -> bool:
        causes = []
        for col, val_a, val_b in zip(a.keys(), a.values(), b.values()):
            if col in self.columns_to_exclude:
                continue
            evaluation_function = self.evalutation_functions[col] if col in self.evalutation_functions else lambda a, b: a == b
            if not evaluation_function(val_a, val_b):
                causes.append((col, val_a, val_b))
            
        return len(causes) == 0, causes

class CsvComparator:
    
    def __init__(self, lines_a: list[dict], lines_b: list[dict], columns_to_exclude: list, search_columns: list, evaluation_functions: [dict, None] = None) -> None:
        self.lines_a = CsvSorter(lines_a, search_columns).sort()
        self.lines_b = CsvSorter(lines_b, search_columns).sort()
        self.search_columns = search_columns
        self.line_comparator = LineComparator(columns_to_exclude=columns_to_exclude, evalutation_functions=evaluation_functions)
    
    def compare_length(self) -> tuple[bool, tuple[int, int, int]]:
        len_a = len(self.lines_a)
        len_b = len(self.lines_b)
        
        return (len_a == len_b, (len_a, len_b, len_a - len_b))

    def compare_lines_in_a(self) -> list[dict]:
        missing_a_lines = []
        i = 0
        last_time = 0
        count_lines_b = len(self.lines_b)
        
        compare_lambda = lambda x: tuple(x[col] for col in (self.search_columns if len(self.search_columns) > 0 else self.lines_b[0].keys()))
        
        for line_b in self.lines_b:
            last_time = print_avancement(i, count_lines_b, len(missing_a_lines), 1, last_time)
            i+=1
            
            search_b = compare_lambda(line_b)
            
            search_index = bisect.bisect_left(self.lines_a, search_b, key=compare_lambda)
            
            if search_index == len(self.lines_a):
                missing_a_lines.append({**line_b, "CAUSE": "Ligne manquante"})
            else:
                found_a = self.lines_a[search_index]
                if search_b != compare_lambda(found_a):
                    missing_a_lines.append({**line_b, "CAUSE": "Ligne manquante"})
                    continue
                    
                valid, causes = self.line_comparator.compare(line_b, found_a)
                    
                if not valid:
                    causes = [f"{col} ({expect_val},{found_val})" for (col, expect_val, found_val) in causes]
                    missing_a_lines.append({**line_b, "CAUSE": f"Ecart detecté: {', '.join(causes)}"})

        return missing_a_lines
    
    def compare_lines_in_b(self) -> list[dict]:
        missing_b_lines = []
        i = 0
        last_time = 0
        count_lines_a = len(self.lines_a)
        
        compare_lambda = lambda x: tuple(x[col] for col in (self.search_columns if len(self.search_columns) > 0 else self.lines_a[0].keys()))
        
        for line_a in self.lines_a:
            last_time = print_avancement(i, count_lines_a, len(missing_b_lines), 1, last_time)
            i+=1
            
            search_a = compare_lambda(line_a)
            
            search_index = bisect.bisect_left(self.lines_b, search_a, key=compare_lambda)
            
            if search_index == len(self.lines_b):
                missing_b_lines.append({**line_a, "CAUSE": "Ligne manquante"})
            else:
                found_b = self.lines_b[search_index]
                if search_a != compare_lambda(found_b):
                    missing_b_lines.append({**line_a, "CAUSE": "Ligne manquante"})
                    continue
                    
                valid, causes = self.line_comparator.compare(line_a, found_b)
                    
                if not valid:
                    causes = [f"{col} ({expect_val},{found_val})" for (col, expect_val, found_val) in causes]
                    missing_b_lines.append({**line_a, "CAUSE": f"Ecart detecté: {', '.join(causes)}"})
        
        return missing_b_lines
