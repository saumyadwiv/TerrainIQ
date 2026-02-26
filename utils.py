import numpy as np

# ================= CLASS COLORS =================
CLASS_COLORS = {
    0: [34, 139, 34],
    1: [144, 238, 144],
    2: [255, 255, 0],
    3: [139, 69, 19],
    4: [50, 50, 50],
    5: [255, 105, 180],
    6: [160, 82, 45],
    7: [128, 128, 128],
    8: [210, 180, 140],
    9: [135, 206, 235]
}

CLASS_NAMES = [
    "Trees",
    "Lush Bushes",
    "Dry Grass",
    "Dry Bushes",
    "Ground Clutter",
    "Flowers",
    "Logs",
    "Rocks",
    "Landscape",
    "Sky"
]


# ================= MASK OVERLAY =================
def overlay_mask(image, mask):
    colored_mask = np.zeros_like(image)

    for class_id, color in CLASS_COLORS.items():
        colored_mask[mask == class_id] = color

    blended = image * 0.6 + colored_mask * 0.4
    return blended.astype("uint8")


# ================= CLASS PERCENTAGES =================
def calculate_percentages(mask):
    total_pixels = mask.size
    percentages = {}

    for class_id, name in enumerate(CLASS_NAMES):
        class_pixels = np.sum(mask == class_id)
        percentages[name] = (class_pixels / total_pixels) * 100

    return percentages


# ================= RISK SCORE =================
def calculate_risk_score(percentages):

    risk_weights = {
        "Trees": 0.9,
        "Lush Bushes": 0.6,
        "Dry Grass": 0.2,
        "Dry Bushes": 0.7,
        "Ground Clutter": 0.8,
        "Flowers": 0.1,
        "Logs": 0.95,
        "Rocks": 1.0,
        "Landscape": 0.3,
        "Sky": 0.0
    }

    risk_score = 0
    for cls, pct in percentages.items():
        risk_score += pct * risk_weights[cls]

    return round(risk_score / 100, 2)


# ================= TERRAIN TYPE =================
def detect_terrain_type(percentages):

    if percentages["Rocks"] > 25:
        return "Rocky Terrain"
    elif percentages["Dry Grass"] + percentages["Dry Bushes"] > 40:
        return "Dry Field"
    elif percentages["Trees"] + percentages["Lush Bushes"] > 40:
        return "Dense Vegetation"
    elif percentages["Landscape"] > 50:
        return "Open Landscape"
    else:
        return "Mixed Terrain"


# ================= VEHICLE RECOMMENDATION =================
def recommend_vehicle(risk_score):

    if risk_score < 0.3:
        return "Safe for Normal Vehicles"
    elif risk_score < 0.6:
        return "Recommended: SUV / 4x4"
    else:
        return "High Risk! Use Off-Road Vehicle Only"


# ================= ADVANCED ENGINEERING METRICS =================
def advanced_metrics(percentages):

    obstacle_density = (
        percentages["Trees"] +
        percentages["Logs"] +
        percentages["Rocks"] +
        percentages["Ground Clutter"]
    )

    vegetation_density = (
        percentages["Trees"] +
        percentages["Lush Bushes"] +
        percentages["Dry Bushes"]
    )

    surface_stability = (
        percentages["Landscape"] +
        percentages["Dry Grass"]
    ) - (
        percentages["Rocks"] +
        percentages["Logs"]
    )

    surface_stability = max(0, min(100, surface_stability))

    traversability = 100 - (0.6 * obstacle_density + 0.4 * vegetation_density)
    traversability = max(0, min(100, traversability))

    if obstacle_density > 40:
        nav_complexity = "High"
    elif obstacle_density > 20:
        nav_complexity = "Medium"
    else:
        nav_complexity = "Low"

    if traversability > 70:
        speed = "40–60 km/h"
    elif traversability > 40:
        speed = "20–40 km/h"
    else:
        speed = "Below 20 km/h"

    if percentages["Sky"] > 30:
        drone = "Good for Drone Surveillance"
    else:
        drone = "Limited Drone Visibility"

    return {
        "obstacle_density": round(obstacle_density, 2),
        "vegetation_density": round(vegetation_density, 2),
        "surface_stability": round(surface_stability, 2),
        "traversability": round(traversability, 2),
        "navigation_complexity": nav_complexity,
        "recommended_speed": speed,
        "drone_suitability": drone
    }


# ================= MASTER ANALYSIS =================
def analyze_terrain(mask):

    percentages = calculate_percentages(mask)
    risk_score = calculate_risk_score(percentages)
    terrain_type = detect_terrain_type(percentages)
    vehicle = recommend_vehicle(risk_score)
    advanced = advanced_metrics(percentages)

    return {
        "percentages": percentages,
        "risk_score": risk_score,
        "terrain_type": terrain_type,
        "vehicle_recommendation": vehicle,
        "advanced": advanced
    }