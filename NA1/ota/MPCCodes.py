#!/usr/bin/env python3
# -*- coding: latin-1 -*-
# HEREHEREHERE

#############################################################################
#
#  /home/wayne/git/clones/Strasburg/py/MPCCodes.py
#
#emacs helpers
# (insert (format "\n# " (buffer-file-name)))
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
import numpy as np
import matplotlib.pyplot as plt
import sqlite3 as db
import datetime


# (wg-python-graphics)
__doc__ = """

MPCCodes.py

With a recent copy of the MPC codes, from the web
https://www.minorplanetcenter.net/iau/lists/ObsCodesF.html

Make a sqlite3 database and generate the guts of a QComboBox
for the observatories. This for the SiteUI/Site py modules.


"""


__author__  = 'Wayne Green'
__version__ = '0.1'

zerore = re.compile(r'[^0.]+')
tickre = re.compile(r'\'')

# Code |  Long.   |  cos     |   sin     | Name

MPCText = """000  |  0.0000  | 0.62411  | +0.77873  | Greenwich
001  |  0.1542  | 0.62992  | +0.77411  | Crowborough
002  |  0.62    | 0.622    | +0.781    | Rayleigh
003  |  3.90    | 0.725    | +0.687    | Montpellier
004  |  1.4625  | 0.72520  | +0.68627  | Toulouse
005  |  2.23100 | 0.659891 | +0.748875 | Meudon
006  |  2.12417 | 0.751042 | +0.658129 | Fabra Observatory, Barcelona
007  |  2.33675 | 0.659470 | +0.749223 | Paris
008  |  3.0355  | 0.80172  | +0.59578  | Algiers-Bouzareah
009  |  7.4417  | 0.6838   | +0.7272   | Berne-Uecht
010  |  6.92124 | 0.723655 | +0.688135 | Caussols
011  |  8.7975  | 0.67920  | +0.73161  | Wetzikon
012  |  4.35821 | 0.633333 | +0.771306 | Uccle
013  |  4.48397 | 0.614813 | +0.786029 | Leiden
014  |  5.39509 | 0.728859 | +0.682384 | Marseilles
015  |  5.12929 | 0.615770 | +0.785285 | Utrecht
016  |  5.9893  | 0.68006  | +0.73076  | Besancon
017  |  6.84924 | 0.641946 | +0.764282 | Hoher List
018  |  6.7612  | 0.62779  | +0.77578  | Dusseldorf-Bilk
019  |  6.9575  | 0.68331  | +0.72779  | Neuchatel
020  |  7.3004  | 0.72391  | +0.68767  | Nice
021  |  8.3855  | 0.65701  | +0.75138  | Karlsruhe
022  |  7.7748  | 0.70790  | +0.70409  | Pino Torinese
023  |  8.2625  | 0.64299  | +0.76335  | Wiesbaden
024  |  8.7216  | 0.65211  | +0.75570  | Heidelberg-Konigstuhl
025  |  9.19650 | 0.660205 | +0.748637 | Stuttgart
026  |  7.46511 | 0.684884 | +0.726402 | Berne-Zimmerwald
027  |  9.1912  | 0.70254  | +0.70929  | Milan
028  |  9.9363  | 0.64686  | +0.76009  | Wurzburg
029  | 10.2406  | 0.59640  | +0.80000  | Hamburg-Bergedorf
030  | 11.25446 | 0.723534 | +0.688012 | Arcetri Observatory, Florence
031  | 11.18985 | 0.639061 | +0.766705 | Sonneberg
032  | 11.58295 | 0.631624 | +0.772706 | Jena
033  | 11.71124 | 0.630900 | +0.773333 | Karl Schwarzschild Observatory, Tautenburg
034  | 12.45246 | 0.745176 | +0.664656 | Monte Mario Observatory, Rome
035  | 12.57592 | 0.565008 | +0.822321 | Copenhagen
036  | 12.65040 | 0.747247 | +0.662420 | Castel Gandolfo
037  | 13.7333  | 0.73660  | +0.67416  | Collurania Observatory, Teramo
038  | 13.7704  | 0.70033  | +0.71144  | Trieste
039  | 13.1874  | 0.56485  | +0.82243  | Lund
040  | 13.7298  | 0.63019  | +0.77387  | Lohrmann Institute, Dresden
041  | 11.38083 | 0.679862 | +0.731012 | Innsbruck
042  | 13.06428 | 0.611721 | +0.788439 | Potsdam
043  | 11.52643 | 0.697656 | +0.714269 | Asiago Astrophysical Observatory, Padua
044  | 14.2559  | 0.75738  | +0.65082  | Capodimonte Observatory, Naples
045  | 16.3390  | 0.66739  | +0.74227  | Vienna (since 1879)
046  | 14.2881  | 0.65922  | +0.74965  | Klet Observatory, Ceske Budejovice
047  | 16.8782  | 0.61146  | +0.78864  | Poznan
048  | 15.84080 | 0.641709 | +0.764432 | Hradec Kralove
049  | 17.6067  | 0.5088   | +0.8580   | Uppsala-Kvistaberg
050  | 18.0582  | 0.51118  | +0.85660  | Stockholm (before 1931)
051  | 18.4766  | 0.83055  | -0.55508  | Royal Observatory, Cape of Good Hope
052  | 18.3083  | 0.51224  | +0.85597  | Stockholm-Saltsjobaden
053  | 18.9642  | 0.67688  | +0.73373  | Konkoly Observatory, Budapest (since 1934)
054  | 11.6654  | 0.56595  | +0.82169  | Brorfelde
055  | 19.9596  | 0.64321  | +0.76316  | Cracow
056  | 20.2450  | 0.65501  | +0.75346  | Skalnate Pleso
057  | 20.5133  | 0.71074  | +0.70116  | Belgrade
058  | 20.4950  | 0.57897  | +0.81262  | Kaliningrad
059  | 20.2201  | 0.65500  | +0.75364  | Lomnicky Stit
060  | 21.4200  | 0.61572  | +0.78535  | Warsaw-Ostrowik
061  | 22.29850 | 0.662142 | +0.746904 | Uzhgorod
062  | 22.2293  | 0.49440  | +0.86632  | Turku
063  | 22.4450  | 0.49496  | +0.86601  | Turku-Tuorla
064  | 22.7500  | 0.49489  | +0.86605  | Turku-Kevola
065  | 12.6318  | 0.67222  | +0.73800  | Traunstein
066  | 23.71817 | 0.789321 | +0.611946 | Athens
067  | 24.0297  | 0.64632  | +0.76058  | Lvov University Observatory
068  | 24.0142  | 0.64627  | +0.76062  | Lvov Polytechnic Institute
069  | 24.4042  | 0.54925  | +0.83287  | Baldone
070  | 25.2865  | 0.57940  | +0.81233  | Vilnius (before 1939)
071  | 24.73782 | 0.74803  | +0.66185  | NAO Rozhen, Smolyan
072  |  7.17    | 0.629    | +0.774    | Scheuren Observatory
073  | 26.0967  | 0.71549  | +0.69630  | Bucharest
074  | 26.4058  | 0.87518  | -0.48263  | Boyden Observatory, Bloemfontein
075  | 26.7216  | 0.52557  | +0.84791  | Tartu
076  | 27.8768  | 0.90127  | -0.43225  | Johannesburg-Hartbeespoort
077  | 28.0292  | 0.89819  | -0.43876  | Yale-Columbia Station, Johannesburg
078  | 28.0750  | 0.89824  | -0.43868  | Johannesburg
079  | 28.2288  | 0.90120  | -0.43251  | Radcliffe Observatory, Pretoria
080  | 28.9667  | 0.75566  | +0.65278  | Istanbul
081  | 27.8768  | 0.90127  | -0.43225  | Leiden Station, Johannesburg
082  | 15.7561  | 0.66929  | +0.74063  | St. Polten
083  | 30.5056  | 0.63918  | +0.76651  | Golosseevo-Kiev
084  | 30.3274  | 0.50471  | +0.86041  | Pulkovo
085  | 30.5023  | 0.63800  | +0.76749  | Kiev
086  | 30.7582  | 0.68987  | +0.72152  | Odessa
087  | 31.3411  | 0.86799  | +0.49495  | Helwan
088  | 31.8250  | 0.86741  | +0.49608  | Kottomia
089  | 31.9747  | 0.68359  | +0.72743  | Nikolaev
090  |  8.25    | 0.645    | +0.762    | Mainz
091  |  4.20919 | 0.703630 | +0.708287 | Observatoire de Nurol, Aurec sur Loire
092  | 18.5546  | 0.60177  | +0.79601  | Torun-Piwnice
093  | 20.3647  | 0.3537   | +0.9322   | Skibotn
094  | 33.9974  | 0.71565  | +0.69620  | Crimea-Simeis
095  | 34.0160  | 0.71172  | +0.70024  | Crimea-Nauchnij
096  |  9.4283  | 0.69967  | +0.71215  | Merate
097  | 34.7625  | 0.86165  | +0.50608  | Wise Observatory, Mitzpeh Ramon
098  | 11.56900 | 0.697916 | +0.714090 | Asiago Observatory, Cima Ekar
099  | 25.53    | 0.483    | +0.873    | Lahti
100  | 24.13    | 0.462    | +0.884    | Ahtari
101  | 36.2322  | 0.64403  | +0.76246  | Kharkov
102  | 36.75953 | 0.564841 | +0.822468 | Zvenigorod
103  | 14.52774 | 0.695365 | +0.716346 | Ljubljana
104  | 10.8042  | 0.71985  | +0.69202  | San Marcello Pistoiese
105  | 37.5706  | 0.56403  | +0.82302  | Moscow
106  | 14.0711  | 0.69662  | +0.71519  | Crni Vrh
107  | 11.0030  | 0.70998  | +0.70186  | Cavezzo
108  | 11.0278  | 0.72367  | +0.68784  | Montelupo
109  |  3.0705  | 0.80241  | +0.59481  | Algiers-Kouba
110  | 39.4150  | 0.54316  | +0.83683  | Rostov
111  | 10.9721  | 0.72439  | +0.68710  | Piazzano Observatory, Florence
112  | 10.9039  | 0.70232  | +0.70950  | Pleiade Observatory, Verona
113  | 13.0166  | 0.63502  | +0.77001  | Volkssternwarte Drebach, Schoenbrunn
114  | 41.4277  | 0.72489  | +0.68702  | Engelhardt Observatory, Zelenchukskaya Station
115  | 41.4416  | 0.72492  | +0.68699  | Zelenchukskaya
116  | 11.5958  | 0.66893  | +0.74094  | Giesing
117  | 11.5385  | 0.66897  | +0.74092  | Sendling
118  | 17.2740  | 0.66558  | +0.74394  | Astronomical and Geophysical Observatory, Modra
119  | 42.8200  | 0.74731  | +0.66262  | Abastuman
120  | 13.7261  | 0.70489  | +0.70699  | Visnjan
121  | 36.93403 | 0.648856 | +0.758394 | Kharkov University, Chuguevskaya Station
122  |  3.5035  | 0.72017  | +0.69176  | Pises Observatory
123  | 44.2917  | 0.76352  | +0.64398  | Byurakan
124  |  2.2550  | 0.72534  | +0.68612  | Castres
125  | 44.78950 | 0.747594 | +0.662026 | Tbilisi
126  |  9.7903  | 0.71893  | +0.69283  | Monte Viseggi
127  |  6.9797  | 0.63385  | +0.77088  | Bornheim
128  | 46.00661 | 0.623279 | +0.779393 | Saratov
129  | 45.92    | 0.777    | +0.628    | Ordubad
130  | 10.23963 | 0.700143 | +0.711791 | Lumezzane
131  |  4.725   | 0.7123   | +0.6996   | Observatoire de l\'Ardeche
132  |  5.2461  | 0.71919  | +0.69260  | Bedoin
133  |  5.0906  | 0.72819  | +0.68309  | Les Tardieux
134  | 11.48245 | 0.631607 | +0.772773 | Groszschwabhausen
135  | 49.1210  | 0.56353  | +0.82334  | Kasan
136  | 48.8156  | 0.56282  | +0.82383  | Engelhardt Observatory, Kasan
137  | 34.8147  | 0.84821  | +0.52790  | Givatayim Observatory
138  |  7.5717  | 0.67550  | +0.73494  | Village-Neuf
139  |  7.1108  | 0.72526  | +0.68618  | Antibes
140  |  3.6294  | 0.69945  | +0.71241  | Augerolles
141  |  7.3672  | 0.65646  | +0.75189  | Hottviller
142  |  7.1874  | 0.62156  | +0.78075  | Sinsen
143  |  9.02406 | 0.692986 | +0.718590 | Gnosca
144  |  1.6660  | 0.65549  | +0.75268  | Bray et Lu
145  |  4.5597  | 0.62734  | +0.77614  | \'s-Gravenwezel
146  | 10.6673  | 0.71715  | +0.69487  | Frignano
147  |  8.57391 | 0.700430 | +0.711392 | Osservatorio Astronomico di Suno
148  |  2.0375  | 0.72481  | +0.68667  | Guitalens
149  |  4.2236  | 0.65403  | +0.75396  | Beine-Nauroy
150  |  2.1572  | 0.65806  | +0.75045  | Maisons Laffitte
151  |  8.7440  | 0.67719  | +0.73346  | Eschenberg Observatory, Winterthur
152  | 25.5633  | 0.57036  | +0.81868  | Moletai Astronomical Observatory
153  |  9.1747  | 0.66080  | +0.74814  | Stuttgart-Hoffeld
154  | 12.1043  | 0.68923  | +0.72250  | Cortina
155  | 10.1971  | 0.55864  | +0.82664  | Ole Romer Observatory, Aarhus
156  | 15.0858  | 0.79431  | +0.60549  | Catania Astrophysical Observatory
157  | 12.8117  | 0.74166  | +0.66864  | Frasso Sabino
158  |  7.6033  | 0.69871  | +0.71333  | Promiod
159  | 10.5153  | 0.72065  | +0.69115  | Monte Agliale
160  | 10.84144 | 0.722651 | +0.688913 | Castelmartini
161  |  8.1605  | 0.70725  | +0.70467  | Cerrina Tololo Observatory
162  | 15.7805  | 0.75988  | +0.64808  | Potenza
163  |  6.1492  | 0.65017  | +0.75731  | Roeser Observatory, Luxembourg
164  |  6.8861  | 0.66631  | +0.74325  | St. Michel sur Meurthe
165  |  1.7553  | 0.74984  | +0.65946  | Piera Observatory, Barcelona
166  | 16.0117  | 0.63730  | +0.76812  | Upice
167  |  8.5727  | 0.67662  | +0.73398  | Bulach Observatory
168  | 59.5472  | 0.54541  | +0.83541  | Kourovskaya
169  |  8.4016  | 0.70737  | +0.70453  | Airali Observatory
170  |  1.9206  | 0.75217  | +0.65711  | Observatorio de Begues
171  | 14.4697  | 0.81089  | +0.58327  | Flarestar Observatory, San Gwann
172  |  7.0364  | 0.68593  | +0.72539  | Onnens
173  | 55.5061  | 0.93464  | -0.35447  | St. Clotilde, Reunion
174  | 25.5131  | 0.46536  | +0.88219  | Nyrola Observatory, Jyvaskyla
175  |  7.6083  | 0.6932   | +0.7188   | F.-X. Bagnoud Observatory, St-Luc
176  |  2.8225  | 0.77098  | +0.63475  | Observatorio Astronomico de Consell
177  |  3.9414  | 0.72477  | +0.68669  | Le Cres
178  |  6.1344  | 0.69423  | +0.71745  | Collonges
179  |  9.0175  | 0.69694  | +0.71507  | Monte Generoso
180  |  3.9519  | 0.72571  | +0.68570  | Mauguio
181  | 55.4100  | 0.93288  | -0.35941  | Observatoire des Makes, Saint-Louis
182  | 55.2586  | 0.93394  | -0.35634  | St. Paul, Reunion
183  | 41.4200  | 0.72496  | +0.68695  | Starlab Observatory, Karachay-Cherkessia
184  |  6.0361  | 0.72081  | +0.69097  | Valmeca Observatory, Puimichel
185  |  7.4219  | 0.67876  | +0.73200  | Observatoire Astronomique Jurassien-Vicques
186  | 66.8821  | 0.77679  | +0.62781  | Kitab
187  | 17.0733  | 0.61314  | +0.78735  | Astronomical Observatory, Borowiec
188  | 66.89555 | 0.782059 | +0.621762 | Majdanak
189  |  6.1514  | 0.69340  | +0.71823  | Geneva (before 1967)
190  | 68.6819  | 0.78382  | +0.61909  | Gissar
191  | 68.7811  | 0.78306  | +0.62006  | Dushanbe
192  | 69.2936  | 0.75213  | +0.65692  | Tashkent
193  | 69.2178  | 0.78648  | +0.61610  | Sanglok
194  | 18.0094  | 0.91807  | -0.39579  | Tivoli
195  | 11.4492  | 0.66804  | +0.74174  | Untermenzing Observatory, Munich
196  |  7.3331  | 0.65296  | +0.75490  | Homburg-Erbach
197  | 12.1836  | 0.71739  | +0.69434  | Bastia
198  |  8.75674 | 0.662195 | +0.746924 | Wildberg
199  |  2.4380  | 0.66659  | +0.74294  | Buthiers
200  |  4.3036  | 0.63385  | +0.77088  | Beersel Hills Observatory
201  |  7.6033  | 0.69871  | +0.71332  | Jonathan B. Postel Observatory
202  |  5.8997  | 0.73137  | +0.67971  | Tamaris Observatoire, La Seyne sur Mer
203  |  8.9955  | 0.70161  | +0.71021  | GiaGa Observatory
204  |  8.7708  | 0.69765  | +0.71430  | Schiaparelli Observatory
205  | 11.2731  | 0.71478  | +0.69703  | Obs. Casalecchio di Reno, Bologna
206  | 10.5667  | 0.4922   | +0.8677   | Haagaar Observatory, Eina
207  |  9.3065  | 0.70156  | +0.71025  | Osservatorio Antonio Grosso
208  |  9.5875  | 0.70893  | +0.70294  | Rivalta
209  | 11.56883 | 0.697904 | +0.714100 | Asiago Observatory, Cima Ekar-ADAS
210  | 76.9573  | 0.73042  | +0.68104  | Alma-Ata
211  | 11.1764  | 0.72338  | +0.68815  | Scandicci
212  |355.35747 | 0.803253 | +0.593708 | Observatorio La Dehesilla
213  |  2.38539 | 0.749843 | +0.659421 | Observatorio Montcabre
214  | 11.6569  | 0.66709  | +0.74258  | Garching Observatory
215  | 10.7328  | 0.67021  | +0.73981  | Buchloe
216  |  5.6914  | 0.65732  | +0.75114  | Observatoire des Cote de Meuse
217  | 77.87114 | 0.730114 | +0.681643 | Assah
218  | 78.4541  | 0.95444  | +0.29768  | Hyderabad
219  | 78.7283  | 0.95618  | +0.29216  | Japal-Rangapur
220  | 78.8263  | 0.97627  | +0.21634  | Vainu Bappu Observatory, Kavalur
221  | 16.3631  | 0.91960  | -0.39228  | IAS Observatory, Hakos
222  |  2.4939  | 0.66113  | +0.74777  | Yerres-Canotiers
223  | 80.2464  | 0.97427  | +0.22465  | Madras
224  |  7.50171 | 0.673178 | +0.737048 | Ottmarsheim
225  |288.8250  | 0.7298   | +0.6814   | Northwood Ridge Observatory
226  | 11.8858  | 0.70293  | +0.70888  | Guido Ruggieri Observatory, Padua
227  |281.2853  | 0.73683  | +0.67392  | OrbitJet Observatory, Colden
228  | 13.8750  | 0.70038  | +0.71147  | Bruno Zugna Observatory, Trieste
229  | 14.9743  | 0.75936  | +0.64857  | G. C. Gloriosi Astronomical Observatory, Salerno
230  | 12.0133  | 0.6744   | +0.7363   | Mt. Wendelstein Observatory
231  |  5.3983  | 0.64403  | +0.76253  | Vesqueville
232  |  1.3317  | 0.7500   | +0.6593   | Masquefa Observatory
233  | 10.5403  | 0.72226  | +0.68931  | Sauro Donati Astronomical Observatory, San Vito
234  |  1.12833 | 0.614951 | +0.785931 | Coddenham Observatory
235  | 13.11352 | 0.696669 | +0.714993 | CAST Observatory, Talmassons
236  | 84.9465  | 0.55370  | +0.82995  | Tomsk
237  |  2.7333  | 0.6822   | +0.7288   | Baugy
238  | 10.9094  | 0.50204  | +0.86197  | Grorudalen Optical Observatory
239  |  8.4114  | 0.64506  | +0.76159  | Trebur
240  |  8.83317 | 0.662308 | +0.746832 | Herrenberg Sternwarte
241  | 13.4700  | 0.66465  | +0.74474  | Schaerding
242  |  1.6956  | 0.72681  | +0.68460  | Varennes
243  |  9.4130  | 0.59572  | +0.80050  | Umbrella Observatory, Fredenbeck
244  |  0.00000 | 0.000000 |  0.000000 | Geocentric Occultation Observation
245  |          |          |           | Spitzer Space Telescope
246  | 14.2881  | 0.65922  | +0.74965  | Klet Observatory-KLENOT
247  |          |          |           | Roving Observer
248  |  0.00000 | 0.000000 |  0.000000 | Hipparcos
249  |          |          |           | SOHO
250  |          |          |           | Hubble Space Telescope
251  |293.24692 | 0.949577 | +0.312734 | Arecibo
252  |243.20512 | 0.817719 | +0.573979 | Goldstone DSS 13, Fort Irwin
253  |243.11047 | 0.815913 | +0.576510 | Goldstone DSS 14, Fort Irwin
254  |288.51128 | 0.736973 | +0.673692 | Haystack, Westford
255  | 33.18689 | 0.705965 | +0.705886 | Evpatoria
256  |280.16017 | 0.784451 | +0.618320 | Green Bank
257  |243.12461 | 0.816796 | +0.575252 | Goldstone DSS 25, Fort Irwin
258  |          |          |           | Gaia
259  | 19.22586 | 0.349828 | +0.933688 | EISCAT Tromso UHF
260  |149.0661  | 0.85560  | -0.51626  | Siding Spring Observatory-DSS
261  |243.14022 | 0.836325 | +0.546877 | Palomar Mountain-DSS
262  |289.26626 | 0.873440 | -0.486052 | European Southern Observatory, La Silla-DSS
266  |204.52344 | 0.941701 | +0.337237 | New Horizons KBO Search-Subaru
267  |204.53044 | 0.941705 | +0.337234 | New Horizons KBO Search-CFHT
268  |289.30803 | 0.875516 | -0.482342 | New Horizons KBO Search-Magellan/Clay
269  |289.30914 | 0.875510 | -0.482349 | New Horizons KBO Search-Magellan/Baade
276  | 20.38279 | 0.608295 | +0.791076 | Plonsk
277  |356.8175  | 0.56158  | +0.82467  | Royal Observatory, Blackford Hill, Edinburgh
278  |116.4494  | 0.76818  | +0.63809  | Peking, Transit of Venus site
279  | 10.72822 | 0.631526 | +0.772827 | Seeberg Observatory, Gotha (1787-1857)
280  |  8.9118  | 0.60114  | +0.79646  | Lilienthal
281  | 11.3522  | 0.71448  | +0.69733  | Bologna
282  |  4.3603  | 0.72245  | +0.68912  | Nimes
283  |  8.8163  | 0.60204  | +0.79579  | Bremen
284  | 15.8311  | 0.60536  | +0.79329  | Driesen
285  |  2.3708  | 0.66135  | +0.74759  | Flammarion Observatory, Juvisy
286  |102.7883  | 0.90694  | +0.42057  | Yunnan Observatory
290  |250.10799 | 0.842743 | +0.537438 | Mt. Graham-VATT
291  |248.4009  | 0.84947  | +0.52647  | LPL/Spacewatch II
292  |285.1058  | 0.76630  | +0.64033  | Burlington, New Jersey
293  |285.5899  | 0.76936  | +0.63668  | Burlington remote site
294  |285.8467  | 0.76031  | +0.64739  | Astrophysical Obs., College of Staten Island
295  |283.0000  | 0.7789   | +0.6251   | Catholic University Observatory, Washington
296  |286.2515  | 0.7365   | +0.6742   | Dudley Observatory, Albany (after 1893)
297  |286.819   | 0.7203   | +0.6913   | Middlebury
298  |287.3408  | 0.74943  | +0.65988  | Van Vleck Observatory
299  |107.6160  | 0.99316  | -0.11808  | Bosscha Observatory, Lembang
300  |133.54444 | 0.823370 | +0.565720 | Bisei Spaceguard Center-BATTeRS
301  |288.8467  | 0.70279  | +0.70926  | Mont Megantic
302  |288.88    | 0.990    | +0.150    | University of the Andes station
303  |289.1296  | 0.98890  | +0.15185  | OAN de Llano del Hato, Merida
304  |289.2980  | 0.87559  | -0.48217  | Las Campanas Observatory
305  |109.5514  | 0.82066  | +0.56963  | Purple Mountain, Hainan Island station
306  |290.6769  | 0.98477  | +0.17381  | Observatorio Taya Beixo, Barquisimeto
307  |287.7166  | 0.72410  | +0.68743  | Shattuck Observatory, Hanover
309  |289.59569 | 0.909943 | -0.414336 | Cerro Paranal
310  |288.87164 | 0.739802 | +0.670574 | Minor Planet Center Test Code
312  |112.334   | 0.9574   | +0.2877   | Tsingtao field station, Xisha Islands
318  |115.691   | 0.85206  | -0.52170  | Quinns Rock
319  |116.1350  | 0.84883  | -0.52702  | Perth Observatory, Perth-Lowell Telescope
320  |116.4381  | 0.85859  | -0.51102  | Chiro Observatory
321  |115.7571  | 0.85078  | -0.52378  | Craigie
322  |116.1340  | 0.84882  | -0.52703  | Perth Observatory, Bickley-MCT
323  |116.1350  | 0.84882  | -0.52703  | Perth Observatory, Bickley
324  |116.3277  | 0.76598  | +0.64072  | Peking Observatory, Shaho Station
327  |117.5750  | 0.76278  | +0.64470  | Peking Observatory, Xinglong Station
330  |118.8209  | 0.84828  | +0.52788  | Purple Mountain Observatory, Nanking
333  |249.5236  | 0.84936  | +0.52642  | Desert Eagle Observatory
334  |120.3196  | 0.80925  | +0.58552  | Tsingtao
337  |121.1843  | 0.85708  | +0.51348  | Sheshan, formerly Zo-Se
340  |135.4853  | 0.82199  | +0.56762  | Toyonaka
341  |137.9486  | 0.80669  | +0.58923  | Akashina
342  |134.3189  | 0.83425  | +0.54955  | Shishikui
343  |127.1258  | 0.78688  | +0.61507  | Younchun
344  |128.9767  | 0.80841  | +0.58695  | Bohyunsan Optical Astronomy Observatory
345  |128.4575  | 0.80046  | +0.59773  | Sobaeksan Optical Astronomy Observatory
346  |127.3854  | 0.80474  | +0.59166  | KNUE Astronomical Observatory
347  |139.9086  | 0.80417  | +0.59244  | Utsunomiya-Imaizumi
348  |135.2669  | 0.81698  | +0.57475  | Ayabe
349  |139.56622 | 0.810402 | +0.583916 | Ageo
350  |139.2635  | 0.80504  | +0.59132  | Kurohone
351  |135.8678  | 0.81939  | +0.57135  | Sakamoto
352  |136.1778  | 0.82061  | +0.56963  | Konan
353  |135.0648  | 0.82265  | +0.56669  | Nishi Kobe
354  |140.0206  | 0.80109  | +0.59674  | Kawachi
355  |139.2133  | 0.81618  | +0.57590  | Hadano
356  |141.0867  | 0.78319  | +0.61970  | Kogota
357  |140.0064  | 0.80807  | +0.58712  | Shimotsuma
358  |140.1586  | 0.78856  | +0.61296  | Nanyo
359  |135.1719  | 0.82782  | +0.55912  | Wakayama
360  |132.9442  | 0.83314  | +0.55138  | Kuma Kogen
361  |134.8933  | 0.82649  | +0.56106  | Sumoto
362  |140.6550  | 0.73673  | +0.67398  | Ray Observatory
363  |130.7703  | 0.83416  | +0.54967  | Yamada
364  |130.5747  | 0.85213  | +0.52164  | YCPM Kagoshima Station
365  |135.9579  | 0.82597  | +0.56196  | Uto Observatory
366  |138.3003  | 0.81147  | +0.58267  | Miyasaka Observatory
367  |133.1670  | 0.81504  | +0.57747  | Yatsuka
368  |138.8117  | 0.81213  | +0.58191  | Ochiai
369  |139.1500  | 0.8101   | +0.5844   | Chichibu
370  |133.5273  | 0.83424  | +0.54956  | Kochi
371  |133.5965  | 0.82433  | +0.56431  | Tokyo-Okayama
372  |133.8276  | 0.83450  | +0.54920  | Geisei
373  |135.3397  | 0.82866  | +0.55797  | Oishi
374  |134.7196  | 0.81915  | +0.57174  | Minami-Oda Observatory
375  |134.8708  | 0.8206   | +0.5697   | Uzurano
376  |139.0392  | 0.81321  | +0.58022  | Uenohara
377  |135.7933  | 0.82014  | +0.57031  | Kwasan Observatory, Kyoto
378  |136.0142  | 0.82437  | +0.56426  | Murou
379  |137.6279  | 0.82300  | +0.56613  | Hamamatsu-Yuto
380  |137.0349  | 0.82190  | +0.56772  | Ishiki
381  |137.62542 | 0.812172 | +0.581777 | Tokyo-Kiso
382  |137.5553  | 0.80915  | +0.58639  | Tokyo-Norikura
383  |137.8959  | 0.80218  | +0.59526  | Chirorin
384  |138.1792  | 0.8219   | +0.5678   | Shimada
385  |138.4680  | 0.82039  | +0.56997  | Nihondaira Observatory
386  |138.3217  | 0.81121  | +0.58309  | Yatsugatake-Kobuchizawa
387  |139.1944  | 0.81000  | +0.58469  | Tokyo-Dodaira
388  |139.5421  | 0.81330  | +0.57991  | Tokyo-Mitaka
389  |139.7447  | 0.81347  | +0.57965  | Tokyo (before 1938)
390  |139.8725  | 0.80425  | +0.59234  | Utsunomiya
391  |140.77843 | 0.786177 | +0.615960 | Sendai Observatory, Ayashi Station
392  |141.3667  | 0.73355  | +0.67741  | JCPM Sapporo Station
393  |140.1292  | 0.8090   | +0.5858   | JCPM Sakura Station
394  |142.3208  | 0.70692  | +0.70493  | JCPM Hamatonbetsu Station
395  |142.3583  | 0.7224   | +0.6891   | Tokyo-Asahikawa
396  |142.4208  | 0.7236   | +0.6879   | Asahikawa
397  |141.4761  | 0.73210  | +0.67892  | Sapporo Science Center
398  |139.1080  | 0.80870  | +0.58630  | Nagatoro
399  |144.5900  | 0.73158  | +0.67950  | Kushiro
400  |143.7827  | 0.72344  | +0.68811  | Kitami
401  |139.4208  | 0.8088   | +0.5861   | Oosato
402  |136.3078  | 0.81800  | +0.57335  | Dynic Astronomical Observatory
403  |137.0556  | 0.81593  | +0.57625  | Kani
404  |140.9292  | 0.7909   | +0.6099   | Yamamoto
405  |139.3292  | 0.8069   | +0.5887   | Kamihoriguchi
406  |141.8233  | 0.72946  | +0.68174  | Bibai
407  |140.3099  | 0.78426  | +0.61837  | Kahoku
408  |138.1747  | 0.81121  | +0.58328  | Nyukasa
409  |139.5211  | 0.81234  | +0.58124  | Kiyose and Mizuho
410  |134.8910  | 0.81883  | +0.57222  | Sengamine
411  |139.4170  | 0.80739  | +0.58805  | Oizumi
412  |140.5991  | 0.80011  | +0.59803  | Iwaki
413  |149.06608 | 0.855595 | -0.516262 | Siding Spring Observatory
414  |149.0077  | 0.81694  | -0.57499  | Mount Stromlo
415  |149.0636  | 0.81615  | -0.57606  | Kambah
416  |149.1336  | 0.81701  | -0.57485  | Barton
417  |137.1371  | 0.79611  | +0.60317  | Yanagida Astronomical Observatory
418  |150.94034 | 0.857259 | -0.513294 | Tamworth
419  |150.8329  | 0.83370  | -0.55038  | Windsor
420  |151.2050  | 0.83126  | -0.55404  | Sydney
421  |133.7650  | 0.83244  | +0.55262  | Mt. Kajigamori, Otoyo
422  |151.0461  | 0.85503  | -0.51709  | Loomberah
423  |151.12473 | 0.831807 | -0.553222 | North Ryde
424  |149.0658  | 0.81758  | -0.57405  | Macquarie
425  |152.9316  | 0.88796  | -0.45843  | Taylor Range Observatory, Brisbane
426  |136.8217  | 0.85618  | -0.51498  | Woomera
427  |138.7283  | 0.82667  | -0.56084  | Stockport
428  |153.3970  | 0.88271  | -0.46837  | Reedy Creek
429  |149.0400  | 0.81761  | -0.57402  | Hawker
430  |149.2123  | 0.85550  | -0.51623  | Rainbow Observatory, near Coonabarabran
431  |149.7578  | 0.83548  | -0.54793  | Mt. Tarana Observatory, Bathurst
432  |153.08222 | 0.863790 | -0.502166 | Boambee
433  |152.1078  | 0.84197  | -0.53771  | Bagnall Beach Observatory
434  | 10.9206  | 0.70765  | +0.70419  | S. Benedetto Po
435  | 11.8936  | 0.70330  | +0.70852  | G. Colombo Astronomical Observatory, Padua
436  | 11.3356  | 0.71658  | +0.69528  | Osservatorio di Livergnano
437  |284.6971  | 0.76700  | +0.63953  | Haverford
438  |287.3621  | 0.74059  | +0.66978  | Smith College Observatory, Northampton
439  |253.2539  | 0.81156  | +0.58288  | ROTSE-III, Los Alamos
440  |278.6842  | 0.73025  | +0.68097  | Elginfield Observatory
441  |357.1697  | 0.55559  | +0.82867  | Swilken Brae, St. Andrews
442  |357.4822  | 0.7477   | +0.6619   | Gualba Observatory
443  |301.4656  | 0.82370  | -0.56513  | Obs. Astronomico Plomer, Buenos Aires
444  |243.2794  | 0.83507  | +0.54868  | Star Cruiser Observatory
445  |359.4200  | 0.7802   | +0.6235   | Observatorio d\'Ontinyent
446  |262.1666  | 0.87049  | +0.49058  | Kingsnake Observatory, Seguin
447  |255.2056  | 0.77154  | +0.63448  | Centennial Observatory
448  |253.2801  | 0.84543  | +0.53268  | Desert Moon Observatory, Las Cruces
449  |279.6503  | 0.82617  | +0.56156  | Griffin Hunter Observatory, Bethune
450  |279.3339  | 0.81857  | +0.57254  | Carla Jane Observatory, Charlotte
451  |262.7569  | 0.79447  | +0.60536  | West Skies Observatory, Mulvane
452  |279.1063  | 0.8980   | +0.4385   | Big Cypress Observatory, Fort Lauderdale
453  |242.1331  | 0.82030  | +0.57021  | Edwards Raven Observatory
454  |283.37678 | 0.774542 | +0.630425 | Maryland Space Grant Consortium Observatory
455  |237.9636  | 0.78912  | +0.61218  | CBA Concord
456  |358.8278  | 0.61348  | +0.78709  | Daventry Observatory
457  | 18.3403  | 0.66221  | +0.74685  | Partizanske
458  |355.9806  | 0.75992  | +0.64805  | Guadarrama Observatory
459  |288.1172  | 0.72607  | +0.68538  | Smith River Observatory, Danbury
460  |265.9981  | 0.83010  | +0.55579  | Area 52 Observatory, Nashville
461  | 19.8943  | 0.67153  | +0.73869  | University of Szeged, Piszkesteto Stn. (Konkoly)
462  |283.0842  | 0.77905  | +0.62488  | Mount Belleview Observatory
463  |254.7375  | 0.76726  | +0.63959  | Sommers-Bausch Observatory, Boulder
464  |288.5013  | 0.75109  | +0.65799  | Toby Point Observatory, Narragansett
465  |174.7801  | 0.80166  | -0.59578  | Takapuna
466  |174.8487  | 0.8002   | -0.5977   | Mount Molehill Observatory, Auckland
467  |174.7766  | 0.80058  | -0.59724  | Auckland Observatory
468  | 13.3296  | 0.74652  | +0.66349  | Astronomical Observatory, Campo Catino
469  |  7.3820  | 0.67873  | +0.73205  | Courroux
470  | 13.32756 | 0.749268 | +0.660088 | Ceccano
471  |  8.2389  | 0.56364  | +0.82325  | Houstrup
472  |  6.3203  | 0.71225  | +0.69998  | Merlette
473  | 13.31661 | 0.694793 | +0.716822 | Remanzacco
474  |170.46496 | 0.720773 | -0.691079 | Mount John Observatory, Lake Tekapo
475  |  7.6965  | 0.70747  | +0.70443  | Turin (before 1913)
476  |  7.14075 | 0.706596 | +0.705358 | Grange Observatory, Bussoleno
477  |  0.4856  | 0.62103  | +0.78117  | Galleywood
478  |  3.0896  | 0.72548  | +0.68597  | Lamalou-les-Bains
479  |  6.0505  | 0.73020  | +0.68096  | Sollies-Pont
480  |  0.7733  | 0.61466  | +0.78616  | Cockfield
481  |  7.93    | 0.596    | +0.800    | Moorwarfen
482  |357.1854  | 0.55560  | +0.82866  | St. Andrews
483  |173.8036  | 0.74734  | -0.66254  | Carter Observatory, Black Birch Station
484  |174.7594  | 0.75191  | -0.65706  | Happy Valley, Wellington
485  |174.7654  | 0.75256  | -0.65635  | Carter Observatory, Wellington
486  |175.47    | 0.765    | -0.643    | Palmerston North
487  |355.4444  | 0.56858  | +0.81989  | Macnairston Observatory
488  |358.3664  | 0.57486  | +0.81553  | Newcastle-upon-Tyne
489  |359.87    | 0.612    | +0.788    | Hemingford Abbots
490  |358.00    | 0.633    | +0.772    | Wimborne Minster
491  |356.9000  | 0.76131  | +0.64644  | Centro Astronomico de Yebes
492  |358.47    | 0.605    | +0.795    | Mickleover
493  |357.4542  | 0.79753  | +0.60182  | Calar Alto
494  |357.8361  | 0.61126  | +0.78879  | Stakenbridge
495  |357.66247 | 0.597857 | +0.798936 | Altrincham
496  |358.6860  | 0.6311   | +0.7731   | Bishopstoke
497  |359.29449 | 0.622323 | +0.780160 | Loudwater
498  |359.2581  | 0.61334  | +0.78718  | Earls Barton
499  |359.79078 | 0.625578 | +0.777562 | Cheam
500  |  0.00000 | 0.000000 |  0.000000 | Geocentric
501  |  0.3475  | 0.63237  | +0.77208  | Herstmonceux
502  |  0.84793 | 0.618111 | +0.783475 | Colchester
503  |  0.0948  | 0.61400  | +0.78667  | Cambridge
504  |  4.3944  | 0.68553  | +0.72570  | Le Creusot
505  |  4.5639  | 0.6229   | +0.7797   | Simon Stevin
506  |  9.96    | 0.598    | +0.797    | Bendestorf
507  |  5.22    | 0.617    | +0.783    | Nyenheim
508  |  5.29    | 0.617    | +0.783    | Zeist
509  |  5.8725  | 0.73132  | +0.67976  | La Seyne sur Mer
510  |  8.0256  | 0.63185  | +0.77257  | Siegen
511  |  5.7157  | 0.72140  | +0.69034  | Haute Provence
512  |  4.4893  | 0.61477  | +0.78606  | Leiden (before 1860)
513  |  4.7855  | 0.69971  | +0.71209  | Lyons
514  |  8.438   | 0.6513   | +0.7563   | Mundenheim (1907-1913)
515  |  7.4956  | 0.64656  | +0.76038  | Volkssternwarte Dhaun, near Kirn
516  |  9.97321 | 0.595399 | +0.800741 | Hamburg (before 1909)
517  |  6.1358  | 0.69201  | +0.71957  | Geneva (from 1967)
518  |  9.9727  | 0.59545  | +0.80071  | Marine Observatory, Hamburg
519  |  8.2867  | 0.62598  | +0.77729  | Meschede
520  |  7.0966  | 0.63427  | +0.77053  | Bonn
521  | 10.88794 | 0.645624 | +0.761154 | Remeis Observatory, Bamberg
522  |  7.7677  | 0.66279  | +0.74633  | Strasbourg
523  |  8.6512  | 0.64251  | +0.76374  | Frankfurt
524  |  8.4605  | 0.6509   | +0.7566   | Mannheim
525  |  8.76917 | 0.633171 | +0.771473 | Marburg
526  | 10.1477  | 0.58426  | +0.80886  | Kiel
527  |  9.9431  | 0.5955   | +0.8007   | Altona
528  |  9.9426  | 0.62340  | +0.77931  | Gottingen
529  | 10.7229  | 0.50259  | +0.86163  | Christiania
530  | 10.6898  | 0.5911   | +0.8039   | Lubeck
531  | 12.4797  | 0.74545  | +0.66434  | Collegio Romano, Rome
532  | 11.6084  | 0.66853  | +0.74130  | Munich
533  | 11.8715  | 0.70335  | +0.70847  | Padua
534  | 12.3913  | 0.62606  | +0.77719  | Leipzig (since 1861)
535  | 13.3578  | 0.78782  | +0.61386  | Palermo
536  | 13.1062  | 0.61135  | +0.78873  | Berlin-Babelsberg
537  | 13.3642  | 0.6097   | +0.7900   | Urania Observatory, Berlin
538  | 13.8461  | 0.70998  | +0.70187  | Pola
539  | 14.1316  | 0.66968  | +0.74024  | Kremsmunster
540  | 14.2753  | 0.66470  | +0.74477  | Linz
541  | 14.3953  | 0.64306  | +0.76331  | Prague
542  | 13.0374  | 0.6091   | +0.7904   | Falkensee
543  | 12.3688  | 0.6260   | +0.7772   | Leipzig (before 1861)
544  | 13.35131 | 0.610644 | +0.789263 | Wilhelm Foerster Observatory, Berlin
545  | 16.3817  | 0.66767  | +0.74200  | Vienna (before 1879)
546  | 16.3549  | 0.66760  | +0.74207  | Oppolzer Observatory, Vienna
547  | 17.0363  | 0.62904  | +0.77479  | Breslau
548  | 13.3950  | 0.60999  | +0.78976  | Berlin (1835-1913)
549  | 17.6257  | 0.50341  | +0.86116  | Uppsala
550  | 11.4196  | 0.5943   | +0.8015   | Schwerin
551  | 18.1895  | 0.67201  | +0.73808  | Hurbanovo, formerly O\'Gyalla
552  | 11.3418  | 0.71485  | +0.69700  | Osservatorio S. Vittore, Bologna
553  | 18.9938  | 0.64002  | +0.76574  | Chorzow
554  |  8.3959  | 0.63684  | +0.76845  | Burgsolms Observatory, Wetzlar
555  | 19.8263  | 0.64336  | +0.76306  | Cracow-Fort Skala
556  | 11.26    | 0.675    | +0.734    | Reintal, near Munich
557  | 14.7837  | 0.64530  | +0.76148  | Ondrejov
558  | 21.0303  | 0.61396  | +0.78672  | Warsaw
559  | 14.98    | 0.793    | +0.607    | Serra La Nave
560  | 10.93100 | 0.703262 | +0.708561 | Madonna di Dossobuono
561  | 19.8943  | 0.67153  | +0.73869  | Piszkesteto Stn. (Konkoly)
562  | 15.9236  | 0.66938  | +0.74062  | Figl Observatory, Vienna
563  | 13.60    | 0.671    | +0.739    | Seewalchen
564  | 11.19    | 0.671    | +0.741    | Herrsching
565  | 10.1344  | 0.70437  | +0.70746  | Bassano Bresciano
566  |203.7424  | 0.93623  | +0.35156  | Haleakala-NEAT/GEODSS
567  | 12.7117  | 0.69783  | +0.71387  | Chions
568  |204.5278  | 0.94171  | +0.33725  | Mauna Kea
569  | 24.9587  | 0.49891  | +0.86375  | Helsinki
570  | 25.2990  | 0.5794   | +0.8123   | Vilnius (since 1939)
571  | 10.63    | 0.704    | +0.708    | Cavriana
572  |  6.89    | 0.631    | +0.772    | Cologne
573  |  9.6612  | 0.6145   | +0.7862   | Eldagsen
574  | 10.27    | 0.704    | +0.708    | Gottolengo
575  |  6.808   | 0.68219  | +0.72894  | La Chaux de Fonds
576  |  0.38    | 0.631    | +0.774    | Burwash
577  |  7.50    | 0.678    | +0.734    | Metzerlen Observatory
578  | 27.99    | 0.898    | -0.439    | Linden Observatory
579  |  8.85    | 0.711    | +0.701    | Novi Ligure
580  | 15.4936  | 0.68242  | +0.72862  | Graz
581  | 22.80    | 0.830    | -0.556    | Sedgefield
582  |  1.2408  | 0.61682  | +0.78447  | Orwell Park
583  | 30.2717  | 0.69087  | +0.72056  | Odessa-Mayaki
584  | 30.2946  | 0.50213  | +0.86189  | Leningrad
585  | 30.52462 | 0.640079 | +0.765763 | Kyiv comet station
586  |  0.1423  | 0.73358  | +0.67799  | Pic du Midi
587  |  9.22918 | 0.697459 | +0.714479 | Sormano
588  | 11.25    | 0.715    | +0.697    | Eremo di Tizzano
589  | 12.64369 | 0.738223 | +0.672386 | Santa Lucia Stroncone
590  |  7.46    | 0.678    | +0.734    | Metzerlen
591  |  9.6258  | 0.60995  | +0.78979  | Resse Observatory
592  |  7.02114 | 0.628245 | +0.775437 | Solingen
593  | 11.17    | 0.739    | +0.671    | Monte Argentario
594  | 13.2033  | 0.74497  | +0.66529  | Monte Autore
595  | 13.52578 | 0.696925 | +0.714749 | Farra d\'Isonzo
596  | 12.6183  | 0.74446  | +0.66545  | Colleverde di Guidonia
597  |  9.6631  | 0.61461  | +0.78621  | Springe
598  | 11.33409 | 0.717444 | +0.694448 | Loiano
599  | 13.55764 | 0.739311 | +0.671604 | Campo Imperatore-CINEOS
600  | 11.4708  | 0.71618  | +0.69564  | TLC Observatory, Bologna
601  | 13.7281  | 0.63009  | +0.77394  | Engelhardt Observatory, Dresden
602  | 16.3854  | 0.66764  | +0.74203  | Urania Observatory, Vienna
603  | 10.1300  | 0.58622  | +0.80745  | Bothkamp
604  | 13.47524 | 0.610235 | +0.789572 | Archenhold Sternwarte, Berlin-Treptow
605  |  7.1130  | 0.62142  | +0.78086  | Marl
606  |  9.9956  | 0.59353  | +0.80212  | Norderstedt
607  |  8.0000  | 0.6277   | +0.7760   | Hagen Observatory, Ronkhausen
608  |203.7420  | 0.93623  | +0.35156  | Haleakala-AMOS
609  | 12.8533  | 0.73772  | +0.67314  | Osservatorio Polino
610  | 11.3431  | 0.71577  | +0.69604  | Pianoro
611  |  8.6531  | 0.64877  | +0.75848  | Starkenburg Sternwarte, Heppenheim
612  |  7.10    | 0.625    | +0.778    | Lenkerbeck
613  |  7.0709  | 0.62504  | +0.77800  | Heisingen
614  |  2.467   | 0.6621   | +0.7469   | Soisy-sur-Seine
615  |  6.9067  | 0.71233  | +0.70014  | St. Veran
616  | 16.58348 | 0.654655 | +0.753466 | Brno
617  |  2.5725  | 0.66496  | +0.74437  | Arbonne la Foret
618  |  5.0077  | 0.72750  | +0.68382  | Martigues
619  |  2.09013 | 0.749506 | +0.659828 | Sabadell
620  |  2.9517  | 0.77110  | +0.63463  | Observatorio Astronomico de Mallorca
621  |  7.48503 | 0.629461 | +0.774501 | Bergisch Gladbach
622  |  7.5680  | 0.68778  | +0.72358  | Oberwichtrach
623  |  5.5667  | 0.63577  | +0.76932  | Liege
624  |  9.6167  | 0.64723  | +0.75977  | Dertingen
625  |203.5683  | 0.93557  | +0.35201  | Kihei-AMOS Remote Maui Experimental Site
626  |  4.9864  | 0.62847  | +0.77524  | Geel
627  |  5.2146  | 0.72002  | +0.69168  | Blauvac
628  |  6.84366 | 0.624789 | +0.778184 | Mulheim-Ruhr
629  | 20.1511  | 0.69273  | +0.71880  | Szeged Observatory
630  |  7.2367  | 0.67051  | +0.73951  | Osenbach
631  | 10.02293 | 0.595992 | +0.800307 | Hamburg-Georgswerder
632  | 11.1739  | 0.72380  | +0.68773  | San Polo A Mosciano
633  |  9.9339  | 0.71930  | +0.69238  | Romito
634  |  5.1456  | 0.70182  | +0.71007  | Crolles
635  |  2.9019  | 0.73605  | +0.67467  | Pergignan
636  |  6.9794  | 0.62524  | +0.77783  | Essen
637  | 10.0903  | 0.59326  | +0.80232  | Hamburg-Himmelsmoor
638  |  8.8933  | 0.61778  | +0.78374  | Detmold
639  | 13.7233  | 0.62933  | +0.77456  | Dresden
640  | 13.5996  | 0.6429   | +0.7634   | Senftenberger Sternwarte
641  | 20.0272  | 0.82468  | -0.56374  | Overberg
642  |236.6850  | 0.6648   | +0.7445   | Oak Bay, Victoria
643  |243.2794  | 0.83507  | +0.54868  | OCA-Anza Observatory
644  |243.14022 | 0.836325 | +0.546877 | Palomar Mountain/NEAT
645  |254.17942 | 0.841945 | +0.538563 | Apache Point-Sloan Digital Sky Survey
646  |242.4369  | 0.82999  | +0.55603  | Santana Observatory, Rancho Cucamonga
647  |245.9683  | 0.6337   | +0.7712   | Stone Finder Observatory, Calgary
648  |249.39822 | 0.852115 | +0.522053 | Winer Observatory, Sonoita
649  |265.3003  | 0.78207  | +0.62117  | Powell Observatory, Louisburg
650  |242.9028  | 0.83510  | +0.54836  | Temecula
651  |249.41916 | 0.852069 | +0.522123 | Grasslands Observatory, Tucson
652  |245.9333  | 0.6291   | +0.7749   | Rock Finder Observatory, Calgary
653  |237.8678  | 0.68091  | +0.72996  | Torus Observatory, Buckley
654  |242.31841 | 0.826471 | +0.561727 | Table Mountain Observatory, Wrightwood-PHMC
655  |236.383   | 0.6656   | +0.7438   | Sooke
656  |236.3921  | 0.66580  | +0.74367  | Victoria
657  |236.6903  | 0.66437  | +0.74491  | Climenhaga Observatory, Victoria
658  |236.58300 | 0.663631 | +0.745601 | National Research Council of Canada
659  |237.0514  | 0.66257  | +0.74650  | Heron Cove Observatory, Orcas
660  |237.7379  | 0.79038  | +0.61059  | Leuschner Observatory, Berkeley
661  |245.7117  | 0.63251  | +0.77222  | Rothney Astrophysical Observatory, Priddis
662  |238.3545  | 0.79619  | +0.60335  | Lick Observatory, Mount Hamilton
663  |248.3136  | 0.83483  | +0.54879  | Red Mountain Observatory
664  |239.2775  | 0.6840   | +0.7273   | Manastash Ridge Observatory
665  |240.9903  | 0.82215  | +0.56781  | Wallis Observatory
666  |241.1692  | 0.8270   | +0.5604   | Moorpark College Observatory
667  |240.00921 | 0.684483 | +0.726626 | Wanapum Dam
668  |240.82    | 0.821    | +0.568    | San Emigdio Peak
669  |240.8238  | 0.82540  | +0.56279  | Ojai
670  |240.9558  | 0.82775  | +0.55922  | Camarillo
671  |242.00198 | 0.827184 | +0.560523 | Stony Ridge
672  |241.9436  | 0.82794  | +0.55942  | Mount Wilson
673  |242.31783 | 0.826474 | +0.561722 | Table Mountain Observatory, Wrightwood
674  |242.33605 | 0.826464 | +0.561730 | Ford Observatory, Wrightwood
675  |243.13746 | 0.836357 | +0.546831 | Palomar Mountain
676  |242.3907  | 0.83553  | +0.54762  | San Clemente
677  |242.8281  | 0.82746  | +0.56012  | Lake Arrowhead
678  |248.2597  | 0.83352  | +0.55083  | Fountain Hills
679  |244.5367  | 0.85792  | +0.51292  | San Pedro Martir
680  |244.78    | 0.833    | +0.554    | Los Angeles
681  |245.8858  | 0.62954  | +0.77459  | Calgary
682  |247.6381  | 0.79932  | +0.59932  | Kanab
683  |248.9182  | 0.84751  | +0.52922  | Goodricke-Pigott Observatory, Tucson
684  |247.5100  | 0.82512  | +0.56356  | Prescott
685  |247.84    | 0.816    | +0.575    | Williams
686  |249.2092  | 0.84512  | +0.53359  | U. of Minn. Infrared Obs., Mt. Lemmon
687  |248.3473  | 0.81848  | +0.57318  | Northern Arizona University, Flagstaff
688  |248.4645  | 0.81938  | +0.57193  | Lowell Observatory, Anderson Mesa Station
689  |248.2601  | 0.81851  | +0.57319  | U.S. Naval Observatory, Flagstaff
690  |248.3367  | 0.81832  | +0.57344  | Lowell Observatory, Flagstaff
691  |248.39966 | 0.849466 | +0.526479 | Steward Observatory, Kitt Peak-Spacewatch
692  |249.0513  | 0.84679  | +0.53036  | Steward Observatory, Tucson
693  |249.26745 | 0.845317 | +0.533211 | Catalina Station, Tucson
694  |248.9943  | 0.84700  | +0.53009  | Tumamoc Hill, Tucson
695  |248.40533 | 0.849504 | +0.526425 | Kitt Peak
696  |249.1154  | 0.85205  | +0.52249  | Whipple Observatory, Mt. Hopkins
697  |248.3842  | 0.84956  | +0.52629  | Kitt Peak, McGraw-Hill
698  |249.26736 | 0.845316 | +0.533212 | Mt. Bigelow
699  |248.46331 | 0.819380 | +0.571930 | Lowell Observatory-LONEOS
700  |250.3817  | 0.80656  | +0.58960  | Chinle
701  |249.79716 | 0.853823 | +0.519224 | Junk Bond Observatory, Sierra Vista
702  |252.8117  | 0.8305   | +0.5561   | Joint Obs. for cometary research, Socorro
703  |249.26736 | 0.845315 | +0.533213 | Catalina Sky Survey
704  |253.34093 | 0.831869 | +0.553542 | Lincoln Laboratory ETS, New Mexico
705  |254.17942 | 0.841945 | +0.538563 | Apache Point
706  |253.9366  | 0.78294  | +0.62043  | Salida
707  |254.56    | 0.774    | +0.633    | Chamberlin field station
708  |255.0475  | 0.77092  | +0.63520  | Chamberlin Observatory, Denver
709  |254.22882 | 0.840250 | +0.541096 | W & B Observatory, Cloudcroft
710  |254.7336  | 0.77980  | +0.62458  | MPO Observatory, Florissant
711  |255.9785  | 0.86114  | +0.50731  | McDonald Observatory, Fort Davis
712  |255.11867 | 0.778365 | +0.626250 | USAF Academy Observatory, Colorado Springs
713  |254.9897  | 0.76865  | +0.63793  | Thornton
714  |246.8173  | 0.82444  | +0.56439  | Bagdad
715  |253.2759  | 0.84546  | +0.53264  | Jornada Observatory, Las Cruces
716  |255.2489  | 0.77753  | +0.62731  | Palmer Divide Observatory, Colorado Springs
717  |256.0481  | 0.86160  | +0.50636  | Prude Ranch
718  |247.7042  | 0.76004  | +0.64802  | Tooele
719  |253.08608 | 0.829384 | +0.557204 | Etscorn Observatory
720  |259.6261  | 0.90216  | +0.43018  | Universidad de Monterrey
721  |259.7312  | 0.76271  | +0.64476  | Lime Creek
722  |264.4192  | 0.87017  | +0.49110  | Missouri City
723  |263.3300  | 0.82134  | +0.56861  | Cottonwood Observatory, Ada
724  |260.8053  | 0.94388  | +0.33026  | National Observatory, Tacubaya
725  |261.3453  | 0.86883  | +0.49358  | Fair Oaks Ranch
726  |265.6933  | 0.69024  | +0.72120  | Brainerd
727  |262.53872 | 0.813941 | +0.579096 | Zeno Observatory, Edmond
728  |262.6084  | 0.88610  | +0.46194  | Corpus Christi
729  |262.87858 | 0.648804 | +0.758451 | Glenlea Astronomical Observatory, Winnipeg
730  |262.84143 | 0.671544 | +0.738537 | University of North Dakota, Grand Forks
731  |272.6711  | 0.77290  | +0.63244  | Rose-Hulman Observatory, Terre Haute
732  |263.2300  | 0.95591  | +0.29359  | Oaxaca
733  |263.3546  | 0.83802  | +0.54387  | Allen, Texas
734  |263.9986  | 0.77943  | +0.62449  | Farpoint Observatory, Eskridge
735  |264.40640 | 0.872133 | +0.487634 | George Observatory, Needville
736  |263.3357  | 0.87006  | +0.49132  | Houston
737  |275.6633  | 0.8282   | +0.5586   | New Bullpen Observatory, Alpharetta
738  |267.6733  | 0.7788   | +0.6252   | Observatory of the State University of Missouri
739  |265.2440  | 0.77965  | +0.62419  | Sunflower Observatory, Olathe
740  |265.3383  | 0.8511   | +0.5233   | SFA Observatory, Nacogdoches
741  |266.8503  | 0.71493  | +0.69692  | Goodsell Observatory, Northfield
742  |266.31216 | 0.748989 | +0.660428 | Drake University, Des Moines
743  |267.76148 | 0.708545 | +0.703382 | University of Minnesota, Minneapolis
744  |273.8378  | 0.76884  | +0.63735  | Doyan Rose Observatory, Indianapolis
745  |267.1747  | 0.77569  | +0.62906  | Morrison Obervatory, Glasgow
746  |275.2254  | 0.72551  | +0.68597  | Brooks Observatory, Mt. Pleasant
747  |268.9292  | 0.86373  | +0.50227  | Highland Road Park Observatory
748  |268.4680  | 0.75014  | +0.65912  | Van Allen Observatory, Iowa City
749  |276.1642  | 0.82795  | +0.55902  | Oakwood
750  |268.7282  | 0.71059  | +0.70131  | Hobbs Observatory, Fall Creek
751  |269.2439  | 0.78038  | +0.62324  | Lake Saint Louis
752  |275.4647  | 0.82278  | +0.56659  | Puckett Observatory, Mountain Town
753  |270.59069 | 0.731622 | +0.679491 | Washburn Observatory, Madison
754  |271.4432  | 0.73762  | +0.67303  | Yerkes Observatory, Williams Bay
755  |274.6478  | 0.73353  | +0.67743  | Optec Observatory
756  |272.3257  | 0.74361  | +0.66641  | Dearborn Observatory, Evanston
757  |280.0050  | 0.8096   | +0.5851   | High Point
758  |279.2379  | 0.88044  | +0.47257  | BCC Observatory, Cocoa
759  |273.1947  | 0.80946  | +0.58530  | Nashville
760  |273.6048  | 0.77216  | +0.63337  | Goethe Link Observatory, Brooklyn
761  |277.6456  | 0.88138  | +0.47083  | Zephyrhills
762  |274.2008  | 0.70885  | +0.70304  | Four Winds Observatory, Lake Leelanau
763  |280.4658  | 0.72157  | +0.69009  | King City
764  |275.1439  | 0.83264  | +0.55205  | Puckett Observatory, Stone Mountain
765  |275.5775  | 0.77669  | +0.62784  | Cincinnati
766  |275.5167  | 0.73600  | +0.67477  | Michigan State University Obs., East Lansing
767  |276.2697  | 0.74102  | +0.66930  | Ann Arbor
768  |272.32500 | 0.743590 | +0.666435 | Dearborn Observatory
769  |276.9892  | 0.76716  | +0.63936  | McMillin Observatory, Columbus
770  |274.0786  | 0.77573  | +0.62900  | Crescent Moon Observatory, Columbus
771  |277.57    | 0.922    | +0.389    | Boyeros Observatory, Havana
772  |284.0865  | 0.70517  | +0.70669  | Boltwood Observatory, Stittsville
773  |278.4318  | 0.74966  | +0.65966  | Warner and Swasey Observatory, Cleveland
774  |278.9250  | 0.74905  | +0.66039  | Warner and Swasey Nassau Station, Chardon
775  |284.6168  | 0.76029  | +0.64743  | Sayre Observatory, South Bethlehem
776  |284.4669  | 0.73472  | +0.67619  | Foggy Bottom, Hamilton
777  |280.6017  | 0.72454  | +0.68695  | Toronto
778  |279.9778  | 0.76172  | +0.64582  | Allegheny Observatory, Pittsburgh
779  |280.5779  | 0.72219  | +0.68943  | David Dunlap Observatory, Richmond Hill
780  |281.4778  | 0.78868  | +0.61280  | Leander McCormick Observatory, Charlottesville
781  |281.5075  | 1.00045  | -0.00405  | Quito
782  |281.65    | 0.999    | +0.000    | Quito, comet astrograph station
783  |282.02    | 0.783    | +0.622    | Rixeyville
784  |282.2146  | 0.74140  | +0.66895  | Stull Observatory, Alfred University
785  |285.3542  | 0.76323  | +0.64397  | Fitz-Randolph Observatory, Princeton
786  |282.9345  | 0.77906  | +0.62487  | U.S. Naval Obs., Washington (since 1893)
787  |282.9494  | 0.77934  | +0.62451  | U.S. Naval Obs., Washington (before 1893)
788  |284.3667  | 0.76953  | +0.63650  | Mount Cuba Observatory, Wilmington
789  |284.5940  | 0.73188  | +0.67922  | Litchfield Observatory, Clinton
790  |284.2835  | 0.70343  | +0.70840  | Dominion Observatory, Ottawa
791  |284.5236  | 0.76713  | +0.63937  | Flower and Cook Observatory, Philadelphia
792  |288.30    | 0.753    | +0.657    | University of Rhode Island, Quonochontaug
793  |286.2200  | 0.73660  | +0.67407  | Dudley Observatory, Albany (before 1893)
794  |286.1100  | 0.74789  | +0.66161  | Vassar College Observatory, Poughkeepsie
795  |286.0123  | 0.7589   | +0.6491   | Rutherford
796  |286.45    | 0.755    | +0.654    | Stamford
797  |287.0751  | 0.75218  | +0.65676  | Yale Observatory, New Haven
798  |287.0154  | 0.75093  | +0.65822  | Yale Observatory, Bethany
799  |288.8650  | 0.73896  | +0.67150  | Winchester
800  |288.4511  | 0.96006  | -0.28021  | Harvard Observatory, Arequipa
801  |288.44233 | 0.738364 | +0.672183 | Oak Ridge Observatory
802  |288.87164 | 0.739802 | +0.670574 | Harvard Observatory, Cambridge
803  |288.9167  | 0.74543  | +0.66436  | Taunton
804  |289.3121  | 0.83421  | -0.54976  | Santiago-San Bernardo
805  |288.9800  | 0.83997  | -0.54145  | Santiago-Cerro El Roble
806  |289.4513  | 0.83584  | -0.54738  | Santiago-Cerro Calan
807  |289.1941  | 0.86560  | -0.49980  | Cerro Tololo Observatory, La Serena
808  |290.6708  | 0.85098  | -0.52414  | El Leoncito
809  |289.26626 | 0.873440 | -0.486052 | European Southern Observatory, La Silla
810  |288.5154  | 0.73712  | +0.67352  | Wallace Observatory, Westford
811  |289.89565 | 0.752586 | +0.656289 | Maria Mitchell Observatory, Nantucket
812  |288.4543  | 0.83992  | -0.54093  | Vina del Mar
813  |289.3083  | 0.83533  | -0.54805  | Santiago-Quinta Normal (1862-1920)
814  |288.41917 | 0.746007 | +0.663734 | North Scituate
815  |289.3479  | 0.83539  | -0.54799  | Santiago-Santa Lucia (1849-1861)
816  |285.7583  | 0.71645  | +0.69542  | Rand Observatory
817  |288.6104  | 0.74018  | +0.67017  | Sudbury
818  |286.4167  | 0.7040   | +0.7079   | Gemeaux Observatory, Laval
819  |284.3850  | 0.69720  | +0.71451  | Val-des-Bois
820  |295.37581 | 0.930491 | -0.365872 | Tarija
821  |295.45041 | 0.852688 | -0.521032 | Cordoba-Bosque Alegre
822  |295.80137 | 0.854203 | -0.518325 | Cordoba
823  |288.1691  | 0.73715  | +0.67354  | Fitchburg
824  |285.7528  | 0.71641  | +0.69546  | Lake Clear
825  |288.2595  | 0.74033  | +0.67003  | Granville
826  |288.2282  | 0.69312  | +0.71843  | Plessissville
827  |287.5393  | 0.66190  | +0.74710  | Saint-Felicien
828  |288.9758  | 0.74656  | +0.66310  | Assonet
829  |290.6979  | 0.85102  | -0.52411  | Complejo Astronomico El Leoncito
830  |288.5697  | 0.73491  | +0.67590  | Hudson
831  |277.4134  | 0.87191  | +0.48804  | Rosemary Hill Observatory, University of Florida
832  |283.1850  | 0.7653   | +0.6416   | Etters
833  |301.4633  | 0.82373  | -0.56508  | Obs. Astronomico de Mercedes, Buenos Aires
834  |301.5654  | 0.82398  | -0.56473  | Buenos Aires-AAAA
835  |288.6428  | 0.73709  | +0.67354  | Drum Hill Station, Chelmsford
836  |288.5011  | 0.74708  | +0.66252  | Furnace Brook Observatory, Cranston
837  |279.7553  | 0.89228  | +0.44996  | Jupiter
838  |275.8628  | 0.77000  | +0.63596  | Dayton
839  |302.0678  | 0.82097  | -0.56906  | La Plata
840  |276.2833  | 0.73235  | +0.67870  | Flint
841  |279.44233 | 0.796229 | +0.603220 | Martin Observatory, Blacksburg
842  |282.7678  | 0.76901  | +0.63713  | Gettysburg College Observatory
843  |273.0648  | 0.82481  | +0.56357  | Emerald Lane Observatory, Decatur
844  |303.80982 | 0.822499 | -0.566884 | Observatorio Astronomico Los Molinos
845  |283.5058  | 0.73942  | +0.67107  | Ford Observatory, Ithaca
846  |269.65501 | 0.779842 | +0.623926 | Principia Astronomical Observatory, Elsah
847  |275.9750  | 0.7078   | +0.7041   | Lunar Cafe Observator, Flint
848  |237.0219  | 0.72412  | +0.68741  | Tenagra Observatory, Cottage Grove
849  |265.1694  | 0.77927  | +0.62467  | Everstar Observatory, Olathe
850  |274.0802  | 0.81810  | +0.57333  | Cordell-Lorenz Observatory, Sewanee
851  |296.4189  | 0.71284  | +0.69900  | Burke-Gaffney Observatory, Halifax
852  |269.4050  | 0.7805   | +0.6231   | River Moss Observatory, St. Peters
853  |249.1517  | 0.84365  | +0.53544  | Biosphere 2 Observatory
854  |249.17995 | 0.846183 | +0.531351 | Sabino Canyon Observatory, Tucson
855  |266.5383  | 0.7093   | +0.7026   | Wayside Observatory, Minnetonka
856  |242.5540  | 0.8300   | +0.5560   | Riverside
857  |249.3992  | 0.85213  | +0.52204  | Iowa Robotic Observatory, Sonoita
858  |253.7800  | 0.8194   | +0.5719   | Tebbutt Observatory, Edgewood
859  |316.3097  | 0.94132  | -0.33707  | Wykrota Observatory-CEAMIG
860  |313.0347  | 0.92108  | -0.38842  | Valinhos
861  |312.9204  | 0.92253  | -0.38487  | Barao Geraldo
862  |138.5262  | 0.80861  | +0.58658  | Saku
863  |137.18    | 0.807    | +0.588    | Furukawa
864  |130.7533  | 0.84257  | +0.53680  | Kumamoto
865  |285.8792  | 0.74765  | +0.66189  | Emmy Observatory, New Paltz
866  |283.5100  | 0.7784   | +0.6257   | U.S. Naval Academy, Michelson
867  |134.1222  | 0.81671  | +0.57522  | Saji Observatory
868  |135.1359  | 0.83066  | +0.55492  | Hidaka Observatory
869  |133.4298  | 0.83480  | +0.54870  | Tosa
870  |313.17    | 0.934    | -0.359    | Campinas
871  |134.3925  | 0.82256  | +0.56678  | Akou
872  |134.2411  | 0.82904  | +0.55734  | Tokushima
873  |133.7717  | 0.82410  | +0.56455  | Kurashiki Observatory
874  |314.41735 | 0.924359 | -0.380986 | Observatorio do Pico dos Dias, Itajuba
875  |139.2353  | 0.80896  | +0.58593  | Yorii
876  |139.2467  | 0.80762  | +0.58774  | Honjo
877  |139.0828  | 0.81194  | +0.58196  | Okutama
878  |136.9142  | 0.82019  | +0.57019  | Kagiya
879  |137.3535  | 0.81970  | +0.57099  | Tokai
880  |316.7771  | 0.92169  | -0.38664  | Rio de Janeiro
881  |137.2571  | 0.81872  | +0.57230  | Toyota
882  |137.3558  | 0.81842  | +0.57281  | JCPM Oi Station
883  |138.4215  | 0.81986  | +0.57065  | Shizuoka
884  |138.0792  | 0.8187   | +0.5724   | Kawane
885  |138.4667  | 0.82049  | +0.56975  | JCPM Yakiimo Station
886  |138.9367  | 0.81836  | +0.57280  | Mishima
887  |139.3367  | 0.80745  | +0.58798  | Ojima
888  |138.9952  | 0.81885  | +0.57217  | Gekko
889  |140.1427  | 0.80322  | +0.59372  | Karasuyama
890  |140.2500  | 0.8108   | +0.5834   | JCPM Tone Station
891  |140.8633  | 0.78606  | +0.61609  | JCPM Kimachi Station
892  |139.4753  | 0.80852  | +0.58650  | YGCO Hoshikawa and Nagano Stations
893  |140.86222 | 0.786233 | +0.615870 | Sendai Municipal Observatory
894  |138.4476  | 0.81113  | +0.58321  | Kiyosato
895  |140.7203  | 0.78573  | +0.61658  | Hatamae
896  |138.3678  | 0.81132  | +0.58292  | Yatsugatake South Base Observatory
897  |139.4929  | 0.80797  | +0.58725  | YGCO Chiyoda Station
898  |138.1883  | 0.82107  | +0.56899  | Fujieda
899  |142.5500  | 0.7224   | +0.6891   | Toma
900  |135.98994 | 0.819572 | +0.571083 | Moriyama
901  |137.0877  | 0.81664  | +0.57525  | Tajimi
902  |132.2208  | 0.82775  | +0.55922  | Ootake
903  |135.1769  | 0.81738  | +0.57418  | Fukuchiyama and Kannabe
904  |135.12    | 0.824    | +0.565    | Go-Chome and Kobe-Suma
905  |135.9246  | 0.83368  | +0.55040  | Nachi-Katsuura Observatory
906  |145.667   | 0.8113   | -0.5837   | Cobram
907  |144.9758  | 0.79082  | -0.61001  | Melbourne
908  |137.2467  | 0.80352  | +0.59330  | Toyama
909  |237.8717  | 0.6711   | +0.7389   | Snohomish Hilltop Observatory
910  |  6.9267  | 0.72368  | +0.68811  | Caussols-ODAS
911  |282.9233  | 0.7429   | +0.6672   | Collins Observatory, Corning Community College
912  |288.2342  | 0.74769  | +0.66186  | Carbuncle Hill Observatory, Greene
913  |303.8161  | 0.82093  | -0.56912  | Observatorio Kappa Crucis, Montevideo
914  |288.0108  | 0.73809  | +0.67254  | Underwood Observatory, Hubbardston
915  |261.8789  | 0.86861  | +0.49393  | River Oaks Observatory, New Braunfels
916  |272.6836  | 0.77287  | +0.63248  | Oakley Observatory, Terre Haute
917  |237.5522  | 0.68140  | +0.72948  | Pacific Lutheran University Keck Observatory
918  |257.8694  | 0.72071  | +0.69110  | Badlands Observatory, Quinn
919  |248.3183  | 0.8419   | +0.5379   | Desert Beaver Observatory
920  |282.3353  | 0.73161  | +0.67947  | RIT Observatory, Rochester
921  |254.4725  | 0.83988  | +0.54159  | SW Institute for Space Research, Cloudcroft
922  |272.8333  | 0.82335  | +0.56569  | Timberland Observatory, Decatur
923  |284.6300  | 0.76655  | +0.64006  | The Bradstreet Observatory, St. Davids
924  |287.6769  | 0.68988  | +0.72150  | Observatoire du Cegep de Trois-Rivieres
925  |249.8589  | 0.85450  | +0.51811  | Palominas Observatory
926  |249.1209  | 0.85394  | +0.51902  | Tenagra II Observatory, Nogales
927  |270.56194 | 0.735007 | +0.675850 | Madison-YRS
928  |286.6761  | 0.75688  | +0.65136  | Moonedge Observatory, Northport
929  |268.7758  | 0.86319  | +0.50319  | Port Allen
930  |210.41224 | 0.953752 | -0.299638 | S. S. Observatory, Pamatai
931  |210.3842  | 0.95330  | -0.30100  | Puna\'auia
932  |286.57394 | 0.749771 | +0.659497 | John J. McCarthy Obs., New Milford
933  |249.7342  | 0.85383  | +0.51924  | Rockland Observatory, Sierra Vista
934  |242.9572  | 0.83985  | +0.54108  | Poway Valley
935  |282.3394  | 0.77977  | +0.62400  | Wyrick Observatory, Haymarket
936  |263.3792  | 0.77614  | +0.62852  | Ibis Observatory, Manhattan
937  |358.6900  | 0.58065  | +0.81143  | Bradbury Observatory, Stockton-on-Tees
938  |351.6162  | 0.77243  | +0.63299  | Linhaceira
939  |359.6033  | 0.76982  | +0.63619  | Observatorio Rodeno
940  |358.9611  | 0.63199  | +0.77238  | Waterlooville
941  |359.6139  | 0.76988  | +0.63608  | Observatorio Pla D\'Arguines
942  |359.3636  | 0.60413  | +0.79423  | Grantham
943  |355.8664  | 0.63881  | +0.76679  | Peverell
944  |354.08315 | 0.796657 | +0.602418 | Observatorio Geminis, Dos Hermanas
945  |354.3986  | 0.72671  | +0.68474  | Observatorio Monte Deva
946  |  0.7931  | 0.75662  | +0.65170  | Ametlla de Mar
947  |  2.1244  | 0.65268  | +0.75511  | Saint-Sulpice
948  |  0.2189  | 0.61048  | +0.78937  | Pymoor
949  |359.8169  | 0.67454  | +0.73577  | Durtal
950  |342.1176  | 0.87764  | +0.47847  | La Palma
951  |358.2983  | 0.62194  | +0.78046  | Highworth
952  |359.7583  | 0.7787   | +0.6253   | Marxuquera
953  |  2.1339  | 0.74602  | +0.66393  | Montjoia
954  |343.4906  | 0.88148  | +0.47142  | Teide Observatory
955  |350.6739  | 0.78146  | +0.62188  | Sassoeiros
956  |356.1908  | 0.76224  | +0.64530  | Observatorio Pozuelo
957  |359.3506  | 0.71047  | +0.70137  | Merignac
958  |358.96961 | 0.724206 | +0.687273 | Observatoire de Dax
959  |  1.4653  | 0.72596  | +0.68548  | Ramonville Saint Agne
960  |  0.6108  | 0.63016  | +0.77387  | Rolvenden
961  |356.8206  | 0.56112  | +0.82498  | City Observatory, Calton Hill, Edinburgh
962  |359.8188  | 0.77845  | +0.62561  | Gandia
963  |359.7333  | 0.6084   | +0.7909   | Werrington
964  |358.8433  | 0.62471  | +0.77826  | Southend Bradfield
965  |351.4008  | 0.79761  | +0.60118  | Observacao Astronomica no Algarve, Portimao
966  |357.20423 | 0.609591 | +0.790100 | Church Stretton
967  |358.9778  | 0.61508  | +0.78585  | Greens Norton
968  |  0.4250  | 0.6158   | +0.7853   | Haverhill
969  |359.8454  | 0.6235   | +0.7792   | London-Regents Park
970  |  0.4954  | 0.62045  | +0.78162  | Chelmsford
971  |350.81249 | 0.781336 | +0.622040 | Lisbon
972  |357.5833  | 0.54359  | +0.83656  | Dun Echt
973  |359.6671  | 0.62271  | +0.77983  | Harrow
974  |  8.9220  | 0.71542  | +0.69637  | Genoa
975  |359.6333  | 0.77292  | +0.63239  | Observatorio Astronomico de Valencia
976  |358.48    | 0.612    | +0.788    | Leamington Spa
977  |351.5483  | 0.58660  | +0.80717  | Markree
978  |357.24541 | 0.588685 | +0.805673 | Conder Brow
979  |358.6697  | 0.62896  | +0.77485  | South Wonston
980  |357.2200  | 0.58864  | +0.80570  | Lancaster
981  |353.3522  | 0.58409  | +0.80898  | Armagh
982  |353.6621  | 0.59771  | +0.79904  | Dunsink Observatory, Dublin
983  |353.79525 | 0.805167 | +0.591067 | San Fernando
984  |357.26975 | 0.631671 | +0.772658 | Eastfield
985  |357.5317  | 0.60801  | +0.79130  | Telford
986  |358.75    | 0.624    | +0.779    | Ascot
987  |355.3735  | 0.58658  | +0.80721  | Isle of Man Observatory, Foxdale
988  |355.7060  | 0.56225  | +0.82421  | Glasgow
989  |357.69    | 0.600    | +0.797    | Wilfred Hall Observatory, Preston
990  |356.3121  | 0.76260  | +0.64487  | Madrid
991  |356.9278  | 0.59750  | +0.79919  | Liverpool (since 1867)
992  |356.9995  | 0.5973   | +0.7993   | Liverpool (before 1867)
993  |357.49556 | 0.629975 | +0.774031 | Woolston Observatory
994  |359.3878  | 0.62827  | +0.77540  | Godalming
995  |358.4177  | 0.57819  | +0.81319  | Durham
996  |358.7483  | 0.62025  | +0.78179  | Oxford
997  |359.15    | 0.619    | +0.783    | Hartwell
998  |359.75753 | 0.622254 | +0.780206 | London-Mill Hill
999  |359.4725  | 0.71033  | +0.70153  | Bordeaux-Floirac
A00  |  0.3770  | 0.62475  | +0.77821  | Gravesend
A01  |  0.7441  | 0.74414  | +0.66596  | Masia Cal Maciarol Modul 2
A02  |  0.7441  | 0.74414  | +0.66596  | Masia Cal Maciarol Modul 8
A03  |  1.4000  | 0.7541   | +0.6546   | Torredembarra
A04  |  1.7181  | 0.72206  | +0.68956  | Saint-Caprais
A05  |  1.8175  | 0.72721  | +0.68417  | Belesta
A06  |  2.4417  | 0.74922  | +0.66012  | Mataro
A07  |  2.7444  | 0.66070  | +0.74815  | Gretz-Armainvilliers
A08  |  2.8847  | 0.72735  | +0.68406  | Malibert
A09  |  1.1803  | 0.65037  | +0.75711  | Quincampoix
A10  |  1.9281  | 0.75278  | +0.65613  | Observatorio Astronomico de Corbera
A11  |  2.4718  | 0.63222  | +0.77219  | Wormhout
A12  |  8.74768 | 0.703404 | +0.708434 | Stazione Astronomica di Sozzago
A13  |  7.1394  | 0.68632  | +0.72501  | Observatoire Naef, Marly
A14  |  5.1864  | 0.72028  | +0.69143  | Les Engarouines Observatory
A15  |  6.7972  | 0.61903  | +0.78275  | Josef Bresser Sternwarte, Borken
A16  |  7.1922  | 0.68622  | +0.72511  | Tentlingen
A17  |  8.68152 | 0.650125 | +0.757317 | Guidestar Observatory, Weinheim
A18  |  7.1761  | 0.62342  | +0.77928  | Herne
A19  |  7.0744  | 0.63164  | +0.77267  | Koln
A20  |  7.51887 | 0.605274 | +0.793357 | Sogel
A21  |  8.0581  | 0.63667  | +0.76862  | Irmtraut
A22  |  8.6531  | 0.64877  | +0.75848  | Starkenburg Sternwarte-SOHAS
A23  |  8.6677  | 0.65027  | +0.75719  | Weinheim
A24  |  8.9481  | 0.69995  | +0.71185  | New Millennium Observatory, Mozzate
A25  |  9.1925  | 0.70104  | +0.71077  | Nova Milanese
A26  |  8.65736 | 0.646597 | +0.760303 | Darmstadt
A27  | 10.3236  | 0.61823  | +0.78341  | Eridanus Observatory, Langelsheim
A28  | 10.3342  | 0.67398  | +0.73642  | Kempten
A29  | 10.6733  | 0.72369  | +0.68782  | Santa Maria a Monte
A30  | 11.22308 | 0.700397 | +0.711555 | Crespadoro
A31  | 11.4186  | 0.70024  | +0.71155  | Corcaroli Observatory
A32  | 10.5517  | 0.58423  | +0.80887  | Panker
A33  | 11.0157  | 0.63231  | +0.77217  | Volkssternwarte Kirchheim
A34  | 10.7911  | 0.64944  | +0.75793  | Grosshabersdorf
A35  | 12.8978  | 0.63511  | +0.76995  | Hormersdorf Observatory
A36  |  9.7911  | 0.69856  | +0.71340  | Ganda di Aviatico
A37  | 13.6634  | 0.61128  | +0.78877  | Mueggelheim
A38  | 13.3747  | 0.74706  | +0.66266  | Campocatino Automated Telescope, Collepardo
A39  | 12.4186  | 0.63084  | +0.77336  | Altenburg
A40  | 14.4978  | 0.81104  | +0.58306  | Pieta
A41  | 14.5911  | 0.69290  | +0.71871  | Rezman Observatory, Kamnik
A42  |  9.5019  | 0.61280  | +0.78760  | Gehrden
A43  | 13.0897  | 0.61201  | +0.78821  | Inastars Observatory, Potsdam (before 2006)
A44  | 13.6972  | 0.66609  | +0.74346  | Altschwendt
A45  |  9.3620  | 0.62525  | +0.77786  | Karrenkneul
A46  | 16.5825  | 0.65349  | +0.75447  | Lelekovice
A47  | 16.6031  | 0.75962  | +0.64829  | Matera
A48  | 10.8885  | 0.70401  | +0.70782  | Povegliano Veronese
A49  | 17.6372  | 0.50372  | +0.86098  | Uppsala-Angstrom
A50  | 28.9973  | 0.64407  | +0.76245  | Andrushivka Astronomical Observatory
A51  | 18.6667  | 0.5837   | +0.8093   | Danzig
A52  | 18.7553  | 0.67756  | +0.73304  | Etyek
A53  | 10.6883  | 0.70294  | +0.70889  | Peschiera del Garda
A54  | 16.6217  | 0.60828  | +0.79108  | Ostrorog
A55  | 13.1181  | 0.73871  | +0.67204  | Osservatorio Astronomico Vallemare di Borbona
A56  | 10.3197  | 0.71406  | +0.69784  | Parma
A57  | 11.1031  | 0.72364  | +0.68791  | Osservatorio Astron. Margherita Hack, Firenze
A58  |  2.4694  | 0.66135  | +0.74758  | Observatoire de Chalandray-Canotiers
A59  | 12.9071  | 0.64123  | +0.76490  | Karlovy Vary Observatory
A60  | 20.8106  | 0.84556  | -0.53260  | YSTAR-NEOPAT Station, Sutherland
A61  |  8.8581  | 0.70949  | +0.70238  | Tortona
A62  |  9.2301  | 0.66233  | +0.74678  | Aichtal
A63  |  4.7567  | 0.69879  | +0.71298  | Cosmosoz Obs., Tassin la Demi Lune
A64  |  6.1151  | 0.69034  | +0.72132  | Couvaloup de St-Cergue
A65  |  2.4083  | 0.71939  | +0.69239  | Le Couvent de Lentin
A66  | 10.3161  | 0.72613  | +0.68526  | Stazione Osservativa Astronomica, Livorno
A67  |  7.6785  | 0.71665  | +0.69522  | Chiusa di Pesio
A68  |  9.6533  | 0.57755  | +0.81362  | Swedenborg Obs., Bockholmwik
A69  | 11.3300  | 0.7287   | +0.6826   | Osservatorio Palazzo Bindi Sergardi
A70  | 25.2033  | 0.42654  | +0.90144  | Lumijoki
A71  | 15.4533  | 0.66486  | +0.74459  | Stixendorf
A72  | 13.6222  | 0.62904  | +0.77481  | Radebeul Observatory
A73  | 16.2895  | 0.66788  | +0.74183  | Penzing Astrometric Obs., Vienna
A74  |  8.76240 | 0.641951 | +0.764216 | Bergen-Enkheim Observatory
A75  |  2.1861  | 0.75124  | +0.65783  | Fort Pius Observatory, Barcelona
A76  | 20.8356  | 0.66948  | +0.74037  | Andromeda Observatory, Miskolc
A77  |  5.6475  | 0.72058  | +0.69119  | Observatoire Chante-Perdrix, Dauban
A78  | 11.71509 | 0.730944 | +0.680264 | Stia
A79  | 23.84340 | 0.743686 | +0.666622 | Zvezdno Obshtestvo Observatory, Plana
A80  | 14.1222  | 0.61408  | +0.78662  | Lindenberg Observatory
A81  | 12.4033  | 0.74578  | +0.66397  | Balzaretto Observatory, Rome
A82  | 13.8744  | 0.70037  | +0.71148  | Osservatorio Astronomico di Trieste
A83  | 29.9969  | 0.45945  | +0.88525  | Jakokoski Observatory
A84  | 30.3333  | 0.80175  | +0.59632  | TUBITAK National Observatory
A85  | 30.8065  | 0.68881  | +0.72252  | Odessa Astronomical Observatory, Kryzhanovka
A86  |  4.3547  | 0.70170  | +0.71021  | Albigneux
A87  |  8.7662  | 0.64935  | +0.75798  | Rimbach
A88  |  8.90133 | 0.714961 | +0.696835 | Bolzaneto
A89  | 10.3308  | 0.67421  | +0.73621  | Sterni Observatory, Kempten
A90  |  2.1431  | 0.75120  | +0.65788  | Sant Gervasi Observatory, Barcelona
A91  | 26.5997  | 0.46678  | +0.88143  | Hankasalmi Observatory
A92  | 26.0927  | 0.71506  | +0.69673  | Urseanu Observatory, Bucharest
A93  | 10.4189  | 0.72222  | +0.68935  | Lucca
A94  | 13.4577  | 0.69641  | +0.71526  | Cormons
A95  | 28.3892  | 0.46584  | +0.88193  | Taurus Hill Observatory, Varkaus
A96  | 16.2867  | 0.66656  | +0.74303  | Klosterneuburg
A97  | 16.4219  | 0.66646  | +0.74308  | Stammersdorf
A98  | 30.2092  | 0.58214  | +0.81040  | Observatory Mazzarot-1, Baran\'
A99  | 10.8589  | 0.69978  | +0.71223  | Osservatorio del Monte Baldo
B00  |  2.5767  | 0.66289  | +0.74622  | Savigny-le-Temple
B01  |  8.4464  | 0.64117  | +0.76499  | Taunus Observatory, Frankfurt
B02  | 20.6566  | 0.63224  | +0.77224  | Kielce
B03  | 16.2698  | 0.66759  | +0.74211  | Alter Satzberg, Vienna
B04  |  7.47851 | 0.698677 | +0.713400 | OAVdA, Saint-Barthelemy
B05  | 37.8831  | 0.57134  | +0.81800  | Ka-Dar Observatory, Barybino
B06  |  2.53372 | 0.747520 | +0.662058 | Montseny Astronomical Observatory
B07  |  9.0033  | 0.69383  | +0.71778  | Camorino
B08  | 11.3807  | 0.71498  | +0.69683  | San Lazzaro di Savena
B09  | 10.6708  | 0.72550  | +0.68593  | Capannoli
B10  |  5.5150  | 0.71564  | +0.69631  | Observatoire des Baronnies Provencales, Moydans
B11  | 10.6286  | 0.69881  | +0.71318  | Osservatorio Cima Rest, Magasa
B12  |  4.4906  | 0.61329  | +0.78721  | Koschny Observatory, Noordwijkerhout
B13  |  8.9311  | 0.69950  | +0.71231  | Osservatorio di Tradate
B14  |  9.0758  | 0.71061  | +0.70138  | Ca del Monte
B15  | 13.0129  | 0.61111  | +0.78890  | Inastars Observatory, Potsdam (since 2006)
B16  | 36.9547  | 0.56382  | +0.82317  | 1st Moscow Gymnasium Observatory, Lipki
B17  | 33.16280 | 0.705588 | +0.706256 | AZT-8 Evpatoria
B18  | 42.5008  | 0.72958  | +0.68232  | Terskol
B19  |  2.4414  | 0.74963  | +0.65966  | Observatorio Iluro, Mataro
B20  |  2.2636  | 0.75026  | +0.65897  | Observatorio Carmelita, Tiana
B21  | 13.4744  | 0.66335  | +0.74589  | Gaisberg Observatory, Schaerding
B22  |  0.7441  | 0.74412  | +0.66598  | Observatorio d\'Ager
B23  | 10.9710  | 0.70124  | +0.71069  | Fiamene
B24  |  2.5983  | 0.66317  | +0.74598  | Cesson
B25  | 15.0557  | 0.79386  | +0.60614  | Catania
B26  |  5.6667  | 0.72204  | +0.68966  | Observatoire des Terres Blanches, Reillanne
B27  | 14.1544  | 0.66425  | +0.74516  | Picard Observatory, St. Veit
B28  | 13.1836  | 0.69466  | +0.71696  | Mandi Observatory, Pagnacco
B29  |  0.6701  | 0.75801  | +0.65008  | L\'Ampolla Observatory, Tarragona
B30  | 16.5689  | 0.60872  | +0.79074  | Szamotuly-Galowo
B31  | 20.8108  | 0.84560  | -0.53254  | Southern African Large Telescope, Sutherland
B32  | 12.9486  | 0.63467  | +0.77030  | Gelenau
B33  | 10.7783  | 0.72588  | +0.68555  | Libbiano Observatory, Peccioli
B34  | 33.7258  | 0.81748  | +0.57405  | Green Island Observatory, Gecitkale
B35  | 35.0317  | 0.84991  | +0.52524  | Bareket Observatory, Macabim
B36  | 13.7125  | 0.66684  | +0.74278  | Redshed Observatory, Kallham
B37  |  2.25934 | 0.748338 | +0.661147 | Obs. de L\' Ametlla del Valles, Barcelona
B38  | 11.85746 | 0.724995 | +0.686523 | Santa Mama
B39  |  8.9072  | 0.69950  | +0.71231  | Tradate
B40  | 15.0706  | 0.79331  | +0.60690  | Skylive Observatory, Catania
B41  | 17.6925  | 0.65449  | +0.75362  | Zlin Observatory
B42  | 30.3275  | 0.57401  | +0.81614  | Vitebsk
B43  |  7.3089  | 0.63404  | +0.77073  | Hennef
B44  |  5.5906  | 0.71772  | +0.69419  | Eygalayes
B45  | 19.9356  | 0.64169  | +0.76447  | Narama
B46  | 12.05439 | 0.714373 | +0.697420 | Sintini Observatory, Alfonsine
B47  | 24.7503  | 0.49826  | +0.86413  | Metsala Observatory, Espoo
B48  |  6.5981  | 0.61901  | +0.78275  | Bocholt
B49  |  2.11250 | 0.749498 | +0.659844 | Paus Observatory, Sabadell
B50  |  8.2767  | 0.65808  | +0.75045  | Corner Observatory, Durmersheim
B51  |  7.06669 | 0.725612 | +0.685830 | Vallauris
B52  |  2.99725 | 0.741344 | +0.668883 | Observatorio El Far
B53  | 12.3536  | 0.74572  | +0.66404  | Casal Lumbroso, Rome
B54  |  0.7439  | 0.74413  | +0.66597  | Ager
B55  | 12.87600 | 0.689553 | +0.721975 | Comeglians
B56  |  2.44935 | 0.749614 | +0.659663 | Observatorio Sant Pere, Mataro
B57  |  2.22439 | 0.749316 | +0.660019 | Laietania Observatory, Parets del Valles
B58  | 19.02529 | 0.676156 | +0.734318 | Polaris Observatory, Budapest
B59  |  6.87881 | 0.619231 | +0.782586 | Borken
B60  |  7.17531 | 0.612824 | +0.787576 | Deep Sky Observatorium, Bad Bentheim
B61  |  2.04350 | 0.750575 | +0.658604 | Valldoreix Obs.,Sant Cugat del Valles
B62  |  9.68531 | 0.609275 | +0.790314 | Brelingen
B63  | 20.10799 | 0.642589 | +0.763698 | Solaris Observatory, Luczanowice
B64  | 24.88779 | 0.491587 | +0.867927 | Slope Rock Observatory, Hyvinkaa
B65  | 24.3878  | 0.49864  | +0.86391  | Komakallio Observatory, Kirkkonummi
B66  |  9.00693 | 0.710595 | +0.701332 | Osservatorio di Casasco
B67  |  9.22419 | 0.685858 | +0.725582 | Sternwarte Mirasteilas, Falera
B68  | 13.53950 | 0.693458 | +0.718372 | Mount Matajur Observatory
B69  |  9.01719 | 0.662152 | +0.746956 | Owls and Ravens Observatory, Holzgerlingen
B70  |  2.4937  | 0.74787  | +0.66165  | Sant Celoni
B71  |  1.5213  | 0.75363  | +0.65510  | Observatorio El Vendrell
B72  |  7.6811  | 0.63470  | +0.77022  | Soerth
B73  |  8.98503 | 0.662074 | +0.747029 | Mauren Valley Observatory, Holzgerlingen
B74  |  1.10536 | 0.747550 | +0.662053 | Santa Maria de Montmagastrell
B75  |  8.80519 | 0.701074 | +0.710741 | Stazione Astronomica Betelgeuse, Magnago
B76  | 13.8944  | 0.63019  | +0.77390  | Sternwarte Schonfeld, Dresden
B77  |  7.95083 | 0.677934 | +0.732833 | Schafmatt Observatory, Aarau
B78  | 14.12811 | 0.670885 | +0.739158 | Astrophoton Observatory, Audorf
B79  | 11.20990 | 0.700480 | +0.711457 | Marana Observatory
B80  | 12.74126 | 0.742254 | +0.667919 | Osservatorio Astronomico Campomaggiore
B81  |  2.8990  | 0.76967  | +0.63634  | Caimari
B82  |  9.9716  | 0.64613  | +0.76072  | Maidbronn
B83  |  5.79769 | 0.706034 | +0.705851 | Gieres
B84  |  3.53775 | 0.622812 | +0.779749 | Cyclops Observatory, Oostkapelle
B85  |  6.51011 | 0.604962 | +0.793587 | Beilen Observatory
B86  |  7.45561 | 0.625931 | +0.777324 | Sternwarte Hagen
B87  |  2.7701  | 0.74295  | +0.66715  | Banyoles
B88  |  8.29681 | 0.710570 | +0.701309 | Bigmuskie Observatory, Mombercelli
B89  |  2.2619  | 0.75018  | +0.65907  | Observatori Astronomic de Tiana
B90  | 13.29686 | 0.693994 | +0.717600 | Malina River Observatory, Povoletto
B91  |  7.25544 | 0.672149 | +0.737995 | Bollwiller
B92  |  0.27539 | 0.681073 | +0.729781 | Chinon
B93  |  6.47856 | 0.607102 | +0.791962 | Hoogeveen
B94  | 34.2817  | 0.47422  | +0.87748  | Petrozavodsk
B95  |  8.15450 | 0.602437 | +0.795492 | Achternholt
B96  |  4.31031 | 0.628378 | +0.775301 | Brixiis Observatory, Kruibeke
B97  |  6.1118  | 0.61688  | +0.78442  | Sterrenwacht Andromeda, Meppel
B98  | 11.31300 | 0.728746 | +0.682563 | Siena
B99  |  0.7443  | 0.74413  | +0.66598  | Santa Coloma de Gramenet
C00  | 30.5150  | 0.55583  | +0.82853  | Velikie Luki
C01  | 13.92293 | 0.630265 | +0.773855 | Lohrmann-Observatorium, Triebenberg
C02  |  2.5305  | 0.74740  | +0.66218  | Observatorio Royal Park
C03  | 24.96114 | 0.492892 | +0.867190 | Clayhole Observatory, Jokela
C04  | 37.6331  | 0.65998  | +0.74878  | Kramatorsk
C05  | 12.1153  | 0.68023  | +0.73088  | Konigsleiten
C06  | 92.9744  | 0.56032  | +0.82553  | Krasnoyarsk
C07  |  0.7442  | 0.74413  | +0.66597  | Anysllum Observatory, Ager
C08  | 17.3761  | 0.50302  | +0.86138  | Fiby
C09  |  3.80397 | 0.722660 | +0.688932 | Rouet
C10  |  3.42622 | 0.661039 | +0.747874 | Maisoncelles
C11  | 14.0901  | 0.64091  | +0.76509  | City Observatory, Slany
C12  |  2.1107  | 0.74967  | +0.65964  | Berta Observatory, Sabadell
C13  |  9.10031 | 0.698332 | +0.713430 | Como
C14  | 15.96700 | 0.668463 | +0.741344 | Sky Vistas Observatory, Eichgraben
C15  |132.1656  | 0.72418  | +0.68737  | ISON-Ussuriysk Observatory
C16  | 11.57261 | 0.673687 | +0.736691 | Isarwinkel Observatory, Bad Tolz
C17  |  0.74381 | 0.744124 | +0.665978 | Observatorio Joan Roget, Ager
C18  |  3.60400 | 0.634888 | +0.770037 | Frasnes-Lez-Anvaing
C19  |  5.4231  | 0.71591  | +0.69599  | ROSA Observatory, Vaucluse
C20  | 42.66191 | 0.723859 | +0.688104 | Kislovodsk Mtn. Astronomical Stn., Pulkovo Obs.
C21  |  0.74383 | 0.744124 | +0.665978 | Observatorio Via Lactea, Ager
C22  | 12.9599  | 0.63858  | +0.76717  | Oberwiesenthal
C23  |  5.15439 | 0.628694 | +0.775052 | Olmen
C24  |  9.1331  | 0.70036  | +0.71145  | Seveso
C25  | 13.55806 | 0.739310 | +0.671605 | Pulkovo Observatory Station, Campo Imperatore
C26  |  4.49928 | 0.614813 | +0.786032 | Levendaal Observatory, Leiden
C27  |  1.35302 | 0.748763 | +0.660753 | Pallerols
C28  |  7.48300 | 0.624224 | +0.778652 | Wellinghofen
C29  |  1.07889 | 0.737202 | +0.673777 | Observatori Astronomic de Les Planes de Son
C30  | 35.3425  | 0.47988  | +0.87440  | Petrozavodsk University Obs., Sheltozero Stn.
C31  |  6.9825  | 0.62777  | +0.77581  | Sternwarte Neanderhoehe Hochdahl e.V., Erkrath
C32  | 41.4258  | 0.72496  | +0.68694  | Ka-Dar Observatory, TAU Station, Nizhny Arkhyz
C33  |  2.8989  | 0.76967  | +0.63634  | Observatorio CEAM, Caimari
C34  | 19.0108  | 0.69361  | +0.71796  | Baja Astronomical Observatory
C35  |  2.0349  | 0.74927  | +0.66012  | Terrassa
C36  | 30.3086  | 0.58230  | +0.81028  | Starry Wanderer Observatory, Baran\'
C37  |  1.01830 | 0.614242 | +0.786484 | Stowupland
C38  |  7.64911 | 0.703322 | +0.708581 | Varuna Observatory, Cuorgne
C39  |  5.7992  | 0.61929  | +0.78253  | Nijmegen
C40  | 39.0308  | 0.70806  | +0.70380  | Kuban State University Astrophysical Observatory
C41  | 42.66126 | 0.723857 | +0.688105 | MASTER-II Observatory, Kislovodsk
C42  | 87.1778  | 0.72711  | +0.68469  | Xingming Observatory, Mt. Nanshan
C43  | 14.2792  | 0.62451  | +0.77842  | Hoyerswerda
C44  |  9.02239 | 0.696268 | +0.715567 | A. Volta Observatory, Lanzo d\'Intelvi
C45  | 12.40639 | 0.744413 | +0.665514 | La Giustiniana
C46  | 69.12219 | 0.576620 | +0.814296 | Horizon Observatory, Petropavlovsk
C47  | 15.2356  | 0.66017  | +0.74871  | Nonndorf
C48  |100.9214  | 0.62235  | +0.78051  | Sayan Solar Observatory, Irkutsk
C49  |          |          |           | STEREO-A
C50  |          |          |           | STEREO-B
C51  |          |          |           | WISE
C52  |          |          |           | Swift
C53  |          |          |           | NEOSSat
C54  |          |          |           | New Horizons
C55  |          |          |           | Kepler
C56  |          |          |           | LISA-Pathfinder
C57  |          |          |           | TESS
C60  |  7.06926 | 0.634261 | +0.770545 | Argelander Institute for Astronomy Obs., Bonn
C61  |  2.58202 | 0.658892 | +0.749723 | Chelles
C62  | 11.3467  | 0.68967  | +0.72175  | Eurac Observatory, Bolzano
C63  |  9.9797  | 0.69363  | +0.71819  | Giuseppe Piazzi Observatory, Ponte in Valtellina
C64  | 15.28439 | 0.671380 | +0.738819 | Puchenstuben
C65  |  0.72965 | 0.743841 | +0.666482 | Observatori Astronomic del Montsec
C66  |  2.8050  | 0.77084  | +0.63493  | Observatorio El Cielo de Consell
C67  | 12.2199  | 0.59747  | +0.79922  | Gnevsdorf
C68  | 23.89339 | 0.789058 | +0.612302 | Ellinogermaniki Agogi Observatory, Pallini
C69  | 13.3611  | 0.65835  | +0.75036  | Bayerwald Sternwarte, Neuhuette
C70  |  4.49775 | 0.614779 | +0.786055 | Uiterstegracht Station, Leiden
C71  |  1.4892  | 0.74780  | +0.66186  | Sant Marti Sesgueioles
C72  | 12.8717  | 0.74621  | +0.66358  | Palestrina
C73  | 28.0325  | 0.70312  | +0.70870  | Galati Observatory
C74  |  0.7449  | 0.74412  | +0.66598  | Observatorio El Teatrillo de Lyra, Ager
C75  | 13.2225  | 0.69384  | +0.71776  | Whitestar Observatory, Borgobello
C76  |  0.74431 | 0.744127 | +0.665974 | Observatorio Estels, Ager
C77  |  7.4535  | 0.71589  | +0.69600  | Bernezzo Observatory
C78  | 34.81242 | 0.849698 | +0.525519 | Martin S. Kraar Observatory, Rehovot
C79  |  2.7855  | 0.74801  | +0.66147  | Roser Observatory, Blanes
C80  | 39.7651  | 0.67959  | +0.73115  | Don Astronomical Observatory, Rostov-on-Don
C81  | 10.84098 | 0.693023 | +0.718872 | Dolomites Astronomical Observatory
C82  | 14.35763 | 0.760171 | +0.647611 | Osservatorio Astronomico Nastro Verde, Sorrento
C83  | 91.8425  | 0.55930  | +0.82626  | Badalozhnyj Observatory
C84  |  2.24372 | 0.750690 | +0.658447 | Badalona
C85  |  1.2408  | 0.77939  | +0.62448  | Observatorio Cala d\'Hort, Ibiza
C86  |  2.7813  | 0.74801  | +0.66147  | Blanes
C87  |  8.7689  | 0.64913  | +0.75817  | Rimbach
C88  | 11.18331 | 0.729763 | +0.681487 | Montarrenti Observatory, Siena
C89  | 21.55558 | 0.730958 | +0.680397 | Astronomical Station Vidojevica
C90  |  1.05181 | 0.754546 | +0.654066 | Vinyols
C91  | 11.22621 | 0.717604 | +0.694214 | Montevenere Observatory, Monzuno
C92  | 13.60995 | 0.727425 | +0.683915 | Valdicerro Observatory, Loreto
C93  | 13.4064  | 0.74042  | +0.67004  | Bellavista Observatory, L\'Aquila
C94  |103.0670  | 0.61962  | +0.78241  | MASTER-II Observatory, Tunka
C95  |  5.71239 | 0.721401 | +0.690345 | SATINO Remote Observatory, Haute Provence
C96  | 13.8786  | 0.73544  | +0.67537  | OACL Observatory, Mosciano Sant Angelo
C97  | 57.97633 | 0.916656 | +0.398354 | Al-Fulaij Observatory, Oman
C98  | 11.1764  | 0.72335  | +0.68818  | Osservatorio Casellina, Scandicci
C99  |  2.89631 | 0.746295 | +0.663419 | Observatori Can Roig, Llagostera
D00  | 42.6536  | 0.72388  | +0.68809  | ISON-Kislovodsk Observatory
D01  | 23.93061 | 0.495920 | +0.865471 | Andean Northern Observatory, Nummi-Pusula
D02  |  2.05189 | 0.751414 | +0.657647 | Observatori Petit Sant Feliu
D03  | 10.5889  | 0.71522  | +0.69670  | Rantiga Osservatorio, Tincana
D04  | 38.8569  | 0.70960  | +0.70225  | Krasnodar
D05  | 42.50005 | 0.729580 | +0.682314 | ISON-Terskol Observatory
D06  | 12.77017 | 0.747232 | +0.662472 | Associazione Tuscolana di Astronomia, Domatore
D07  |  6.2094  | 0.62867  | +0.77508  | Wegberg
D08  |  8.9191  | 0.69024  | +0.72136  | Ghezz Observatory, Leontica
D09  |  5.6794  | 0.63139  | +0.77287  | Observatory Gromme, Maasmechelen
D10  |  8.90181 | 0.661976 | +0.747123 | Gaertringen
D11  |  5.62797 | 0.723085 | +0.688551 | Bastidan Observatory
D12  | 11.33806 | 0.690580 | +0.720900 | Filzi School Observatory, Laives
D13  | 11.56369 | 0.738665 | +0.671859 | Cat\'s Eye Observatory
D14  |113.3231  | 0.92000  | +0.39061  | Nanchuan Observatory, Guangzhou
D16  |113.96422 | 0.925155 | +0.378330 | Po Leung Kuk Observatory, Tuen Mun
D17  |114.2200  | 0.9245   | +0.3799   | Hong Kong
D18  |114.3580  | 0.86219  | +0.50490  | Mt. Guizi Observatory
D19  |114.32300 | 0.924955 | +0.378843 | Hong Kong Space Museum, Tsimshatsui
D20  |115.71311 | 0.854733 | -0.517343 | Zadko Observatory, Wallingup Plain
D21  |115.8150  | 0.8492   | -0.5263   | Shenton Park
D22  |115.81667 | 0.849044 | -0.526558 | UWA Observatory, Crawley
D24  |117.08969 | 0.844095 | -0.534439 | LightBuckets Observatory, Pingelly
D25  |117.08978 | 0.844104 | -0.534424 | Tzec Maun Observatory, Pingelly (before 2010)
D29  |118.4639  | 0.84204  | +0.53767  | Purple Mountain Observatory, XuYi Station
D32  |119.59975 | 0.862770 | +0.504193 | JiangNanTianChi Observatory, Mt. Getianling
D33  |120.6982  | 0.92730  | +0.37308  | Kenting Observatory, Checheng
D34  |120.7839  | 0.92796  | +0.37148  | Kenting Observatory, Hengchun
D35  |120.8736  | 0.91818  | +0.39597  | Lulin Observatory
D36  |120.8897  | 0.91801  | +0.39625  | Tataka, Mt. Yu-Shan National Park
D37  |120.87325 | 0.918176 | +0.395972 | Lulin Widefield Telescope, Mt. Lulin
D39  |122.04961 | 0.793971 | +0.605943 | Shandong University Observatory, Weihai
D44  |124.13928 | 0.911427 | +0.410157 | Ishigakijima Astronomical Observatory
D53  |127.4820  | 0.63981  | +0.76600  | ISON-Blagoveschensk Observatory
D54  |127.4830  | 0.63981  | +0.76601  | MASTER-II Observatory, Blagoveshchensk
D55  |127.9747  | 0.79571  | +0.60370  | Kangwon Science High School Observatory, Ksho
D57  |128.88744 | 0.817572 | +0.573996 | Gimhae Astronomical Observatory, Uhbang-dong
D58  |129.02500 | 0.818419 | +0.572736 | KSA SEM Observatory, Danggam-dong
D61  |134.9131  | 0.82671  | +0.56075  | Suntopia Marina, Sumoto
D62  |130.4494  | 0.83676  | +0.54575  | Miyaki-Argenteus
D70  |133.4686  | 0.83505  | +0.54834  | Tosa
D74  |134.6819  | 0.83041  | +0.55530  | Nakagawa
D78  |136.13281 | 0.822378 | +0.567077 | Iga-Ueno
D79  |138.63092 | 0.821212 | -0.568722 | YSVP Observatory, Vale Park
D80  |138.9728  | 0.80392  | +0.59297  | Gumma Astronomical Observatory
D81  |138.2239  | 0.80310  | +0.59394  | Nagano
D82  |137.6317  | 0.83058  | -0.55504  | Wallaroo
D83  |138.4681  | 0.80501  | +0.59161  | Miwa
D84  |138.5086  | 0.8192   | -0.5716   | Hallet Cove
D85  |138.6597  | 0.82186  | -0.56782  | Ingle Farm
D86  |138.6407  | 0.83075  | -0.55490  | Penwortham
D87  |138.5500  | 0.82079  | -0.56931  | Brooklyn Park
D88  |139.3142  | 0.81635  | +0.57562  | Hiratsuka
D89  |140.3383  | 0.7871   | +0.6149   | Yamagata
D90  |140.3420  | 0.82728  | -0.55991  | RAS Observatory, Moorook
D91  |140.8250  | 0.79261  | +0.60775  | Adati
D92  |140.94638 | 0.782920 | +0.620047 | Osaki
D93  |140.75516 | 0.786291 | +0.615826 | Sendai Astronomical Observatory
D94  |139.9962  | 0.80351  | +0.59335  | Takanezawa, Tochigi
D95  |141.0680  | 0.78035  | +0.62325  | Kurihara
D96  |140.34216 | 0.827287 | -0.559905 | Tzec Maun Observatory, Moorook
D97  |140.5700  | 0.82752  | -0.55956  | Berri
E00  |144.2089  | 0.79902  | -0.59937  | Castlemaine
E01  |144.54142 | 0.798618 | -0.599924 | Barfold
E03  |145.3822  | 0.78756  | -0.61419  | RAS Observatory, Officer
E04  |145.7403  | 0.96545  | +0.25977  | Pacific Sky Observatory, Saipan
E05  |145.69721 | 0.957625 | -0.287092 | Earl Hill Observatory, Trinity Beach
E07  |148.99889 | 0.820544 | -0.569830 | Murrumbateman
E08  |149.33431 | 0.855971 | -0.515472 | Wobblesock Observatory, Coonabarabran
E09  |149.0814  | 0.85551  | -0.51630  | Oakley Southern Sky Observatory, Coonabarabran
E10  |149.07028 | 0.855623 | -0.516200 | Siding Spring-Faulkes Telescope South
E11  |149.6627  | 0.84469  | -0.53362  | Frog Rock Observatory, Mudgee
E12  |149.0642  | 0.85563  | -0.51621  | Siding Spring Survey
E13  |149.0969  | 0.81622  | -0.57597  | Wanniassa
E14  |149.1100  | 0.81852  | -0.57274  | Hunters Hill Observatory, Ngunnawal
E15  |149.6061  | 0.82016  | -0.57041  | Magellan Observatory, near Goulburn
E16  |149.36624 | 0.831681 | -0.553654 | Grove Creek Observatory, Trunkey
E17  |150.3417  | 0.8329   | -0.5519   | Leura
E18  |151.02714 | 0.829819 | -0.556191 | BDI Observatory, Regents Park
E19  |151.0958  | 0.83042  | -0.55528  | Kingsgrove
E20  |151.10320 | 0.832146 | -0.552728 | Marsfield
E21  |151.5667  | 0.8838   | -0.4665   | Norma Rose Observatory, Leyburn
E22  |151.85500 | 0.885337 | -0.463616 | Univ. of Southern Queensland Obs., Mt. Kent
E23  |151.07119 | 0.833596 | -0.550574 | Arcadia
E24  |150.7769  | 0.83176  | -0.55329  | Tangra Observatory, St. Clair
E25  |153.1170  | 0.88713  | -0.45997  | Rochedale (APTA)
E26  |153.3971  | 0.88414  | -0.46566  | RAS Observatory, Biggera Waters
E27  |153.2667  | 0.8871   | -0.4600   | Thornlands
E28  |150.6411  | 0.83319  | -0.55121  | Kuriwa Observatory, Hawkesbury Heights
E81  |173.2617  | 0.75267  | -0.65622  | Nelson
E83  |173.95703 | 0.749648 | -0.659621 | Wither Observatory, Witherlea
E85  |174.89400 | 0.800696 | -0.597064 | Farm Cove
E87  |175.6540  | 0.76249  | -0.64485  | Turitea
E89  |176.2040  | 0.78759  | -0.61421  | Geyserland Observatory, Pukehangi
E94  |177.88331 | 0.782217 | -0.620920 | Possum Observatory, Gisborne
F51  |203.74409 | 0.936241 | +0.351543 | Pan-STARRS 1, Haleakala
F52  |203.74409 | 0.936239 | +0.351545 | Pan-STARRS 2, Haleakala
F59  |201.94100 | 0.932037 | +0.361160 | Ironwood Remote Observatory, Hawaii
F60  |201.95283 | 0.929942 | +0.366558 | Ironwood Observatory, Hawaii
F65  |203.7424  | 0.93624  | +0.35154  | Haleakala-Faulkes Telescope North
F84  |210.3842  | 0.95330  | -0.30100  | Hibiscus Observatory, Punaauia
F85  |210.3842  | 0.95330  | -0.30100  | Tiki Observatory, Punaauia
F86  |210.38381 | 0.953304 | -0.301004 | Moana Observatory, Punaauia
G07  |  3.06386 | 0.719394 | +0.692378 | Millau Observatory
G08  |  1.99694 | 0.748752 | +0.660794 | Observatorio Les Pedritxes, Matadepera
G09  |  0.61056 | 0.621784 | +0.780574 | SWF Observatory, South Woodham Ferrers
G10  |354.45055 | 0.792574 | +0.607765 | Clavier Observatory, Lora Del Rio
G17  | 11.20261 | 0.723508 | +0.688023 | BAS Observatory, Scandicci
G18  | 11.26383 | 0.712881 | +0.698948 | ALMO Observatory, Padulle
G19  | 12.7460  | 0.63252  | +0.77202  | Immanuel Kant Observatory,Limbach
G20  |  6.05989 | 0.727743 | +0.683615 | Brignoles Observatory
G21  | 13.73789 | 0.796024 | +0.603377 | Osservatorio Castrofilippo
G22  |  9.21439 | 0.655435 | +0.752770 | Experimenta Observatory, Heilbronn
G23  | 19.09234 | 0.675698 | +0.734739 | Vulpecula Observatory, Budapest
G24  |  9.09350 | 0.662443 | +0.746701 | Dettenhausen
G25  |288.1050  | 0.70317  | +0.70867  | Sherbrooke
G26  |109.8236  | 0.82499  | +0.56338  | Fushan Observatory, Mt Shaohua
G27  |  0.72935 | 0.743842 | +0.666483 | Fabra Observatory, Montsec
G28  |  1.00850 | 0.609900 | +0.789830 | Wyncroft Observatory, Attleborough
G29  |358.9124  | 0.77285  | +0.63263  | Requena
G30  |284.90719 | 0.704518 | +0.707320 | Casselman
G31  | 13.7253  | 0.69946  | +0.71233  | CCAT Trieste
G32  |291.82040 | 0.921639 | -0.387713 | Elena Remote Observatory, San Pedro de Atacama
G33  |  7.60879 | 0.623411 | +0.779293 | Wickede
G34  | 13.7015  | 0.63254  | +0.77203  | Oberfrauendorf
G35  |249.15789 | 0.849476 | +0.526134 | Elephant Head Obsevatory, Sahuarita
G36  |357.45250 | 0.797538 | +0.601812 | Calar Alto-CASADO
G37  |248.57749 | 0.822887 | +0.566916 | Lowell Discovery Telescope
G38  |356.76842 | 0.759967 | +0.647951 | Observatorio La Senda, Cabanillas del Campo
G39  |291.82039 | 0.921640 | -0.387711 | ROAD, San Pedro de Atacama
G40  |343.49174 | 0.881470 | +0.471441 | Slooh.com Canary Islands Observatory
G41  |264.73816 | 0.867040 | +0.496575 | Insperity Observatory, Humble
G42  |259.0230  | 0.90391  | +0.42687  | Observatorio Astronomico UAdeC, Saltillo
G43  |293.6879  | 0.83817  | -0.54382  | Observatorio Buenaventura Suarez, San Luis
G44  |313.3061  | 0.92118  | -0.38816  | Observatorio Longa Vista, Sao Paulo
G45  |253.63564 | 0.832748 | +0.552480 | Space Surveillance Telescope, Atom Site
G46  |244.66153 | 0.818022 | +0.573711 | Pinto Valley Observatory
G47  |253.80654 | 0.819827 | +0.571261 | HillTopTop Observatory, Edgewood
G48  |251.10148 | 0.849514 | +0.526196 | Harlingten Research Observatory, Rancho Hildalgo
G49  |266.5943  | 0.70889  | +0.70302  | Minnetonka
G50  |253.3300  | 0.84629  | +0.53134  | Organ Mesa Observatory, Las Cruces
G51  |239.95778 | 0.823164 | +0.565990 | Byrne Observatory, Sedgwick Reserve
G52  |237.49604 | 0.785917 | +0.616275 | Stone Edge Observatory, El Verano
G53  |240.58727 | 0.799043 | +0.599625 | Alder Springs Observatory, Auberry
G54  |243.0630  | 0.83295  | +0.55166  | Hemet
G55  |241.09533 | 0.816361 | +0.575651 | Bakersfield
G56  |237.9294  | 0.78983  | +0.61128  | Walnut Creek
G57  |236.8564  | 0.70171  | +0.71009  | Dilbert Observatory, Forest Grove
G58  |237.8180  | 0.79100  | +0.60988  | Chabot Space and Science Center, Oakland
G59  |237.4530  | 0.67475  | +0.73559  | Maiden Lane Obs., Bainbridge Island
G60  |240.33888 | 0.825544 | +0.562496 | Carroll Observatory, Montecito
G61  |238.1524  | 0.79270  | +0.60760  | Pleasanton
G62  |238.5469  | 0.72214  | +0.68971  | Sunriver Nature Center Observatory, Sunriver
G63  |238.6858  | 0.70152  | +0.71031  | Mill Creek Observatory, The Dalles
G64  |239.2911  | 0.77535  | +0.62979  | Blue Canyon Observatory
G65  |238.3612  | 0.79616  | +0.60338  | Vulcan North, Lick Observatory, Mount Hamilton
G66  |238.9169  | 0.78135  | +0.62206  | Lake Forest Observatory, Forest Hills
G67  |239.3650  | 0.78134  | +0.62225  | Rancho Del Sol, Camino
G68  |240.2250  | 0.78044  | +0.62355  | Sierra Stars Observatory, Markleeville
G69  |241.0158  | 0.82829  | +0.55850  | Via Capote Sky Observatory, Thousand Oaks
G70  |241.4547  | 0.82543  | +0.56273  | Francisquito Observatory, Los Angeles
G71  |241.6047  | 0.83216  | +0.55276  | Rancho Palos Verdes
G72  |241.82408 | 0.829301 | +0.556970 | University Hills
G73  |241.9400  | 0.82804  | +0.55925  | Mount Wilson-TIE
G74  |242.88538 | 0.837429 | +0.544849 | Boulder Knolls Observatory, Escondido
G75  |243.2783  | 0.8351   | +0.5487   | Starry Knight Observatory, Coto de Caza
G76  |242.4178  | 0.83388  | +0.55015  | Altimira Observatory, Coto de Caza
G77  |243.7183  | 0.8274   | +0.5603   | Baldwin Lake
G78  |244.3127  | 0.84158  | +0.53832  | Desert Wanderer Observatory, El Centro
G79  |243.6165  | 0.82718  | +0.56030  | Goat Mountain Astronomical Research Station
G80  |240.5873  | 0.79904  | +0.59962  | Sierra Remote Observatories, Auberry
G81  |242.91300 | 0.834904 | +0.548639 | Temecula
G82  |248.40025 | 0.849488 | +0.526449 | SARA Observatory, Kitt Peak
G83  |250.11039 | 0.842740 | +0.537440 | Mt. Graham-LBT
G84  |249.21084 | 0.845112 | +0.533610 | Mount Lemmon SkyCenter
G85  |247.56518 | 0.799502 | +0.599067 | Vermillion Cliffs Observatory, Kanab
G86  |249.0697  | 0.84645  | +0.53090  | Tucson-Winterhaven
G87  |248.1894  | 0.74666  | +0.66331  | Calvin M. Hooper Memorial Observatory, Hyde Park
G88  |247.8881  | 0.83064  | +0.55514  | LAMP Observatory, New River
G89  |248.3069  | 0.81933  | +0.57197  | Kachina Observatory, Flagstaff
G90  |248.9658  | 0.84301  | +0.53639  | Three Buttes Observatory, Tucson
G91  |249.1219  | 0.85208  | +0.52234  | Whipple Observatory, Mt. Hopkins--2MASS
G92  |249.2814  | 0.84920  | +0.52660  | Jarnac Observatory, Vail
G93  |249.3726  | 0.85215  | +0.52201  | Sonoita Research Observatory, Sonoita
G94  |249.9267  | 0.84971  | +0.52594  | Sonoran Skies Observatory, St. David
G95  |249.7622  | 0.85404  | +0.51888  | Hereford Arizona Observatory, Hereford
G96  |249.21128 | 0.845111 | +0.533614 | Mt. Lemmon Survey
G97  |250.8694  | 0.84965  | +0.52600  | Astronomical League Alpha Observatory, Portal
G98  |251.34354 | 0.815037 | +0.578012 | Calvin-Rehoboth Observatory, Rehoboth
G99  |251.8104  | 0.84192  | +0.53835  | NF Observatory, Silver City
H00  |251.6987  | 0.84247  | +0.53746  | Tyrone
H01  |252.81067 | 0.830474 | +0.556096 | Magdalena Ridge Observatory, Socorro
H02  |253.3706  | 0.81146  | +0.58309  | Sulphur Flats Observatory, La Cueva
H03  |253.3553  | 0.81753  | +0.57440  | Sandia View Observatory, Rio Rancho
H04  |254.0260  | 0.81388  | +0.57964  | Santa Fe
H05  |256.0707  | 0.77126  | +0.63477  | Edmund Kline Observatory, Deer Trail
H06  |254.47130 | 0.840712 | +0.540310 | iTelescope Observatory, Mayhill
H07  |254.47134 | 0.840711 | +0.540310 | 7300 Observatory, Cloudcroft
H08  |254.47081 | 0.840705 | +0.540319 | BlackBird Observatory, Cloudcroft
H09  |255.5886  | 0.77070  | +0.63549  | Antelope Hills Observatory, Bennett
H10  |254.47141 | 0.840711 | +0.540309 | Tzec Maun Observatory, Mayhill
H11  |250.9840  | 0.85029  | +0.52492  | LightBuckets Observatory, Rodeo
H12  |254.47078 | 0.840712 | +0.540307 | TechDome, Mayhill
H13  |248.25212 | 0.840489 | +0.540134 | Lenomiya Observatory, Casa Grande
H14  |249.21233 | 0.846402 | +0.530995 | Morning Star Observatory, Tucson
H15  |254.47156 | 0.840711 | +0.540308 | ISON-NM Observatory, Mayhill
H16  |253.2890  | 0.77152  | +0.63472  | HUT Observatory, Eagle
H17  |254.38333 | 0.783783 | +0.619652 | Angel Peaks Observatory
H18  |249.28798 | 0.849231 | +0.526572 | Vail View Observatory, Vail
H19  |263.86259 | 0.828144 | +0.558685 | Lone Star Observatory, Caney
H20  |271.81682 | 0.772950 | +0.632393 | Eastern Illinois University Obs., Charleston
H21  |272.03173 | 0.772885 | +0.632471 | Astronomical Research Observatory, Westfield
H22  |272.7371  | 0.77438  | +0.63062  | Terre Haute
H23  |273.49858 | 0.862319 | +0.504671 | Pear Tree Observatory, Valparaiso
H24  |274.59881 | 0.733648 | +0.677310 | J. C. Veen Observatory, Lowell
H25  |266.87082 | 0.714467 | +0.697388 | Harvest Moon Observatory, Northfield
H26  |270.78922 | 0.735075 | +0.675789 | Doc Greiner Research Observatory, Janesvillle
H27  |266.23134 | 0.780074 | +0.623645 | Moonglow Observatory, Warrensburg
H28  |263.23150 | 0.836912 | +0.545569 | Preston Hills Observatory, Celina
H29  |262.5494  | 0.81372  | +0.57940  | Ivywood Observatory, Edmond
H30  |262.5558  | 0.81808  | +0.57328  | University of Oklahoma Observatory, Norman
H31  |263.3300  | 0.87011  | +0.49123  | Star Ridge Observatory, Weimar
H32  |263.6334  | 0.86174  | +0.50567  | Texas A&M Physics Observatory, College Station
H33  |264.1217  | 0.80990  | +0.58466  | Bixhoma Observatory, Bixby
H34  |264.8258  | 0.84600  | +0.53143  | Chapel Hill
H35  |264.9517  | 0.77423  | +0.63085  | Leavenworth
H36  |264.2936  | 0.78043  | +0.62323  | Sandlot Observatory, Scranton
H37  |265.2003  | 0.72947  | +0.68182  | Grems Timmons Observatories, Graettinger
H38  |265.9864  | 0.75079  | +0.65840  | Timberline Observatory, Urbandale
H39  |266.6828  | 0.70944  | +0.70247  | S.O.S. Observatory, Minneapolis
H40  |266.7306  | 0.82519  | +0.56302  | Nubbin Ridge Observatory
H41  |267.0742  | 0.81870  | +0.57238  | Petit Jean Mountain
H42  |267.5078  | 0.73568  | +0.67512  | Wartburg College Observatory, Waverly
H43  |267.4998  | 0.81918  | +0.57163  | Conway
H44  |267.7982  | 0.81880  | +0.57220  | Cascade Mountain
H45  |267.0831  | 0.81890  | +0.57210  | Arkansas Sky Obs., Petit Jean Mountain South
H46  |265.7297  | 0.77818  | +0.62602  | Ricky Observatory, Blue Springs
H47  |269.1439  | 0.84639  | +0.53079  | Vicksburg
H48  |265.0139  | 0.79424  | +0.60565  | PSU Greenbush Observatory, Pittsburg
H49  |266.8636  | 0.81712  | +0.57457  | ATU Astronomical Observatory, Russellville
H50  |267.54139 | 0.819253 | +0.571536 | University of Central Arkansas Obs., Conway
H51  |270.4003  | 0.73117  | +0.68011  | Greiner Research Observatory, Verona
H52  |270.67354 | 0.739151 | +0.671335 | Hawkeye Observatory, Durand
H53  |271.22842 | 0.789618 | +0.611581 | Thompsonville
H54  |271.6514  | 0.71305  | +0.69883  | Cedar Drive Observatory, Pulaski
H55  |271.8558  | 0.77283  | +0.63254  | Astronomical Research Observatory, Charleston
H56  |272.16764 | 0.742693 | +0.667433 | Northbrook Meadow Observatory
H57  |275.97246 | 0.758850 | +0.649150 | Ohio State University Observatory, Lima
H58  |273.3353  | 0.82349  | +0.56548  | NASA/MSFC ALaMO, Redstone Arsenal
H59  |273.3651  | 0.76362  | +0.64356  | Prairie Grass Observatory, Camp Cullom
H60  |273.86542 | 0.767435 | +0.639034 | Heartland Observatory, Carmel
H61  |281.41689 | 0.721533 | +0.690080 | Newcastle
H62  |274.4117  | 0.73335  | +0.67763  | Calvin College Observatory
H63  |274.9276  | 0.75227  | +0.65672  | DeKalb Observatory, Auburn
H64  |275.4364  | 0.77796  | +0.62623  | Thomas More College Observatory, Crestview Hills
H65  |275.4364  | 0.77995  | +0.62381  | Waltonfields Observatory, Walton
H66  |276.1460  | 0.76956  | +0.63651  | Yellow Springs
H67  |276.16241 | 0.740813 | +0.669522 | Stonegate Observatory, Ann Arbor
H68  |276.34824 | 0.854246 | +0.518152 | Red Barn Observatory, Ty Ty
H69  |276.94463 | 0.764320 | +0.642741 | Perkins Observatory, Delaware
H70  |277.4458  | 0.81412  | +0.57897  | Asheville
H71  |276.48282 | 0.852885 | +0.520378 | Chula
H72  |278.2258  | 0.89584  | +0.44289  | Evelyn L. Egan Observatory, Fort Myers
H73  |278.6351  | 0.74850  | +0.66097  | Lakeland Astronomical Observatory, Kirtland
H74  |278.8747  | 0.87602  | +0.48066  | Bar J Observatory, New Smyrna Beach
H75  |278.91856 | 0.749551 | +0.659816 | Indian Hill North Observatory, Huntsburg
H76  |279.4133  | 0.90197  | +0.43036  | Oakridge Observatory, Miami
H77  |279.7653  | 0.89877  | +0.43695  | Buehler Observatory
H78  |282.70896 | 1.000183 | +0.021030 | University of Narino Observatory, Pasto
H79  |280.49270 | 0.723258 | +0.688308 | York University Observatory, Toronto
H80  |285.33567 | 0.763194 | +0.644015 | Halstead Observatory, Princeton
H81  |283.61539 | 0.738959 | +0.671615 | Hartung-Boothroyd Observatory, Ithaca
H82  |281.7839  | 0.77836  | +0.62576  | CBA-NOVAC Observatory, Front Royal
H83  |282.6641  | 0.77926  | +0.62463  | Timberlake Observatory, Oakton
H84  |282.4961  | 0.73259  | +0.67843  | Northview Observatory, Mendon
H85  |283.0029  | 0.77784  | +0.62638  | Silver Spring
H86  |283.1576  | 0.77693  | +0.62749  | CBA-East Observatory, Laurel
H87  |282.4361  | 0.79309  | +0.60708  | Fenwick Observatory, Richmond
H88  |283.7577  | 0.77295  | +0.63235  | Hope Observatory, Belcamp
H89  |284.2975  | 0.70235  | +0.70945  | Galaxy Blues Observatory, Gatineau
H90  |284.4731  | 0.70267  | +0.70914  | Ottawa
H91  |285.04839 | 0.712263 | +0.699590 | Reynolds Observatory, Potsdam
H92  |285.6211  | 0.76785  | +0.63849  | Arcturus Observatory
H93  |285.5758  | 0.75934  | +0.64853  | Berkeley Heights
H94  |285.5439  | 0.75781  | +0.65032  | Cedar Knolls
H95  |285.82120 | 0.758745 | +0.649211 | NJIT Observatory, Newark
H96  |286.6142  | 0.69143  | +0.72005  | Observatoire des Pleiades, Mandeville
H97  |287.20132 | 0.746487 | +0.663233 | Talcott Mountain Science Center, Avon
H98  |287.2655  | 0.74987  | +0.65938  | Dark Rosanne Obs., Middlefield
H99  |288.8036  | 0.74040  | +0.66992  | Sunhill Observatory, Newton
I00  |288.2294  | 0.74794  | +0.66157  | Carbuncle Hill Observatory, Coventry
I01  |288.86253 | 0.740677 | +0.669630 | Clay Center Observatory, Brookline
I02  |289.1949  | 0.86558  | -0.49976  | Cerro Tololo Observatory, La Serena--2MASS
I03  |289.26626 | 0.873440 | -0.486052 | European Southern Obs., La Silla--ASTROVIRTEL
I04  |289.3152  | 0.86693  | -0.49697  | Mamalluca Observatory
I05  |289.2980  | 0.87559  | -0.48217  | Las Campanas Observatory-TIE
I06  |289.8061  | 0.74801  | +0.66147  | Werner Schmidt Obs., Dennis-Yarmouth Regional HS
I07  |288.0971  | 0.74279  | +0.66735  | Conlin Hill Observatory, Oxford
I08  |290.6932  | 0.85116  | -0.52394  | Alianza S4, Cerro Burek
I09  |289.80377 | 0.910166 | -0.413875 | Cerro Armazones
I10  |291.8200  | 0.92165  | -0.38770  | CAO, San Pedro de Atacama (until 2012)
I11  |289.26345 | 0.865020 | -0.500901 | Gemini South Observatory, Cerro Pachon
I12  |288.87053 | 0.736679 | +0.673998 | Phillips Academy Observatory, Andover
I13  |282.93006 | 0.779116 | +0.624793 | Burleith Observatory, Washington D.C.
I14  |288.58931 | 0.740298 | +0.670040 | Tigh Speuran Observatory, Framingham
I15  |288.70076 | 0.747034 | +0.662558 | Wishing Star Observatory, Barrington
I16  |291.82033 | 0.921638 | -0.387715 | IAA-AI Atacama, San Pedro de Atacama
I17  |284.32206 | 0.748993 | +0.660451 | Thomas G. Cupillari Observatory, Fleetville
I18  |281.3067  | 0.79038  | +0.61070  | Fan Mountain Observatory, Covesville
I19  |295.40711 | 0.854834 | -0.517422 | Observatorio El Gato Gris, Tanti
I20  |295.68161 | 0.838551 | -0.543122 | Observatorio Astronomico Salvador, Rio Cuarto
I21  |295.8281  | 0.85465  | -0.51760  | El Condor Observatory, Cordoba
I22  |296.1740  | 0.71212  | +0.69973  | Abbey Ridge Observatory, Stillwater Lake
I23  |292.26649 | 0.714173 | +0.697623 | Frosty Cold Observatory, Mash Harbor
I24  |282.2306  | 0.78534  | +0.61702  | Lake of the Woods Observatory, Locust Grove
I25  |295.44381 | 0.850887 | -0.523945 | ECCCO Observatory, Bosque Alegre
I26  |295.8214  | 0.85417  | -0.51839  | Observatorio Kappa Crucis, Cordoba
I27  |284.0006  | 0.70401  | +0.70783  | Barred Owl Observatory, Carp
I28  |289.0889  | 0.74643  | +0.66324  | Starhoo Observatory, Lakeville
I29  |288.63304 | 0.738432 | +0.672081 | Middlesex School Observatory, Concord
I30  |299.3417  | 0.83966  | -0.54131  | Observatorio Geminis Austral
I31  |299.3649  | 0.83995  | -0.54086  | Observatorio Astronomico del Colegio Cristo Rey
I32  |299.3464  | 0.83969  | -0.54125  | Observatorio Beta Orionis, Rosario
I33  |289.2608  | 0.86504  | -0.50086  | SOAR, Cerro Pachon
I34  |284.1297  | 0.76548  | +0.64134  | Morgantown
I35  |301.5572  | 0.82198  | -0.56762  | Sidoli
I36  |301.28271 | 0.819978 | -0.570483 | Observatorio Los Campitos, Canuelas
I37  |301.35275 | 0.825603 | -0.562360 | Astrodomi Observatory, Santa Rita
I38  |302.02141 | 0.854400 | -0.517885 | Observatorio Los Algarrobos, Salto
I39  |301.42661 | 0.823342 | -0.565652 | Observatorio Cruz del Sur, San Justo
I40  |289.26061 | 0.873472 | -0.485986 | La Silla--TRAPPIST
I41  |243.14022 | 0.836325 | +0.546877 | Palomar Mountain--ZTF
I42  |288.9081  | 0.74895  | +0.66041  | Westport Observatory
I43  |261.90237 | 0.846901 | +0.530084 | Tarleton State University Obs., Stephenville
I44  |273.5176  | 0.86201  | +0.50521  | Northwest Florida State College, Niceville
I45  |301.4281  | 0.82326  | -0.56577  | W Crusis Astronomical Observatory, San Justo
I46  |281.6108  | 0.76192  | +0.64558  | The Cottage Observatory, Altoona
I47  |290.5503  | 0.81526  | -0.57753  | Pierre Auger Observatory, Malargue
I48  |295.6757  | 0.80340  | -0.59348  | Observatorio El Catalejo, Santa Rosa
I49  |253.98617 | 0.813183 | +0.580617 | Sunflower Observatory, Santa Fe
I50  |254.47142 | 0.840712 | +0.540309 | P2 Observatory, Mayhill
I51  |283.0547  | 0.78133  | +0.62203  | Clinton
I52  |249.21108 | 0.845113 | +0.533611 | Steward Observatory, Mt. Lemmon Station
I53  |356.3783  | 0.79822  | +0.60052  | Armilla
I54  |353.03081 | 0.779853 | +0.623912 | Observatorio Las Vaguadas, Badajoz
I55  |359.64214 | 0.772769 | +0.632566 | Valencia
I56  |357.71066 | 0.801182 | +0.596429 | Observatorio Astronomico John Beckman, Almeria
I57  |359.3256  | 0.78579  | +0.61646  | Elche
I58  |359.5374  | 0.77206  | +0.63345  | Betera
I59  |356.1558  | 0.72754  | +0.68377  | Observatorio Fuente de los matos, Muriedas
I60  |357.1781  | 0.67397  | +0.73630  | Guernanderf
I61  |352.1494  | 0.74047  | +0.66989  | Ourense
I62  |356.42639 | 0.767072 | +0.639561 | Observatorio Helios Ontigola
I63  |358.8330  | 0.62944  | +0.77446  | Cygnus Observatory, New Airesford
I64  |359.29386 | 0.623532 | +0.779182 | Maidenhead
I65  |355.0796  | 0.80245  | +0.59491  | Yunquera
I66  |312.0000  | 0.96235  | -0.27153  | Taurus Australis Observatory, Brasilia
I67  |359.08753 | 0.626440 | +0.776870 | Hartley Wintney
I68  |312.4981  | 0.96931  | -0.24573  | Pousada dos Anoes Observatory
I69  |352.0069  | 0.85232  | +0.52140  | AGM Observatory, Marrakech
I70  |359.94158 | 0.604128 | +0.794217 | Gedney House Observatory, Kirton
I71  |353.6698  | 0.77330  | +0.63205  | Observatorio Los Milanos, Caceres
I72  |355.9849  | 0.75923  | +0.64893  | Observatorio Carpe-Noctem, Madrid
I73  |359.58711 | 0.670611 | +0.739353 | Salvia Observatory, Saulges
I74  |358.18739 | 0.629588 | +0.774337 | Baxter Garden Observatory, Salisbury
I75  |359.9650  | 0.76735  | +0.63910  | Observatorio Castellon
I76  |355.93681 | 0.761573 | +0.646107 | Observatorio Tesla, Valdemorillo
I77  |316.0025  | 0.94119  | -0.33714  | CEAMIG-REA Observatory, Belo Horizonte
I78  |355.5721  | 0.80240  | +0.59481  | Observatorio Principia, Malaga
I79  |357.6733  | 0.78743  | +0.61474  | AstroCamp, Nerpio
I80  |358.13328 | 0.590762 | +0.804183 | Rose Cottage Observatory, Keighley
I81  |356.20111 | 0.533510 | +0.842967 | Tarbatness Observatory, Portmahomack
I82  |343.5797  | 0.88105  | +0.47156  | Guimar
I83  |353.1900  | 0.59630  | +0.80008  | Cherryvalley Observatory, Rathmolyon
I84  |353.0212  | 0.77967  | +0.62415  | Cerro del Viento, Badajoz
I85  |357.9848  | 0.80086  | +0.59686  | Las Negras
I86  |356.2739  | 0.76211  | +0.64543  | Observatorio UCM, Madrid
I87  |352.9593  | 0.60121  | +0.79643  | Astroshot Observatory, Monasterevin
I88  |356.0823  | 0.79287  | +0.60753  | Fuensanta de Martos
I89  |357.6739  | 0.78744  | +0.61474  | iTelescope Observatory, Nerpio
I90  |351.59760 | 0.618315 | +0.783298 | Blackrock Castle Observatory
I91  |357.69250 | 0.801192 | +0.596407 | Retamar
I92  |353.95289 | 0.795987 | +0.603315 | Astreo Observatory, Mairena del Aljarafe
I93  |359.79700 | 0.713711 | +0.698096 | St Pardon de Conques
I94  |356.1367  | 0.76162  | +0.64603  | Observatorio Rho Ophiocus, Las Rozas de Madrid
I95  |356.81394 | 0.771993 | +0.633666 | Observatorio de la Hita
I96  |356.50384 | 0.758233 | +0.649960 | Hyperion Observatory, Urbanizacion Caraquiz
I97  |359.50178 | 0.621889 | +0.780493 | Penn Heights Observatory, Rickmansworth
I98  |356.41339 | 0.757256 | +0.651181 | El Berrueco
I99  |356.46043 | 0.763221 | +0.644121 | Observatorio Blanquita, Vaciamadrid
J00  |359.5056  | 0.76880  | +0.63744  | Segorbe
J01  |354.28450 | 0.739938 | +0.670609 | Observatorio Cielo Profundo, Leon
J02  |359.5550  | 0.78391  | +0.61884  | Busot
J03  |355.13250 | 0.638787 | +0.766833 | Gothers Observatory, St. Dennis
J04  |343.48817 | 0.881463 | +0.471461 | ESA Optical Ground Station, Tenerife
J05  |355.29639 | 0.749617 | +0.659822 | Bootes Observatory, Boecillo
J06  |358.81247 | 0.604374 | +0.794039 | Trent Astronomical Observatory, Clifton
J07  |353.89543 | 0.767881 | +0.638546 | Observatorio SPAG Monfrague, Palazuelo-Empalme
J08  |359.6549  | 0.77127  | +0.63439  | Observatorio Zonalunar, Puzol
J09  |353.7917  | 0.59450  | +0.80141  | Balbriggan
J10  |359.59839 | 0.784437 | +0.618151 | Alicante
J11  |351.31769 | 0.746984 | +0.662617 | Matosinhos
J12  |356.51061 | 0.758248 | +0.649949 | Caraquiz
J13  |342.1208  | 0.87763  | +0.47851  | La Palma-Liverpool Telescope
J14  |345.99281 | 0.880303 | +0.472891 | La Corte
J15  |352.83061 | 0.755420 | +0.653125 | Muxagata
J16  |354.20356 | 0.584292 | +0.808826 | An Carraig Observatory, Loughinisland
J17  |357.20313 | 0.609723 | +0.790018 | Ragdon
J18  |356.90600 | 0.609920 | +0.789845 | Dingle Observatory, Montgomery
J19  |359.83036 | 0.764671 | +0.642359 | El Maestrat
J20  |356.21926 | 0.762019 | +0.645541 | Aravaca
J21  |356.08003 | 0.759065 | +0.649062 | El Boalo
J22  |342.13235 | 0.878415 | +0.476543 | Tacande Observatory, La Palma
J23  |358.49361 | 0.671765 | +0.738300 | Centre Astronomique de La Couyere
J24  |343.55719 | 0.881661 | +0.470499 | Observatorio Altamira
J25  |354.48883 | 0.728241 | +0.683076 | Penamayor Observatory, Nava
J26  |356.98119 | 0.612507 | +0.787898 | The Spaceguard Centre, Knighton
J27  |355.96899 | 0.760373 | +0.647528 | El Guijo Observatory
J28  |356.21381 | 0.791408 | +0.609366 | Jaen
J29  |346.34213 | 0.875695 | +0.481318 | Observatorio Nira, Tias
J30  |356.29300 | 0.761925 | +0.645666 | Observatorio Ventilla, Madrid
J31  |355.77411 | 0.802445 | +0.594759 | La Axarquia
J32  |352.97769 | 0.796769 | +0.602268 | Aljaraque
J33  |359.90600 | 0.620040 | +0.781953 | University of Hertfordshire Obs., Bayfordbury
J34  |355.22711 | 0.748695 | +0.660858 | La Fecha
J35  |356.02911 | 0.792167 | +0.608432 | Tucci Observatory, Martos
J36  |356.94519 | 0.765179 | +0.641659 | Observatorio DiezALaOnce, Illana
J37  |353.06469 | 0.796893 | +0.602104 | Huelva
J38  |353.60890 | 0.726876 | +0.684507 | Observatorio La Vara, Valdes
J39  |344.5636  | 0.88429  | +0.46547  | Ingenio
J40  |355.55847 | 0.802546 | +0.594601 | Malaga
J41  |353.8189  | 0.59779  | +0.79897  | Raheny
J42  |359.6989  | 0.77138  | +0.63425  | Puzol
J43  |352.13354 | 0.856441 | +0.515339 | Oukaimeden Observatory, Marrakech
J44  |357.6552  | 0.73506  | +0.67596  | Observatorio Iturrieta, Alava
J45  |344.46735 | 0.883626 | +0.466916 | Observatorio Montana Cabreja, Vega de San Mateo
J46  |346.3594  | 0.87569  | +0.48131  | Observatorio Montana Blanca, Tias
J47  |346.4440  | 0.87501  | +0.48260  | Observatorio Nazaret
J48  |343.6960  | 0.87977  | +0.47393  | Observatory Mackay, La Laguna
J49  |359.4482  | 0.78695  | +0.61496  | Santa Pola
J50  |342.1176  | 0.87764  | +0.47847  | La Palma-NEON
J51  |343.72898 | 0.879789 | +0.473809 | Observatorio Atlante, Tenerife
J52  |358.6608  | 0.74198  | +0.66826  | Observatorio Pinsoro
J53  |354.89278 | 0.791142 | +0.609607 | Posadas
J54  |343.4906  | 0.88149  | +0.47142  | Bradford Robotic Telescope
J55  |344.3144  | 0.88549  | +0.46313  | Los Altos de Arguineguin Observatory
J56  |344.4536  | 0.88416  | +0.46624  | Observatorio La Avejerilla
J57  |358.89089 | 0.767817 | +0.638833 | Centro Astronomico Alto Turia, Valencia
J58  |356.6644  | 0.62304  | +0.77959  | Brynllefrith Observatory, Llantwit Fardre
J59  |356.20256 | 0.726956 | +0.684386 | Observatorio Linceo, Santander
J60  |354.3406  | 0.74773  | +0.66201  | Tocororo Observatory, Arquillinos
J61  |353.4264  | 0.59719  | +0.79942  | Brownstown Observatory, Kilcloon
J62  |351.6345  | 0.59017  | +0.80459  | Kingsland Observatory, Boyle
J63  |359.4831  | 0.78548  | +0.61683  | San Gabriel
J64  |359.3459  | 0.78871  | +0.61271  | La Mata
J65  |353.4497  | 0.59830  | +0.79860  | Celbridge
J66  |357.7833  | 0.61071  | +0.78922  | Kinver
J67  |359.4667  | 0.77114  | +0.63457  | Observatorio La Puebla de Vallbona
J68  |357.7055  | 0.61813  | +0.78345  | Tweenhills Observatory, Hartpury
J69  |358.98034 | 0.631443 | +0.772863 | North Observatory, Clanfield
J70  |358.8404  | 0.78968  | +0.61149  | Obs. Astronomico Vega del Thader, El Palmar
J71  |357.8947  | 0.59350  | +0.80217  | Willow Bank Observatory
J72  |358.9664  | 0.79065  | +0.61028  | Valle del Sol
J73  |359.0833  | 0.6187   | +0.7830   | Quainton
J74  |357.0961  | 0.72950  | +0.68169  | Bilbao
J75  |357.43471 | 0.789388 | +0.612222 | OAM Observatory, La Sagra
J76  |358.79718 | 0.790771 | +0.610163 | La Murta
J77  |357.5947  | 0.63154  | +0.77276  | Golden Hill Observatory, Stourton Caundle
J78  |358.8244  | 0.78887  | +0.61253  | Murcia
J79  |358.38066 | 0.795516 | +0.603908 | Observatorio Calarreona, Aguilas
J80  |359.1083  | 0.70862  | +0.70323  | Sainte Helene
J81  |358.1350  | 0.7360   | +0.6749   | Guirguillano
J82  |357.3067  | 0.5935   | +0.8021   | Leyland
J83  |357.3883  | 0.59274  | +0.80270  | Olive Farm Observatory, Hoghton
J84  |358.9803  | 0.63144  | +0.77285  | South Observatory, Clanfield
J85  |357.4833  | 0.5666   | +0.8213   | Makerstoun
J86  |356.6153  | 0.79930  | +0.59968  | Sierra Nevada Observatory
J87  |355.5067  | 0.76047  | +0.64753  | La Canada
J88  |358.5592  | 0.63165  | +0.77266  | Strawberry Field Obs., Southampton
J89  |356.2861  | 0.76045  | +0.64739  | Tres Cantos Observatory
J90  |358.5317  | 0.62251  | +0.78000  | West Challow
J91  |357.0483  | 0.7411   | +0.6692   | Alt emporda Observatory, Figueres
J92  |359.3487  | 0.62214  | +0.78031  | Beaconsfield
J93  |357.7426  | 0.61927  | +0.78255  | Mount Tuffley Observatory, Gloucester
J94  |357.7886  | 0.61909  | +0.78270  | Abbeydale
J95  |358.55301 | 0.624152 | +0.778715 | Great Shefford
J96  |356.05669 | 0.735326 | +0.675690 | Observatorio de Cantabria
J97  |359.5333  | 0.7754   | +0.6293   | Alginet
J98  |359.5344  | 0.77275  | +0.63259  | Observatorio Manises
J99  |359.57808 | 0.772589 | +0.632790 | Burjassot
K01  |  0.62091 | 0.618636 | +0.783060 | Astrognosis Observatory, Bradwell
K02  |  0.66761 | 0.622858 | +0.779718 | Eastwood Observatory, Leigh on Sea
K03  |  0.74411 | 0.744133 | +0.665979 | Observatori AAS Montsec
K04  |  0.74416 | 0.744130 | +0.665983 | Lo Fossil Observatory, Ager
K05  |  1.02311 | 0.610689 | +0.789233 | Eden Observatory, Banham
K06  |  1.99950 | 0.749658 | +0.659703 | Observatorio Montagut, Can Sola
K07  |  2.4614  | 0.65973  | +0.74902  | Observatoire de Gravelle, St. Maurice
K08  |  1.8800  | 0.75142  | +0.65773  | Observatorio Lledoner, Vallirana
K09  |  2.2400  | 0.74889  | +0.66051  | Llica d\'Amunt
K10  |  5.4214  | 0.71851  | +0.69332  | Micro Palomar, Reilhanette
K11  |  2.88079 | 0.697458 | +0.714390 | Observatoire de Pommier
K12  |  2.7267  | 0.77121  | +0.63447  | Obsevatorio Astronomico de Marratxi
K13  |  2.9124  | 0.77015  | +0.63575  | Albireo Observatory, Inca
K14  |  2.9131  | 0.77090  | +0.63485  | Observatorio de Sencelles
K15  |  3.75522 | 0.725152 | +0.686311 | Murviel-les-Montpellier
K16  |  5.42106 | 0.718540 | +0.693283 | Reilhanette
K17  |  7.02679 | 0.692802 | +0.718806 | Observatoire des Valentines, Bex
K18  |  7.5242  | 0.67588  | +0.73460  | Hesingue
K19  |  5.64731 | 0.720582 | +0.691187 | PASTIS Observatory, Banon
K20  |  4.68015 | 0.642261 | +0.763954 | Danastro Observatory, Romeree
K21  |  4.9292  | 0.72101  | +0.69061  | Saint-Saturnin-les-Avignon
K22  |  5.07611 | 0.724222 | +0.687283 | Les Barres Observatory, Lamanon
K23  |  9.4023  | 0.70168  | +0.71014  | Gorgonzola
K24  |  6.86069 | 0.651487 | +0.756168 | Schmelz
K25  |  5.7136  | 0.72157  | +0.69014  | Haute Provence Sud, Saint-Michel-l\'Observatoire
K26  |  6.2201  | 0.64965  | +0.75775  | Contern
K27  |  6.2094  | 0.68296  | +0.72816  | St-Martin Observatory, Amathay Vesigneux
K28  |  6.8947  | 0.63326  | +0.77137  | Sternwarte Eckdorf
K29  |  7.78347 | 0.696415 | +0.715918 | Stellarium Gornergrat
K30  |  7.14839 | 0.682674 | +0.728365 | Luscherz
K31  |  7.00361 | 0.713656 | +0.698546 | Osservatorio Astronomico di Bellino
K32  |  7.52964 | 0.716152 | +0.695733 | Maritime Alps Observatory, Cuneo
K33  |  7.49761 | 0.715775 | +0.696117 | San Defendente
K34  |  7.7005  | 0.70697  | +0.70492  | Turin
K35  |  8.16369 | 0.639883 | +0.765937 | Huenfelden
K36  |  8.24887 | 0.645167 | +0.761522 | Ebersheim
K37  |  8.3148  | 0.70738  | +0.70449  | Cereseto
K38  |  8.91824 | 0.697505 | +0.714297 | M57 Observatory, Saltrio
K39  |  8.95556 | 0.714080 | +0.697844 | Serra Observatory
K40  |  9.0135  | 0.66228  | +0.74685  | Altdorf
K41  |  8.7930  | 0.71113  | +0.70075  | Vegaquattro Astronomical Obs., Novi Ligure
K42  |  8.3332  | 0.65685  | +0.75151  | Knielingen
K43  |  9.8389  | 0.69215  | +0.71970  | OVM Observatory, Chiesa in Valmalencom
K44  |  9.97331 | 0.615161 | +0.785779 | Marienburg Sternwarte, Hildesheim
K45  | 10.49814 | 0.733299 | +0.677639 | Oss. Astronomico di Punta Falcone, Piombino
K46  | 10.9114  | 0.64561  | +0.76115  | Bamberg
K47  | 10.68822 | 0.724257 | +0.687222 | BSCR Observatory, Santa Maria a Monte
K48  | 10.83881 | 0.705714 | +0.706127 | Keyhole Observatory, San Giorgio di Mantova
K49  | 11.18581 | 0.724381 | +0.687146 | Carpione Observatory, Spedaletto
K50  | 11.13300 | 0.646903 | +0.760116 | Sternwarte Feuerstein, Ebermannstadt
K51  | 11.6579  | 0.69563  | +0.71626  | Osservatorio del Celado, Castello Tesino
K52  |  7.6478  | 0.70548  | +0.70642  | Gwen Observatory, San Francesco al Campo
K53  | 12.04564 | 0.744479 | +0.665409 | Marina di Cerveteri
K54  | 11.33678 | 0.728803 | +0.682494 | Astronomical Observatory University of Siena
K55  |  7.76500 | 0.645586 | +0.761172 | Wallhausen
K56  | 12.70497 | 0.732993 | +0.678008 | Osservatorio di Foligno
K57  | 13.0444  | 0.69854  | +0.71317  | Fiore Observatory
K58  |  7.4497  | 0.62655  | +0.77685  | Gevelsberg
K59  | 13.27744 | 0.620411 | +0.781663 | Elsterland Observatory, Jessnigk
K60  | 13.51069 | 0.568623 | +0.819848 | Lindby
K61  | 13.6026  | 0.64741  | +0.75967  | Rokycany Observatory
K62  | 13.84675 | 0.635514 | +0.769557 | Teplice Observatory
K63  | 10.4620  | 0.71953  | +0.69218  | G. Pascoli Observatory, Castelvecchio Pascoli
K64  | 11.74397 | 0.644963 | +0.761748 | Waizenreuth
K65  | 12.2339  | 0.71879  | +0.69290  | Cesena
K66  | 12.62861 | 0.750491 | +0.658684 | Osservatorio Astronomico di Anzio
K67  | 13.3610  | 0.65835  | +0.75036  | Bayerwald Sternwarte, Spiegelau
K68  | 14.90512 | 0.759709 | +0.648110 | Osservatorio Elianto, Pontecagnano
K69  | 10.9941  | 0.62938  | +0.77452  | Riethnordhausen
K70  | 15.9736  | 0.78375  | +0.61901  | Rosarno
K71  | 12.2159  | 0.65748  | +0.75101  | Neutraubling
K72  | 16.3396  | 0.77485  | +0.63021  | Celico
K73  | 16.4158  | 0.75789  | +0.65029  | Gravina in Puglia
K74  | 10.2364  | 0.64667  | +0.76025  | Muensterschwarzach Observatory, Schwarzach
K75  | 11.7289  | 0.68897  | +0.72269  | Astro Dolomites, Santa Cristina Valgardena
K76  |  7.62898 | 0.713488 | +0.698410 | BSA Osservatorio, Savigliano
K77  | 11.2903  | 0.64680  | +0.76019  | EHB01 Observatory, Engelhardsberg
K78  |  9.85356 | 0.718987 | +0.692718 | iota Scorpii Observatory, La Spezia
K79  | 11.05789 | 0.631175 | +0.773097 | Erfurt
K80  | 16.63733 | 0.610859 | +0.789111 | Platanus Observatory, Lusowko
K81  | 13.78511 | 0.748666 | +0.660819 | P.M.P.H.R. Deep Sky Observatory, Atina
K82  | 17.5894  | 0.75937  | +0.64854  | Alphard Observatory, Ostuni
K83  | 11.04317 | 0.723487 | +0.688080 | Beppe Forti Astronomical Observatory, Montelupo
K84  | 10.75861 | 0.718340 | +0.693581 | Felliscopio Observatory, Fellicarolo
K85  |  6.03161 | 0.634354 | +0.770499 | Kelmis
K86  | 10.18189 | 0.701516 | +0.710308 | Brescia
K87  | 10.17011 | 0.646647 | +0.760288 | Dettelbach Vineyard Observatory
K88  | 19.8936  | 0.67154  | +0.73869  | GINOP-KHK, Piszkesteto
K89  | 11.56339 | 0.738665 | +0.671860 | Digital Stargate Observatory, Manciano
K90  | 20.54577 | 0.714093 | +0.697776 | Sopot Astronomical Observatory
K91  | 20.81019 | 0.845561 | -0.532618 | Sutherland-LCO A
K92  | 20.81004 | 0.845561 | -0.532618 | Sutherland-LCO B
K93  | 20.81011 | 0.845560 | -0.532620 | Sutherland-LCO C
K94  | 20.81097 | 0.845561 | -0.532606 | Sutherland
K95  | 20.81106 | 0.845555 | -0.532613 | MASTER-SAAO Observatory, Sutherland
K96  | 16.75119 | 0.774870 | +0.630302 | Savelli Observatory
K97  |  7.18026 | 0.664361 | +0.745050 | Freconrupt
K98  | 17.07217 | 0.608205 | +0.791142 | 6ROADS Observatory 1, Wojnowko
K99  | 22.45350 | 0.663064 | +0.746102 | ISON-Uzhgorod Observatory
L00  | 12.5375  | 0.74535  | +0.66446  | East Rome Observatory, Rome
L01  | 13.74930 | 0.704742 | +0.707169 | Visnjan Observatory, Tican
L02  | 20.81658 | 0.771051 | +0.634781 | NOAK Observatory, Stavraki
L03  | 14.73081 | 0.671765 | +0.738393 | SGT Observatory, Gaflenz
L04  | 23.59640 | 0.685544 | +0.725675 | ROASTERR-1 Observatory, Cluj-Napoca
L05  | 10.0699  | 0.70093  | +0.71089  | Dridri Observatory, Franciacorta
L06  |  9.25403 | 0.696280 | +0.715445 | Sormano 2 Observatory, Bellagio Via Lattea
L07  | 14.56406 | 0.760166 | +0.647727 | Osservatorio Salvatore di Giacomo, Agerola
L08  | 24.39447 | 0.497926 | +0.864325 | Metsahovi Optical Telescope, Metsahovi
L09  | 20.80987 | 0.845559 | -0.532619 | Sutherland-LCO Aqawan A #1
L10  | 22.6186  | 0.78943  | +0.61203  | Kryoneri Observatory
L11  | 17.2092  | 0.50421  | +0.86070  | Sandvreten Observatory
L12  |  2.67789 | 0.629068 | +0.774754 | Koksijde
L13  | 25.62193 | 0.700409 | +0.711479 | Stardust Observatory, Brasov
L14  |  4.92247 | 0.698669 | +0.713095 | Planetarium de Vaulx-en-Velin Observatory
L15  | 25.97839 | 0.708234 | +0.703665 | St. George Observatory, Ploiesti
L16  | 26.04561 | 0.705820 | +0.706098 | Stardreams Observatory, Valenii de Munte
L17  |  2.7114  | 0.74071  | +0.66964  | Observatori Astronomic Albanya
L18  | 26.71828 | 0.659348 | +0.749399 | QOS Observatory, Zalistci
L19  | 11.15258 | 0.716257 | +0.695653 | Osservatorio Felsina AAB, Montepastore
L20  | 18.32069 | 0.722441 | +0.689239 | AG_Sarajevo Observatory, Sarajevo
L21  | 27.42128 | 0.720179 | +0.691479 | Ostrov Observatory, Constanta
L22  | 27.66953 | 0.692963 | +0.718573 | Barlad Observatory
L23  | 27.8319  | 0.70211  | +0.70968  | Schela Observatory
L24  | 27.9289  | 0.89882  | -0.43743  | Gauteng
L25  | 14.43739 | 0.598174 | +0.798700 | Smolecin
L26  | 11.81019 | 0.743368 | +0.666653 | Sanderphil Urban Observatory, Civitavecchia
L27  |  5.64704 | 0.720583 | +0.691197 | 29PREMOTE Observatory, Dauban
L28  | 15.46339 | 0.758034 | +0.650341 | ISON-Castelgrande Observatory
L29  | 18.0169  | 0.91802  | -0.39574  | Drebach-South Observatory, Windhoek
L30  |  7.51469 | 0.624126 | +0.778737 | Lohbach Observatory, Benninghofen
L31  | 12.85615 | 0.632524 | +0.772019 | RaSo Observatory, Chemnitz
L32  | 20.81044 | 0.845576 | -0.532593 | Korea Microlensing Telescope Network-SAAO
L33  | 29.9546  | 0.67379  | +0.73646  | Ananjev
L34  | 14.02061 | 0.789742 | +0.611548 | Galhassin Robotic Telescope, Isnello
L35  | 30.5086  | 0.64055  | +0.76537  | DreamSky Observatory, Lisnyky
L36  | 14.78008 | 0.645319 | +0.761467 | Ondrejov--BlueEye600 Telescope
L37  |353.73883 | 0.803937 | +0.592739 | Observatorio Alnitak, El Puerto de Santa Maria
L38  |  9.69997 | 0.615648 | +0.785407 | Gartensternwarte Schafsweide, Sehlde
L39  | 11.04031 | 0.723062 | +0.688490 | Osservatorio Spica, Signa
L40  |  6.95681 | 0.654011 | +0.754011 | Sternwarte Saarbruecken Rastpfuhl
L41  | 12.30181 | 0.720683 | +0.691022 | Ponte Uso
L42  | 11.5633  | 0.73670  | +0.67400  | Observatory-Astrocamp Manciano
L43  |  0.74439 | 0.744131 | +0.665982 | Ager, Leida
L44  |  6.22111 | 0.688185 | +0.723360 | AstroVal, Le Chenit
L45  | 15.06243 | 0.793975 | +0.605979 | ObsCT, Catania
L46  |356.11939 | 0.762017 | +0.645574 | Observatorio Majadahonda
L47  | 12.50711 | 0.725542 | +0.685961 | Osservatorio Astronomico, Piobbico
L48  | 23.56873 | 0.674816 | +0.735566 | Baia Mare
L49  | 13.00730 | 0.671444 | +0.738747 | VEGA-Sternwarte, Dorfleiten
L50  | 34.0114  | 0.71157  | +0.70039  | GenShtab Observatory, Nauchnij
L51  | 34.0164  | 0.71169  | +0.70028  | MARGO, Nauchnij
L52  | 34.01694 | 0.711679 | +0.700287 | MASTER-Tavrida
L53  |  9.03381 | 0.699589 | +0.712226 | Lomazzo Observatory, Como
L54  | 22.88881 | 0.700709 | +0.711161 | Berthelot Observatory, Hunedoara
L55  | 35.08750 | 0.666222 | +0.743283 | Sura Gardens, Dnipro
L56  |  8.05858 | 0.638960 | +0.766697 | Sternwarte Limburg, Limburg
L57  | 26.90419 | 0.688762 | +0.722601 | Bacau Observatory, Bacau
L58  | 30.57108 | 0.691710 | +0.719771 | Heavenly Owl observatory
L59  |  1.22606 | 0.651546 | +0.756108 | Compustar Observatory, Rouen
L60  | 30.69722 | 0.644961 | +0.761695 | Popovich Observatory, Ivanivka
L61  | 20.81028 | 0.845575 | -0.532593 | MONET South, Sutherland
L62  | 12.52889 | 0.719467 | +0.692209 | Hypatia Observatory, Rimini
L63  | 11.00914 | 0.723671 | +0.687849 | HOB Observatory, Capraia Fiorentina
L64  |  9.36314 | 0.701822 | +0.710005 | Martesana Observatory, Cassina de Pecchi
L65  |  8.82831 | 0.602059 | +0.795784 | Bredenkamp Observatory, Bremen
L66  | 20.81122 | 0.845577 | -0.532615 | MeerLICHT-1, Sutherland
L67  | 37.79889 | 0.561057 | +0.825033 | Cherkizovo Observatory, Moscow Oblast
L68  | 25.53683 | 0.830048 | -0.555874 | PESCOPE, Port Elizabeth
L71  | 38.5839  | 0.71089  | +0.70101  | Vedrus Observatory, Azovskaya
L72  | 38.6928  | 0.55979  | +0.82589  | Melezhy Astrophoto Observatory
L75  | 26.46394 | 0.527292 | +0.846853 | Tartu Observatory of Tartu University
L76  | 39.65161 | 0.683530 | +0.727483 | Nomad Observatory, Kochevanchik
L80  | 18.0175  | 0.91802  | -0.39574  | SpringBok Observatory, Tivoli
L81  | 16.36169 | 0.919631 | -0.392204 | Skygems Namibia Remote Observatory
L82  |352.67950 | 0.775227 | +0.629726 | Crow Observatory, Portalegre
L83  |356.22231 | 0.791355 | +0.609451 | UJA Observatory, Jaen
L84  | 41.27989 | 0.695443 | +0.716182 | Kairos Observatory, Letnik
L94  |354.14561 | 0.728187 | +0.683146 | Observatorio MOMA, Oviedo
L95  |358.95159 | 0.793164 | +0.607000 | Observatorio Astronomico de Cartagena
L96  | 44.2745  | 0.76340  | +0.64416  | ISON-Byurakan Observatory
L97  |357.99161 | 0.624666 | +0.778298 | Castle Fields Observatory, Calne
L98  |357.43425 | 0.789394 | +0.612232 | La Sagra Observatory, Puebla de Don Fadrique
M43  | 54.68478 | 0.912805 | +0.407034 | Al Sadeem Observatory, Abu Dhabi
N27  | 73.7253  | 0.57847  | +0.81298  | Omsk-Yogik Observatory
N30  | 74.3694  | 0.85369  | +0.51909  | Zeds Astronomical Observatory, Lahore
N31  | 74.44422 | 0.853321 | +0.519690 | Eden Astronomical Observatory, Lahore
N42  | 76.97181 | 0.732126 | +0.679511 | Tien-Shan Astronomical Observatory
N43  | 77.1167  | 0.16712  | -0.98328  | Plateau Observatory for Dome A, Kunlun Station
N50  | 78.96383 | 0.842176 | +0.538692 | Himalayan Chandra Telescope, IAO, Hanle
N55  | 80.02623 | 0.846497 | +0.532089 | Corona Borealis Observatory, Ngari
N87  | 87.17503 | 0.727076 | +0.684720 | Nanshan Station, Xinjiang Observatory
N88  | 87.17322 | 0.727098 | +0.684697 | Xingming Observatory #3, Nanshan
O02  | 90.52614 | 0.866434 | +0.498958 | Galaxy Tibet YBJ Observatory,Yangbajing
O37  | 98.48553 | 0.948521 | +0.316891 | TRT-NEO, Chiangmai
O43  | 99.78111 | 0.994005 | +0.109127 | Observatori Negara, Langkawi
O44  |100.0310  | 0.89435  | +0.44698  | Lijiang Station, Yunnan Observatories
O45  |100.03261 | 0.894444 | +0.446808 | Yunnan-HK Observatory, Gaomeigu
O49  |101.18111 | 0.903206 | +0.428474 | Purple Mountain Observatory, Yaoan Station
O50  |101.43942 | 0.998617 | +0.052565 | Hin Hua Observatory, Klang
O75  |107.05180 | 0.672284 | +0.738151 | ISON-Hureltogoot Observatory
O85  |109.21300 | 0.826583 | +0.561181 | LiShan Observatory, Lintong
P25  |118.31274 | 0.910976 | +0.411089 | Kinmen Educational Remote Observatory, Jincheng
P34  |120.32031 | 0.855040 | +0.516826 | Lvye Observatory, Suzhou
P35  |120.55699 | 0.913398 | +0.405722 | Cuteip Remote Observatory, Changhua
P36  |120.62669 | 0.855207 | +0.516553 | ULTRA Observatory,Suzhou
P40  |121.53958 | 0.905916 | +0.422185 | Chinese Culture University, Taipei
P64  |127.00489 | 0.796371 | +0.602805 | GSHS Observatory, Suwon
P66  |127.44675 | 0.824763 | +0.563603 | Deokheung Optical Astronomy Observatory
P67  |127.7415  | 0.79040  | +0.61057  | Kangwon National University Observatory
P73  |129.0820  | 0.81744  | +0.57412  | BSH Byulsem Observatory, Busan
P87  |132.09419 | 0.830358 | +0.555374 | Hirao Observatory, Yamaguchi
P93  |133.54433 | 0.823371 | +0.565729 | Space Tracking and Communications Center, JAXA
Q02  |135.49344 | 0.825315 | +0.562809 | Sakai Observatory, Osaka
Q11  |137.52069 | 0.820236 | +0.570158 | Shinshiro
Q19  |139.4390  | 0.81430  | +0.57852  | Machida
Q21  |139.85335 | 0.804747 | +0.591654 | Southern Utsunomiya
Q23  |140.3864  | 0.79654  | +0.60264  | Sukagawa
Q24  |140.52350 | 0.810991 | +0.583108 | Katori
Q33  |142.48278 | 0.715989 | +0.695814 | Nayoro Observatory, Hokkaido University
Q38  |143.5506  | 0.81654  | -0.57538  | Swan Hill
Q54  |147.28772 | 0.739290 | -0.671278 | Harlingten Telescope, Greenhill Observatory
Q56  |148.97642 | 0.821480 | -0.568478 | Heaven\'s Mirror Observatory, Yass
Q57  |149.06173 | 0.855649 | -0.516175 | Korea Microlensing Telescope Network-SSO
Q58  |149.07085 | 0.855632 | -0.516199 | Siding Spring-LCO Clamshell #1
Q59  |149.07081 | 0.855626 | -0.516197 | Siding Spring-LCO Clamshell #2
Q60  |149.06900 | 0.855626 | -0.516198 | ISON-SSO Observatory, Siding Spring
Q61  |149.0619  | 0.85564  | -0.51618  | PROMPT, Siding Spring
Q62  |149.06442 | 0.855629 | -0.516206 | iTelescope Observatory, Siding Spring
Q63  |149.07064 | 0.855632 | -0.516202 | Siding Spring-LCO A
Q64  |149.07078 | 0.855632 | -0.516202 | Siding Spring-LCO B
Q65  |149.19313 | 0.855519 | -0.516201 | Warrumbungle Observatory
Q66  |149.06425 | 0.855627 | -0.516205 | Siding Spring-Janess-G, JAXA
Q67  |149.49233 | 0.835816 | -0.547369 | JBL Observatory, Bathurst
Q68  |150.33742 | 0.832917 | -0.551813 | Blue Mountains Observatory, Leura
Q69  |150.44933 | 0.832777 | -0.551945 | Hazelbrook
Q78  |152.94789 | 0.886807 | -0.460619 | Woogaroo Observatory, Forest Lake
Q79  |152.8481  | 0.88871  | -0.45696  | Samford Valley Observatory
Q80  |153.2160  | 0.88762  | -0.45904  | Birkdale
R57  |170.47278 | 0.720489 | -0.691309 | Aorangi Iti Observatory, Lake Tekapo
R58  |170.49039 | 0.697579 | -0.714138 | Beverly-Begg Observatory, Dunedin
T03  |203.74247 | 0.936240 | +0.351538 | Haleakala-LCO Clamshell #3
T04  |203.74249 | 0.936241 | +0.351538 | Haleakala-LCO OGG B #2
T05  |203.74299 | 0.936235 | +0.351547 | ATLAS-HKO, Haleakala
T08  |204.42395 | 0.943290 | +0.332467 | ATLAS-MLO, Mauna Loa
T09  |204.52398 | 0.941706 | +0.337237 | Mauna Kea-UH/Tholen NEO Follow-Up (Subaru)
T10  |204.52241 | 0.941706 | +0.337212 | Submillimeter Array, Mauna Kea (SMA)
T12  |204.53057 | 0.941729 | +0.337199 | Mauna Kea-UH/Tholen NEO Follow-Up (2.24-m)
T14  |204.53113 | 0.941714 | +0.337236 | Mauna Kea-UH/Tholen NEO Follow-Up (CFHT)
U53  |237.1603  | 0.70274  | +0.70909  | Murray Hill Observatory, Beaverton
U54  |237.31286 | 0.782952 | +0.620081 | Hume Observatory, Santa Rosa
U55  |237.41456 | 0.653977 | +0.753984 | Golden Ears Observatory, Maple Ridge
U56  |237.86917 | 0.795044 | +0.604511 | Palo Alto
U57  |237.84128 | 0.795776 | +0.603616 | Black Mountain Observatory, Los Altos
U63  |239.19456 | 0.681217 | +0.729770 | Burnt Tree Hill Observatory, Cle Elum
U64  |239.46151 | 0.683272 | +0.727821 | CWU-Lind Observatory, Ellensburg
U67  |240.20358 | 0.776325 | +0.628595 | Jack C. Davis Observatory, Carson City
U68  |240.58701 | 0.799040 | +0.599620 | JPL SynTrack Robotic Telescope, Auberry
U69  |240.5870  | 0.79904  | +0.59962  | iTelescope SRO Observatory, Auberry
U70  |240.5869  | 0.79904  | +0.59962  | RASC Observatory, Alder Springs
U71  |241.3633  | 0.82520  | +0.56305  | AHS Observatory, Castaic
U72  |241.46000 | 0.828150 | +0.558687 | Tarzana
U73  |241.6172  | 0.83164  | +0.55346  | Redondo Beach
U76  |242.1279  | 0.82855  | +0.55810  | Glendora
U77  |242.9181  | 0.84002  | +0.54076  | Rani Observatory, San Diego
U78  |242.8449  | 0.82758  | +0.55989  | Cedar Glen Observatory
U79  |242.79187 | 0.838837 | +0.542598 | Cosmos Research Center, Encinitas
U80  |243.6151  | 0.82737  | +0.56004  | CS3-DanHenge Observatory, Landers
U81  |243.61514 | 0.827367 | +0.560037 | CS3-Trojan Station, Landers
U82  |243.61519 | 0.827368 | +0.560036 | CS3-Palmer Divide Station, Landers
U83  |243.57311 | 0.841238 | +0.53938  | Mount Laguna Observatory
U96  |246.68600 | 0.579007 | +0.812698 | Athabasca University Geophysical Observatory
V00  |248.39981 | 0.849456 | +0.526492 | Kitt Peak-Bok
V01  |248.23911 | 0.762243 | +0.645493 | Mountainville Observatory, Alpine
V02  |248.05794 | 0.835743 | +0.547377 | Command Module, Tempe
V03  |248.3314  | 0.79889  | +0.59979  | Big Water
V04  |248.46331 | 0.819378 | +0.571927 | FRoST, Anderson Mesa
V05  |248.63195 | 0.836631 | +0.546101 | Rusty Mountain Observatory, Gold Canyon
V06  |249.26745 | 0.845317 | +0.533211 | Catalina Sky Survey-Kuiper
V07  |249.1219  | 0.85208  | +0.52234  | Whipple Observatory, Mount Hopkins-PAIRITEL
V08  |249.33900 | 0.848249 | +0.528126 | Mountain Creek Ranch, Vail
V09  |249.74202 | 0.849537 | +0.526080 | Moka Observatory, Benson
V10  |248.32772 | 0.818623 | +0.572977 | Sierra Sinagua Observatory, Flagstaff
V11  |249.21119 | 0.847025 | +0.530011 | Saguaro Observatory, Tucson
V12  |249.39819 | 0.852110 | +0.522050 | Elgin
V14  |248.78336 | 0.762292 | +0.645691 | Moose Springs Observatory, Timber Lakes
V16  |251.10288 | 0.849510 | +0.526194 | Dark Sky New Mexico, Animas
V19  |251.79086 | 0.841371 | +0.539217 | Whiskey Creek Observatory
V20  |251.77822 | 0.827004 | +0.560943 | Killer Rocks Observatory, Pie Town
V23  |252.76406 | 0.828722 | +0.558332 | FOAH Observatory, Magdalena
V26  |253.39020 | 0.911283 | +0.410639 | UAS-ISON Observatory, Cosala
V28  |254.34647 | 0.817018 | +0.575271 | Deep Sky West Observatory, Rowe
V29  |254.26660 | 0.840062 | +0.541466 | Tzec Maun Cloudcroft Facility
V30  |254.47105 | 0.840710 | +0.540313 | Heaven on Earth Observatory, Mayhill
V31  |254.4750  | 0.84061  | +0.54046  | Hazardous Observatory, Mayhill
V34  |255.36992 | 0.778401 | +0.626222 | Black Forest
V35  |255.91881 | 0.861839 | +0.506046 | Deep Sky Observatory Collaborative, Pier 5
V36  |255.61742 | 0.843042 | +0.536333 | The Ranch Observatory, Lakewood
V37  |255.98483 | 0.861053 | +0.507428 | McDonald Observatory-LCO ELP
V38  |255.98493 | 0.861051 | +0.507431 | McDonald Observatory-LCO ELP Aqawan A #1
V39  |255.98452 | 0.861051 | +0.507430 | McDonald Observatory-LCO ELP B
V59  |261.0734  | 0.86642  | +0.49781  | Millwood Observatory, Comfort
V60  |261.09473 | 0.862140 | +0.505126 | Putman Mountain Observatory
V70  |263.33572 | 0.870056 | +0.491332 | Starry Night Observatory, Columbus
V78  |265.10780 | 0.700141 | +0.711688 | Spirit Marsh Observatory. Sauk Centre
V81  |265.7604  | 0.80902  | +0.58590  | Fayetteville
V83  |266.25728 | 0.781733 | +0.621590 | Rolling Hills Observatory, Warrensburg
V86  |266.8927  | 0.78221  | +0.62099  | Rattle Snake Observatory, Sedalia
V88  |267.42811 | 0.820618 | +0.569618 | River Ridge Observatory, Conway
V93  |268.61611 | 0.759765 | +0.648058 | Pin Oak Observatory, Fort Madison
V94  |268.66169 | 0.759876 | +0.647933 | Cherokeeridge Observatory, Fort Madison
W04  |271.00944 | 0.761606 | +0.645927 | Mark Evans Observatory, Bloomington
W08  |271.88331 | 0.747086 | +0.662545 | Jimginny Observatory, Naperville
W11  |272.6247  | 0.75272  | +0.65618  | Northwest Indiana Robotic Telescope, Lowell
W14  |273.24511 | 0.821914 | +0.567774 | Harvest
W16  |273.76869 | 0.822976 | +0.566292 | Pleasant Groves Observatory
W19  |274.37283 | 0.740783 | +0.669559 | Kalamazoo
W22  |275.00447 | 0.844595 | +0.533635 | WestRock Observatory, Columbus
W25  |275.63506 | 0.776417 | +0.628165 | RMS Observatory, Cincinnati
W28  |276.3883  | 0.83011  | +0.55581  | Ex Nihilo Observatory, Winder
W30  |276.77117 | 0.838735 | +0.542749 | Georgia College Observatory, Milledgeville
W31  |277.23736 | 0.834226 | +0.549613 | Deerlick Observatory, Crawfordville
W32  |277.23750 | 0.834222 | +0.549619 | Crawfordville Observatory
W33  |277.83451 | 0.819315 | +0.571499 | Transit Dreams Observatory, Campobello
W34  |277.8453  | 0.81784  | +0.57360  | Squirrel Valley Observatory, Columbus
W38  |278.58531 | 0.807479 | +0.588163 | Dark Sky Observatory, Boone
W46  |280.41192 | 0.818614 | +0.572448 | Foxfire Village
W49  |281.06757 | 0.778794 | +0.625380 | CBA-MM Observatory, Mountain Meadows
W50  |281.25404 | 0.813127 | +0.580167 | Apex
W54  |282.28944 | 0.785431 | +0.616890 | Mark Slade Remote Observatory, Wilderness
W55  |282.58389 | 0.773703 | +0.631447 | Natelli Observatory, Frederick
W61  |283.74492 | 0.713380 | +0.698447 | Leeside Observatory, Elgin
W63  |284.30958 | 0.996767 | +0.082976 | Observatorio Astronomico UTP, Pereira
W65  |284.79169 | 0.697761 | +0.713966 | Observatoire GOZ, Montpellier
W66  |285.05381 | 0.756278 | +0.652109 | SVH Observatory, Blairstown
W67  |285.10211 | 0.759453 | +0.648444 | Paul Robinson Observatory, Voorhees State Park
W70  |285.91386 | 0.698475 | +0.713264 | Loose Goose Observatory, Saint-Jerome
W71  |285.99297 | 0.717404 | +0.694456 | Rand II Observatory, Lake Placid
W74  |289.26245 | 0.873451 | -0.486040 | Danish Telescope, La Silla
W75  |289.60944 | 0.910001 | -0.414150 | SPECULOOS-South Observatory, Paranal
W76  |289.23695 | 0.862826 | -0.504288 | CHILESCOPE Observatory, Rio Hurtad
W77  |287.4010  | 0.75196  | +0.65702  | Skyledge Observatory, Killingworth
W78  |288.88325 | 0.739859 | +0.670509 | Clay Telescope, Harvard University
W79  |289.19535 | 0.865587 | -0.499763 | Cerro Tololo-LCO Aqawan B #1
W80  |288.7678  | 0.74138  | +0.66885  | Westwood
W81  |288.99967 | 0.724557 | +0.686948 | Nebula Knoll Observatoy, East Wakefield
W82  |288.87804 | 0.736419 | +0.674274 | Mendel Observatory, Merrimack College
W83  |288.69747 | 0.740821 | +0.669461 | Whitin Observatory, Wellesley
W84  |289.19358 | 0.865572 | -0.499793 | Cerro Tololo-DECam
W85  |289.19519 | 0.865591 | -0.499760 | Cerro Tololo-LCO A
W86  |289.19533 | 0.865592 | -0.499759 | Cerro Tololo-LCO B
W87  |289.19532 | 0.865591 | -0.499761 | Cerro Tololo-LCO C
W88  |289.46570 | 0.837136 | -0.545574 | Slooh.com Chile Observatory, La Dehesa
W89  |289.19533 | 0.865589 | -0.499764 | Cerro Tololo-LCO Aqawan A #1
W90  |289.05814 | 0.732740 | +0.678229 | Phillips Exeter Academy Grainger Observatory
W91  |289.60257 | 0.910007 | -0.414148 | VHS-VISTA, Cerro Paranal
W92  |290.67357 | 0.850987 | -0.524150 | MASTER-OAFA Observatory, San Juan
W93  |289.19600 | 0.865589 | -0.499755 | Korea Microlensing Telescope Network-CTIO
W94  |291.82019 | 0.921646 | -0.387713 | AMACS1, San Pedro de Atacama
W95  |291.82012 | 0.921639 | -0.387712 | Observatorio Panameno, San Pedro de Atacama
W96  |291.82006 | 0.921637 | -0.387717 | CAO, San Pedro de Atacama (since 2013)
W97  |291.82024 | 0.921638 | -0.387716 | Atacama Desert Observatory, San Pedro de Atacama
W98  |291.82030 | 0.921639 | -0.387712 | Polonia Observatory, San Pedro de Atacama
W99  |291.82015 | 0.921638 | -0.387716 | SON, San Pedro de Atacama Station
X00  |292.60125 | 0.910349 | -0.413802 | Observatorio Astronomico Tolar
X01  |289.23502 | 0.862846 | -0.504270 | Observatory Hurtado, El Sauce
X02  |289.23517 | 0.862833 | -0.504255 | Telescope Live, El Sauce
X03  |289.20361 | 0.862286 | -0.505209 | Observatoire SADR, Poroto
X12  |295.71200 | 0.803430 | -0.593455 | Observatorio Los Cabezones
X13  |295.4498  | 0.85269  | -0.52103  | Observatorio Remoto Bosque Alegre
X14  |295.83222 | 0.854475 | -0.517879 | Observatorio Orbis Tertius, Cordoba
X31  |299.47934 | 0.850485 | -0.524263 | Galileo Galilei Observatory, Oro Verde
X38  |301.13711 | 0.825648 | -0.562299 | Observatorio Pueyrredon, La Lonja
X39  |301.1378  | 0.82615  | -0.56158  | Observatorio Antares, Pilar
X50  |303.82419 | 0.821025 | -0.568999 | Observatorio Astronomico de Montevideo
X57  |305.40626 | 0.903659 | -0.426885 | Polo Astronomico CMF,Foz do Iguacu
X74  |309.1506  | 0.92987  | -0.36684  | Observatorio Campo dos Amarais
X87  |312.0889  | 0.96218  | -0.27210  | Dogsheaven Observatory, Brasilia
X88  |312.49131 | 0.918012 | -0.395458 | Observatorio Adhara, Sorocaba
Y00  |315.21504 | 0.935906 | -0.351562 | SONEAR Observatory, Oliveira
Y16  |318.68794 | 0.929268 | -0.368170 | ROCG, Campos dos Goytacazes
Y28  |321.3126  | 0.98840  | -0.15179  | OASI, Nova Itacuruba
Y40  |324.03889 | 0.989706 | -0.143217 | Discovery Observatory, Caruaru
Z10  |353.37235 | 0.786766 | +0.615329 | PGC, Fregenal de la Sierra
Z11  |358.96669 | 0.601635 | +0.796115 | Appledorne Observatory, Farnsfield
Z12  |359.0961  | 0.78494  | +0.61762  | La Romaneta, Monovar
Z13  |355.54519 | 0.802515 | +0.594662 | Observatorio AGP GUAM 4, Malaga
Z14  |353.37226 | 0.786773 | +0.615335 | ART, Fregenal de la Sierra
Z15  |359.65331 | 0.630352 | +0.773724 | Southwater
Z16  |358.95192 | 0.793166 | +0.607001 | Asociacion Astronomica de Cartagena
Z17  |343.48827 | 0.881476 | +0.471456 | Tenerife-LCO Aqawan A #2
Z18  |342.10811 | 0.877671 | +0.478415 | Gran Telescopio Canarias, Roque de los Muchachos
Z19  |342.11094 | 0.877701 | +0.478380 | La Palma-TNG
Z20  |342.1217  | 0.87763  | +0.47850  | La Palma-MERCATOR
Z21  |343.48830 | 0.881468 | +0.471452 | Tenerife-LCO Aqawan A #1
Z22  |343.4894  | 0.88148  | +0.47143  | MASTER-IAC Observatory, Tenerife
Z23  |342.11492 | 0.877679 | +0.478433 | Nordic Optical Telescope, La Palma
Z25  |343.49031 | 0.881476 | +0.471450 | Artemis Observatory, Teide
Z26  |343.38969 | 0.883010 | +0.467899 | Observatorio Astronomico Arcangel, Las Zocas
Z27  |343.6998  | 0.87976  | +0.47393  | Observatorio Coralito, La Laguna
Z29  |354.11944 | 0.751634 | +0.657576 | Observatorio Astronomico Sobradillo
Z30  |355.52500 | 0.586571 | +0.807215 | Glyn Marsh Observatory, Douglas
Z32  |358.98372 | 0.766879 | +0.640130 | Observatorio Astrofisico de Javalambre
Z33  |357.67331 | 0.787438 | +0.614748 | 6ROADS Observatory 2, Nerpio
Z34  |359.11233 | 0.612800 | +0.787622 | NNHS Drummonds Observatory
Z35  |358.8985  | 0.76788  | +0.63877  | OAO University Observatory Station Aras
Z36  |354.94553 | 0.805224 | +0.591005 | Cancelada
Z37  |357.80426 | 0.632788 | +0.771754 | Northolt Branch Observatory 3, Blandford Forum
Z38  |351.15294 | 0.768722 | +0.637456 | Picoto Observatory, Leiria
Z39  |346.4989  | 0.87535  | +0.48189  | Observatorio Costa Teguise
Z40  |355.5127  | 0.80240  | +0.59482  | El Manzanillo Observatory, Puerto de la Torre
Z41  |356.6264  | 0.76087  | +0.64689  | Irydeo Observatory, Camarma de Esteruelas
Z42  |357.66579 | 0.631495 | +0.772801 | Rushay Farm Observatory, Sturminster Newton
Z43  |357.4622  | 0.66474  | +0.74460  | Landehen
Z44  |351.67248 | 0.728723 | +0.682549 | Observatorio Terminus, A Coruna
Z45  |355.14264 | 0.804657 | +0.591779 | Cosmos Observatory, Marbella
Z46  |356.80700 | 0.623612 | +0.779131 | Cardiff
Z47  |357.2925  | 0.59846  | +0.79849  | Runcorn
Z48  |359.74915 | 0.623799 | +0.778975 | Northolt Branch Observatory 2, Shepherd\'s Bush
Z49  |357.40631 | 0.591893 | +0.803336 | Alston Observatory
Z50  |355.28431 | 0.744053 | +0.666069 | Mazariegos
Z51  |356.4486  | 0.76313  | +0.64423  | Anunaki Observatory, Rivas Vaciamadrid
Z52  |359.33899 | 0.604299 | +0.794113 | The Studios Observatory, Grantham
Z53  |352.1336  | 0.85645  | +0.51534  | TRAPPIST-North, Oukaimeden
Z54  |358.92214 | 0.623422 | +0.779306 | Greenmoor Observatory, Woodcote
Z55  |354.9150  | 0.79391  | +0.60604  | Uraniborg Observatory, Ecija
Z56  |350.2119  | 0.61577  | +0.78529  | Knocknaboola
Z57  |355.42589 | 0.803207 | +0.593753 | Observatorio Zuben, Alhaurin de la Torre
Z58  |355.63068 | 0.762093 | +0.645483 | ESA Cebreros TBT Observatory, Cebreros
Z59  |357.71540 | 0.599292 | +0.797871 | Chelford Observatory
Z60  |357.8506  | 0.73205  | +0.67900  | Observatorio Zaldibia
Z61  |359.06400 | 0.748594 | +0.660857 | Montecanal Observatory, Zaragoza
Z62  |351.62912 | 0.737181 | +0.673585 | Observatorio Forcarei
Z63  |358.47002 | 0.746291 | +0.663495 | Skybor Observatory, Borja
Z64  |352.1424  | 0.74016  | +0.67021  | Observatorio el Miron del Cielo
Z65  |352.17252 | 0.741388 | +0.668906 | Observatorio Astronomico Corgas
Z66  |355.59156 | 0.783284 | +0.619848 | DeSS Deimos Sky Survey, Niefla Mountain
Z67  |353.52314 | 0.597320 | +0.799328 | Dunboyne Castle Observatory
Z68  |353.4003  | 0.77964  | +0.62418  | Observatorio Torreaguila, Barbano
Z69  |353.1870  | 0.79823  | +0.60034  | Observatorio Mazagon Huelva
Z70  |353.35711 | 0.737583 | +0.673113 | Ponferrada
Z71  |353.60972 | 0.773272 | +0.632064 | Observatorio Norba Caesarina, Aldea Moret
Z72  |353.88864 | 0.599295 | +0.797856 | Cademuir Observatory, Dalkey
Z73  |353.96731 | 0.795365 | +0.604101 | Observatorio Nuevos Horizontes, Camas
Z74  |354.1562  | 0.79610  | +0.60315  | Amanecer de Arrakis
Z75  |354.4676  | 0.73736  | +0.67346  | Observatorio Sirius, Las Lomas
Z76  |354.5644  | 0.72675  | +0.68460  | Observatorio Carda, Villaviciosa
Z77  |354.88958 | 0.797212 | +0.601739 | Osuna
Z78  |358.32420 | 0.788031 | +0.613690 | Arroyo Observatory, Arroyo Hurtado
Z79  |357.45327 | 0.797556 | +0.601783 | Calar Alto TNO Survey
Z80  |359.62808 | 0.623054 | +0.779568 | Northolt Branch Observatory
Z81  |355.73240 | 0.802530 | +0.594629 | Observatorio Estrella de Mar
Z82  |355.95903 | 0.802135 | +0.595173 | BOOTES-2 Observatory, Algarrobo
Z83  |356.2881  | 0.76033  | +0.64755  | Chicharronian 3C Observatory, Tres Cantos
Z84  |357.45179 | 0.797523 | +0.601826 | Calar Alto-Schmidt
Z85  |356.75028 | 0.801058 | +0.596932 | Observatorio Sierra Contraviesa
Z86  |356.8900  | 0.62347  | +0.77923  | St. Mellons
Z87  |357.10210 | 0.608005 | +0.791293 | Stanley Laver Observatory, Pontesbury
Z88  |357.5101  | 0.62716  | +0.77632  | Fosseway Observatoy, Stratton-on-the-Fosse
Z89  |357.8281  | 0.59942  | +0.79777  | Macclesfield
Z90  |357.8482  | 0.79540  | +0.60418  | Albox
Z91  |358.74999 | 0.631731 | +0.772595 | Curdridge
Z92  |358.39222 | 0.591378 | +0.803713 | Almalex Observatory, Leeds
Z93  |359.85589 | 0.782380 | +0.620769 | Observatorio Polop, Alicante
Z94  |358.8565  | 0.62725  | +0.77623  | Kempshott
Z95  |358.8909  | 0.76782  | +0.63883  | Astronomia Para Todos Remote Observatory
Z96  |359.19369 | 0.747818 | +0.661731 | Observatorio Cesaraugusto
Z97  |359.41647 | 0.704568 | +0.707270 | OPERA Observatory, Saint Palais
Z98  |359.5216  | 0.77156  | +0.63405  | Observatorio TRZ, Betera
Z99  |359.97874 | 0.595468 | +0.800687 | Clixby Observatory, Cleethorpes
"""


