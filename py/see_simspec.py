#!/usr/bin/env python3
# HEREHEREHERE

#############################################################################
# 
#  /home/wayne/play/see_simspec.py
#
#emacs helpers
# (insert (buffer-file-name))
#
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
#############################################################################
import optparse
import re
import sys

__doc__ = """

/home/wayne/play/see_simspec.py
[options] files...

With the spreadsheet:

open in oocalc
   Tools -> Options -> Calc -> View
    check formulas
    uncheck the rest
OK
Then select all and paste into a text file.
Columns are letters, rows are numbers
the text file is tab delimited

The program simply walks the file line by line
(the number) and col by col (the letter)

Here goes.

Per usual extended ascii for french
0xc2 is the degrees
"""


__author__  = 'Wayne Green'
__version__ = '0.1'

_colnames = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
             'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
             'V', 'W', 'X', 'Y', 'Z',
             'AA', 'BB', 'CC', 'DD', 'EE', 'FF', 'GG', 'HH', 'II', 'JJ', 'KK',
             'LL', 'MM', 'NN', 'OO', 'PP', 'QQ', 'RR', 'SS', 'TT', 'UU',
             'VV', 'WW', 'XX', 'YY', 'ZZ'
           ]

def emit(line,parts):
   """Given a properly parted line, emit it"""
   col = 1
   for p in parts:
      print("%s %3d   %s" % (_colnames[col],line,p))
      col+= 1


##############################################################################
#                                    Main
#                               Regression Tests
##############################################################################

if __name__ == "__main__":
   opts = optparse.OptionParser(usage="%prog "+__doc__)

   opts.add_option("-v", "--verbose", action="store_true", dest="verboseflag",
                   default=False,
                   help="<bool>     be verbose about work.")

   (options, args) = opts.parse_args()




   #if(len(args) == 0 ): args.append(None)
   for filename in args:
      line = col = 0
      with open(filename,'r') if filename else sys.stdin as f:
         for l in f:
            line += 1
            parts = list(map(str.strip,l.split()))
            emit(line,parts)



