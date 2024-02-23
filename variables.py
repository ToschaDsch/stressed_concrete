from dataclasses import dataclass

from PySide6.QtGui import QColor


@dataclass
class Languages:
    english = 'english'
    german = 'german'


@dataclass
class Geometry:
    dx_dy_by_moved_node = (0, 0)
    regime: str | None = None  #


@dataclass
class GUIObjects:
    list_of_points_for_listbox = None
    ico_pictures = []
    check_box_var = []
    popup_menu_screen = None
    listbox_show = None


@dataclass
class Variables:
    language = Languages.german
    screen_width = 0
    screen_height = 0
    general_window = None
    bh_screen_label = (300, 300)
    border_for_screen = 20

    @dataclass
    class MyColors:
        joint = QColor(150, 150, 0)
        points = QColor(250, 10, 0)
        lines = QColor(250, 50, 0)
        transparency = 100
        background = QColor(40, 40, 40)
        spans = QColor(60, 60, 60)


class Translation:
    def __init__(self, english: str = None, german: str = None):
        self._english = english
        self._german = german

    @property
    def text(self) -> str:
        name = None
        match Variables.language:
            case Languages.english:
                name = self._english
            case Languages.german:
                name = self._german
        if name is None:
            return self._english
        else:
            return name


@dataclass
class TextTranslation:
    at_the_beginning = Translation(english='at the beginning', german='am Anfang')
    at_the_end = Translation(english='at the end', german='am Ende')
    axes = Translation(english='axes', german='Achsen')
    axis = Translation(english='axis', german='Achse')
    back = Translation(english='Undo', german='Zurück')
    begin_or_end = Translation(english='begin or end',  german='am Anfang oder am Ende')
    boundary_conditions = Translation(english='boundary conditions', german='Randbedingungen')
    cancel = Translation(english='Cancel', german='Abbrechnen')
    check_the_numbers = Translation(english='check the numbers!', german='prüfe die Zahlen')
    copy_shift = Translation(english='copy/shift', german='copieren/schieben')
    color = Translation(english='color', german='Farbe')
    comments: Translation = Translation(english='comments', german='Kommentare')
    circular = Translation(english='circular', german='kreisförmig')
    concrete = Translation(english='concrete', german='Beton')
    displacement = Translation(english='displacement', german='Verformung')
    dead_loads = Translation(english='dead_loads', german='ständige')
    default = Translation(english='default', german='Default')
    delete_the_point = Translation(english='delete the point', german='den Punkt entfernen')
    delete_points_without_lines = Translation(english='delete \npoints \nwithout \nlines',
                                              german='entfernen \nPunkte \nohne \nLinien')
    delete = Translation(english='delete', german='entfernen')
    divide = Translation(english='divide', german='teilen')
    distance = Translation(english='distance', german='Abstand')
    edit = Translation(english='edit', german='bearbeiten')
    earthquake = Translation(english='earthquake', german='Erdbeben')
    element = Translation(english='element', german='Element')
    exchange_begin_end_of_line = Translation(english='exchange begin end of line', german='tausche Anfang und Ende auf')
    export_to_excel = Translation('export to excel', 'Export nach Excel')
    export_to_dxf = Translation('export to dxf', 'Export nach dxf')
    node_0 = Translation(english='node 0', german='Node 0')
    node_1 = Translation(english='node 1', german='Node 1')
    forward = Translation(english='Redo', german='Vorwärts')
    for_n_points = Translation(english='points are picked', german='Punkten sind gewählt')
    for_n_lines = Translation(english='lines are picked', german='Linien sind gewählt')
    from_start = Translation(english='from start', german='ab Anfang')
    from_end = Translation(english='from end', german='ab Ende')
    from_point_to_point = Translation('from point to point', german='von Punkt zu Punkt')
    group = Translation(english='group', german='Gruppe')
    group_of_loads = Translation(english='group of loads', german='Gruppen von Lasten')
    id_for_section = Translation(english='id for sections', german='id für Querschnitten')
    import_from_excel = Translation('import fro excel', 'Import aus Excel')
    import_from_dxf = Translation('import fro dxf', 'Import aus dxf')
    influence_line = Translation(english='influence line', german='Einflußlinie')
    i_sections = Translation(english='I sections', german='I Profile')
    isosceles = Translation(english='isosceles', german='gleichschenklig')
    hinges = Translation(english='hinges', german='Gelenke')
    live_loads = Translation(english='live loads', german='Verkehr')
    lines = Translation(english='Lines', german='Linien')
    line_id = Translation(english='lines_id', german='id Lines')
    line_comment = Translation(english='lines comment', german='Linienskommentar')
    line_loads = Translation(english='line-loads', german='Linielasten')
    loads = Translation(english='loads', german='Lasten')
    load_size = Translation(english='load size, m', german='Lastensgröße, m')
    load_text = Translation(english='load with text', german='Lasten mit Text')
    local_axes = Translation(english='local axes', german='lokale Achse')
    l_sections = Translation(english='L sections', german='Winkel')
    material = Translation(english='material', german='Material')
    merge = Translation(english='merge->', german='vereinen->')
    minus_a_span = Translation(english='- a span', german='- ein Feld')
    mirror = Translation(english='mirror', german='spiegeln')
    mirror_along_the_axis = Translation(english='mirror_along_the_axis', german='spiegeln entlang die Achse')
    moment_y = Translation(english='moment, y', german='Moment, y')
    moment_z = Translation(english='moment, z', german='Moment, z')
    name = Translation(english='name', german='Name')
    new_mesh = Translation(english='new mesh', german='neue Vernetzung')
    new_span = Translation(english='new span', german='neues Feld')
    normal_forge = Translation(english='normal forge', german='Normalfraft')
    not_isosceles = Translation(english='not isosceles', german='ungleichschenklig')
    objects = Translation(english='objects', german='Objekts')
    ok = Translation(english='Ok', german='Ok')
    open_file = Translation(english='Open', german='Offnen')
    o_sections = Translation(english='O sections', german='Hohlprofile')
    pieces = Translation(english='pieces', german='Strecken')
    parameters = Translation(english='parameters', german='Parameter')
    points = Translation(english='points', german='Punkte')
    points_coordinates = Translation(english='points coordinates', german='Koordinaten der Punkten')
    points_import_Excel: Translation = Translation(english='Excel import')
    points_export_Excel: Translation = Translation(english='Excel export')
    point_loads = Translation(english='point-loads', german='Punktlasten')
    profile_with_parameters = Translation(english='profile \nwith \nparameters', german='Profile \nmit \nParameters')
    pick_up_the_point = Translation(english='pick up the point ->', german='den Punkt wählen ->')
    pick_up_lines = Translation(english='pick up lines', german='wähle Linien')
    plus_a_new_section = Translation(english='+ a new section', german='+ einen Punkt')
    plus_one_point = Translation(english='+ one point', german='+ einen Punkt')
    plus_a_span = Translation(english='+ a span', german='+ ein Feld')
    plus_one_line_table = Translation(english='+ one line, table', german='+ eine Linie, Tabelle')
    plus_one_load = Translation(english='+ one load', german='+ eine Last')
    plus_one_group = Translation(english='plus one group', german='+ eine Gruppe')
    plus_one_boundary = Translation(english='plus  one boundary conditions', german='plus eine Randbedingung')
    plus_one_section = Translation(english='plus one section', german='+ einen Querschnitt')
    plus_lines_mouse = Translation(english='+ lines with mouse', german='+ Linien mit Maus')
    plus_polylines_mouse = Translation(english='+ polylines with mouse', german='+ Polylinien mit Maus')
    point = Translation(english='point', german='Punkt')
    point_comment = Translation(english='points comment', german='Punktskommentar')
    point_id = Translation(english='points id', german='id Punktes')
    reaction = Translation(english='reactions', german='Lagerreaktionen')
    reaction_moment = Translation(english='reactions moment', german='Momentreaktionen')
    result_for_beam = Translation(english='result for beams', german='Resultat für Stäbe')
    rolled_section = Translation(english='rolled section', german='gewalzte Profile')
    rotate = Translation(english='rotate', german='umkehren')
    rotate_around_axis = Translation(english='rotate around axis', german='drehen um die Achse')
    rotate_around_point = Translation(english='around the point ', german='drehen um den Punkt')
    rectangular = Translation(english='rectangular', german='rechteckig ')
    result = Translation(english='result', german='Resultat')
    save_file = Translation(english='Save', german='Speichern')
    save_file_as = Translation(english='Save as', german='Speichern wie')
    section = Translation(english='Section', german='Querschnitten')
    shear_forge_y = Translation(english='shear forge, y', german='Querkraft, y')
    shear_forge_z = Translation(english='shear forge, z', german='Querkraft, z')
    scale = Translation(english='scale', german='Maßstab')
    scale_of_displacement = Translation(english='scale of displacement', german='Verformungsmaßstab')
    sections_with_color = Translation(english='sections with color', german='Querschnitten mit Farben')
    show = Translation(english='show', german='zeige')
    show_displacement = Translation(english='show displacement', german='zeige Verformung')
    show_only = Translation(english='show only -', german='zeige nur -')
    show_only_point_loads = Translation(english='show only point loads', german='zeige nur Punkt')
    show_reactions = Translation(english='show reactions', german='zeige Lagerreaktionen')
    show_result = Translation(english='show the result', german='zeige das Resultat')
    show_all = Translation(english='show all', german='zeige alles')
    size_of_elements = Translation(english='size of elements, m', german='Elementsgröße, m')
    size_of_joints = Translation(english='size of joints, m =', german='Gelenksgröße, m =')
    snow = Translation(english='snow', german='Schnee')
    show_elements = Translation(english='show elements', german='zeige Elemente')
    steel = Translation(english='steel', german='Stahl')
    span = Translation(english='span', german='Feld')
    square = Translation(english='square', german='quadratisch')
    value = Translation(english='value', german='Value')
    type_ = Translation(english='type', german='Typ')
    type_of = Translation(english='type of', german='Art')
    too_few_points = Translation(english='too few points', german='zu wenig Punkten')
    torsion = Translation(english='torsion', german='Torsion')
    tolerance = Translation(english='tolerance, m =', german='Toleranz, m =')
    there_is_no_point_nr = Translation(english='there is no point Nr', german='Es gibt keinen Punkt Nr.')
    the_number_is_too_big = Translation(english='the number is too big', german='die Zahl ist zu gross')
    intensity = Translation(english='intensity, kN/m', german='Intensität, kN/m')
    type_of_projection = Translation(english='projection', german='Projektion')
    u_sections = Translation(english='U sections', german='U Profile')
    welded_profile = Translation(english='welded profile', german='geschweißte Profile')
    wind = Translation(english='wind', german='Wind')
    wood = Translation(english='wood', german='Holz')



