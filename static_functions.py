from scipy import interpolate

from small_classes import XY


def make_spline(x_points: [], y_points: [], list_of_new_x: [float]) -> [XY]:
    spline = interpolate.splrep(x_points, y_points)
    spline_line: [XY] = []
    for x in list_of_new_x:
        y: float = interpolate.splev(x, spline)
        spline_line.append(XY(x=x, y=y, i=0))
    return spline_line
