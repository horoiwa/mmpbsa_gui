from modeller import *
from modeller.automodel import *

log.verbose()
env = environ()

a = automodel(env,
              alnfile  = 'align.pir',
              knowns   = ['3IXP', '1R1K'],
              sequence = 'TARGET')
a.starting_model= 1
a.ending_model  = 1
a.make()
