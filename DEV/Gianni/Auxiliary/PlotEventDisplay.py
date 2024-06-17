import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os 

# Initial Settings
FileName = 'AnalysisResults_FindableTreeGammas' # File name, should be a .csv or parquet file!!
PROJECT_PATH = '/storage1/liveraro/ML_Strangeness/' # Project main directory path
#FILE_PATH = PROJECT_PATH+'Dataset/Processed/{}.parquet'.format(FileName)
FILE_PATH = PROJECT_PATH+'DEV/Gianni/Studies/FindableExercise/{}.parquet'.format(FileName)
StudyName = "FindableExercise"

# Creating directory to save analysis results
EXPLORATORYANALYSIS_PATH = PROJECT_PATH+'DEV/Gianni/Studies/{}/ExploratoryAnalysis/'.format(StudyName)
os.makedirs(EXPLORATORYANALYSIS_PATH, exist_ok=True)

#--------------------------------------------------------------
# Set random seed for reproducibility
np.random.seed(42)

# Constants
c = 3e8  # Speed of light in vacuum (m/s)
e = 1.602176634e-19  # Elementary charge (Coulombs)
# Magnetic field (assumed uniform in the z-direction)
B = 0.5  # Tesla

# Known particle masses in GeV/c^2 (example set: electron, muon, pion)
known_masses = [0.000511, 0.105, 0.140]

#---------------------------------------------------- FUNCTIONS ---------------------------------------------------
def calculate_radius_of_curvature(p_T, q, B):
    """
    Calculate the radius of curvature for a charged particle in a magnetic field.
    p_T should be in GeV/c, q in elementary charge units (e), B in Tesla.
    Returns radius in meters.
    """
    q_coulombs = q * e  # Convert charge to Coulombs
    p_T_kg_m_s = p_T * 1.602176634e-10 / c  # Convert p_T from GeV/c to kg·m/s
    return p_T_kg_m_s / (q_coulombs * B)

def helical_path_xy(x0, y0, p_x, p_y, q, B, theta_constant, num_points=200):
    """
    Calculate the helical path of a charged particle in a magnetic field in the xy plane.
    """
    p_T = np.sqrt(p_x**2 + p_y**2)
    R = calculate_radius_of_curvature(p_T, q, B)
    
    # Center of the circular trajectory
    x_circ = x0 + (p_y * (1.602176634e-10 / c) / (q * e * B))  # p_y in GeV/c
    y_circ = y0 - (p_x * (1.602176634e-10 / c) / (q * e * B))  # p_x in GeV/c
    
    # Correct calculation of the initial angle
    theta_start = np.arctan2(y0 - y_circ, x0 - x_circ)
    
    theta = np.linspace(theta_start, theta_start - theta_constant * np.pi * np.sign(q), num_points)
    x = x_circ + abs(R) * np.cos(theta)
    y = y_circ + abs(R) * np.sin(theta)

    return x, y

def generate_random_particle():
    """
    Generate a random particle with reasonable values for momentum, mass, and charge.
    """
    mass = np.random.choice(known_masses)
    charge = np.random.choice([-1, 1])

    x0 = np.random.uniform(-0.85, 0.85)
    y0 = np.random.uniform(-0.85, 0.85)
    p_x = charge*np.random.uniform(0, 1.0)
    p_y = charge*np.random.uniform(0, 1.0)
    p_z = charge*np.random.uniform(0, 1.2)
    
    return {
        "mass": mass,
        "charge": charge,
        "x0": x0,
        "y0": y0,
        "p_x": p_x,
        "p_y": p_y,
        "p_z": p_z
    }

#---------------------------------------------------- DATA ---------------------------------------------------

fUseParticleFromData = True
num_particles = 10

if fUseParticleFromData:
    # Load the dataset
    df = pd.read_parquet(FILE_PATH)
    df = df[df.fPDGCodeMother==3212]
    #df = df[df.fV0radius>20] # include selections here!

    particles = []
    for p in range(num_particles):
        df2 = df.iloc[p]
        x = df2[['fX']].values[0]*0.01
        y = df2[['fY']].values[0]*0.01

        PxPos = df2[['fPxPos']].values[0]
        PyPos = df2[['fPyPos']].values[0]
        PzPos = df2[['fPzPos']].values[0]

        PxNeg = df2[['fPxNeg']].values[0]
        PyNeg = df2[['fPyNeg']].values[0]
        PzNeg = df2[['fPzNeg']].values[0]

        Posparticle = {'mass': 0.000511, 'charge': 1, 'x0': x, 'y0': y, 'p_x': PxPos, 'p_y': PyPos, 'p_z': PzPos}
        Negparticle = {'mass': 0.000511, 'charge': -1, 'x0': x, 'y0': y, 'p_x': PxNeg, 'p_y': PyNeg, 'p_z': PzNeg}

        print("Positive: ", Posparticle)
        print("Negative: ", Negparticle)
        particles.append(Posparticle)
        particles.append(Negparticle)

