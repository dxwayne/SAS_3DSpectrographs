__init__ = ["SiteUI_savejsondict","SiteUI_loadjsondict"]
def SiteUI_savejsondict(self,jdict):
   '''Autogenerated code from ui's make/awk trick.'''
   jdict['currentSite'] = self.currentSite.text()
   jdict['obsgeo_b'] = self.obsgeo_b.text()
   jdict['obsgeo_h'] = self.obsgeo_h.text()
   jdict['obsgeo_l'] = self.obsgeo_l.text()

# def SiteUI_savejsondict
def SiteUI_loadjsondict(self,jdict):
   '''Autogenerated code from ui's make/awk trick.'''
   self.currentSite.setText(jdict['currentSite'])
   self.obsgeo_b.setText(jdict['obsgeo_b'])
   self.obsgeo_h.setText(jdict['obsgeo_h'])
   self.obsgeo_l.setText(jdict['obsgeo_l'])

# def SiteUI_loadjsondict
