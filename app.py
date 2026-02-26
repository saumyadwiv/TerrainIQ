import streamlit as st
import numpy as np
from PIL import Image
import torch
import inference
import utils
import matplotlib.pyplot as plt

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="TerrainIQ - Smart Offroad Vision ",
    layout="wide",
    page_icon="🚓"
)

# ================= SESSION STATE =================
if "entered" not in st.session_state:
    st.session_state.entered = False

# ================= BACKGROUND =================
def set_background():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1500530855697-b586d89ba3ee");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }
        .block-container {
            background: rgba(0, 0, 0, 0.82);
            padding: 2rem;
            border-radius: 18px;
        }
        h1, h2, h3, h4, h5, h6, p, div {
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_background()

# ================= LANDING SCREEN =================
if not st.session_state.entered:
    st.markdown(
        "<h1 style='text-align:center;'>🚓 TerrainIQ - Smart Offroad Vision </h1>",
        unsafe_allow_html=True
    )
    st.markdown("---")
    st.markdown(
        "<h3 style='text-align:center;'>"
        "“Turning Unseen Terrain into Intelligent Decisions .”"
        "</h3>",
        unsafe_allow_html=True
    )
    st.markdown("<br><br>", unsafe_allow_html=True)

    col = st.columns(3)
    with col[1]:
        if st.button("🚀 Enter Command Center", use_container_width=True):
            st.session_state.entered = True
            st.rerun()
    st.stop()

# ================= DEVICE =================
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ================= LOAD MODEL =================
@st.cache_resource
def load_ai_model():
    model = inference.load_model()
    model.to(DEVICE)
    model.eval()
    return model

model = load_ai_model()

# ================= HEADER =================
st.markdown("<h1 style='text-align:center;'> TerrainIQ- Smart Offroad Vision </h1>", unsafe_allow_html=True)
st.markdown("---")

# ================= SIDEBAR =================
st.sidebar.title("🚨 System Monitor")
st.sidebar.success("AI Model Loaded")
st.sidebar.write(f"Device: {DEVICE}")
st.sidebar.write("Model: UNet (ResNet34)")
st.sidebar.write("Use Case: Tactical & Emergency Deployment")

# ================= FILE UPLOAD =================
uploaded_file = st.file_uploader("Upload Terrain Image", type=["jpg", "png"])

if not uploaded_file:
    st.info("⬆ Upload terrain image to begin analysis.")
    st.stop()

# ================= LOAD IMAGE =================
image = Image.open(uploaded_file).convert("RGB")
image_np = np.array(image)

col1, col2 = st.columns(2)

with col1:
    st.image(image_np, caption="Original Terrain", use_container_width=True)

# ================= INFERENCE =================
with st.spinner("Analyzing Terrain..."):

    mask = inference.predict(model, image_np, DEVICE)
    segmented_output = utils.overlay_mask(image_np, mask)
    analysis = utils.analyze_terrain(mask)

    percentages = analysis["percentages"]
    risk_score = analysis["risk_score"]
    terrain_type = analysis["terrain_type"]
    advanced = analysis["advanced"]

with col2:
    st.image(segmented_output, caption="Segmented Terrain Map", use_container_width=True)

# =====================================================
# CORE TERRAIN SUMMARY
# =====================================================
st.markdown("## 🧠 Terrain Risk Overview")

colA, colB, colC = st.columns(3)

with colA:
    st.metric("Terrain Type", terrain_type)

with colB:
    st.metric("Base Risk Score", round(risk_score,2))

with colC:
    if risk_score < 0.3:
        level = "LOW"
    elif risk_score < 0.6:
        level = "MEDIUM"
    else:
        level = "HIGH"
    st.metric("Risk Level", level)

traversability = advanced["traversability"]
stability = advanced["surface_stability"]
obstacles = advanced["obstacle_density"]
speed = advanced["recommended_speed"]

# =====================================================
# VEHICLE SUITABILITY
# =====================================================
st.markdown("## 🚗 Vehicle Suitability Analysis")

vehicle_scores = {
    "Sedan": max(0, traversability - 30),
    "SUV": traversability,
    "4x4": min(100, traversability + 10),
    "Pickup": max(0, traversability - 10),
    "Tractor": min(100, traversability + 5)
}

fig, ax = plt.subplots()
ax.bar(vehicle_scores.keys(), vehicle_scores.values())
ax.set_ylim(0, 100)
ax.set_ylabel("Suitability Score")
ax.set_title("Vehicle Compatibility")

st.pyplot(fig)

# =====================================================
# DELHI POLICE TACTICAL MODULE
# =====================================================
st.markdown("---")
st.markdown("## 🚓 Tactical Deployment Intelligence (Delhi Police Mode)")

mode = st.selectbox(
    "Select Operational Mode",
    ["Normal Patrol", "Emergency Response", "Disaster Rescue", "Tactical Operation"]
)

rain = st.slider("🌧 Simulated Rain Intensity (%)", 0, 100, 0)

weather_risk = min(1.0, risk_score + rain * 0.003)

st.write(f"Adjusted Risk (Weather Impact): {round(weather_risk,2)}")

# Emergency vehicle access
patrol = max(0, traversability - rain * 0.3)
riot = max(0, traversability - 10 - rain * 0.4)
ambulance = max(0, traversability - 5 - rain * 0.2)
rescue = max(0, traversability - 15 - rain * 0.5)

emergency_scores = {
    "PCR Patrol": patrol,
    "Riot Vehicle": riot,
    "Ambulance": ambulance,
    "Rescue Truck": rescue
}

fig2, ax2 = plt.subplots()
ax2.bar(emergency_scores.keys(), emergency_scores.values())
ax2.set_ylim(0, 100)
ax2.set_ylabel("Operational Access Score")
ax2.set_title("Emergency Vehicle Accessibility")

st.pyplot(fig2)

# =====================================================
# DRONE DEPLOYMENT
# =====================================================
st.markdown("## 🚁 Drone Surveillance Index")

drone_score = max(0, 100 - obstacles - rain * 0.5)
st.metric("Drone Deployment Score", f"{int(drone_score)}/100")

if drone_score > 70:
    st.success("Aerial surveillance highly effective.")
elif drone_score > 40:
    st.warning("Moderate drone interference possible.")
else:
    st.error("Drone visibility limited.")

# =====================================================
# INCIDENT SIMULATION
# =====================================================
if st.button("🚨 Simulate Emergency Deployment"):
    st.markdown("### 🧭 Simulation Result")

    if patrol > 60:
        st.write("• PCR vehicle can reach quickly.")
    else:
        st.write("• Patrol movement may face delays.")

    if ambulance > 60:
        st.write("• Ambulance access feasible.")
    else:
        st.write("• Medical evacuation may require alternate transport.")

    if rescue > 60:
        st.write("• Heavy rescue deployment possible.")
    else:
        st.write("• Rescue truck access limited.")

    st.info("Simulation complete based on terrain & weather factors.")

# =====================================================
# FINAL DECISION
# =====================================================
st.markdown("---")
st.markdown("## 📌 Final Operational Decision")

if weather_risk < 0.3:
    st.success("✅ Terrain operationally safe for rapid deployment.")
elif weather_risk < 0.6:
    st.warning("⚠ Controlled deployment recommended.")
else:
    st.error("🚨 High risk zone. Specialized response required.")