#!/usr/bin/env python3
# -*- coding: utf-8; mode: xub -*-
# HEREHEREHERE

#############################################################################
#
#  /home/git/clones/external/SAS_3DSpectrographs/py/gratingequation.py
# ;  read-quoted-char-radix
#emacs helpers
# (insert (format "\n# " (buffer-file-name)))
#
# (set-input-method 'TeX' t)
# (toggle-input-method)
# (ediff-current-file)
# (wg-python-fix-pdbrc)
# (find-file-other-frame "./.pdbrc")
# (wg-python-fix-pdbrc)   # PDB DASH DEBUG end-comments
#
# (setq mypdbcmd (concat (buffer-file-name) "<args...>"))
# (progn (wg-python-fix-pdbrc) (pdb mypdbcmd))
#
# (wg-astroconda-pdb)       # IRAF27
# (wg-astroconda3-pdb)      # CONDA Python3
#
# (set-background-color "light blue")
# (wg-python-toc)
#
#  conda install jupyterlab
#  conda install -c conda-forge voila
#  conda install nodejs
#  jupyter labextension install @jupyter-widgets/jupyterlab-manager
#
#  M-x set-input-mode RET TeX  (then toggle-input-mode )
#
# (wg-python-toc)
#
#
# __doc__ = """
#
# __author__  = 'Wayne Green'
#
# __version__ = '0.1'
#
# class GratingException(Exception):
#    def __init__(self,message,errors=None):
#    @staticmethod
#    def __format__(e):
#
# class Grating:  # Grating(object) if inherited
#    def __init__(self,alpha : "degrees",              # Grating::__init__()
#    def setalpha(self,newalpha: "degrees"):           # Grating::setalpha()
#    def setmode(self,newmode: "integer"):             # Grating::setmode()
#    def setgrating(self,linesmm:float):               # Grating::setgrating()
#    def setsize(self,length:float ,width:float):      # Grating::setsize()
#    def setblaze(self,blaze: float):                  # Grating::setblaze()
#    def setlmm(self,lmm: float):                      # Grating::setlmm()
#    def difftable(self,df: pd.DataFrame, key: str):   # Grating::difftable()
#    def debug(self,msg="",os=sys.stderr):             # Grating::debug()
#    def grating_quation(self, waverange,step = 0) -> 'radians':             # Grating::grating_quation()
#    def report(self):                                 # Grating::report()
#    def csv(self,fname: 'string'):                    # Grating::csv()
#    def groovedepth(self):                            # Grating::groovedepth()
#    def startplot(self):                              # Grating::startplot
#    def plot(self,keys=[]):                           # Grating::plot
#    def littrow_equation(self,α):                     # Grating.littrow_equation()
#    def peakAngle(self,λ: "angstroms" ):              # Grating::peakAngle()
#    def phi(self,λ : "angstroms") -> 'degrees':       # Grating::phi()
#
# if __name__ == "__main__":
#
#
#
#
#############################################################################
import optparse
import re
import sys
import numpy  as np
import pandas as pd
from numpy import sin,cos,arcsin,arccos,radians,degrees

import matplotlib.pyplot as plt

# (wg-python-graphics)
__doc__ = """

gratingequation.py   [options]

options:

-p, --plot           make a Matplotlib plot
-r, --report         make a 'report' to stdout
-c, --csv <pathname> produce a CSV file to path/file name.

This is a basic stand-alone program that is a useful regression
testbed for the Grating class. It permits playing with grating
equations. The idea is to collect attributes of the grating and
provide a set of equations and other functions to compute values for a
grating design. It will produce plots and tables.

Again, this is a regression test for the Grating class. It shows
some of the features (OK I was lazy and did not fully regression
test!). Use it as you will.

Tony Rodda's favorite grating web site:
https://www.spectrogon.com/product-services/gratings/grating-design-tool/

handy notes about Pandas
https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf

"""

__copyright__ = """Copyright 2020 Wayne Green.

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Open Source Initiative Approved License: MIT 
"""


__author__  = 'Wayne Green'
__version__ = '0.1'

_all__      = ['GratingException','Grating']   # expose these things


