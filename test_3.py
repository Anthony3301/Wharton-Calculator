import statistics as st

nums = [0, 792.2808673128169, 8.3152174949646, 6.573684090062192, 10.547826186470365]

def remove_outliers_in_final_two(data):
    outliers = []
    temp = []
    threshold = 1.75
    mean = st.mean(data)
    std = st.stdev(data)

    for num in data:
        z_score = (num - mean) / std
        
        if abs(z_score) > threshold:
            outliers.append(num)
    
    for i in range(5):
        if data[i] not in outliers:
            temp.append(data[i])
    
    return temp

def final_filter(data):
    #outlier_filtered = remove_outliers_in_final_two(data)
    outlier_filtered = data.copy()

    for i in range(len(outlier_filtered)):
        if outlier_filtered[i] < 0: outlier_filtered[i] = 0
    
    outlier_filtered = remove_outliers_in_final_two(outlier_filtered)
    
    return outlier_filtered
    