@dataclass
class Material:
    concrete = 'concrete'
    steel = 'steel'
    concrete_class = ('C12/15', 'C16/20', 'C20/25', 'C25/30', 'C30/37', 'C35/45', 'C40/50', 'C45/55', 'C50/60',
                      'C55/67', 'C60/75', 'C70/85', 'C80/95', 'C90/105')
    concrete_e_modul = {'C12/15': 27000, 'C16/20': 29000, 'C20/25': 30000, 'C25/30': 31000, 'C30/37': 33000,  # N/mm2
                        'C35/45': 34000, 'C40/50': 35000, 'C45/55': 36000, 'C50/60': 37000, 'C55/67': 38000,
                        'C60/75': 39000, 'C70/85': 41000, 'C80/95': 42000, 'C90/105': 44000}

    steel_class = ('S235', 'S275', 'S355', 'S420', 'S460')

    wood_class = ('C14', 'C16', 'C18', 'C20', 'C22', 'C24', 'C27', 'C30', 'C35', 'C40', 'C45', 'C50',
                  'D30', 'D35', 'D40', 'D50', 'D60', 'D70',
                  'GL24h', 'GL24c', 'GL28h', 'GL28c', 'GL30h', 'GL30c', 'GL32h', 'GL32c')

    D = (6, 8, 10, 12, 14, 16, 20, 25, 28, 32, 40)

