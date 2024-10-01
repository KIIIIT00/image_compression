import importlib.util

class ModuleChecker:
    def __init__(self):
        self.imported_modules = {}
        
    def check_and_import(self, module_name):
        if module_name in self.imported_modules:
            print(f"Module '{module_name}' is already been imported.")
        else:
            spec = importlib.util.find_spec(module_name)
            if spec is None:
                print(f"{module_name} does not exist.")
            else:
                try:
                    module = importlib.import_module(module_name)
                    print(f"{module_name} has been imported.")
                    self.imported_modules[module_name] = module  
                except ImportError:
                    print(f"Failed to import {module_name}.")
    def use_module_function(self, module_name, func_name, *args, **kwargs):
        if module_name in self.imported_modules:
            module = self.imported_modules[module_name]
            if hasattr(module, func_name):
                func = getattr(module, func_name)
                return func(*args, **kwargs)
            else:
                print(f"The function {func_name} does not exist in {module_name}.")
        else:
            print(f"{module_name} is not imported yet.")
            
    def get_imported_modules(self):
        return self.imported_modules
