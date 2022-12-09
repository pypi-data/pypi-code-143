"""
This file contains the Plotter class.
The plotting methods take a single FileData instance as argument.
To use them with a DataSet instance, use the DataSet.map method.
"""

from matplotlib import pyplot as plt
import matplotlib as mpl

class Plotter:
    nth_plot = 0

    @staticmethod
    def set_theme():
        mpl.rcParams["mathtext.fontset"] = "cm"
        plt.rcParams["font.family"] = "serif"
        plt.rcParams["figure.autolayout"] = True
        mpl.rcParams.update({'font.size': 22})
    
    @classmethod
    def start_session(cls):
        cls.set_theme()
        cls.nth_plot = 0

    @staticmethod
    def end_session():
        plt.show()

    @classmethod
    def new_plot(cls, xlabel, ylabel, title, size=(9, 7)):
        cls.nth_plot += 1
        fig = plt.figure(cls.nth_plot, figsize=size)
        fig.suptitle(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)

    @classmethod
    def scatter(cls, x, y, legend=None, *args, **kwargs):
        def _scatter(file_data):
            plt.scatter(
                file_data.data[x], 
                file_data.data[y], 
                label=legend.format(**file_data.context) if legend else None,
                *args, 
                **kwargs
            )
            if legend:
                plt.legend(loc="best")
        return _scatter