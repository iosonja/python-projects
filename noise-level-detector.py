"""
Creator: Sonja Ek
Created: 15.2.2020
A short python script to determine whether a noise at a measured level of dB is dangerous 
for the human ear. If the detected value is over 80 dB two times in a row or 10% of 
overall measurements, the program will give a warning.
"""

def noise_level_detector():

    # After this dB value the noise gets dangerous for the human ear:
    BORDERLINE = 80
    
    # Setting the baselines for counters:
    excess_count = 0
    previous_result = 0
    
    # Let's assume the noise level is fine for now: 
    too_high = False
    
    # Let's start taking measurements in!
    meas = input("Enter the number of measurements: ")
    measures = int(meas)
    
    # We don't want to play with non-natural results - if an input value is 
    # less than zero, the measurement is wrong, so let's reject those:
    if measures <= 0:
        print("The number of measurements must be a positive number.")
    else:
        for i in range(measures):
            result = int(input("Enter the measurement result "+ str(i + 1) + ": "))

            if result > BORDERLINE:
                excess_count = excess_count + 1
                
                # The following is a case of "two over-the-line results in a row" and
                # therefore the noise level is too high and ear protection is needed:
                if previous_result > BORDERLINE:
                    print("High noise level. Ear protection needed!")
                    too_high = True
                    break

                # Over 10% of the measurements given so far have exceeded the acceptable 
                # noise level, which also means ear protection is needed:
                if excess_count > (0.1 * measures):
                    print("High noise level. Ear protection needed!")
                    too_high = True
                    break
            # This is so that we can continue comparing subsequent values with each other 
            # looking for a case of "two over-the-line results in a row":
            previous_result = result
        if not too_high:
            print("Noise level is acceptable.")


noise_level_detector()