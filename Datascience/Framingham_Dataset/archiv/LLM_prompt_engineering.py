import pandas as pd
import numpy as np
data = pd.read_csv('01_framingham_clean.csv')

data = data.iloc[np.random.randint(data.shape[0])]
print(data.head(20))

api_key =  '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'


from haystack import Pipeline
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.generators import HuggingFaceAPIGenerator
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack import Document
from haystack.utils import Secret


docstore = InMemoryDocumentStore()
docstore.write_documents([Document(content="Gender,  = 1 patient have a higher Risk of getting CHD"), 
                          Document(content="The higher the Age the bigger the Risk, is like it is"),
                          Document(content="Smoking increases the Risk, stop smoking, Quit Smoking: Seek support if needed."),
                          Document(content="The BMI increases the Risk, think about loosing weight, if the BMI is to high, Achieve and Maintain a Healthy Weight: Excess weight increases the risk of CHD, diabetes, and high blood pressure. Focus on losing weight through a combination of a healthy diet and regular exercise. Diet & Exercise: A healthy diet, regular physical activity, and weight management can significantly reduce CHD risk. Aim for a BMI of less than 25."),
                          ])

query =  "Generate a personal written text based report that provides recommendations on lifestyle changes or actions to improve health and reduce the risk of CHD."

template = """
Personal Report in text form that gives **personalized recommendations** to help you lower your risk of Coronary Heart Disease (CHD), based on your provided health information.


Context: 
{% for document in documents %}
    {{ document.content }}
{% endfor %}

Patient Form Details:
Gender: {{ Gender }}
Age: {{ Age }}
Currently Smoking: {{ CurrentlySmoking }}
Cigarets per day if smoker: {{ CigarettesPerDayIfSmoker }}
Blod pressure Medication: {{ BloodPressureMedication }}
Prevalent Stroke: {{ PrevalentStroke }}
Prevalent Hypertensis: {{ PrevalentHypertension }}
Diabetes: {{ Diabetes }}
Systolic Blood Pressure: {{ SystolicBloodPressure }}
Diastolic Blood Pressure: {{ DiastolicBloodPressure }}
Body Mass Index: {{ BodyMassIndex }}
Heart Rate: {{ HeartRate }}
Glocose Level: {{ GlucoseLevel }}

Query: {{ query }}?

**Instruction**: Based on the provided information, write a personalized health report. Focus on giving actionable recommendations, such as lifestyle changes or medical advice that can help reduce their risk of CHD. 
Use a **friendly, direct tone** such as "you could try to..." or "it would be helpful for you to...". 
**Do not calculate any risk scores** or provide numerical risk assessments. The goal is to offer useful suggestions that the patient can follow to improve their health.
**Do not use Dear [patient], and no greeting**
"""

generator = HuggingFaceAPIGenerator(api_type="serverless_inference_api",
                                    api_params={"model": "HuggingFaceH4/zephyr-7b-beta"},
                                    token=Secret.from_token(api_key))

# mistralai/Mistral-Nemo-Instruct-2407
# HuggingFaceH4/zephyr-7b-beta


pipe = Pipeline()

pipe.add_component("retriever", InMemoryBM25Retriever(document_store=docstore))
pipe.add_component("prompt_builder", PromptBuilder(template=template))
pipe.add_component("llm", generator)
pipe.connect("retriever", "prompt_builder.documents")
pipe.connect("prompt_builder", "llm")



res=pipe.run({
    "prompt_builder": {
                "Gender": data.male,
                "Age": data.age,
                # "EducationalLevel": data.education,
                "CurrentlySmoking": data.currentSmoker,
                "CigarettesPerDayIfSmoker": data.cigsPerDay,
                "BloodPressureMedication": data.BPMeds,
                "PrevalentStroke": data.prevalentStroke,
                "PrevalentHypertension": data.prevalentHyp,
                "Diabetes": data.diabetes,
                "SystolicBloodPressure": data.sysBP,
                "DiastolicBloodPressure": data.diaBP,
                "BodyMassIndex": data.BMI,
                "HeartRate": data.heartRate,
                "GlucoseLevel": data.glucose
    },
    "retriever": {
        "query": query
    }
})

print(res['llm']['replies'][0].strip())
