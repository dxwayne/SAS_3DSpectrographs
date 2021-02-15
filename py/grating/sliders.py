#!/home/wayne/anaconda3/bin/bokeh serve
# -*- coding: utf-8 -*-
# HEREHEREHERE

#############################################################################
#
#  /home/git/clones/external/SAS_3DSpectrographs/py/grating/sliders.py
#
#emacs helpers
# (insert (format "\n# %s " (buffer-file-name)))
#
# (set-input-method 'TeX' t)
# (toggle-input-method)
#
# (wg-astroconda3-pdb)      # CONDA Python3
#
# (wg-python-fix-pdbrc)  # PDB DASH DEBUG end-comments
#
# (ediff-current-file)
# (find-file-other-frame "./.pdbrc")

# (setq mypdbcmd (concat (buffer-file-name) "<args...>"))
# (progn (wg-python-fix-pdbrc) (pdb mypdbcmd))
#
# (wg-astroconda-pdb)       # IRAF27
#
# (set-background-color "light blue")
#
# (wg-python-toc)
#
#############################################################################
from __future__ import annotations
import optparse
import re
import sys

''' 
at your command prompt. Then navigate to the URL

    http://localhost:5006/sliders

in your browser.

'''
import numpy as np

from bokeh.events import ButtonClick
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, TextInput, Button
from bokeh.plotting import figure

# (wg-python-graphics)
__doc__ = """

/home/git/clones/external/SAS_3DSpectrographs/py/grating/sliders.py
[options] files...


"""

__author__  = 'Wayne Green'
__version__ = '0.1'
__all__     = []   # list of quoted items to export

##############################################################################
# update_data
#
##############################################################################
def update_data(attrname, old, new):

    # Get the current slider values
    a = amplitude.value
    b = offset.value
    w = phase.value
    k = freq.value

    # Generate the new curve
    x = np.linspace(0, 4*np.pi, N)
    y = a*np.sin(k*x + w) + b

    source.data = dict(x=x, y=y)

def quitbutton():
    sys.exit(0)

# def update_data


# Set up data
N      = 200
x      = np.linspace(0, 4*np.pi, N)
y      = np.sin(x)
source = ColumnDataSource(data=dict(x=x, y=y))


# Set up plot
plot = figure(plot_height=400, plot_width=400, title="my sine wave",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[0, 4*np.pi], y_range=[-2.5, 2.5])

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)


# Set up widgets
text        = TextInput(title="title", value='my sine wave')
offset      = Slider(title="offset", value=0.0, start=-5.0, end=5.0, step=0.1)
amplitude   = Slider(title="amplitude", value=1.0, start=-5.0, end=5.0, step=0.1)
phase       = Slider(title="phase", value=0.0, start=0.0, end=2*np.pi)
freq        = Slider(title="frequency", value=1.0, start=0.1, end=5.1, step=0.1)
button_quit = Button(label="Quit", disabled=False)

# Set up callbacks
def update_title(attrname, old, new):
    plot.title.text = text.value

text.on_change('value', update_title)

for w in [offset, amplitude, phase, freq]:
    w.on_change('value', update_data)

button_quit.on_event(ButtonClick, quitbutton)
latex = LatexLabel(text="f = \sum_{n=1}^\infty\\frac{-e^{i\pi}}{2^n}!",
                   x=40, y=420, x_units='screen', y_units='screen',
                   render_mode='css', text_font_size='16pt',
                   background_fill_alpha=0)


# Set up layouts and add to document
inputs = column(text, offset, amplitude, phase, freq, button_quit)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Sliders"

