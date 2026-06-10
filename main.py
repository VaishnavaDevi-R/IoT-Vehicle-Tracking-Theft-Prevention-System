from simulation.geofence import check_geofence

lat = 11.0170
lon = 76.9560

inside, distance = check_geofence(lat, lon)

print("Distance:", round(distance, 2), "meters")

if inside:
    print("✅ Vehicle Inside Safe Zone")
else:
    print("🚨 Vehicle Outside Safe Zone")