else: 
    # Generate random particles
    particles = [generate_random_particle() for _ in range(num_particles)]

print(particles)

#---------------------------------------------- PLOT --------------------------------------------
plt.rcParams['axes.facecolor']='black'
plt.figure(figsize=(10, 10))

#-------------------------- DETECTORS STRUCTURE PLOTS -----------------------------------
Detectors_theta = np.linspace(0, 2 * np.pi, 100) # azimuthal angle

# Plotting ITS Layer
# Create an array of angles from 0 to 2pi
  
DetectorsRadius = [22.4, 30.1, 37.8, 194.4, 243.9, 342.3, 391.8, 610, 788, 848, 2466, 2580, 2780]
Detectors_Layers = ["ITS L. 0", "ITS L. 1", "ITS L. 2", "ITS L. 3", "ITS L. 4", "ITS L. 5", "ITS L. 6", "TPC Min Radial size of vessel (outer dimensions)", "TPC Min Radial size of vessel (gas volume)", "TPC Min Radial Position (active volume)", "TPC Max Radial Position (active volume)", "TPC Max Radial size of vessel (gas volume)", "TPC Max Radial size of vessel (outer dimensions)"]

DetectorsColors = ["#cb6682", "#cb6682", "#cb6682", "#78bf88", "#78bf88", "#6962b1", "#6962b1", 
		   "#476a71", "#476a71", "#476a71", "#476a71", "#476a71", "#4cbc70"]
# Calculate the x and y coordinates of the circle
for r in range(0, len(DetectorsRadius)):
    x_det = DetectorsRadius[r]*0.001* np.cos(Detectors_theta)
    y_det = DetectorsRadius[r]*0.001* np.sin(Detectors_theta)
    #plt.plot(x_det, y_det, color="black", label=Detectors_Layers[r], linestyle="--")
    plt.plot(x_det, y_det, color=DetectorsColors[r], label=Detectors_Layers[r], linestyle="-")


# -------------------------- TPC specific ------------------------------------
# Plotting TPC details
# Angles for dividing the region
angles = np.linspace(0, 2 * np.pi, 18 + 1)
for angle in angles:
    x_inner = 848*0.001 * np.cos(angle)
    y_inner = 848*0.001 * np.sin(angle)
    x_outer = 2466*0.001 * np.cos(angle)
    y_outer = 2466*0.001 * np.sin(angle)
    #plt.plot([x_inner, x_outer], [y_inner, y_outer], color='black')
    plt.plot([x_inner, x_outer], [y_inner, y_outer], color="#476a71")
    
# Parameters
num_sides = 18  # Number of sides of the polygon
d = (2466-848)*0.001/6  # Distance from the center to the vertices
dd = 848*0.001 

# Angles for the vertices
angles = np.linspace(0, 2 * np.pi, num_sides, endpoint=False)

for ii in range(0, 6):
	dd = dd + d
	# Coordinates of the vertices
	x_coords = dd * np.cos(angles)
	y_coords = dd * np.sin(angles)

	# Plot the polygon
	#plt.plot(np.append(x_coords, x_coords[0]), np.append(y_coords, y_coords[0]), color='blue', linestyle='-', linewidth=1)
	plt.plot(np.append(x_coords, x_coords[0]), np.append(y_coords, y_coords[0]), color="#476a71", linestyle='-', linewidth=1)


# ----------------------------------------- TRACK SPECIFIC --------------------------
for particle in particles:
    print('particle: ', particle)
    q = particle["charge"]
    x0 = particle["x0"]
    y0 = particle["y0"]
    p_x = particle["p_x"]
    p_y = particle["p_y"]
    theta_constant = 1.0 #np.random.uniform(0.0, 0.2)  # Randomize theta constant between 0.0 and 0.5

    x, y = helical_path_xy(x0, y0, p_x, p_y, q, B, theta_constant)
    
    #plt.plot(x, y, label=f"Charge {q}, mass={particle['mass']}, x0={x0:.2f}, y0={y0:.2f}, px={p_x:.2f}, py={p_y:.2f}") 
    if q>0:
       plt.plot(x, y, color="blue", linewidth=1.0)
    else: 
       plt.plot(x, y, color="red", linewidth=1.0)



# ------------------ FINAL SETTINGS -----------------------------------
#ax = plt.axes()
 # Setting the background color of the plot 
# using set_facecolor() method
#ax.set_facecolor("black")

plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.xlim(-3, +3)
plt.ylim(-3, +3)
plt.title('Particle Tracks in xy Plane')
#plt.legend()
#plt.grid(True)
#plt.savefig('EventDisplay_{}V0s_NotFound.png'.format(num_particles), dpi=300)    
#plt.show()
plt.savefig(EXPLORATORYANALYSIS_PATH+'EventDisplay2D_{}V0s.png'.format(num_particles), dpi=300)    