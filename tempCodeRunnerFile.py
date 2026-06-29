import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =====================================================
# ENTER YOUR VALIDATION DATA HERE
# =====================================================

actual = [100, 200, 300, 400, 500, 600]
predicted = [102.8, 201.0, 302.4, 399.2, 494.3, 605.4]

# =====================================================
# CREATE OUTPUT FOLDER
# =====================================================

os.makedirs("outputs/reports", exist_ok=True)
os.makedirs("outputs/graphs", exist_ok=True)

# =====================================================
# METRICS
# =====================================================

actual = np.array(actual)
predicted = np.array(predicted)

absolute_error = np.abs(actual - predicted)

accuracy = (1 - absolute_error / actual) * 100

mae = np.mean(absolute_error)

rmse = np.sqrt(np.mean((actual - predicted) ** 2))

std_dev = np.std(actual - predicted)

max_error = np.max(absolute_error)

min_error = np.min(absolute_error)

# =====================================================
# PRINT RESULTS
# =====================================================

print("\n========== Validation Report ==========\n")

print("Actual Distances :", actual.tolist())
print("Predicted Distances :", predicted.tolist())
print("Absolute Errors :", absolute_error.tolist())

print()

print(f"MAE       : {mae:.2f} mm")
print(f"RMSE      : {rmse:.2f} mm")
print(f"Accuracy  : {accuracy.mean():.2f}%")
print(f"Std Dev   : {std_dev:.2f} mm")
print(f"Max Error : {max_error:.2f} mm")
print(f"Min Error : {min_error:.2f} mm")

# =====================================================
# SAVE CSV REPORT
# =====================================================

df = pd.DataFrame({
    "Actual_Z_mm": actual,
    "Predicted_Z_mm": predicted,
    "Absolute_Error_mm": absolute_error,
    "Accuracy_%": accuracy
})

df.to_csv(
    "outputs/reports/validation_report.csv",
    index=False
)

print("\n[OK] validation_report.csv saved")

# =====================================================
# GRAPH 1
# =====================================================

plt.figure(figsize=(8,5))

plt.plot(
    actual,
    actual,
    marker="o",
    linewidth=2,
    label="Ideal"
)

plt.plot(
    actual,
    predicted,
    marker="s",
    linewidth=2,
    label="Predicted"
)

plt.xlabel("Actual Distance (mm)")
plt.ylabel("Predicted Distance (mm)")
plt.title("Actual vs Predicted Distance")

plt.grid(True)
plt.legend()

plt.savefig(
    "outputs/graphs/actual_vs_predicted.png",
    dpi=300
)

# =====================================================
# GRAPH 2
# =====================================================

plt.figure(figsize=(8,5))

plt.bar(
    actual.astype(str),
    absolute_error
)

plt.xlabel("Actual Distance (mm)")
plt.ylabel("Absolute Error (mm)")
plt.title("Absolute Error")

plt.grid(True)

plt.savefig(
    "outputs/graphs/absolute_error.png",
    dpi=300
)

# =====================================================
# GRAPH 3
# =====================================================

plt.figure(figsize=(8,5))

plt.plot(
    actual,
    accuracy,
    marker="o",
    linewidth=2
)

plt.xlabel("Actual Distance (mm)")
plt.ylabel("Accuracy (%)")
plt.title("Accuracy vs Distance")

plt.ylim(95,100)

plt.grid(True)

plt.savefig(
    "outputs/graphs/accuracy.png",
    dpi=300
)

# =====================================================
# SHOW ALL GRAPHS
# =====================================================

plt.show()

print("\n[OK] Graphs saved in outputs/graphs/")