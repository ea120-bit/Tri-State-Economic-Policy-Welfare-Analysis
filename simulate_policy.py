from census import Census
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt

print("Stage 1: Fetching real economic metrics across PA, NJ, and MD...")

CENSUS_API_KEY = "5ff475ddd6469f4984ac0008b4b191c8ecd0fc95"
c = Census(CENSUS_API_KEY)

all_states_data = []
state_codes = ["42", "34", "24"]

for state in state_codes:
    raw_data = c.acs5.get(
        fields=("NAME", "B25064_001E", "B19013_001E", "B23025_003E", "B23025_005E", "B22003_002E", "B22003_001E"),
        geo={'for': 'county:*', 'in': f'state:{state}'},
        year=2022
    )
    all_states_data.extend(raw_data)

df = pd.DataFrame(all_states_data)

df = df.rename(columns={
    "B25064_001E": "median_gross_rent",
    "B19013_001E": "median_income",
    "B23025_003E": "labor_force",
    "B23025_005E": "unemployed_count",
    "B22003_002E": "snap_households",
    "B22003_001E": "total_households"
})

for col in ["median_gross_rent", "median_income", "labor_force", "unemployed_count", "snap_households", "total_households"]:
    df[col] = pd.to_numeric(df[col])

df["snap_participation_rate"] = (df["snap_households"] / df["total_households"]) * 100
df["unemployment_rate"] = (df["unemployed_count"] / df["labor_force"]) * 100

# Assign historical statutory minimum wages
df["minimum_wage"] = 7.25
df.loc[df["NAME"].str.contains("New Jersey"), "minimum_wage"] = 13.00
df.loc[df["NAME"].str.contains("Maryland"), "minimum_wage"] = 12.50

# ECONOMIC NORMALIZATION: Calculate the Wage-to-Rent Purchasing Power Ratio
df["wage_to_rent_ratio"] = df["minimum_wage"] / df["median_gross_rent"]

df.to_csv("real_interstate_welfare_data.csv", index=False)
print(f"Stage 1 Complete: Total counties mapped: {len(df)}")

# =====================================================================
# STAGE 2: MODEL TRAINING USING NORMALIZED RATIOS
# =====================================================================
print("\nStage 2: Training model on normalized cost-of-living profiles...")

# We replace raw 'minimum_wage' with our proportional 'wage_to_rent_ratio'
features = ["median_gross_rent", "median_income", "unemployment_rate", "wage_to_rent_ratio"]
X = df[features]
y = df["snap_participation_rate"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print("Machine learning model successfully trained on proportional attributes.")

y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Model Performance Evaluation:")
print(f"   -> Mean Absolute Error (MAE): {mae:.2f}% percentage points")
print(f"   -> Proportional R-squared Score (R2): {r2:.2f}")

# =====================================================================
# STAGE 3: CAUSAL SIMULATION & 30 PERCENT HOUSING RULE
# =====================================================================
print("\nStage 3: Running Lancaster Causal Simulation and 30% Affordability Rule...")

lancaster_row = df[df["NAME"].str.contains("Lancaster County")]

base_rent = lancaster_row["median_gross_rent"].values[0]
base_income = lancaster_row["median_income"].values[0]
base_unemployment = lancaster_row["unemployment_rate"].values[0]
current_snap = lancaster_row["snap_participation_rate"].values[0]

# Calculate the 30% Affordability Metric
monthly_income_needed = base_rent / 0.30
annual_income_needed = monthly_income_needed * 12
hourly_wage_needed = annual_income_needed / (40 * 52)

print(f"Lancaster Baselines - Rent: ${base_rent:.2f} | Income: ${base_income:,.2f}")
print(f"Housing Affordability Metrics (30% Rule):")
print(f"   -> Annual Income Required to satisfy 30% rule: ${annual_income_needed:,.2f}")
print(f"   -> True Target Hourly Wage needed: ${hourly_wage_needed:.2f}/hr")

# Simulate standard policy increments up to our true proportional target wage
proposed_wages = [7.25, 10.00, 12.50, 15.00, hourly_wage_needed]
simulated_snap_results = []

print("\nRunning predictive simulation loop...")
for wage in proposed_wages:
    hourly_increase = wage - 7.25
    annual_winnings = hourly_increase * 40 * 52
    simulated_income = base_income + annual_winnings
    
    # Calculate the simulated adjusted purchasing ratio for this specific step
    simulated_ratio = wage / base_rent
    
    sim_input = pd.DataFrame([{
        "median_gross_rent": base_rent,
        "median_income": simulated_income,
        "unemployment_rate": base_unemployment,
        "wage_to_rent_ratio": simulated_ratio
    }], columns=features)
    
    predicted_snap = model.predict(sim_input)[0]
    predicted_snap = max(1.5, predicted_snap)
    simulated_snap_results.append(predicted_snap)
    
    if wage == hourly_wage_needed:
        print(f"   -> TARGET WAGE (${wage:.2f}/hr) Proportional SNAP: {predicted_snap:.2f}%")
    else:
        print(f"   -> At Wage ${wage:5.2f}/hr Proportional SNAP: {predicted_snap:.2f}%")
