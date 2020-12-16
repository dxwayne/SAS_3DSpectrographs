#############################################################################
# Makefile -- turn ui files into their python counterparts.
#############################################################################

UIC = pyside2-uic

%.py : %.ui
	$(UIC) -o $@ $<

PYTHONFILES = ../AttitudeUI.py        \
              ../NASpectrographyUI.py \
              ../SiteUI.py            \
              ../SpectrographUI.py    \
              ../LogDialogUI.py


UISRCS      = AttitudeUI.ui           \
              NASpectrographyUI.ui    \
              SiteUI.ui               \
              SpectrographUI.ui       \
              LogDialogUI.ui

SEDSCR = sed -e 's/^.*class=//g; s/name=/ /g; s/>//g; s/"//g; '
GREPCMD = grep -v "\(/widget\|QLabel\|QToolButton\|QPushButton\|Snapshot\|DialogButton\)"

all: $(PYTHONFILES)

../AttitudeUI.py        : AttitudeUI.ui ./varmake.awk
	$(UIC) -o $@ $<
	-(grep widget AttitudeUI.ui | $(GREPCMD) | $(SEDSCR) | sort | ./varmake.awk -v prefix=AttitudeUI)  > ../AttitudeVariables.py

../NASpectrographyUI.py : NASpectrographyUI.ui ./varmake.awk
	$(UIC) -o $@ $<
	-(grep widget NASpectrographyUI.ui | $(GREPCMD) | $(SEDSCR) | sort | ./varmake.awk -v prefix=NASpectrographyUI)  > ../NASpectrographyVariables.py

../SiteUI.py            : SiteUI.ui ./varmake.awk
	$(UIC) -o $@ $<
	-(grep widget SiteUI.ui | $(GREPCMD) | $(SEDSCR) | sort | ./varmake.awk -v prefix=SiteUI)  > ../SiteVariables.py

../SpectrographUI.py    : SpectrographUI.ui ./varmake.awk
	$(UIC) -o $@ $<
	-(grep widget SpectrographUI.ui | $(GREPCMD) | $(SEDSCR) | sort | ./varmake.awk -v prefix=SpectrographUI)  > ../SpectrographVariables.py


../LogDialogUI.py : LogDialogUI.ui ./varmake.awk
	$(UIC) -o $@ $<
	-(grep widget LogDialogUI.ui | $(GREPCMD) | $(SEDSCR) | sort | ./varmake.awk -v prefix=LogDialogUI)  > ../LogDialogVariables.py
