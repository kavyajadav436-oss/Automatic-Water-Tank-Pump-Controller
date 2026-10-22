import os
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

METRICS_FILE = "runs/water_tank_v2/reports/metrics.csv"
OUTPUT_DIR = "graphs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(METRICS_FILE, newline="") as f:
    rows = list(csv.DictReader(f))

if not rows:
    raise SystemExit("ERROR: No OpenLane metrics found.")

data = rows[-1]

def get_metric(key):
    try:
        return float(data[key])
    except (ValueError, TypeError, KeyError):
        return None

def save_graph(filename):
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=200)
    plt.close()
    print("Saved:", filename)

# GRAPH 1: Physical design flow
stages = [
    "Floorplan",
    "Placement",
    "Clock Tree\nSynthesis",
    "Routing",
    "Final Layout"
]

fig, ax = plt.subplots(figsize=(12, 3))
ax.axis("off")

for i, stage in enumerate(stages):
    x = i * 2.2
    ax.text(
        x, 0, stage,
        ha="center", va="center", fontsize=10,
        bbox=dict(boxstyle="round,pad=0.7", fc="white", ec="black")
    )
    if i < len(stages) - 1:
        ax.annotate(
            "", xy=(x + 1.55, 0), xytext=(x + 0.7, 0),
            arrowprops=dict(arrowstyle="->", lw=1.5)
        )

ax.set_xlim(-1, 10)
ax.set_ylim(-1, 1)
ax.set_title("Water Tank Controller - Physical Design Flow")
save_graph("physical_design_flow.png")

# GRAPH 2: Area analysis
labels = []
values = []

for key, label in [
    ("CoreArea_um^2", "Core area (um²)"),
    ("DIEAREA_mm^2", "Die area (mm²)")
]:
    value = get_metric(key)
    if value is not None:
        labels.append(label)
        values.append(value)

if values:
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(labels, values)
    ax.set_title("Water Tank Controller - Area Analysis")
    ax.set_ylabel("Area (units shown per category)")
    ax.bar_label(bars, fmt="%.4g")
    save_graph("area_analysis.png")

# GRAPH 3: Timing metrics
labels = []
values = []

for key, label in [
    ("critical_path_ns", "Critical path (ns)"),
    ("suggested_clock_period", "Suggested period (ns)"),
    ("CLOCK_PERIOD", "Configured period (ns)")
]:
    value = get_metric(key)
    if value is not None:
        labels.append(label)
        values.append(value)

if values:
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(labels, values)
    ax.set_title("Water Tank Controller - Timing Metrics")
    ax.set_ylabel("Time (ns)")
    ax.bar_label(bars, fmt="%.3g")
    ax.tick_params(axis="x", rotation=10)
    save_graph("timing_analysis.png")

# GRAPH 4: Aggregate timing slack
labels = []
values = []

for key, label in [
    ("wns", "WNS"),
    ("tns", "TNS")
]:
    value = get_metric(key)
    if value is not None:
        labels.append(label)
        values.append(value)

if values:
    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(labels, values)
    ax.axhline(0, linewidth=1)
    ax.set_title("Water Tank Controller - Aggregate Timing Slack")
    ax.set_ylabel("Slack metric (ns, as reported)")
    ax.bar_label(bars, fmt="%.4g")
    save_graph("setup_hold_slack.png")

# GRAPH 5: Typical power
labels = []
values = []

for key, label in [
    ("power_typical_internal_uW", "Internal"),
    ("power_typical_switching_uW", "Switching"),
    ("power_typical_leakage_uW", "Leakage")
]:
    value = get_metric(key)
    if value is not None:
        labels.append(label)
        values.append(value)

if values:
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(labels, values)
    ax.set_title("Water Tank Controller - Typical Power")
    ax.set_ylabel("Power (uW)")
    ax.bar_label(bars, fmt="%.4g")
    save_graph("power_analysis.png")

print("\nFinished generating available graphs.")
print("Output directory:", OUTPUT_DIR)
