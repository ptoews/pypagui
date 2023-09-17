import inspect
import sys

import pypagui.gui.qt
import pypagui.parameter


def wrap_function(func):
    signature = inspect.signature(func)

    parameters = {parameter_name: pypagui.parameter.Parameter.from_inspect_parameter(parameter)
                  for parameter_name, parameter in signature.parameters.items()}

    def callback(param_values):
        func(param_values)

    def f(*args, **kwargs):
        bound_arguments = signature.bind_partial(*args, **kwargs)
        for param_name, arg_value in bound_arguments.arguments.items():
            parameters[param_name].default_value = arg_value
        pypagui.gui.qt.make_gui(parameters, callback)
    return f


def is_relevant_member(name, value):
    return not name.startswith("__") and not (
        inspect.ismodule(value) or
        inspect.isclass(value) or
        inspect.ismethod(value) or
        inspect.isfunction(value) or
        inspect.isgeneratorfunction(value) or
        inspect.isgenerator(value) or
        inspect.isbuiltin(value) or
        inspect.isroutine(value)
    )


def extract_module_parameters(module):
    members = inspect.getmembers(module)
    return {m[0]: pypagui.parameter.Parameter(m[0], type(m[1]), m[1])
            for m in members if is_relevant_member(*m)}


def wrap_module(module_name: str):
    module = sys.modules[module_name]
    parameters = extract_module_parameters(module)

    def callback(param_values):
        for param_name, param_value in param_values.items():
            setattr(module, param_name, parameters[param_name].value_from_input(param_value))

    pypagui.gui.qt.make_gui(parameters, callback, exit_on_run=True)