sqlitetable = """CREATE TABLE MPCCodes
(
   code         text,    -- combination of numbers and letters
   observatory  text,    -- the text of observatory
   longitude    float,   -- MPC states longitude...
   latitide     float,   -- Proxy for MPC latitude
   cosphi       float,   -- cos of phi prime
   sinphi       float    -- sin of phi prime
);
"""

##############################################################################
# fixmpc
#
##############################################################################
def fixmpc(site,longitude,cosphi,sinphi):
   """Convert the cos/sin into a rough long/lat
   The mpc has cosphi and sinphi already computed. No need to do that.
   We are backing all that back to a real latitude anyway.
   uhuo
   https://astronomy.stackexchange.com/questions/35535/can-i-use-the-parallax-coefficients-for-observatories-as-a-proxy-for-latitude-us
   """
   radlong = np.radians(longitude)
   coslong, sinlong = np.cos(radlong), np.sin(radlong)
   h       = 1000.
   a, b    = 6378.1370, 6356.7523 # only their ratio matters in this case
   denom = np.sqrt(a**2 * cosphi**2 + b**2 * sinphi**2)
   ret = np.NaN
   if(np.abs(denom) > 1e-9):
      N       = a**2 / np.sqrt(a**2 * cosphi**2 + b**2 * sinphi**2)
      X       = (N + h) * cosphi * np.cos(longitude)
      Y       = (N + h) * cosphi * np.sin(longitude)
      Z       = ((b/a)**2 * N + h) * sinphi

      ret = phi_prime = np.arctan(Z/X) # two quandrants so no need for arctan2
   else:
      raise Exception("fixmpc error: {}".format(f'   site {site}\n   longitude {longitude}\n   cosphi {cosphi}\n   sinphi {sinphi}'))
   return ret

