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
    
    def __init__(self, lines_a: list[dict], lines_b: list[dict], columns_to_exclude: list, search_columns: list, evaluation_functions: [dict, None] = None, search_functions: [dict, None] = None) -> None:
        self.lines_a = CsvSorter(lines_a, search_columns).sort()
        self.lines_b = CsvSorter(lines_b, search_columns).sort()
        self.search_columns = search_columns
        self.line_comparator = LineComparator(columns_to_exclude=columns_to_exclude, evalutation_functions=evaluation_functions)
        self.search_functions = search_functions
    
    def compare_length(self) -> tuple[bool, tuple[int, int, int]]:
        len_a = len(self.lines_a)
        len_b = len(self.lines_b)
        
        return (len_a == len_b, (len_a, len_b, len_a - len_b))

    def bisect_key_function(self, line):
        columns = []
        
        search_columns = self.search_columns if len(self.search_columns) > 0 else self.lines_b[0].keys()
        
        for col in search_columns:
            value = self.search_functions[col](line[col]) if col in self.search_functions else line[col]
            columns.append(value)
        
        return tuple(columns)

    def determine_best_match(self, line: dict, matches: list[dict]) -> tuple[bool, list]:
        best_score = -1
        match_causes = None
        
        line_keys = self.bisect_key_function(line)
        
        for match in matches:
            match_keys = self.bisect_key_function(match)
            if match_keys != line_keys:
                continue
            
            valid, causes = self.line_comparator.compare(line, match)
            
            # We found a line that match perfectly
            if valid:
                return valid, []
            
            score = len(causes)
            
            if best_score == -1 or score < best_score:
                best_score = score
                match_causes = [f"{col} ({expect_val},{found_val})" for (col, expect_val, found_val) in causes]
        
        # No line with matching unique key was found
        if match_causes is None:
            return False, "Ligne manquante"
            
        # One was found, but with differences
        return False, f"Ecart detecté: {', '.join(match_causes)}"

    def compare_lines_in_a(self) -> list[dict]:
        missing_a_lines = []
        i = 0
        last_time = 0
        count_lines_b = len(self.lines_b)
        
        for line_b in self.lines_b:
            last_time = print_avancement(i, count_lines_b, len(missing_a_lines), 1, last_time)
            i+=1
            
            search_b = self.bisect_key_function(line_b)
            
            search_index = bisect.bisect_left(self.lines_a, search_b, key=self.bisect_key_function)
            search_index_end = bisect.bisect(self.lines_a, search_b, key=self.bisect_key_function)
            
            matches = [self.lines_a[i] for i in range(search_index, search_index_end)]
            
            valid, causes = self.determine_best_match(line_b, matches)
                
            if not valid:
                missing_a_lines.append({**line_b, "CAUSE": causes})

        return missing_a_lines
                
    
    def compare_lines_in_b(self) -> list[dict]:
        missing_b_lines = []
        i = 0
        last_time = 0
        count_lines_a = len(self.lines_a)
        
        for line_a in self.lines_a:
            last_time = print_avancement(i, count_lines_a, len(missing_b_lines), 1, last_time)
            i+=1
            
            search_a = self.bisect_key_function(line_a)
            
            search_index = bisect.bisect_left(self.lines_b, search_a, key=self.bisect_key_function)
            search_index_end = bisect.bisect(self.lines_b, search_a, key=self.bisect_key_function)

            matches = [self.lines_b[i] for i in range(search_index, search_index_end)]
            
            valid, causes = self.determine_best_match(line_a, matches)
                
            if not valid:
                missing_b_lines.append({**line_a, "CAUSE": causes})
        
        return missing_b_lines
