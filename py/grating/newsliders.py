#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# HEREHEREHERE

#############################################################################
#
#  /home/git/clones/external/SAS_3DSpectrographs/py/grating/newsliders.py
#
#emacs helpers
# (insert (format "\n# %s " (buffer-file-name)))
#
# (set-input-method 'TeX' t)
# (toggle-input-method)
#
# α
# β
# λ
# ω
# θ
# Å
# µ
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
# (wg-python-graphics)
__doc__ = """

/home/git/clones/external/SAS_3DSpectrographs/py/grating/newsliders.py
[options] files...

This is a test demo:
1) TeX toggle-input-method mode for unicode works  the characters are OK
2) The API follows other's mistakes:
   A dropdown is a "button" The handeler takes an "event" and the event.item
   has the results.
Row spacing is OK 


"""


__author__  = 'Wayne Green'
__version__ = '0.1'
__all__     = []   # list of quoted items to export
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
import optparse
import re
import sys

import numpy as np
from bokeh.models.callbacks import CustomJS
from bokeh.events import ButtonClick
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import Button, ColumnDataSource, Dropdown, FileInput
from bokeh.models import Slider, Spinner, TextInput
from bokeh.models.widgets import Div
from bokeh.plotting import figure

# (wg-python-graphics)
__doc__ = """

/home/git/clones/external/SAS_3DSpectrographs/py/grating/sliders.py
[options] files...

bokeh serve ./sliders.py 
at your command prompt. Then navigate to the URL

    http://localhost:5006/sliders

in your browser.

"""

__author__  = 'Wayne Green'
__version__ = '0.1'
__all__     = []   # list of quoted items to export



#bk_FL_Colliminator.value
#bk_FL_Camera.value
#bk_SlitWidth.value
#bk_Range_Start.value
#bk_Range_End.value
#button_quit.value
#bk_Grating.value
##############################################################################
# Callback (placeholders)
#
##############################################################################
def bk_Mode_on_change(attr, old, new):
    the_mode            = bk_Mode.value
    print(f"the_mode = {the_mode}") # ,file=log)

# bk_Mode

def bk_lmm_on_change(attr, old, new):
    the_lmm             = bk_lmm.value
    print(f"the_lmm {the_lmm}") # ,file=log)

# bk_lmm_on_change

def bk_alpha_on_change(attr, old, new):
    the_alpha           = bk_alpha.value
    print(f"the_alpha {the_alpha}") # ,file=log)

# bk_alpha_on_change

def bk_beta_on_change(attr, old, new):
    the_beta            = bk_beta.value
    print(f"the_beta {the_beta}") # ,file=log)

# bk_beta_on_change

def bk_FL_Colliminator_on_change(attr, old, new):
    the_fl_colliminator = bk_FL_Colliminator.value
    print(f"the_fl_colliminator {the_fl_colliminator}")

# bk_FL_Colliminator_on_change

def bk_FL_Camera_on_change(attr, old, new):
    the_fl_camera       = bk_FL_Camera.value
    print(f"the_fl_camera {the_fl_camera}")

# bk_FL_Camera_on_change

def bk_SlitWidth_on_change(attr, old, new):
    the_slitwidth       = bk_SlitWidth.value
    print(f"the_slitwidth {the_slitwidth}")

# bk_SlitWidth_on_change

def bk_Range_Start_on_change(attr, old, new):
    the_range_start     =  bk_Range_Start.value
    print(f"the_range_start {the_range_start}")

# bk_Range_Start_on_change

def bk_Range_End_on_change(attr, old, new):
    the_bk_range_end    = bk_Range_End.value
    print(f"the_bk_range_end {the_bk_range_end}")

# bk_Range_End_on_change

def bk_Grating_on_change(event):
    print("Grating called...")
    the_bk_Grating      = event.item
    print(f"the_bk_Grating {the_bk_Grating}")

# bk_Grating_on_change

def pass_on_change(attr, old, new):
    print("PASS ON CHANGE Called.")


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

def quitbutton():
    sys.exit(0)

# def update_data

def update_title(attrname, old, new):
    plot.title.text = text.value
# def update_title

# Set up data
N      = 200
x      = np.linspace(0, 4*np.pi, N)
y      = np.sin(x)
source = ColumnDataSource(data=dict(x=x, y=y))

