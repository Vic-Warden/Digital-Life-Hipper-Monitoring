import statistics

def calculate_median(steps_list):
    
    if not steps_list:
        return 0
    
    return statistics.median(steps_list)