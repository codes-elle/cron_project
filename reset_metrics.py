import json

#Load the current stats (from stats.json)
with open("stats.json", "r") as f:
    stats = json.load(f)

#Reset only the numerical fields
for job, data in stats.items():
    if isinstance(data, dict):
        if "runs" in data:
            data["runs"] = 0
        if "total_duration" in data:
            data["total_duration"] = 0
        if "errors" in data:
            data["errors"] = 0

#Save the updated stats
with open("stats.json", "w") as f:
    json.dump(stats, f, indent=4)

print("Stats reset: run counts, durations, and errors set to 0.")