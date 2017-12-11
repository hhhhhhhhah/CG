#!/usr/bin/env python
import numpy
import matplotlib.pyplot as plt

class polyplot:
    def __init__(self, figure_size_inches=(8,8), dpi=None):
        self.points = []
        self.fig = plt.figure(figsize=figure_size_inches, dpi=dpi)
        self.ax = self.fig.add_subplot(1, 1, 1)

    def add_point(self, xy_point):
        self.points.append(numpy.asarray(xy_point))

    def set_points(self, points):
        self.points = points

    def add_points(self, points):
        self.points = numpy.concatenate((self.points, points), axis=0)

    def plot_all_to_all(self, line_color='black', line_width=2,
            line_style='solid',
            plot_points=False, points_style='wo',
            show_axes=False, exceptions=[]):
        self.points = numpy.asarray(self.points)
        for i in range(self.points.shape[0]):
            for j in range(self.points.shape[0]):
                if (i != j and
                        ([i,j] in exceptions) == False and
                        ([j,i] in exceptions) == False):
                    plt.plot([self.points[i,0], self.points[j,0]],
                            [self.points[i,1], self.points[j,1]],
                            color=line_color, linestyle=line_style,
                            linewidth=line_width)
        if plot_points == True:
            plt.plot(self.points[:,0], self.points[:,1], points_style)
        plt.axis('equal')
        if show_axes == False:
            plt.axis('off')

    def plot_circle(self, coord, radius, color='black'):
        circ = plt.Circle(coord, radius=radius, color=color)
        self.ax.add_patch(circ)

    def save_plot(self, image_name='all_to_all', image_format='png',
            background_color='white',
            transparent_background=False):
        if transparent_background == True:
            self.fig.savefig(image_name + '.' + image_format,
                    transparent=True)
        else:
            self.fig.savefig(image_name + '.' + image_format,
                    facecolor=background_color, transparent=False)
        self.fig.clf()


class regular_star_polygon:
    def __init__(self, n=5, radius=1.0):

        if n < 3:
            raise Exception('regular_star_polygon: Error, this function ' +
            'doesn\'t work with n < 3.')

        self.n = n
        self.generate_regular_star_polygon(radius=radius)

    def generate_regular_star_polygon(self, radius=1.0):
        self.points = numpy.empty((self.n, 2))

        for i in range(self.n):
            theta = i*(2.0*numpy.pi/self.n)
            x = radius*numpy.cos(theta)
            y = radius*numpy.sin(theta)
            self.points[i,0] = x
            self.points[i,1] = y