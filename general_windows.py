import math
from functools import partial

from PySide6 import QtGui
from PySide6.QtCore import QPointF
from PySide6.QtGui import QColor, QPolygonF
from PySide6.QtWidgets import (QHBoxLayout, QWidget, QMainWindow, QVBoxLayout, QLayout, QLabel, QTabWidget,
                               QPushButton, QLineEdit, QGridLayout)

from small_classes import XY
from static_functions import make_spline
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
        self._vertical_scale_of_spans = 10
        self._dx = 1
        self._coordinate_for_spline: dict[XY] = dict()
        self._list_of_p_bottom: [float] = []
        self._list_of_p_top: [float] = []
        self._list_of_h: [float] = []
        self._list_of_l: [float] = []
        self._list_of_y: [float] = []
        self._list_of_e0: [float] = []
        self._list_of_f: [float] = []
        self._list_of_en: [float] = []
        self._list_of_x: list[float] = list()
        self._h_max: float = 0  # max height of the beam

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
        self._init_right_layout(right_layout=right_layout)
        general_layout.addLayout(right_layout)

        widget = QWidget()
        widget.setLayout(general_layout)
        self.setCentralWidget(widget)
        self._calculate_ans_draw_all()

    def _init_left_layout(self, left_layout: QLayout):
        plus_minus_span_layout = self._make_plus_minus_span_layout()
        left_layout.addLayout(plus_minus_span_layout)

        left_layout.addWidget(self._tab_menu)
        self._tab_menu.currentChanged.connect(self._change_tab)
        self._make_a_new_tab_element()

    def _init_middle_layout(self, middle_layout: QLayout):
        self._screen_label.setFixedHeight(Variables.bh_screen_label[1])
        self._screen_label.setFixedWidth(Variables.bh_screen_label[0])
        middle_layout.addWidget(self._screen_label)

    def _init_right_layout(self, right_layout: QLayout):
        label_scale = QLabel(TextTranslation.scale_of_the_span.text)
        right_layout.addWidget(label_scale)
        entry_scale = QLineEdit(str(self._vertical_scale_of_spans))
        entry_scale.textChanged.connect(partial(self._new_value, 'v_scale', self._number_of_spans))
        right_layout.addWidget(entry_scale)
        label_dx = QLabel('dx, m = ')
        right_layout.addWidget(label_dx)
        entry_dx = QLineEdit(str(self._dx))
        entry_dx.textChanged.connect(partial(self._new_value, 'dx', self._number_of_spans))
        right_layout.addWidget(entry_dx)

    def _change_tab(self, i):
        self._current_span = i

    def _make_a_new_tab_element(self):
        new_tab_layout = QWidget()
        general_layout = QVBoxLayout()
        name_of_the_tab = TextTranslation.span.text + ' Nr.' + str(self._number_of_spans)
        parameters_of_the_span = self._make_layout_parameter_of_the_span()
        parameters_of_ideal_cables = self._make_parameters_of_ideal_cables()

        general_layout.addLayout(parameters_of_the_span)
        general_layout.addLayout(parameters_of_ideal_cables)
        new_tab_layout.setLayout(general_layout)
        self._list_of_tabs.append(new_tab_layout)
        self._tab_menu.addTab(new_tab_layout, name_of_the_tab)

        self._number_of_spans += 1

    def _make_parameters_of_ideal_cables(self) -> QWidget:
        parameters_layout = QGridLayout()
        label_e0 = QLabel('e0, m =')
        label_e0.setEnabled(self._number_of_spans != 1)
        parameters_layout.addWidget(label_e0, 0, 0)
        new_e0 = 0.2 if self._number_of_spans == 0 else self._list_of_en[-1]
        self._list_of_e0.append(new_e0)
        entry_e0 = QLineEdit(str(self._list_of_e0[self._number_of_spans]))
        entry_e0.setEnabled(self._number_of_spans != 1)
        entry_e0.textChanged.connect(partial(self._new_value, 'e0', self._number_of_spans))
        parameters_layout.addWidget(entry_e0, 0, 1)

        label_f = QLabel('f, m =')
        parameters_layout.addWidget(label_f, 1, 0)
        new_f = 0.2 if self._number_of_spans == 0 else self._list_of_f[-1]
        self._list_of_f.append(new_f)
        entry_f = QLineEdit(str(self._list_of_f[self._number_of_spans]))
        entry_f.textChanged.connect(partial(self._new_value, 'f', self._number_of_spans))
        parameters_layout.addWidget(entry_f, 1, 1)

        label_en = QLabel('en, m =')
        parameters_layout.addWidget(label_en, 2, 0)
        new_en = 0.2 if self._number_of_spans == 0 else self._list_of_en[-1]
        self._list_of_en.append(new_en)
        entry_en = QLineEdit(str(self._list_of_en[self._number_of_spans]))
        entry_en.textChanged.connect(partial(self._new_value, 'en', self._number_of_spans))
        parameters_layout.addWidget(entry_en, 2, 1)
        return parameters_layout

    def _make_layout_parameter_of_the_span(self) -> QWidget:
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

        label_p = QLabel(TextTranslation.p_under.text)
        parameters_of_the_span.addWidget(label_p, 3, 0)
        new_p = 3500 if self._number_of_spans == 0 else self._list_of_p_bottom[-1]
        self._list_of_p_bottom.append(new_p)
        entry_p = QLineEdit(str(self._list_of_p_bottom[self._number_of_spans]))
        entry_p.textChanged.connect(partial(self._new_value, 'p_bottom', self._number_of_spans))
        parameters_of_the_span.addWidget(entry_p, 3, 1)

        label_p_top = QLabel(TextTranslation.p_top.text)
        parameters_of_the_span.addWidget(label_p_top, 4, 0)
        new_p = 3500 if self._number_of_spans == 0 else self._list_of_p_top[-1]
        self._list_of_p_top.append(new_p)
        entry_p_top = QLineEdit(str(self._list_of_p_top[self._number_of_spans]))
        entry_p_top.textChanged.connect(partial(self._new_value, 'p_top', self._number_of_spans))
        parameters_of_the_span.addWidget(entry_p_top, 4, 1)
        return parameters_of_the_span

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
            case 'p_bottom':
                self._list_of_p_bottom[tab_index] = t
            case 'p_top':
                self._list_of_p_top[tab_index] = t
            case 'v_scale':
                self._vertical_scale_of_spans = t
            case 'e0':
                self._list_of_e0[tab_index] = t
            case 'f':
                self._list_of_f[tab_index] = t
            case 'en':
                self._list_of_en[tab_index] = t
            case 'dx':
                self._dx = t
        self._calculate_ans_draw_all()

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
            self._list_of_p_bottom.pop()
            self._list_of_e0.pop()
            self._list_of_f.pop()
            self._list_of_en.pop()
        self._calculate_ans_draw_all()

    def _make_scale(self):
        s_l = 0
        self._h_max = self._list_of_h[0]
        for i, l_i in enumerate(self._list_of_l):
            s_l += l_i
            if self._list_of_h[i] > self._h_max:
                self._h_max = self._list_of_h[i] * self._vertical_scale_of_spans
        if s_l == 0 or self._h_max <= 0:
            return None
        scale_x = (Variables.bh_screen_label[0] - 2 * Variables.border_for_screen) / s_l
        scale_y = (Variables.bh_screen_label[1] - 2 * Variables.border_for_screen) / self._h_max
        self._scale_spans = min(scale_x, scale_y)

    def _draw_graph(self, m_dir: []):
        self._make_scale()
        canvas = self._screen_label.pixmap()
        canvas.fill(Variables.MyColors.background)
        self._painter = QtGui.QPainter(canvas)

        self._draw_spans()
        self._draw_spline_for_ideal_cable()
        self._draw_moment_ideal(list_of_m_dir=m_dir)
        self._painter.end()
        self._screen_label.setPixmap(canvas)

    def _draw_spans(self):
        color = Variables.MyColors.spans
        brush = QtGui.QBrush(color)
        self._painter.setBrush(brush)
        pen = QtGui.QPen()
        pen.setColor(color)
        pen.setWidth(1)

        pen_y = QtGui.QPen()
        pen_y.setColor(Variables.MyColors.y_line)

        x0 = Variables.border_for_screen
        y0 = Variables.border_for_screen
        # joint 0
        a = 10
        polygon = QPolygonF()
        polygon.append(QPointF(x0, y0 + self._list_of_h[0] * self._scale_spans * self._vertical_scale_of_spans))
        polygon.append(QPointF(x0 + a, y0 + self._list_of_h[0] * self._scale_spans * self._vertical_scale_of_spans + a))
        polygon.append(QPointF(x0 - a, y0 + self._list_of_h[0] * self._scale_spans * self._vertical_scale_of_spans + a))
        self._painter.drawPolygon(polygon)

        for i in range(self._number_of_spans):
            # draw a span
            dx = self._list_of_l[i] * self._scale_spans
            dy = self._list_of_h[i] * self._scale_spans * self._vertical_scale_of_spans
            self._painter.drawRect(x0, y0, dx, dy)
            # draw line y
            self._painter.setPen(pen_y)
            y_ = y0 + (self._list_of_h[i] - self._list_of_y[i]) * self._scale_spans * self._vertical_scale_of_spans
            self._painter.drawLine(x0, y_, x0 + dx, y_)
            self._painter.setPen(pen)
            x0 += dx
            # draw a joint
            self._painter.drawEllipse(x0 - a * .5, y0 + dy, a, a)

    def _draw_spline_for_ideal_cable(self):
        if len(self._coordinate_for_spline) < 4:
            return None
        x_points = []
        y_points = []
        list_x_sorted = sorted(self._coordinate_for_spline.values(), key=lambda point: point.x)
        for point in list_x_sorted:
            x_points.append(point.x)
            y_points.append(point.y)
        spline_line = make_spline(x_points=x_points, y_points=y_points, list_of_new_x=self._list_of_x)
        color = QColor(*(10, 255, 0))
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor(color))
        pen.setWidth(1)
        self._painter.setPen(pen)
        if spline_line is None:
            return None
        b0 = Variables.border_for_screen
        j = 0
        l_0 = self._list_of_l[0]
        for i in range(len(spline_line) - 1):
            point0: XY = spline_line[i]
            point1: XY = spline_line[i + 1]
            if point1.x > l_0:
                j += 1
                l_0 += self._list_of_l[j]

            x1 = self._scale_spans * point0.x + b0
            y1 = b0 + self._scale_spans * self._vertical_scale_of_spans * (self._list_of_h[j] - self._list_of_y[j] -
                                                                           point0.y)
            x2 = self._scale_spans * point1.x + b0
            y2 = b0 + self._scale_spans * self._vertical_scale_of_spans * (self._list_of_h[j] - self._list_of_y[j] -
                                                                           point1.y)
            self._painter.drawLine(x1, y1, x2, y2)

    def _calculate_init(self):
        self._make_dict_of_x()
        self._calculate_spline_for_ideal()

    def _calculate_ans_draw_all(self):
        self._calculate_init()
        m_direct = self._make_m_direct()
        m_indirect = self._make_m_indirect()
        self._draw_graph(m_dir=m_dir)

    def _calculate_spline_for_ideal(self):
        self._coordinate_for_spline = dict()
        x0 = 0
        for i in range(self._number_of_spans):
            l_i = self._list_of_l[i]
            if i == 0:
                self._coordinate_for_spline[f'e0 {i}'] = XY(x=x0, y=self._list_of_e0[i], i=i)
                if self._number_of_spans == 1:
                    self._coordinate_for_spline[f'e025 {i}'] = XY(x=x0 + l_i * .15, y=0, i=i)
                    self._coordinate_for_spline[f'e075 {i}'] = XY(x=x0 + l_i * .85, y=0, i=i)
            self._coordinate_for_spline[f'f {i}'] = XY(x=x0 + .5 * l_i, y=-self._list_of_f[i], i=i)
            self._coordinate_for_spline[f'en {i}'] = XY(x=x0 + l_i, y=self._list_of_en[i], i=i)
            x0 += l_i

    def _make_dict_of_x(self):
        self._list_of_x = list()
        if self._dx == 0:
            return None
        x0 = 0
        self._list_of_x.append(x0)
        for i, l in enumerate(self._list_of_l):
            n = math.ceil(l / self._dx)
            dl = l / n
            for j in range(1, n + 1):
                x0 += dl
                self._list_of_x.append(x0)

    def _make_m_direct(self) -> [float]:
        j = 0
        l_i = self._list_of_l[0]
        l_0 = 0
        f_i = .5 * (self._list_of_e0[0] + self._list_of_en[0]) + self._list_of_f[0]
        p_i_top_left = self._list_of_p_bottom[0]
        p_i_bottom = self._list_of_p_bottom[0]
        p_i_top_right = self._list_of_p_top[0]
        e_l = self._list_of_e0[0]
        e_r = self._list_of_en[0]
        list_of_m_dir = []
        for x in self._list_of_x:
            if x > l_i + l_0:
                j += 1
                l_i = self._list_of_l[j]
                l_0 += self._list_of_l[j - 1]
                e_l = self._list_of_en[j - 1]
                e_r = self._list_of_en[j]
                f_i = .5 * (e_l + e_r) + self._list_of_f[j]
                p_i_top_left = self._list_of_p_top[j - 1]
                p_i_bottom = self._list_of_p_bottom[j]
                p_i_top_right = self._list_of_p_top[j]

            x_i = x - l_0
            g = 8 * f_i * p_i_bottom / l_i ** 2
            mf = .5 * g * (l_i * x_i - x_i ** 2)  # moment from f - parabola
            me_l = -(1 - x_i / l_i) * p_i_top_left * e_l  # moment from e left - triangle
            me_r = -x_i / l_i * p_i_top_right * e_r  # moment from e right - triangle
            list_of_m_dir.append(mf + me_l + me_r)
        return list_of_m_dir

    def _make_m_indirect(self):
        pass

    def _draw_moment_ideal(self, list_of_m_dir: [float]):
        color = Variables.MyColors.ideal_dir
        brush = QtGui.QBrush(color)
        self._painter.setBrush(brush)
        pen = QtGui.QPen()
        pen.setColor(color)
        pen.setWidth(1)

        b0 = Variables.border_for_screen
        y0 = 2 * b0 + self._scale_spans * self._vertical_scale_of_spans * self._h_max
        # scale the graph
        m_max = max(list_of_m_dir)
        m_min = min(list_of_m_dir)
        if m_min > 0:
            m_min = 0
        scale = Variables.h_of_curves / (m_max - m_min)
        for i in range(0, len(list_of_m_dir)):
            x_1 = self._list_of_x[i] * self._scale_spans + b0
            y_1 = (list_of_m_dir[i] + abs(m_min)) * scale + y0
            if i != 0:
                self._painter.drawLine(x_0, y_0, x_1, y_1)
            x_0 = x_1
            y_0 = y_1
        # draw null
        x_0 = b0
        x_1 = self._list_of_x[-1] * self._scale_spans + b0
        y_1 = abs(m_min) * scale + y0
        self._painter.drawLine(x_0, y_1, x_1, y_1)
