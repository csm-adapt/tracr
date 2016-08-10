#!/usr/bin/env python

"""
DESCRIPTION

    Script for saving the outputs (u, s, v, b, T, e) from several versions of
    the PCR scripts.
"""
import numpy as np
from pcr_mednn import wrap as mednn
from pcr_vol import wrap as vol
from pcr_RdTdRad_mednn import wrap as RdTdRad_mednn
from pcr_RdTdRad_vol import wrap as RdTdRad_vol
from pcr_PolAzi_mednn import wrap as pcr_PolAzi_mednn
from pcr_PolAzi_vol import wrap as pcr_PolAzi_vol

u, s, v, b, T, e = mednn()
mednn_dict = {'u': u, 's': s, 'v': v, 'b': b, 'T': T, 'e': e}
np.save('PCR_mednn.npy', mednn_dict)
u, s, v, b, T, e = vol()
vol_dict = {'u': u, 's': s, 'v': v, 'b': b, 'T': T, 'e': e}
np.save('PCR_vol.npy', vol_dict)
u, s, v, b, T, e = RdTdRad_mednn()
RTRad_mednn_dict = {'u': u, 's': s, 'v': v, 'b': b, 'T': T, 'e': e}
np.save('PCR_RdTdRad_mednn.npy', RTRad_mednn_dict)
u, s, v, b, T, e = RdTdRad_vol()
RTRad_vol_dict = {'u': u, 's': s, 'v': v, 'b': b, 'T': T, 'e': e}
np.save('PCR_RdTdRad_vol.npy', RTRad_vol_dict)
u, s, v, b, T, e = pcr_PolAzi_mednn()
PolAzi_mednn_dict = {'u': u, 's': s, 'v': v, 'b': b, 'T': T, 'e': e}
np.save('PCR_PolAzi_mednn.npy', PolAzi_mednn_dict)
u, s, v, b, T, e = pcr_PolAzi_vol()
PolAzi_vol_dict = {'u': u, 's': s, 'v': v, 'b': b, 'T': T, 'e': e}
np.save('PCR_PolAzi_vol.npy', PolAzi_vol_dict)
