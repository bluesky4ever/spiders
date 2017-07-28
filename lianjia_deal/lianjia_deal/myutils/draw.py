
from pyecharts import Line

class Draw(object):
    item_collection = []

    def __init__(self, item_collection):
        self.item_collection = item_collection[:]
    
    def draw_line(self, figure_name):
        x_axis = []
        points = []
        for i in self.item_collection:
            x_axis.append(i['dealDate'][0])
            points.append(i['unitPrice'][0])

        line = Line(figure_name)
        line.add(figure_name, x_axis, points)
        line.show_config()
        line.render(figure_name + '.html')