import inspect

import pypagui.gui.qt
import pypagui.parameter


def wrap_function(func):
    signature = inspect.signature(func)

    parameters = {parameter_name: pypagui.parameter.Parameter.from_inspect_parameter(parameter)
                  for parameter_name, parameter in signature.parameters.items()}

    def callback(param_values):
        casted_param_values = {param_name: parameters[param_name].value_from_input(param_value)
                               for param_name, param_value in param_values.items()}
        func(**casted_param_values)

    def f(*args, **kwargs):
        bound_arguments = signature.bind_partial(*args, **kwargs)
        for param_name, arg_value in bound_arguments.arguments.items():
            parameters[param_name].default_value = arg_value
        pypagui.gui.qt.make_gui(parameters, callback)
    return f


def wrap_module(module):
    members = inspect.getmembers(module)
    non_dunder_members = [m for m in members if not m[0].startswith("__")]
    print(f"{non_dunder_members=}")
