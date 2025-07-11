def time_str_to_minutes(time_str):
    hour, minute = map(int, time_str.split(":"))
    return hour * 60 + minute

def is_overlap(start1_str, end1_str, start2_str, end2_str):
    start1 = time_str_to_minutes(start1_str)
    end1 = time_str_to_minutes(end1_str)
    start2 = time_str_to_minutes(start2_str)
    end2 = time_str_to_minutes(end2_str)
    return max(start1, start2) < min(end1, end2)