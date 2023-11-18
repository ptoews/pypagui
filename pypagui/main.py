import inspect
import sys
import threading

import pypagui.gui.qt
import pypagui.parameter


def wrap_function(func):
    signature = inspect.signature(func)

    parameters = {parameter_name: pypagui.parameter.Parameter.from_inspect_parameter(parameter)
                  for parameter_name, parameter in signature.parameters.items()}

    def callback(param_values, on_finish_callback):
        """
        This method is called by the GUI after the user has pressed run.
        It is run in the main thread.
        """
        def func_with_callback():
            """
            This method runs the actual execution. Additionally, it calls a callback that
            goes back to the GUI to inform it about the execution having finished.
            """
            func(**param_values)
            on_finish_callback()

        # Run the actual execution in a separate thread to not block the GUI
        thread = threading.Thread(target=func_with_callback)
        thread.start()

    def f(*args, **kwargs):
        bound_arguments = signature.bind_partial(*args, **kwargs)
        for param_name, arg_value in bound_arguments.arguments.items():
            param = parameters[param_name]
            param.default_value = arg_value
            if param.type_annotation is None:
                param.type_annotation = type(arg_value)
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
