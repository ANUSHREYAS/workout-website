import streamlit as st

# ----------------------------
# Function to check home build feasibility
# ----------------------------
def check_home_conditions(features):
    """
    features: dict with keys for each feature
    returns True if all conditions satisfied, else False with reason
    """
    reasons = []

    if not (100000 <= features["budget"] <= 500000):
        reasons.append("Budget not sufficient")
    if features["land_area"] < 1000:
        reasons.append("Land size too small")
    if not features["soil_quality"]:
        reasons.append("Soil unsuitable")
    if not features["legal_permits"]:
        reasons.append("Permits missing")
    if features["zoning"] != "residential":
        reasons.append("Zoning laws not satisfied")
    if not all(features["utilities"].values()):
        reasons.append("Utilities missing")
    if features["environmental_restrictions"]:
        reasons.append("Environmental restrictions apply")
    if not all(material in features["materials_available"] for material in ["cement", "bricks", "steel", "sand", "timber"]):
        reasons.append("Materials unavailable")
    if features["labor_available"] < features["required_labor"]:
        reasons.append("Insufficient labor")
    if features["timeline"] > 12:
        reasons.append("Timeline too long")

    if reasons:
        return False, reasons
    return True, ["All conditions satisfied"]

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="Smart Home Decision Maker", layout="centered")
st.title("🏡 Smart Home Decision Checker")

with st.form("home_form"):
    st.header("Enter Home Build Parameters")

    budget = st.number_input("Budget ($)", min_value=0, step=1000, value=150000)
    land_area = st.number_input("Land Area (sq ft)", min_value=0, step=10, value=1200)
    soil_quality = st.checkbox("Soil Suitable?")
    legal_permits = st.checkbox("Legal Permits Obtained?")
    zoning = st.selectbox("Zoning Type", ["residential", "commercial", "industrial"])
    
    st.subheader("Utilities")
    electricity = st.checkbox("Electricity Available?")
    water = st.checkbox("Water Available?")
    sewage = st.checkbox("Sewage Available?")
    internet = st.checkbox("Internet Available?")
    utilities = {"electricity": electricity, "water": water, "sewage": sewage, "internet": internet}

    environmental_restrictions = st.checkbox("Any Environmental Restrictions?")

    st.subheader("Construction Materials")
    materials_available = st.multiselect(
        "Available Materials",
        ["cement", "bricks", "steel", "sand", "timber", "other"]
    )

    labor_available = st.number_input("Number of Skilled Workers Available", min_value=0, step=1, value=10)
    required_labor = st.number_input("Required Skilled Workers", min_value=0, step=1, value=8)

    timeline = st.number_input("Expected Timeline (months)", min_value=1, max_value=24, value=10)

    submitted = st.form_submit_button("Check Feasibility")

if submitted:
    features = {
        "budget": budget,
        "land_area": land_area,
        "soil_quality": soil_quality,
        "legal_permits": legal_permits,
        "zoning": zoning,
        "utilities": utilities,
        "environmental_restrictions": environmental_restrictions,
        "materials_available": materials_available,
        "labor_available": labor_available,
        "required_labor": required_labor,
        "timeline": timeline
    }

    possible, reasons = check_home_conditions(features)
    if possible:
        st.success("✅ All conditions satisfied! Home can be built.")
    else:
        st.error("❌ Not feasible due to:")
        for reason in reasons:
            st.write(f"- {reason}")
