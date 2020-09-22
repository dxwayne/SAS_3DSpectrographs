#!/usr/bin/env python3
# -*- coding: utf-8  -*-
#
# HEREHEREHERE

#############################################################################
# 
#  /home/git/clones/external/SAS_3DSpectrographs/py/prism.py
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
import optparse
import re
import sys
# (wg-python-graphics)
__doc__ = """

/home/git/clones/external/SAS_3DSpectrographs/py/prism.py
[options] files...



"""


__author__  = 'Wayne Green'
__version__ = '0.1'
_all__      = [PrismException,Prism]


##############################################################################
# PrismException
#
##############################################################################
class PrismException(Exception):
   """Special exception to allow differentiated capture of exceptions"""
   def __init__(self,message,errors=None):
      super(PrismException,self).__init__("Prism "+ message)
      self.errors = errors
   @staticmethod
   def __format__(e):
      return "Prism" % e
# PrismException



##############################################################################
# Prism
#
##############################################################################
class Prism:  # Prism(object) if inherited
   """ The index of refraction varies with wavelength. Here we use the
       Sellmeir coefficents (https://refractiveindex.info/?shelf=glass&book=SF5&page=SCHOTT)
       https://refractiveindex.info/?shelf=glass&book=SF10&page=SCHOTT
       Wavelengths are input in angstroms (1e-7 converts to nm)
       Equations are from refractiveindex, and are in nm.
   """

   glass_equations = {
      'sf5'  : lambda λ: sqrt(1 + 1.52481889/(1-0.011254756/λ**2) 
                      + 0.187085527/(1-0.0588995392/λ**2)
                      + 1.42729015/(1-129.141675/λ**2)),
   
      'sf10' : lambda λ: sqrt(1 + 1.62153902/(1-0.0122241457/λ**2)
                      +0.256287842/(1-0.0595736775/λ**2) 
                      + 1.64447552/(1-147.468793/λ**2)),
   
      'bk7'  : lambda λ: sqrt(1 + 1.03961212/(1-0.00600069867/λ**2)
                      + 0.231792344/(1-0.0200179144/λ**2)
                      + 1.01046945/(1-103.560653/λ**2)),
   
      'fk10' : lambda λ: sqrt(1 + 0.971247817/(1-0.00472301995/λ**2)
                      + 0.216901417/(1-0.0153575612/λ**2)
                      + 0.904651666/(1-168.68133/λ**2))
   }

   def __init__(self,glass='sf5', apex=60.0, equation=None):    # Prism::__init__()
      """Initialize this class."""
      #super(base,self).__init__()
      #self.
      self.glass = glass
      self.apex  = apex
      if(equation is None and glass in glass_equations):
         self.equation = glass_equations(glass)
      else:
         raise PrismException(f'Unknown glass {glass}')


   ### Prism.__init__()


   def debug(self,msg="",os=sys.stderr):           # Prism::debug()
      """Help with momentary debugging, file to fit."""
      print("Prism - %s " % msg, file=os)
      for key,value in self.__dict__.items():
         print("%20s = %s" % (key,value),file=os)

      return self

   ### Prism.debug()

   __Prism_debug = debug  # preserve our debug name if we're inherited

   def __float__(self):                              # Prism::__float__()
      """What to do if used as a a float (int etc)"""

   ### Prism.__float__()

# class Prism



##############################################################################
#                                    Main
#                               Regression Tests
##############################################################################
# HEREHEREHERE
if __name__ == "__main__":
   opts = optparse.OptionParser(usage="%prog "+__doc__)

   opts.add_option("-v", "--verbose", action="store_true", dest="verboseflag",
                   default=False,
                   help="<bool>     be verbose about work.")

   (options, args) = opts.parse_args()

   #if(len(args) == 0 ): args.append(None)
   for filename in args:
      with open(filename,'r') if filename else sys.stdin as f:
         for l in f:
            if('#' in l):
               continue
            parts = map(str.strip,l.split()) 



