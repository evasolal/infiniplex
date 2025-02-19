import csv
import random

# List of example outcomes
outcomes = ['Recovered', 'Improved', 'Declined', 'Stable', 'Deteriorated',
            'Discharged', 'Relapsed', 'Remission', 'Deceased', 'Complicated']


# Function to generate a CSV file with 50 rows
def generate_patient_data(filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['patient_id', 'outcome'])

        # Writing 50 rows of data
        for _ in range(1, 1000):
            patient_id = random.randint(1, 1000)
            outcome = random.choice(outcomes)
            writer.writerow([patient_id, outcome])


if __name__ == '__main__':
    generate_patient_data("patients_data3.csv")
