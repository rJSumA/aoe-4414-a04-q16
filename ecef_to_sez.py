# ecef_to_sez.py
# Access Python through CMD: cd Desktop\Phyton
# Clear Sreen on CMD: cls
#
# Usage: ecef_to_sez.py o_x_km o_y_km o_z_km x_km y_km z_km
#  Example: python3 ecef_to_sez.py 822.933 -4787.187 4120.262 1131.698 -4479.324 4430.228
#  Output: -398.7785383067472
#           356.45918107494236
#           10.339379251970144

# Parameters:
#  o_x_km, o_y_km, o_z_km: ECEF origin of SEZ frame
#  x_km, y_km, z_km: ECEF position
#  ...
# Output:
#  SEZ position
#
# Written by Ryo Jumadiao
# Other contributors: None
#
# Optional license statement, e.g., See the LICENSE file for the license.

# import Python modules
# e.g., import math # math module
import math # math module
import sys # argv

# "constants"
R_E_KM = 6378.137
E_E = 0.081819221456

# helper functions
def calc_denom (E_E,lat_rad):
    return math.sqrt(1.0-E_E**2.0 * math.sin(lat_rad)**2.0)

# initialize script arguments

# ECEF origin of SEZ frame
o_x_km = 0.0
o_y_km = 0.0 
o_z_km = 0.0 

# ECEF position
x_km = 0.0
y_km = 0.0
z_km = 0.0

# parse script arguments
# How many arguments are passed to python -- 6 arguments pass 7
# Converts string to float

if len(sys.argv)==7:
    o_x_km = float(sys.argv[1])
    o_y_km = float(sys.argv[2])
    o_z_km = float(sys.argv[3])
    x_km = float(sys.argv[4])
    y_km = float(sys.argv[5])
    z_km = float(sys.argv[6])
    
else:
   print(\
    'Usage: '\
    'python3 ecef_to_sez.py o_x_km o_y_km o_z_km x_km y_km z_km'\
   )
   exit()

#======================================
x_vec_km = x_km - o_x_km
y_vec_km = y_km - o_y_km
z_vec_km = z_km - o_z_km

#-----------------------------------ECEF_TO_LLH script------
# calculate longitude
lon_rad = math.atan2(o_y_km,o_x_km)
lon_deg = lon_rad*180.0/math.pi

# initialize lat_rad, r_lon_km, r_z_km
lat_rad = math.asin(z_vec_km/math.sqrt(o_x_km**2+o_y_km**2+o_z_km**2))
r_lon_km = math.sqrt(o_x_km**2+o_y_km**2)
prev_lat_rad = float('nan')

# iteratively find latitude
c_E = float('nan')
count = 0
while (math.isnan(prev_lat_rad) or abs(lat_rad-prev_lat_rad)>10e-7) and count<5:
  denom = calc_denom(E_E,lat_rad)
  c_E = R_E_KM/denom
  prev_lat_rad = lat_rad
  lat_rad = math.atan((o_z_km+c_E*(E_E**2)*math.sin(lat_rad))/r_lon_km)
  count = count+1
  
# calculate hae
hae_km = r_lon_km/math.cos(lat_rad)-c_E
#-------------------------------------------------------------

#Phi = Latitude, Theta = Longtitude
Ry_inv_sez_1 = x_vec_km*math.cos(lon_rad) + y_vec_km*math.sin(lon_rad)
Ry_inv_sez_2 = x_vec_km*-math.sin(lon_rad) + y_vec_km*math.cos(lon_rad)
Ry_inv_sez_3 = z_vec_km

Rz_inv_sez_1 = Ry_inv_sez_1*math.sin(lat_rad) - Ry_inv_sez_3*math.cos(lat_rad)
Rz_inv_sez_2 = Ry_inv_sez_2
Rz_inv_sez_3 = Ry_inv_sez_1*math.cos(lat_rad) + Ry_inv_sez_3*math.sin(lat_rad)
s_km = Rz_inv_sez_1
e_km = Rz_inv_sez_2
z_km = Rz_inv_sez_3

print(s_km)
print(e_km)
print(z_km)

#print('Longtitude [deg]: '+str(lon_deg))
#print('Latitude [deg]: '+str(lat_rad*180.0/math.pi))
#print('Height [km]: '+str(hae_km))