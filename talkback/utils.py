""" 
Utilities for Talkback
"""
def get_module(module_name):
    """
    Imports and returns the named module.
    """
    module = __import__(module_name)
    components = module_name.split('.')
    for comp in components[1:]:
        module = getattr(module,comp)
    return module

def get_function(module_name,function_name):
    """
    Imports and returns the named function in the specified module.
    """
    module = get_module(module_name)
    return getattr(module,function_name)

def gf(function_path):
    """
    Shortcut to get function.
    """
    module_name, function_name = function_path.rsplit('.',1)
    return get_function(module_name,function_name)
