class HealthReportGenerator:
    def __init__(self):
        # Define normal ranges and risk thresholds
        self.ranges = {
            'age': {'normal': (18, 39), 'warning': (40, 59), 'high': (60, 100)},
            'cigsPerDay': {'low': (1, 10), 'moderate': (11, 20), 'high': (21, 100)},
            'totChol': {'normal': (0, 200), 'borderline': (201, 239), 'high': (240, 500)},
            'sysBP': {'normal': (90, 120), 'elevated': (121, 129), 'high': (130, 200)},
            'diaBP': {'normal': (60, 85), 'high': (86, 120)},
            'BMI': {'normal': (18.5, 24.9), 'overweight': (25, 29.9), 'obese': (30, 100)},
            'heartRate': {'normal': (60, 100)},
            'glucose': {'normal': (70, 99), 'prediabetes': (100, 125), 'diabetes': (126, 500)}
        }
        
        # Education level descriptions
        # self.education_levels = {
        #     'education_1.0': "Some High School",
        #     'education_2.0': "High School or GED",
        #     'education_3.0': "Some College/vocational school",
        #     'education_4.0': "College Graduate"
        # }

    def _get_age_advice(self, age):
        if age >= 60:
            return (f"Given your age of {age}, regular health check-ups are crucial. It's recommended to have comprehensive "
                   "cardiovascular screenings at least annually. Your age puts you in a higher risk category for heart disease, "
                   "making preventive care is especially important.")
        elif age >= 40:
            return (f"At age {age}, it's recommended to have regular health check-ups every 1-3 years, depending on your other "
                   "risk factors. This is a good time to establish baseline measurements for heart health indicators.")
        else:
            return (f"While you're in a younger age group at {age}, it's still important to maintain heart-healthy habits. "
                   "Consider this an opportunity to establish good health practices that will benefit you in the long term.")

    def _get_smoking_advice(self, is_smoker, cigs_per_day):
        if not is_smoker:
            return "You're currently a non-smoker, which is excellent for your heart health. Continue maintaining this healthy choice."
        
        intensity = "heavy" if cigs_per_day > 20 else "moderate" if cigs_per_day > 10 else "light"
        return (f"As a {intensity} smoker ({cigs_per_day} cigarettes per day), quitting smoking would significantly reduce your "
                "heart disease risk. Consider visiting www.lungenliga.ch for resources on smoking cessation. Even reducing "
                "consumption can have immediate health benefits.")

    def _get_blood_pressure_advice(self, sys_bp, dia_bp, bp_meds, prevalent_hyp):
        bp_status = ""
        if sys_bp > 130 or dia_bp >= 86:
            bp_status = "high"
        elif sys_bp > 120 and dia_bp < 80:
            bp_status = "elevated"
        else:
            bp_status = "normal"
        
        advice = f"Your blood pressure is {sys_bp}/{dia_bp} mmHg, which is {bp_status}. "
        
        if bp_meds:
            advice += ("Continue taking your prescribed blood pressure medications consistently. Regular monitoring and "
                      "medication compliance are crucial for managing your blood pressure.")
        
        if bp_status != "normal":
            advice += ("\nConsider lifestyle modifications such as:\n"
                      "- Reducing sodium intake\n"
                      "- Regular physical activity\n"
                      "- Stress management techniques\n"
                      "- Limiting alcohol consumption")
        
        return advice

    def _get_cholesterol_advice(self, tot_chol):
        if tot_chol >= 240:
            return (f"Your total cholesterol of {tot_chol} mg/dL is high. Consider working with your healthcare provider "
                   "on a plan to lower it through diet, exercise, and possibly medication.")
        elif tot_chol >= 200:
            return (f"Your total cholesterol of {tot_chol} mg/dL is borderline high. Focus on heart-healthy dietary choices "
                   "and regular exercise to help maintain healthy cholesterol levels.")
        else:
            return f"Your total cholesterol of {tot_chol} mg/dL is within the normal range. Keep up your healthy habits!"

    def _get_diabetes_advice(self, diabetes, glucose):
        if diabetes:
            return ("As you have diabetes, controlling blood sugar is crucial for your heart health. Regular monitoring, "
                   f"medication compliance, and lifestyle management are essential. Your current glucose level is {glucose} mg/dL.")
        elif glucose >= 126:
            return (f"Your fasting glucose level of {glucose} mg/dL is in the diabetic range. Please consult with your healthcare "
                   "provider for proper evaluation and management.")
        elif glucose >= 100:
            return (f"Your fasting glucose level of {glucose} mg/dL indicates pre-diabetes. Focus on diet, exercise, and weight "
                   "management to prevent progression to diabetes. It is recommended to consult a healthcare provider to check"
                   "for undiagnosed diabetes")
        else:
            return f"Your fasting glucose level of {glucose} mg/dL is normal. Maintain healthy habits to keep it in this range."

    def _get_bmi_advice(self, bmi):
        if bmi >= 30:
            return (f"Your BMI of {bmi:.1f} falls into the obese range. Consider working with healthcare providers on a "
                   "weight management plan. Even a 5-10% weight loss can significantly improve heart health.")
        elif bmi >= 25:
            return (f"Your BMI of {bmi:.1f} falls into the overweight range. Focus on achieving a healthy weight through "
                   "balanced nutrition and regular physical activity.")
        elif bmi >= 18.5:
            return f"Your BMI of {bmi:.1f} is in the healthy range. Maintain your healthy weight through balanced nutrition and regular exercise."
        else:
            return f"Your BMI of {bmi:.1f} is below the healthy range. Consider consulting with a healthcare provider about healthy weight gain strategies."

    def generate_report(self, patient_data):
        """
        Generate a personalized health report based on patient data.
        
        Parameters:
        patient_data (dict): Dictionary containing patient health parameters
        """
        
        sections = []
        
        # Personal Information
        # education_level = None
        # for edu_key in self.education_levels.keys():
        #     if patient_data.get(edu_key, 0) == 1:
        #         education_level = self.education_levels[edu_key]
        #         break
                
        # sections.append("PERSONAL HEALTH REPORT\n" + "="*20 + "\n")
        # sections.append(f"Gender: {'Male' if patient_data['male'] else 'Female'}")
        # sections.append(f"Age: {patient_data['age']}")
        # if education_level:
            # sections.append(f"Education Level: {education_level}\n")
        
        # Age-related advice
        sections.append("<b>Age-Related Recommendations:</b> ")# """ + "-"*20 """)
        sections.append(self._get_age_advice(patient_data['age']) + "\n")
        
        # Smoking status
        sections.append("<br><br><b>Smoking Status and Recommendations:</b> ")# """ + "-"*20 """)
        sections.append(self._get_smoking_advice(
            patient_data['currentSmoker'],
            patient_data['cigsPerDay']) + "\n")
        
        # Blood Pressure
        sections.append("<br><br><b>Blood Pressure Analysis:</b> ")# """ + "-"*20 """)
        sections.append(self._get_blood_pressure_advice(
            patient_data['sysBP'],
            patient_data['diaBP'],
            patient_data['BPMeds'],
            patient_data['prevalentHyp']) + "\n")
        
        # Cholesterol
        sections.append("<br><br><b> Cholesterol Status:</b> ")# """ + "-"*20 """)
        sections.append(self._get_cholesterol_advice(patient_data['totChol']) + "\n")
        
        # Diabetes and Glucose
        sections.append("<br><br> <b> Diabetes and Blood Sugar Analysis:</b> ")# """ + "-"*20 """)
        sections.append(self._get_diabetes_advice(
            patient_data['diabetes'],
            patient_data['glucose']) + "\n")
        
        # BMI
        sections.append("<br><br> <b> Weight Status and Recommendations:</b>")# """ + "-"*20 """)
        sections.append(self._get_bmi_advice(patient_data['BMI']) + "\n")
        
        # Additional Risk Factors
        sections.append("<br> <br><b> Additional Risk Factors:</b>")# """ + "-"*20 """)
        if patient_data['prevalentStroke']:
            sections.append("You have a history of stroke. This makes preventive care and risk factor management especially crucial.")
        
        if patient_data['heartRate'] > 100:
            sections.append(f"Your resting heart rate of {patient_data['heartRate']} is elevated. Consider discussing this with your healthcare provider.")
        elif patient_data['heartRate'] < 60:
            sections.append(f"Your resting heart rate of {patient_data['heartRate']} is low. If you're not a trained athlete, discuss this with your healthcare provider.")
        
        # Join all sections
        return "\n".join(sections)