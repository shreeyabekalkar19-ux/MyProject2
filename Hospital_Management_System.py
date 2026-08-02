from abc import ABC, abstractmethod
import csv
import os

class Person(ABC):

    def __init__(self, name, patient_id, age):
        self.__name = name
        self.__patient_id = patient_id
        self.__age = age

    def get_name(self):
        return self.__name

    def get_patient_id(self):
        return self.__patient_id

    def get_age(self):
        return self.__age

    def set_name(self, name):
        self.__name = name

    def set_age(self, age):
        self.__age = age

    @abstractmethod
    def display_details(self):
        pass

class Patient(Person):

    def __init__(self, name, patient_id, age, disease):
        super().__init__(name, patient_id, age)
        self.__disease = disease

    def get_disease(self):
        return self.__disease

    def set_disease(self, disease):
        self.__disease = disease

    def display_details(self):
        print("\n------------------------")
        print(f"Patient Name: {self.get_name()}")
        print(f"Patient ID   : {self.get_patient_id()}")
        print(f"Patient Age   : {self.get_age()}")
        print(f"Patient Disease    : {self.get_disease()}")
        print("\n------------------------")

class HospitalManagementSystem:

    file_name = 'patients.csv'

    def __init__(self):
        self.patients = []
        self.load_records()

    def register_patient(self):
        try:
            patient_id = input("Enter Patient ID: ")

            if self.search_patient(patient_id, show=False):
                print("Patient ID already exists")
                return

            name = input("Enter the Patient's name: ")
            age = input("Enter the Patient's age: ")
            disease = input("Enter the Patient's disease:" )
            patient = Patient(name, patient_id, age, disease)

            self.patients.append(patient)

            print("Patient registered successfully!")

        except ValueError:
            print("Age must be a number.")
            
        except Exception as e:
            print("Error registering Patient", e)

    def search_patient(self, patient_id=None, show=True):
        if patient_id is None:
            patient_id = input("Enter the Patient ID:")

        for patient in self.patients:
            if patient.get_patient_id() == patient_id:
                if show:
                    print("\nPatient found: ")
                    patient.display_details()
                return patient

        if show:
            print("\nPatient not found")

        return None

    def update_patient(self):
        patient_id = input("Enter the Patient ID to update: ")
        patient = self.search_patient(patient_id, show=False)

        if patient:
            try:
                name = input("Enter new name: ")
                age = int(input("Enter new age: "))
                disease = input("Enter new disease: ")

                patient.set_name(name)
                patient.set_age(age)
                patient.set_disease(disease)

                print("Patient Updated Successfully!")

            except:
                print("Age must be a number.")

        else:
            print("Patient not found")

    def delete_patient(self):
        patient_id = input("Enter Patient ID to Delete: ")
        patient = self.search_patient(patient_id, show=False)

        if patient:
            self.patients.remove(patient)
            print("Patient Deleted Succesfully!")
            
        else:
            print("Patient not found")
            
    def save_records(self):

        try:
            with open(self.file_name, "w", newline="") as file:
                writer = csv.writer(file)

                writer.writerow(["Patient Name", "Patient ID", "Patient Age", "Disease"])

                for patient in self.patients:
                    
                    writer.writerow([
                        patient.get_name(),
                        patient.get_patient_id(),
                        patient.get_age(),
                        patient.get_disease()
                    ])
            print("Records saved Successfully!")

            print("File saved at:")
            print(os.path.abspath(self.file_name))

        except IOError:
            print("Error saving records")

    def load_records(self):
        if not os.path.exists(self.file_name):
            return

        try:
            with open(self.file_name, "r") as file:
                reader = csv.reader(file)

                next(reader)

                for row in reader:

                    patient = Patient(
                        row[0],
                        row[1],
                        int(row[2]),
                        row[3]
                    )

                    self.patients.append(patient)
        except (IOError, ValueError):
            print("Error loading records.")

    def menu(self):
        
        while True:

            print("\n=======Hospital Management System=======")
            print("1. Register Patient")
            print("2. Search Patient")
            print("3. Update Patient")
            print("4. Delete Patient")
            print("5. Save Records")
            print("6. Exit")
            
            choice = input("Enter your choice: ")

            if choice == "1":
                self.register_patient()

            elif choice == "2":
                self.search_patient()

            elif choice == "3":
                self.update_patient()

            elif choice == "4":
                self.delete_patient()

            elif choice == "5":
                self.save_records()

            elif choice == "6":
                self.load_records()
                print("Thank you!")
                break

            else:
                print("Invalid choice.")

if __name__ == "__main__":
    system = HospitalManagementSystem()
    system.menu()
