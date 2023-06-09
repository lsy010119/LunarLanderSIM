from base       import *


class AMRCS1ThrustChamber5:

    def __init__(self, DB):

        params = DB.AM["AM_RCS1_THRUST_CHAMBER5"]

        self.m       = params["m_0"]
        self.p_c     = array(params["p_c"]   )
        self.p_cg    = array(params["p_cg"]  )
        self.dim     = array(params["dim"]   )

        self.uvec    = zeros(3)
        self.Mvec    = zeros(3)

        self.DB      = DB

    
    def update(self):

        self.uvec    = self.DB.u[5] * array([-1,0,0])
        self.Mvec    = cross(self.p_cg, self.uvec)
