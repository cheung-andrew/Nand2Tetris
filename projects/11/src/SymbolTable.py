import sys 

class SymbolTable:
    def __init__(self):
        self.class_table = {}
        self.subroutine_table = {}
        self.static_index = 0
        self.field_index = 0
        self.arg_index = 0
        self.local_index = 0
        
    def reset(self):
        #self.class_table = []
        self.subroutine_table = {}
        self.static_index = 0
        self.field_index = 0
        self.arg_index = 0
        self.local_index = 0
        
    def returnClassTable(self):
        return self.class_table
        
    def returnSubroutineTable(self):
        return self.subroutine_table
        
    def define(self, var_name, var_type, var_kind):
        index = self.assignIndex(var_kind)
        new_var = [var_type, var_kind, index]
        if var_kind in ["static", "field"]:
            self.class_table[var_name] = new_var
        else:
            self.subroutine_table[var_name] = new_var
        
    def assignIndex(self, var_kind):
        if var_kind == "static":
            index = self.static_index
            self.static_index = self.static_index + 1
        elif var_kind == "field":
            index = self.field_index
            self.field_index = self.field_index + 1
        elif var_kind == "arg":
            index = self.arg_index
            self.arg_index = self.arg_index + 1
        elif var_kind == "local":
            index = self.local_index
            self.local_index = self.local_index + 1
        return index 
        
    def varCount(self, var_kind):
        if var_kind == "static":
            return self.static_index
        elif var_kind == "field":
            return self.field_index
        elif var_kind == "arg":
            return self.arg_index
        elif var_kind == "local":
            return self.local_index
    
    def typeOf(self, var_name):
        if var_name in self.class_table:
            return self.class_table[var_name][0]
        elif var_name in self.subroutine_table:
            return self.subroutine_table[var_name][0]
        else:
            return "NONE"
    
    def kindOf(self, var_name):
        if var_name in self.class_table:
            return self.class_table[var_name][1]
        elif var_name in self.subroutine_table:
            return self.subroutine_table[var_name][1]
            
    def indexOf(self, var_name):
        if var_name in self.class_table:
            return self.class_table[var_name][2]
        elif var_name in self.subroutine_table:
            return self.subroutine_table[var_name][2]
        
    def getVar(self, var_name):
        if var_name in self.class_table:
            return True

        elif var_name in self.subroutine_table:
            return True

        else:

            return False
            #sys.exit(0)
            
