from base       import *


class AMRCS2ThrustChamber4:

    def __init__(self, DB):

        params = DB.AM["AM_RCS2_THRUST_CHAMBER4"]

        self.m       = params["m_0"]
        self.p_c     = array(params["p_c"]   )
        self.p_cg    = array(params["p_cg"]  )
        self.dim     = array(params["dim"]   )

        self.uvec    = zeros(3)
        self.Mvec    = zeros(3)

        self.DB      = DB

    
    def update(self):

        self.uvec    = self.DB.u[9] * array([0,0,-1])
        self.Mvec    = cross(self.p_cg, self.uvec)