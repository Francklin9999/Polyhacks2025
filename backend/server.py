from fastapi import FastAPI
import math

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

def calculate_planetary_parameters(D, M, T, P, W, B, θ, R, G, X):
    """
    Calculates all planetary parameters and the probability of life on a scale of 0-100.
    
    Parameters:
    - D: Distance from the Sun (AU) [0.3 - 30]
    - M: Planetary mass (Earth masses) [0.1 - 300]
    - T: Surface temperature (K) [50 - 900]
    - P: Atmospheric pressure (bars) [10^-5 - 100]
    - W: Water presence (0 or 1)
    - B: Magnetic field strength (G) [0 - 15]
    - θ: Axial tilt (°) [0 - 98]
    - R: Rotation speed (hours per full rotation) [1 - 5832]
    - G: Geological activity (0-1)
    - X: Radiation levels (Sv) [0.01 - 1000]

    Returns:
    - Dictionary with all calculated values, including probability of life.
    """
    
    # Validate input ranges
    if not (0.3 <= D <= 30):
        raise ValueError("Distance from Sun (D) must be between 0.3 and 30 AU.")
    if not (0.1 <= M <= 300):
        raise ValueError("Planetary Mass (M) must be between 0.1 and 300 Earth masses.")
    if not (50 <= T <= 900):
        raise ValueError("Surface Temperature (T) must be between 50 and 900 K.")
    if not (10**-5 <= P <= 100):
        raise ValueError("Atmospheric Pressure (P) must be between 10^-5 and 100 bars.")
    if W not in [0, 1]:
        raise ValueError("Water Presence (W) must be either 0 (No) or 1 (Yes).")
    if not (0 <= B <= 15):
        raise ValueError("Magnetic Field Strength (B) must be between 0 and 15 G.")
    if not (0 <= θ <= 98):
        raise ValueError("Axial Tilt (θ) must be between 0 and 98 degrees.")
    if not (1 <= R <= 5832):
        raise ValueError("Rotation Speed (R) must be between 1 and 5832 hours.")
    if not (0 <= G <= 1):
        raise ValueError("Geological Activity (G) must be between 0 and 1.")
    if not (0.01 <= X <= 1000):
        raise ValueError("Radiation Levels (X) must be between 0.01 and 1000 Sv.")
    
    # Reference Earth values
    T_E, P_E, W_E, B_E, G_E, X_E = 288, 1, 1, 0.5, 1, 0.01

    # Habitability factors
    f_T = min(1, max(0, math.exp(-abs(T - T_E) / T_E)))  # Temperature factor
    f_P = P / (1 + P)  # Atmospheric factor (balances thin and thick atmospheres)
    f_W = W  # Water presence (1 if water exists, 0 otherwise)
    f_B = B / (B + 1)  # Magnetic field protection
    f_G = G  # Geological activity
    f_X = math.exp(-X)  # Radiation survival factor

    # Compute constant scaling factor (C) based on Earth-like conditions
    C = 1 / (f_T * f_P * f_W * f_B * f_G * f_X)

    # Compute probability of life (scale 0-100)
    P_L = 100 * C * f_T * f_P * f_W * f_B * f_G * f_X

    # Organize results into a dictionary
    results = {
        "Distance from Sun (AU)": D,
        "Planetary Mass (Earth Masses)": M,
        "Surface Temperature (K)": T,
        "Atmospheric Pressure (bars)": P,
        "Water Presence": "Yes" if W == 1 else "No",
        "Magnetic Field Strength (G)": B,
        "Axial Tilt (°)": θ,
        "Rotation Speed (hours)": R,
        "Geological Activity": G,
        "Radiation Levels (Sv)": X,
        "Habitability Probability (0-100)": round(P_L, 2)
    }

    return results