# make a log area -- doesn't work
logdiv = Div(text="A log Message", style={ 'overflow-y'       : 'scroll',
                                        'background-color' : 'lightyellow',
                                        'height'           : '400px',
                                        'width'            : '400px'
                                      })

# Set up plot
plot = figure(plot_height=400, plot_width=400, title="my sine wave",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[0, 4*np.pi], y_range=[-2.5, 2.5])

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

#                    Grating Name       JSON Blaze
#                    (arbitrary)
grating_choices = [ ("150",          "'lmm' : 150,  'blaze' : 4.0"), 
                    ("300  Blue",    "'lmm' : 300,  'blaze' : 3.5"),
                    ("300  Green",   "'lmm' : 300,  'blaze' : 3.5"),
                    ("300  Red ",    "'lmm' : 300,  'blaze' : 3.5"),
                    ("600  Blue",    "'lmm' : 600,  'blaze' : 3.5"),
                    ("600  Green",   "'lmm' : 600,  'blaze' : 3.5"),
                    ("600  Red ",    "'lmm' : 600,  'blaze' : 3.5"),
                    ("1200 Blue",    "'lmm' : 1200, 'blaze' : 3.5"),
                    ("1200 Green",   "'lmm' : 1200, 'blaze' : 3.5"),
                    ("1200 Red ",    "'lmm' : 1200, 'blaze' : 3.5"),
                    ("2400 Blue",    "'lmm' : 2400, 'blaze' : 3.5"),
                    ("2400 Green",   "'lmm' : 2400, 'blaze' : 3.5"),
                    ("2400 Red ",    "'lmm' : 2400, 'blaze' : 3.5")
                  ]

bk_Mode             = Spinner(title="Mode [int]",name="Mode", mode='int', low=-5, high=5, step=1, value=1)
bk_Mode.js_on_event("menu_item_click", CustomJS(code="console.log('spinner: ' + this.item, this.toString())"))

bk_lmm              = TextInput(title="lmm            [mm]",      value="")  # no initial value
bk_alpha            = TextInput(title="α              [degrees]", value="")
bk_beta             = TextInput(title="β              [degrees]", value="")
bk_FL_Colliminator  = TextInput(title="FL Coliminator [mm]",      value="")
bk_FL_Camera        = TextInput(title="FL Camera      [mm]",      value="")
bk_SlitWidth        = TextInput(title="Slit Width     [µm]",      value="")
bk_Range_Start      = TextInput(title="From           [Å]",       value="")
bk_Range_End        = TextInput(title="To             [Å]",       value="")
button_quit         = Button(label="Quit", disabled=False)

bk_Grating          = Dropdown(label="Gratings",  menu=grating_choices, button_type="primary")
#bk_Grating.js_on_event("menu_item_click", CustomJS(code="console.log('dropdown: ' + this.item, this.toString())"))


# Set up callbacks

bk_Mode            .on_change('value', bk_Mode_on_change )
bk_lmm             .on_change('value', bk_lmm_on_change )
bk_lmm             .on_change('value', bk_lmm_on_change )
bk_alpha           .on_change('value', bk_alpha_on_change )
bk_beta            .on_change('value', bk_beta_on_change )
bk_FL_Colliminator .on_change('value', bk_FL_Colliminator_on_change ) 
bk_FL_Camera       .on_change('value', bk_FL_Camera_on_change )
bk_SlitWidth       .on_change('value', bk_SlitWidth_on_change ) 
bk_Range_Start     .on_change('value', bk_Range_Start_on_change )  
bk_Range_End       .on_change('value', bk_Range_End_on_change ) 
bk_Grating         .on_click(          bk_Grating_on_change )
button_quit        .on_event(ButtonClick, quitbutton)


# Set up layouts and add to document
inputs = column( bk_Mode,
                 bk_lmm,
                 row(bk_alpha, bk_beta,width=250),            # ROW
                 bk_FL_Colliminator,
                 bk_FL_Camera,
                 bk_SlitWidth,
                 row(bk_Range_Start, bk_Range_End,width=250), # ROW
                 bk_Grating,
                 button_quit,
                 width=250
               )

curdoc().add_root(row(inputs, 
                      column(plot),
                      width=800)) 

curdoc().title = "New Sliders"

