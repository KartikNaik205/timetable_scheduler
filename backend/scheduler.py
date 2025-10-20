import random

#hardcoded subjects with their respective passing marks
subjects = {
    "MCI": 65,
    "DSP": 70,
    "MCG": 60,
    "OS": 75,
    "SE": 80,
    "ETHICS AND ENTERPRENUERSHIP": 80,
    "MINOR DEGREE": 85
}

#12-hour human readable time slots
time_slots = [
    "9:00-10:00 AM",
    "10:00-11:00 AM",
    "11:00-11:15 AM Break",
    "11:15-12:15 PM",
    "12:15-1:15 PM",
    "1:15-2:00 PM Lunch",
    "2:00-3:00 PM",
    "3:00-4:00 PM",
    "4:00-5:00 PM"
]

weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# which lab is fixed on which day
fixed_labs_by_day = {
    "Tuesday": "MCI Lab",
    "Thursday": "WT Lab"
}

def generate_daily_schedule(subject_order, day):
    """
    subject_order: list of lecture subject names (already sorted/shuffled),
                   does NOT include 'MINOR DEGREE' (handled separately)
    day: weekday string
    returns: list of length len(time_slots) with assigned strings
    """
    schedule = []
    subjects_copy = subject_order[:]
    idx = 0
    while idx < len(time_slots):
        slot = time_slots[idx]

        #Breaks and lunch are fixed
        if "Break" in slot or "Lunch" in slot:
            schedule.append(slot)
            idx += 1
            continue

        #Last slot is always MINOR DEGREE 
        if slot == "4:00-5:00 PM":
            schedule.append("MINOR DEGREE")
            idx += 1
            continue

        #Afternoon lab region: try to place fixed 2-hour lab if this day has one 
        if slot in ("2:00-3:00 PM", "3:00-4:00 PM"):
            # if we are at the start of the 2-hour block (2:00 slot) and day ahs fixed lab
            if idx == 6 and day in fixed_labs_by_day:
                lab_name = fixed_labs_by_day[day]
                schedule.append(lab_name)
                schedule.append(lab_name)
                idx += 2
                continue

            # Friday special: Minor degree lab occupies Friday 2-4 PM
            if day == "Friday" and idx == 6:
                schedule.append("MINOR DEGREE LAB")
                schedule.append("MINOR DEGREE LAB")
                idx += 2
                continue
            # otherwise, if no fixed lab here, fill with lecture(s)
            #if we are at 3:00 alot but a lab was already placed at 2:00, we should never reach here
            # so safe to pop a lecture for each hour
            if subjects_copy:
                schedule.append(subjects_copy.pop(0))
            else:
                schedule.append("Free Slot")
            idx += 1
            continue

        #all other lecture slots (morning / late morning / midday)
        if subjects_copy:
            schedule.append(subjects_copy.pop(0))
        else:
            schedule.append("Free Slot")
        idx += 1


    return schedule

def generate_weekly_timetable():
    """
    Returns dict: {day_name: [slot0_assignment, slot1_assignment, ...]}
    """

    # Sort subjects by ascending average marks (lower marks first)
    # Exculde MINOR DEGREE from lecture shuffling because it's fixed at last slot
    sorted_subjects = sorted(((k, v) for k, v in subjects.items() if k != "MINOR DEGREE"), 
                             key=lambda x: x[1])
    base_subject_list = [name for name, avg in sorted_subjects]

    weekly_timetable = {}
    previous_day_order = None

    for day in weekdays:
        # create a shuffled order that is not identical to previous day's order
        # but keep ordering biased by marks (we shuffler the sorted list - still biased)
        attempt = base_subject_list[:]
        random.shuffle(attempt)
        # prevent exact equality with previous day (loop until different)
        while attempt == previous_day_order:
            random.shuffle(attempt)
        previous_day_order = attempt[:]

        # generate day's schedule, passing the day so fixed labs are placed correctly
        daily = generate_daily_schedule(attempt, day)
        weekly_timetable[day] = daily

    # ensure Friday 2-4 PM is MINOR DEGREE LAB (override if earlier logic)
    friday = weekly_timetable["Friday"]
    friday[6] = "MINOR DEGREE LAB"
    friday[7] = "MINOR DEGREE LAB"
    weekly_timetable["Friday"] = friday

    return weekly_timetable

"""""
#---Test / CLI printing---
if __name__ == "__main__":
    tt = generate_weekly_timetable()
    for day, slots in tt.items():
        print(f"\n{day}:")
        for timestr, subject in zip(time_slots, slots):
            print(f" {timestr} -> {subject}")  """""  