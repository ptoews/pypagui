from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw


class ParameterFormWidget(qtw.QWidget):
    def __init__(self, parameters, callback, exit_on_run=False):
        super().__init__()
        self._callback = callback
        self._exit_on_run = exit_on_run

        self._param_edits = {}
        self._layout = qtw.QVBoxLayout()
        for parameter in parameters.values():
            param_layout = qtw.QHBoxLayout()
            label = qtw.QLabel(parameter.name)
            edit = qtw.QLineEdit(parameter.default_value_to_string())
            self._param_edits[parameter.name] = edit
            param_layout.addWidget(label)
            param_layout.addWidget(edit)
            self._layout.addLayout(param_layout)

        self._run_button = qtw.QPushButton("Run")
        self._run_button.clicked.connect(self._on_button_click)
        self._layout.addWidget(self._run_button)
        self.setLayout(self._layout)

    @qtc.Slot()
    def _on_button_click(self):
        self._callback({n: edit.text() for n, edit in self._param_edits.items()})
        if self._exit_on_run:
            self.close()


def make_gui(parameters, callback, exit_on_run=False):
    app = qtw.QApplication([])

    widget = ParameterFormWidget(parameters, callback, exit_on_run=exit_on_run)
    widget.show()

    app.exec()


if __name__ == "__main__":
    make_gui({"p1": 123, "p2": "abc"}, print)
