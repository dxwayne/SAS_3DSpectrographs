__init__ = ["LogDialogUI_savejsondict","LogDialogUI_loadjsondict"]
def LogDialogUI_savejsondict(self,jdict):
   '''Autogenerated code from ui's make/awk trick.'''
   jdict['logText'] = self.logText.toPlainText()

# def LogDialogUI_savejsondict
def LogDialogUI_loadjsondict(self,jdict):
   '''Autogenerated code from ui's make/awk trick.'''
   self.logText.insertPlainText(jdict['logText'])

# def LogDialogUI_loadjsondict
