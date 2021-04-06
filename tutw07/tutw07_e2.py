# 1. Collect fill data #########################################################

# height of embankment and unit weight of embankment

# additional vertical stress due to fill (immediate) construction

# 2. Collect soft clay data ####################################################

# unit weight (gs), soil modulus (Es), radial permeability (kr), and vertical permeability (kv)

# assume Poisson ratio of soft soil (e.g. 0.3)

# height of clay layer

# compute coefficient of volume compressibility of natural soil (mvs)

# compute coefficient of consolidation due to vertical flow (cv)

# compute coefficient of consolidation due to radial flow (cr)

# 3. Collect stone columns data ################################################

# diameter (dc), length (Lc), spacing (s), unit weight (gc), modulus (Ec) and Poisson (nuc)

# specific gravity of column (Gs_col)

# clay particles in column (D10 and P200)

# porosity of stone column (np)

# permeability of stone column (kc)

# 4. Compute settlement without stone columns ##################################

# compute S

# 5. Compute stress reduction factor (mu) ######################################

# area replacement ratio

# modulus ratio of column to soil

# check modulus ratio (must be smaller than 20)

# stress concentration ratio

# check stress concentration ratio (must be smaller than 5)

# compute stress reduction factor (mu)

# 6. Settlement with stone columns #############################################

# compute settlement with stone columns

# 7. Compute modified coefficients of consolidation ############################

# equivalent diameter of unit cell (de)

# diameter ratio (Nd)

# modified coefficient of consolidation due to vertical flow (cvm)

# modified coefficient of consolidation due to radial flow (crm)

# 8. Compute time factors ######################################################

# convert time to seconds (t)

# vertical drainage path (note that the underlain stiff clay has low permeability) (hdr)

# time factor due to vertical flow (Tvm)

# time factor due to radial flow (Trm)

# 9. Degree of consolidation ###################################################

# degree of consolidation due to the vertical flow according to Terzaghi's (Uvm)

# auxiliary factor for radial consolidation (Fnd)

# degree of consolidation due to the radial flow according to Barron's solution (Urm)

# degree of consolidation due to combined vertical and radial flow (Uvr)

# 10. Consolidation settlement of composite foundation #########################

# compute consolidation after 1 month
