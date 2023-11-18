import inspect
import typing as T

import dataclasses


@dataclasses.dataclass
class Parameter:
    name: str
    type_annotation: T.Optional[type]
    default_value: T.Any

    @classmethod
    def from_inspect_parameter(cls, parameter: inspect.Parameter):
        type_annotation = parameter.annotation if parameter.annotation is not inspect.Parameter.empty else None
        default_value = parameter.default if parameter.default is not inspect.Parameter.empty else None
        if type_annotation is None and default_value is not None:
            type_annotation = type(default_value)
        return cls(name=parameter.name,
                   type_annotation=type_annotation,
                   default_value=default_value)

    def value_from_input(self, input_string: str):
        if self.type_annotation is None:
            if input_string == "":
                return None
            # Try to guess data type
            try:
                return int(input_string)
            except ValueError:
                pass
            try:
                return float(input_string)
            except ValueError:
                pass
            # Not a number; assume string
            return input_string
        else:
            return self.type_annotation(input_string)

    def default_value_to_string(self):
        if self.default_value is None:
            return ""
        return str(self.default_value)

