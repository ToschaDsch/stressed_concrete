import json

from PySide6.QtWidgets import QFileDialog


def open_file(self):
    delete_all_data(self)
    data = open_file_menu(self)
    if data is False:
        return None
    json_data = json.loads(data)
    print(json_data)
    send_data_to_program(self, json_data)


def delete_all_data(self):
    for i in range(self._number_of_spans):
        self._plus_minus_a_span('-')


def send_data_to_program(self, data: dict):
    self._number_of_spans = data['n_spans']
    for i in range(len(self._number_of_spans)):
        self._plus_minus_a_span('+')
    self._entry_dx.setText(str(data['dx']))
    self._entry_scale.setText(str(data['v_scale']))
    data_spans = data['spans']
    for data_span in data_spans:
        self._entry_h.setText(str(data_span['h']))
        self._entry_l.setText(str(data_span['l']))
        self._entry_y.setText(str(data_span['y']))
        self._entry_p.setText(str(data_span['p_bottom']))
        self._entry_p_top.setText(str(data_span['p_top']))
        self._entry_e0.setText(str(data_span['e0']))
        self._entry_f.setText(str(data_span['f']))
        self._entry_en.setText(str(data_span['en']))


def open_file_menu(self) -> bool | str:
    tf = QFileDialog.getOpenFileName(self, 'open', None, "psb (*.psb)")
    try:
        name = tf[0]
        tf = open(name)  # or tf = open(tf, 'r')
        data = tf.read()
        tf.close()
    except (FileExistsError, Exception):
        print('file not found')
        return False
    self.setWindowTitle(name)
    return data


def save_file(self, file=None):
    data: dict = data_to_dict(self)
    json_data = json.dumps(data)

    if file is None:
        file = QFileDialog.getSaveFileName(self, 'save as', 'model', "psb (*.psb)")
    try:
        fob = open(file[0], 'w')
        fob.write(json_data)
        fob.close()
    except (FileExistsError, Exception):
        print('file not found')


def data_to_dict(self) -> dict:
    data = dict()
    data['n_spans'] = self._number_of_spans
    data['v_scale'] = self._vertical_scale_of_spans
    data['dx'] = self._dx
    for i in range(len(self._number_of_spans)):
        data_span = dict()
        data_span['h'] = self._list_of_h[i]
        data_span['l'] = self._list_of_l[i]
        data_span['y'] = self._list_of_y[i]
        data_span['p_bottom'] = self._list_of_p_bottom[i]
        data_span['p_top'] = self._list_of_p_top[i]
        data_span['e0'] = self._list_of_e0[i]
        data_span['f'] = self._list_of_f[i]
        data_span['en'] = self._list_of_en[i]
    return data
