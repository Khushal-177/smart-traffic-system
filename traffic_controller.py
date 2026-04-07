import time
import random
import pandas as pd
import os

# ---------------- Lanes Setup ----------------
lanes = ["Lane 1", "Lane 2", "Lane 3", "Lane 4"]
wait_counter = {lane: 0 for lane in lanes}

# CSV file for simulator
file_name = "traffic_data_fast_5000.csv"

# ---------------- FUNCTION TO SAVE DATA ----------------
def save_data(data_row):
    df = pd.DataFrame([data_row])
    if os.path.isfile(file_name):
        df.to_csv(file_name, mode='a', index=False, header=False)
    else:
        df.to_csv(file_name, mode='a', index=False)

# ---------------- MAIN TRAFFIC SYSTEM ----------------
def start_traffic():
    print("Smart Traffic Simulator Started...\n")

    while True:
        # Random traffic densities
        traffic = {lane: random.randint(10, 100) for lane in lanes}
        next_junction = {lane: random.randint(10, 100) for lane in lanes}

        # Emergency check
        emergencies = []
        for lane in lanes:
            if random.random() < 0.15:  # 15% chance for emergency
                emergencies.append((lane, random.choice(["Ambulance", "Fire Truck", "Police"])))

        # ---------------- EMERGENCY HANDLING ----------------
        if emergencies:
            priority = {"Ambulance": 3, "Fire Truck": 2, "Police": 1}
            emergencies.sort(key=lambda x: priority[x[1]], reverse=True)

            for green_lane, emergency_type in emergencies:
                decision = "Emergency_" + emergency_type
                green_time = 10

                print("\nEmergency vehicle detected:", emergency_type, "in", green_lane)
                print(green_lane, "is GREEN for emergency", green_time, "seconds")

                wait_counter[green_lane] = 0
                for lane in lanes:
                    if lane != green_lane:
                        wait_counter[lane] += 1

                # Save row
                row = {
                    "L1_Density": traffic["Lane 1"],
                    "L2_Density": traffic["Lane 2"],
                    "L3_Density": traffic["Lane 3"],
                    "L4_Density": traffic["Lane 4"],

                    "L1_Next": next_junction["Lane 1"],
                    "L2_Next": next_junction["Lane 2"],
                    "L3_Next": next_junction["Lane 3"],
                    "L4_Next": next_junction["Lane 4"],

                    "L1_Wait": wait_counter["Lane 1"],
                    "L2_Wait": wait_counter["Lane 2"],
                    "L3_Wait": wait_counter["Lane 3"],
                    "L4_Wait": wait_counter["Lane 4"],

                    "Emergency_Type": emergency_type,
                    "Green_Lane": green_lane,
                    "Reason": decision,
                    "Green_Time": green_time
                }
                save_data(row)

                time.sleep(green_time)
                print("Data saved. Green lane:", green_lane, "| Reason:", decision)
                print("----------------------------------")

        # ---------------- NORMAL TRAFFIC ----------------
        else:
            decision = None
            starving_lane = None
            for lane in lanes:
                if wait_counter[lane] >= 3:
                    starving_lane = lane
                    break

            if starving_lane:
                green_lane = starving_lane
                decision = "Starvation"
                print("\nStarvation control activated for", green_lane)
            else:
                green_lane = max(traffic, key=traffic.get)
                decision = "Density"

            # Gridlock check
            if next_junction[green_lane] > 80:
                decision = "Gridlock_Avoidance"
                print("\nGridlock detected on", green_lane)
                sorted_lanes = sorted(traffic, key=traffic.get, reverse=True)
                for lane in sorted_lanes:
                    if next_junction[lane] <= 80:
                        green_lane = lane
                        break

            # Green time based on density
            density = traffic[green_lane]
            if density > 85:
                green_time = 10
            elif density > 70:
                green_time = 6
            else:
                green_time = 3

            print("\n", green_lane, "is GREEN for", green_time, "seconds")

            # Update wait counters
            for lane in lanes:
                if lane == green_lane:
                    wait_counter[lane] = 0
                else:
                    wait_counter[lane] += 1

            # Save row
            row = {
                "L1_Density": traffic["Lane 1"],
                "L2_Density": traffic["Lane 2"],
                "L3_Density": traffic["Lane 3"],
                "L4_Density": traffic["Lane 4"],

                "L1_Next": next_junction["Lane 1"],
                "L2_Next": next_junction["Lane 2"],
                "L3_Next": next_junction["Lane 3"],
                "L4_Next": next_junction["Lane 4"],

                "L1_Wait": wait_counter["Lane 1"],
                "L2_Wait": wait_counter["Lane 2"],
                "L3_Wait": wait_counter["Lane 3"],
                "L4_Wait": wait_counter["Lane 4"],

                "Emergency_Type": "None",
                "Green_Lane": green_lane,
                "Reason": decision,
                "Green_Time": green_time
            }
            save_data(row)
            time.sleep(green_time)
            print("Data saved. Green lane:", green_lane, "| Reason:", decision)
            print("----------------------------------")

# ---------------- RUN SIMULATOR ----------------
if __name__ == "__main__":
    try:
        start_traffic()
    except KeyboardInterrupt:
        print("\nTraffic system stopped")

