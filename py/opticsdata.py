#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# HEREHEREHERE

#############################################################################
# 
#  /home/wayne/iraf/smtsci/py/opticsdata.py
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
from collections import OrderedDict

# (wg-python-graphics)
__doc__ = """

/home/wayne/iraf/smtsci/py/opticsdata.py

Collect tables of weird but useful data.



"""


__author__  = 'Wayne Green'
__version__ = '0.1'
__all__     = ["fronhofer_lines"]   # list of quoted items to export


fronhofer_lines =  {
      # desig,        element,   Å
      "t"        : [  "Ni"   ,   2994.44  ],
      "T"        : [  "Fe"   ,   3021.08  ],
      "P"        : [  "Ti+"  ,   3361.12  ],
      "N"        : [  "Fe"   ,   3581.21  ],
      "L"        : [  "Fe"   ,   3820.44  ],
      "K"        : [  "Ca+"  ,   3933.66  ],
      "H"        : [  "Ca+"  ,   3968.47  ],
      "h"        : [  "Hδ"   ,   4101.75  ],
      "G"        : [  "Ca"   ,   4307.74  ],
      "G"        : [  "Fe"   ,   4307.90  ],
      "G'"       : [  "Hγ"   ,   4340.47  ],
      "e"        : [  "Fe"   ,   4383.55  ],
      "d"        : [  "Fe"   ,   4668.14  ],
      "F"        : [  "Hβ"   ,   4861.34  ],
      "c"        : [  "Fe"   ,   4957.61  ],
      "b4"       : [  "Mg"   ,   5167.33  ],
      "b3"       : [  "Fe"   ,   5168.91  ],
      "b2"       : [  "Mg"   ,   5172.70  ],
      "b1"       : [  "Mg"   ,   5183.62  ],
      "E2"       : [  "Fe"   ,   5270.39  ],
      "e"        : [  "Hg"   ,   5460.73  ],
      "D3 or d"  : [  "He"   ,   5875.618 ],
      "D2"       : [  "Na"   ,   5889.95  ],
      "D1"       : [  "Na"   ,   5895.92  ],
      "a"        : [  "O₂"   ,   6276.61  ],
      "C"        : [  "Hα"   ,   6562.81  ],
      "B"        : [  "O₂"   ,   6867.19  ],
      "A"        : [  "O₂"   ,   7593.70  ],
      "Z"        : [  "O₂"   ,   8226.96  ],
      "y"        : [  "O₂"   ,   8987.65  ]
      }

fronhofer_lines_by_wavelength = {
      # Å           desig         element
        2994.44   : [  "t"        ,  "Ni"  ],
      3021.08   : [  "T"        ,  "Fe"  ],
      3361.12   : [  "P"        ,  "Ti+" ],
      3581.21   : [  "N"        ,  "Fe"  ],
      3820.44   : [  "L"        ,  "Fe"  ],
      3933.66   : [  "K"        ,  "Ca+" ],
      3968.47   : [  "H"        ,  "Ca+" ],
      4101.75   : [  "h"        ,  "Hδ"  ],
      4307.74   : [  "G"        ,  "Ca"  ],
      4307.90   : [  "G"        ,  "Fe"  ],
      4340.47   : [  "G'"       ,  "Hγ"  ],
      4383.55   : [  "e"        ,  "Fe"  ],
      4668.14   : [  "d"        ,  "Fe"  ],
      4861.34   : [  "F"        ,  "Hβ"  ],
      4957.61   : [  "c"        ,  "Fe"  ],
      5167.33   : [  "b4"       ,  "Mg"  ],
      5168.91   : [  "b3"       ,  "Fe"  ],
      5172.70   : [  "b2"       ,  "Mg"  ],
      5183.62   : [  "b1"       ,  "Mg"  ],
      5270.39   : [  "E2"       ,  "Fe"  ],
      5460.73   : [  "e"        ,  "Hg"  ],
      5875.618  : [  "D3 or d"  ,  "He"  ],
      5889.95   : [  "D2"       ,  "Na"  ],
      5895.92   : [  "D1"       ,  "Na"  ],
      6276.61   : [  "a"        ,  "O₂"  ],
      6562.81   : [  "C"        ,  "Hα"  ],
      6867.19   : [  "B"        ,  "O₂"  ],
      7593.70   : [  "A"        ,  "O₂"  ],
      8226.96   : [  "Z"        ,  "O₂"  ],
      8987.65   : [  "y"        ,  "O₂"  ]
   }



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