##############################################################################
# GratingException
#
##############################################################################
class GratingException(Exception):
   """Special exception to allow differentiated capture of exceptions"""
   def __init__(self,message,errors=None):
      super(GratingException,self).__init__("Grating "+ message)
      self.errors = errors
   @staticmethod
   def __format__(e):
      return "Grating" % e
# GratingException

##############################################################################
# Grating
#
##############################################################################
class Grating:  # Grating(object) if inherited
   """ Permit more than one instance per run.
       ALL units in centimeters. 5000 angstroms is 5e-5 cm.
       Gratings are lines per cm
       Mode is integer (signed)
       blaze is stated in degrees (per manufacture's data, we convert to radians)
   """

   #   https://en.jeulin.fr/simple-radial-slits-212076.html
   ovioslits_cm = np.array([10.0, 20.0, 30.0, 40.0, 50.0, 70.0, 100.0,
                     150.0, 200.0, 300.0, 500.0, 700.0])/10000.0 # in cm


   latex1       = """\\frac{m\\lambda}{d} &= sin(\\alpha) + sin(\\beta)"""
   print1       = "mλ/d = sin(β) + sin(α)"       # print a basic equation (unicode to rescue)
   specrange    = np.arange(3300, 8000, 100)     # units: angstroms every 10nm useful default range

   def __init__(self,alpha : "degrees",              # Grating::__init__()
                     m     : "Mode [integer]",
                     lmm   : "lines per mm",
                     blaze : "degrees",
                     slit  : "microns",
                     length: "mm" = 25,
                     width : "mm" = 25):
      """Describe the grating in conventional terms, we use CM and angstroms
      as our basis.

      Key traits of a Grating:
         alpha      rotation of grating w.r.t. grating normal
         m          mode
         d          count of lines per mm
         blaze      The blaze angle for this grating
         length     length of the physical grating surface
         width      width of the physical grating surface

      Developed internally to each instance
         wave       the wavelength range per call, reflect the last one
         dispersion accumulate data for different settings
         df         Pandas dataframe to accumulate/manage data. Key is alpha+mode+lmm

      """
      #super(base,self).__init__()
      #self.
      self.alpha      = alpha               # rotation of grating w.r.t. grating normal
      self.m          = m                   # mode
      self.lmm        = float(lmm)          # remember lines per mm
      self.d          = 1.0/(self.lmm * 10) # inverse count of lines per mm
      self.blaze      = blaze               # The blaze angle for this grating
      self.length     = length              # length of the physical grating surface
      self.width      = width               # width of the physical grating surface
      self.wave       = []                  # the wavelength range per call, reflect the last one
      self.dispersion = {}                  # accumulate data for different settings
      self.df         = None                # manage data as a Pandas dataframe
      self.notes      = []                  # strings of user notes
      self._fig       = None                # plot figure.

   ### Grating.__init__()

   def setalpha(self,newalpha: "degrees"):           # Grating::setalpha()
      """Update alpha for another go."""
      self.alpha = newalpha

      return self

   ### Grating.setalpha()

   def setmode(self,newmode: "integer"):             # Grating::setmode()
      """Set the new mode"""
      self.m = newmode

      return self

   ### Grating.setmode()

   def setgrating(self,linesmm:float):               # Grating::setgrating()
      """Set the d = lines/mm"""
      self.d = float(linesmm)

      return self

   ### Grating.setgrating()

   def setsize(self,length:float ,width:float):      # Grating::setsize()
      """Set the length/width of physical grating"""
      self.length = length
      self.width  = width

      return self

   ### Grating.setsize()

   def setblaze(self,blaze: float):                  # Grating::setblaze()
      """Set the blaze width"""
      self.blaze = float(blaze)

      return self

   ### Grating.setblaze()

   def setlmm(self,lmm: float):                      # Grating::setlmm()
      """Set the lines/mm and remember to update d"""
      self.lmm = float(lmm)
      self.d          = 1.0/(self.lmm * 10) # inverse count of lines per mm

      return self

   ### Grating.setlmm()

   def difftable(self,df: pd.DataFrame, key: str):   # Grating::difftable()
      """Report forward differences on a column. The column is a 'key'
      comprised of alpha and mode"""
      col    = degrees(df[key].values)        # get the angles in radians
      fdiff  = col[1:] - col[:-1]    # first forward diff using np
      ratios = fdiff[1:]/fdiff[:-1]  # reduce scale.
      tmp    = pd.DataFrame({'Diff' : fdiff[1:], 'Ratio' : ratios}, index=self.wave[1:-1]*1e8)
      print(tmp)

      return self

   ### Grating.difftable()

   def debug(self,msg="",os=sys.stderr):             # Grating::debug()
      """Help with momentary debugging, file to fit."""
      print("Grating - %s " % msg, file=os)
      for key,value in self.__dict__.items():
         if(key[0] != '_'):
            print("%20s = %s" % (key,value),file=os)

      return self

   ### Grating.debug()

   __Grating_debug = debug  # preserve our debug name if we're inherited

   def grating_quation(self, waverange = None,step = 0) -> 'radians':             # Grating::grating_quation()
      """Return β from applying the grating equation to a numpy array of wavelengths
      (cm), given the conditions that are held constant of this class.
      """
      np.seterr(invalid='ignore')  # asking for a broad range, sin will blow up.
      if(waverange is None):
         waverange = self.specrange                       # provide a decent default visual span
      m               = float(self.m)
      self.wave       = waverange / 1.e8                  # convert to cm
      sinalpha        = sin(radians(self.alpha))          # constant
      sinb            = m * (self.wave / self.d) + sinalpha    # spread out to watch.
      β               = arcsin(sinb)                      # beta
      key             = """α={:5.2f}, m={:2d} lmm={:d}""".format(self.alpha,self.m,int(self.lmm))
      self.dispersion[key] = degrees(β)                   # save 'last' result
      np.seterr(invalid=None)       # reset for other parts of the code.

      return β

   ### Grating.grating_quation()

   def report(self):                                 # Grating::report()
      """Create a pandas df, make a report by wavelength."""
      if(self.dispersion != []):
         pd.set_option('display.max_rows', None)
         pd.set_option('display.max_columns', None)
         pd.set_option('display.width', None)
         pd.set_option('display.max_colwidth', -1)
         df = pd.DataFrame(self.dispersion,index=self.wave*1e8)
         print(df.round(3))
         for k in self.dispersion.keys():
            print("\n",k)
            self.difftable(df,k)

      return self

   ### Grating.report()

   def csv(self,fname: 'string'):                    # Grating::csv()
      """Create a pandas df, make a csv by wavelength."""
      if(self.dispersion != []):
         df = pd.DataFrame(self.dispersion,index=self.wave*1e8)
         df.to_csv(fname)
         print("made csv",fname)

      return self

   ### Grating.csv()

   def groovedepth(self):                            # Grating::groovedepth()
      """Return the optimum groove depth"""
      return self.d*cos(self.blaze)*sin(self.blaze)

   ### Grating.groovedepth

   def startplot(self):                              # Grating::startplot
      """Initialize the plot as needed. The member _fig allows
      external access, and retains the state between calls."""
      if(self._fig == None):
         self._fig   = plt.figure()                                  # init a figure and axis
         self.ax     = _fig.add_subplot(111, projection='polar')      # overplot axis
         self.ax.set_thetamin(90)                                     # display quads I and II
         self.ax.set_thetamax(-90)
      return self

   ### Grating.startplot

   def plot(self,keys=[]):                           # Grating::plot
      """Make a polar bar chart showing order overlap"""
      rad    = 0.5                                           # set a basic radius for first set, 
      leg    = []                                            # and a legend.
      if(len(keys) == 0):
         keys = self.dispersion.keys()                       # all or specific one
      self.startplot()                                       # start/reuse any plot figure this instance

      for k in keys:                                         # for requested key(s)
         if(k in self.dispersion):
            leg.append(k)
            try:
               data     = self.dispersion[k]                 # angle is β ...
               theta    = radians(data)                      # ... to radians
               r        = np.full_like(data,rad)             # constant radius
               area     = 100                                # decent size on plot
               nans     = np.argwhere(np.isnan(theta))       # just go to first one
               badlist  = list(nans.reshape(nans.shape[0]))  # numpy.array
               if(0): print("Bad color locations:", nans)
               colors   = 1.0 - (theta/max(theta))           # self-normalize the data
               #for w in nans:
               #   colors[w[0]] = 0.0  # 
               ax.set_rlabel_position(-22.5)                 # bend numbers out of way
               if(len(nans) != 0):
                  firstbad = badlist[0]
                  theta    = theta[:firstbad]                # to leave out the NaNs
                  r        = r[:firstbad]
                  colors   = colors[:firstbad]               # don't use array of colors for bad
               ignore = ax.scatter(theta, r, c=colors, s=area, cmap='Spectral', alpha=0.75, label=k)
               line   = np.linspace(0,rad+.1,30)   # PDB-DEBUG
               ltheta = np.full_like(line,theta[0])
               ignore = ax.plot(ltheta,line,color='black',linewidth=2)
               txt = k
               ignore = ax.text(ltheta[-1],line[-1]+.1,txt)
               rad    = rad + .2                 # boost radius for next set
            except Exception as e:
               datalen = data.shape[0]
               print(f'Oops array size: {datalen}',file=sys.stderr)
               raise

      plt.legend(markerscale=-.1,bbox_to_anchor=(0.301,1.05)) # bbox hacks position
      plt.title("{:d} l/mm, {:7.1f} :{:7.1f} Å, φ={:5.2f}".format(int(self.lmm), 
            1e8*min(self.wave), 1e8*max(self.wave), self.blaze))
      plt.show()

      return self

   ### Grating.plot()

   def littrow_equation(self,α):                     # Grating.littrow_equation()
      """ In the Littrow condition, α=β. The equation reduces
      to m λ = d sin(β)"""
      pass

   ### Grating.littrow_equation()

   def peakAngle(self,λ: "angstroms" ):              # Grating::peakAngle()
      """Return β given a wavelength in cm"""
      λ = λ * 1e-8                               # convert to cm
      β = self.d/(m * λ)

      return β

   ### Grating.peakAngle()

   def phi(self,λ : "angstroms") -> 'degrees':       # Grating::phi()
      """With the existing m, d calculate φ (blaze)
         φ = arcsin (\frac{mλ}{d})
      """
      l   = λ * 1e-8                     # rememeber, any nuber in radians will
      φ = ( self.m * l) / self.d         # convert to some degree!

      return degrees(φ)

   ### Grating.phi()
         
