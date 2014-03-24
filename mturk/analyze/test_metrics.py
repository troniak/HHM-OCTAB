from agreement_metrics import *

As = [4,12]
Ae = [9,14]
Bs = [1,4,6,8,13]
Be = [2,4,6,8,15]
print 'eam: ' + str(calc_event_agreement(As,Ae,Bs,Be))

As = [4,12]
Ae = [8,13]
Bs = [2,8,15]
Be = [5,10,15]
print 'sam: ' + str(calc_segmentation_agreement(As,Ae,Bs,Be))
