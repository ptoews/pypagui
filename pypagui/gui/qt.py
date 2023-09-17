import datetime
import pathlib
import typing as T

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw

from pypagui.parameter import Parameter


class ParameterFormWidget(qtw.QWidget):
    def __init__(self, parameters: T.Dict[str, Parameter], callback, exit_on_run=False):
        super().__init__()
        self._parameters = parameters
        self._callback = callback
        self._exit_on_run = exit_on_run

        self._param_edits = {}
        self._layout = qtw.QVBoxLayout()
        for parameter in parameters.values():
            param_layout = qtw.QHBoxLayout()
            label = qtw.QLabel(parameter.name)
            edit = self.create_parameter_editing_widget(parameter)
            self._param_edits[parameter.name] = edit
            param_layout.addWidget(label)
            param_layout.addWidget(edit)
            self._layout.addLayout(param_layout)

        self._run_button = qtw.QPushButton("Run")
        self._run_button.clicked.connect(self._on_button_click)
        self._layout.addWidget(self._run_button)
        self.setLayout(self._layout)

    @staticmethod
    def create_parameter_editing_widget(parameter: Parameter):
        if parameter.type_annotation is None:
            edit = qtw.QLineEdit(parameter.default_value_to_string())
        elif issubclass(parameter.type_annotation, bool):
            edit = qtw.QCheckBox()
            if parameter.default_value is not None:
                edit.setChecked(parameter.default_value)
        elif issubclass(parameter.type_annotation, int):
            edit = qtw.QSpinBox()
            edit.setRange(-2**31, 2**31-1)
            if parameter.default_value is not None:
                edit.setValue(parameter.default_value)
        elif issubclass(parameter.type_annotation, float):
            # QDoubleSpinBox uses a fixed precision that we cannot infer, so use a text widget
            edit = qtw.QLineEdit()
            if parameter.default_value is not None:
                edit.setText(str(parameter.default_value))
        elif issubclass(parameter.type_annotation, datetime.datetime):
            edit = qtw.QDateTimeEdit()
            if parameter.default_value is not None:
                edit.setDateTime(parameter.default_value)
        else:
            edit = qtw.QLineEdit(parameter.default_value_to_string())
        return edit

    @staticmethod
    def extract_parameter_value(parameter, edit_widget):
        if parameter.type_annotation is None:
            value = edit_widget.text()
        elif issubclass(parameter.type_annotation, bool):
            value = edit_widget.isChecked()
        elif issubclass(parameter.type_annotation, int):
            value = edit_widget.value()
        elif issubclass(parameter.type_annotation, float):
            # We use QLineEdit for floats, see create_parameter_editing_widget() for explanation
            value = float(edit_widget.text())
        elif issubclass(parameter.type_annotation, datetime.datetime):
            value = edit_widget.dateTime().toPython()
        else:
            value = edit_widget.text()
        return value

    def _on_run_finished(self):
        """
        Called by the callback method after the run execution has finished. This method runs
        in the execution thread, not in the main thread.
        """
        self._run_button.setEnabled(True)

    @qtc.Slot()
    def _on_button_click(self):
        self._run_button.setEnabled(False)
        parameters = {n: self.extract_parameter_value(self._parameters[n], edit)
                      for n, edit in self._param_edits.items()}
        self._callback(parameters, self._on_run_finished)
        if self._exit_on_run:
            self.close()


def make_gui(parameters, callback, exit_on_run=False):
    app = qtw.QApplication([])

    widget = ParameterFormWidget(parameters, callback, exit_on_run=exit_on_run)
    widget.show()

    app.exec()


if __name__ == "__main__":
    make_gui({"p1": 123, "p2": "abc"}, print)