# class Grating

##############################################################################
#                                    Main
#                               Regression Tests
##############################################################################
# HEREHEREHERE
if __name__ == "__main__":
   opts = optparse.OptionParser(usage="%prog "+__doc__)

#import optparse


   opts = optparse.OptionParser(usage="%prog"+__doc__)

   opts.add_option("-c", "--csv",    action="store", dest="csvflag",
                   default=None,
                   help="<str|None>    provide pathname for a csvfile")

   opts.add_option("-p", "--plot",    action="store_true", dest="plotflag",
                   default=False,
                   help="<bool>    ask for a plot")

   opts.add_option("-r", "--report",    action="store_true", dest="reportflag",
                   default=False,
                   help="<bool>    ask for a report")

   opts.add_option("-v", "--verbose", action="store_true", dest="verboseflag",
                   default=False,
                   help="<bool>     be verbose about work.")

   (options, args) = opts.parse_args()


   specrange = np.arange(3300, 8000, 100)     # units: angstroms every 10nm

   if(0):  # example of one grating three incidence angles
      g = Grating(45.0, 1, 300, 3.5, 25)
      g.grating_quation(specrange)                         # populate/save first settings
      g.setmode(2).grating_quation(specrange)              # set mode up
      g.setalpha(15).setmode(1).grating_quation(specrange) # change alpha mode 1,2
      g.setalpha(15).setmode(2).grating_quation(specrange)
      g.setalpha(10).setmode(1).grating_quation(specrange) # change alpha mode 1,2
      g.setalpha(10).setmode(2).grating_quation(specrange)
      if(options.reportflag):
         g.report()                                        # make a report
      if(options.plotflag):
         g.plot()                                          # show a plot

   if(1):
      α = -45.0
      g = Grating(α, 1, 300, 3.5, 25)
      g.grating_quation(specrange)
      g.setlmm(600).grating_quation(specrange)
      g.setlmm(1200).grating_quation(specrange)
      g.setlmm(1800).grating_quation(specrange)
      g.setlmm(2400).grating_quation(specrange)
      if(options.reportflag):
         g.report()                                        # make a report
      if(options.plotflag):
         g.plot()                                          # show a plot
      if(options.csvflag is not None):
         g.csv(options.csvflag)
      