# def fixmpc

##############################################################################
# plotfixes
#
##############################################################################
def plotfixes():
   """The rest of the example."""
   phi               = np.linspace(-halfpi, halfpi, 101)
   lam               = 0.
   halfpi, pi, twopi = [f*np.pi for f in (0.5, 1, 2)]
   todegs            = 180/pi

   plt.figure()
   plt.plot(todegs*phi, todegs*(phi_prime-phi))
   plt.xlabel('geodetic ("GPS") latitude (degs)', fontsize=12)
   plt.ylabel('geocentric - geodetic latitude (degs)', fontsize=12)
   plt.xlim(-90, 90)
   plt.show()

# def plotfixes

##############################################################################
# MPCCodes -- write the dabtase of codes
#
##############################################################################
def MPCCodes(insertstmt):
   """Given a preformatted list of lines to insert, do it. Remember
   that last COMMIT!
   """
   conn     = db.connect('MPCCodes.db')
   cursor   = conn.cursor()
   tables   = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
   if('MPCCodes' in [ t[0] for t in tables]):
      cursor.execute("DROP TABLE MPCCodes")
   rc1 = cursor.execute(sqlitetable)
   rc2 = cursor.execute(insertstmt)
   rc3 = cursor.execute('COMMIT;')

# MPCCodes

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

   # code     longitude       cosphi      sinphi         text
   # Z99  |359.97874 | 0.595468 | +0.800687 | Clixby Observatory, Cleethorpes

   inserts  = [] # accumulate all the insert statememts
   combobox = []

   lines   = MPCText.split('\n')
   lc = 0
   for l in lines:
      try:
         lc += 1
         parts       = list(map(str.strip,l.split('|')))
         plen = len(parts)
         if(plen != 5):
            if(options.verboseflag): print("Parts is wrong length {}".format(plen),file=sys.stderr)
            continue
         if('' in parts[1:4]):
            if(options.verboseflag): print(parts[4],"Missing one of",parts[1:4],file=sys.stderr)
            continue
         #if(False in map(lambda a: a == None,map(zerore.match,parts[2:4]))):
         #   print("A zero in the mix",parts[2:4],file=sys.stderr)
         #   continue
         code        = parts[0]
         longitude   = float(parts[1])
         cosphi      = float(parts[2])
         sinphi      = float(parts[3])
         observatory = parts[4]
         if("'" in observatory):
            observatory = tickre.suball("\\'",observatory)
         latitude    = fixmpc(observatory,longitude,cosphi,sinphi)
         inserts.append(f'( \'{code}\', \'{observatory}\', {longitude}, {latitude}, {cosphi}, {sinphi} )')
         combobox.append(f'\'{code}: {observatory}\'')
      except Exception as e:
         if(options.verboseflag): print("Error line {:d}\n ".format(lc))
         if(options.verboseflag): print(e.__str__())
         if(options.verboseflag): print(parts)

   with open('MPCCodeCombo.txt','w') as f:
      print("MPCCodeCombo = [",file=f)
      print("{:s}".format(',\n'.join(combobox)),file=f)
      print("]",file=f)

   insertstmt = """INSERT INTO MPCCodes (code, observatory, longitude, latitide, cosphi, sinphi) values\n"""
   insertstmt += ',\n'.join(inserts) + ';\n'
   with open('MPCImport.txt','w') as o:
      print(insertstmt,file=o)

   MPCCodes(insertstmt)