from functools import partial

from PySide6 import QtGui
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QHBoxLayout, QWidget, QMainWindow, QVBoxLayout, QLayout, QLabel, QTabWidget, QPushButton, \
    QLineEdit, QGridLayout

from variables import Variables, TextTranslation


class GeneralWindow(QMainWindow):
    def __init__(self, *args):
        super(GeneralWindow, self).__init__()

        self._number_of_spans = 0

        self._screen_label = QLabel()
        self._button_plus_a_span = QPushButton(TextTranslation.plus_a_span.text)
        self._button_minus_a_span = QPushButton(TextTranslation.minus_a_span.text)
        self._tab_menu = QTabWidget()
        self._current_span = 0
        self._list_of_tabs: [QWidget] = []
        self._scale_spans = 0
        self._list_of_p: [float] = []
        self._list_of_h: [float] = []
        self._list_of_l: [float] = []
        self._list_of_y: [float] = []

        self.canvas = QtGui.QPixmap(Variables.bh_screen_label[0], Variables.bh_screen_label[1])
        self.canvas.fill(Variables.MyColors.background)
        self._screen_label.setPixmap(self.canvas)
        self._painter: QtGui.QPainter | None = None

        general_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        self._init_left_layout(left_layout=left_layout)
        general_layout.addLayout(left_layout)
        middle_layout = QVBoxLayout()
        self._init_middle_layout(middle_layout=middle_layout)
        general_layout.addLayout(middle_layout)
        right_layout = QVBoxLayout()
        general_layout.addLayout(right_layout)

        widget = QWidget()
        widget.setLayout(general_layout)
        self.setCentralWidget(widget)

    def _init_left_layout(self, left_layout: QLayout):
        plus_minus_span_layout = self._make_plus_minus_span_layout()
        left_layout.addLayout(plus_minus_span_layout)

        left_layout.addWidget(self._tab_menu)
        self._tab_menu.currentChanged.connect(self._change_tab)
        self._make_a_new_tab_element()

    def _init_middle_layout(self, middle_layout: QLayout):
        self._screen_label.setFixedHeight(Variables.bh_screen_label[0])
        self._screen_label.setFixedWidth(Variables.bh_screen_label[1])
        middle_layout.addWidget(self._screen_label)

    def _init_right_layout(self, right_layout: QLayout):
        pass

    def _change_tab(self, i):
        self._current_span = i

    def _make_a_new_tab_element(self):
        new_tab_layout = QWidget()
        name_of_the_tab = TextTranslation.span.text + ' Nr.' + str(self._number_of_spans)

        parameters_of_the_span = QGridLayout()
        label_h = QLabel('h, m =')
        parameters_of_the_span.addWidget(label_h, 0, 0)
        new_h = 1 if self._number_of_spans == 0 else self._list_of_h[-1]
        self._list_of_h.append(new_h)
        entry_h = QLineEdit(str(self._list_of_h[self._number_of_spans]))
        entry_h.textChanged.connect(partial(self._new_value, 'h', self._number_of_spans))
        parameters_of_the_span.addWidget(entry_h, 0, 1)

        label_l = QLabel('l, m =')
        parameters_of_the_span.addWidget(label_l, 1, 0)
        new_l = 32 if self._number_of_spans == 0 else self._list_of_l[-1]
        self._list_of_l.append(new_l)
        entry_l = QLineEdit(str(self._list_of_l[self._number_of_spans]))
        entry_l.textChanged.connect(partial(self._new_value, 'l', self._number_of_spans))
        parameters_of_the_span.addWidget(entry_l, 1, 1)

        label_y = QLabel('y, m =')
        parameters_of_the_span.addWidget(label_y, 2, 0)
        new_y = .5 if self._number_of_spans == 0 else self._list_of_y[-1]
        self._list_of_y.append(new_y)
        entry_y = QLineEdit(str(self._list_of_y[self._number_of_spans]))
        entry_y.textChanged.connect(partial(self._new_value, 'y', self._number_of_spans))
        parameters_of_the_span.addWidget(entry_y, 2, 1)

        label_p = QLabel('p, kN =')
        parameters_of_the_span.addWidget(label_p, 3, 0)
        new_p = 3500 if self._number_of_spans == 0 else self._list_of_p[-1]
        self._list_of_p.append(new_p)
        entry_p = QLineEdit(str(self._list_of_p[self._number_of_spans]))
        entry_p.textChanged.connect(partial(self._new_value, 'p', self._number_of_spans))
        parameters_of_the_span.addWidget(entry_p, 3, 1)

        new_tab_layout.setLayout(parameters_of_the_span)
        self._list_of_tabs.append(new_tab_layout)
        self._tab_menu.addTab(new_tab_layout, name_of_the_tab)

        self._number_of_spans += 1

    def _new_value(self, type_of_the_value: str, tab_index: int, new_value: str):
        try:
            t = float(new_value)
        except Exception:
            return None
        match type_of_the_value:
            case 'h':
                self._list_of_h[tab_index] = t
            case 'l':
                self._list_of_l[tab_index] = t
            case 'y':
                self._list_of_y[tab_index] = t
            case 'p':
                self._list_of_p[tab_index] = t
        self._draw_graph()

    def _make_plus_minus_span_layout(self) -> QLayout:
        plus_minus_span_layout = QHBoxLayout()
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self._button_plus_a_span)
        self._button_plus_a_span.clicked.connect(partial(self._plus_minus_a_span, '+'))
        self._button_minus_a_span.clicked.connect(partial(self._plus_minus_a_span, '-'))
        buttons_layout.addWidget(self._button_minus_a_span)
        plus_minus_span_layout.addLayout(buttons_layout)
        return plus_minus_span_layout

    def _plus_minus_a_span(self, plus_or_minus: str):
        """:parameter plus_or_minus '+', '-' """
        if plus_or_minus == '+':
            self._make_a_new_tab_element()
        else:
            if self._number_of_spans == 1:
                return None
            self._number_of_spans -= 1
            self._tab_menu.removeTab(len(self._list_of_tabs) - 1)
            self._list_of_tabs.pop()
            self._list_of_h.pop()
            self._list_of_y.pop()
            self._list_of_l.pop()
            self._list_of_p.pop()
        self._draw_graph()

    def _make_scale(self):
        s_l = 0
        max_h = self._list_of_h[0]
        for i, l_i in enumerate(self._list_of_l):
            s_l += l_i
            if self._list_of_h[i] > max_h:
                max_h = self._list_of_h[i]
        if s_l == 0:
            return None
        scale_x = (Variables.bh_screen_label[0] - 2 * Variables.border_for_screen) / s_l
        scale_y = (Variables.bh_screen_label[1] - 2 * Variables.border_for_screen) / max_h
        self._scale_spans = min(scale_x, scale_y)

    def _draw_graph(self):
        canvas = self._screen_label.pixmap()
        canvas.fill(Qt.black)
        self._painter = QtGui.QPainter(canvas)

        self._draw_spans()
        self._painter.end()
        self._screen_label.setPixmap(canvas)

    def _draw_spans(self):
        x0 = Variables.border_for_screen
        y0 = Variables.border_for_screen
        for i in range(self._number_of_spans):
            color = Variables.MyColors.spans
            pen = QtGui.QPen()
            pen.setColor(color)
            pen.setWidth(1)
            self._painter.setPen(pen)
            x1 = x0 + self._list_of_l[i] * self._scale_spans
            y1 = y0 + self._list_of_h[i] * self._scale_spans
            self._painter.drawRect(x0, y0, x1, y1)
            x0 = x1
            y0 = y1
