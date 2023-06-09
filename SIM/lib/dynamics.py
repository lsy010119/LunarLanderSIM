from base   import *
from lib.transformations    import *


def f(x, t, DB):

    ### 6-DOF Equation of motion ###
    
    r_i       = x[:3]
    v_b       = x[3:6]
    O_i       = x[6:9]
    w_b       = x[9:12]

    C_i2b     = C_W2B(O_i[0],O_i[1],O_i[2])
    T_b2i     = T_w2W(O_i[0],O_i[1],O_i[2])

    sum_F     = DB.sum_F
    sum_M     = DB.sum_M


    g_M       = C_i2b @ (-r_i * G*M/(norm(r_i)**3))

    r_i_dot   = C_i2b.T @ v_b
    
    v_b_dot   = g_M + (1/DB.m) * sum_F - cross(w_b, v_b)

    O_i_dot   = T_b2i @ w_b

    w_b_dot   = inv(DB.I) @ ( sum_M - cross(w_b,(DB.I @ w_b)) )

    x_dot     = zeros(12)

    x_dot[:3]   = r_i_dot
    x_dot[3:6]  = v_b_dot
    x_dot[6:9]  = O_i_dot
    x_dot[9:12] = w_b_dot

    DB.x_dot    = x_dot
    DB.g_M      = g_M

    return x_dot


def update_state(DB):

    ### RK 6 Integration ###
    
    x_1     = DB.x

    K1      = DB.del_t*f(x_1, 0, DB)
    K2      = DB.del_t*f(x_1 + (1/6)*K1, 0, DB)
    K3      = DB.del_t*f(x_1 + (4/75)*K1 + (16/75)*K2, 0, DB)
    K4      = DB.del_t*f(x_1 + (5/6) *K1 - (8/3)  *K2 + (5/2)*K3, 0, DB)
    K5      = DB.del_t*f(x_1 - (165/64)*K1 + (55/6)*K2 - (425/64)*K3 + (85/96)*K4, 0, DB)
    K6      = DB.del_t*f(x_1 + (12/5)*K1 - 8*K2 + (4015/612)*K3 - (11/36)*K4 + (88/255)*K5, 0, DB)
    K7      = DB.del_t*f(x_1 - (8263/15000)*K1 + (124/75)*K2 - (643/680)*K3 - (81/250)*K4 + (2484/10625)*K5, 0, DB)
    K8      = DB.del_t*f(x_1 + (3501/1720)*K1 - (300/43)*K2 + (297275/52632)*K3 - (319/2322)*K4 + (24068/84065)*K5 + (3850/26703)*K7, 0, DB)

    x_2     = x_1 + (3/40)*K1 + (875/2244)*K3 + (23/72)*K4 + (264/1955)*K5 + (125/11592)*K7 +(43/616)*K8

    DB.x    = x_2