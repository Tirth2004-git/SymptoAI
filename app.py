import os
import yaml
import numpy as np
import pandas as pd
from joblib import load
from flask import Flask, jsonify, request, render_template

app = Flask(__name__, template_folder='templates', static_folder='static')

# Configuration
try:
    with open('./config.yaml', 'r') as f:
        config = yaml.safe_load(f)
except Exception as e:
    print("Error reading config.yaml:", e)
    config = {
        'model_save_path': './saved_model/',
        'dataset': {
            'training_data_path': './dataset/training_data.csv'
        }
    }

MODEL_SAVE_PATH = config.get('model_save_path', './saved_model/')

# List of 132 symptoms in the exact training column order
SYMPTOMS_LIST = [
    'itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain',
    'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition',
    'spotting_ urination', 'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings',
    'weight_loss', 'restlessness', 'lethargy', 'patches_in_throat', 'irregular_sugar_level', 'cough',
    'high_fever', 'sunken_eyes', 'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache',
    'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain',
    'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes',
    'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise',
    'blurred_and_distorted_vision', 'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure',
    'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs', 'fast_heart_rate',
    'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus', 'neck_pain',
    'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs', 'swollen_blood_vessels',
    'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties', 'excessive_hunger',
    'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech', 'knee_pain', 'hip_joint_pain',
    'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness', 'spinning_movements',
    'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort',
    'foul_smell_of urine', 'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching',
    'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain', 'altered_sensorium',
    'red_spots_over_body', 'belly_pain', 'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes',
    'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum',
    'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion',
    'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen',
    'history_of_alcohol_consumption', 'fluid_overload.1', 'blood_in_sputum', 'prominent_veins_on_calf',
    'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling',
    'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose',
    'yellow_crust_ooze'
]

# Display friendly names
def get_friendly_name(name):
    friendly = name.replace('_', ' ').replace('  ', ' ').strip().title()
    # Special cleanups
    friendly = friendly.replace('Urination', 'Urination')
    friendly = friendly.replace('Of Urine', 'of Urine')
    friendly = friendly.replace('Of Abdomen', 'of Abdomen')
    friendly = friendly.replace('Of Alcohol Consumption', 'of Alcohol Consumption')
    friendly = friendly.replace('Of One Body Side', 'of One Body Side')
    friendly = friendly.replace('Of Smell', 'of Smell')
    friendly = friendly.replace('In Throat', 'in Throat')
    friendly = friendly.replace('On Tongue', 'on Tongue')
    friendly = friendly.replace('On Calf', 'on Calf')
    friendly = friendly.replace('Over Body', 'over Body')
    friendly = friendly.replace('Behind The Eyes', 'behind the Eyes')
    friendly = friendly.replace('During Bowel Movements', 'during Bowel Movements')
    friendly = friendly.replace('In Anal Region', 'in Anal Region')
    friendly = friendly.replace('In Anus', 'in Anus')
    friendly = friendly.replace('In Limbs', 'in Limbs')
    friendly = friendly.replace('In Nails', 'in Nails')
    friendly = friendly.replace('Around Nose', 'around Nose')
    friendly = friendly.replace('Fluid Overload.1', 'Fluid Overload (Secondary)')
    friendly = friendly.replace('Toxic Look (Typhos)', 'Toxic Look (Typhoid)')
    friendly = friendly.replace('Dischromic Patches', 'Dischromic Patches')
    return friendly

# Load models
models = {}
available_models = ['random_forest', 'decision_tree', 'mnb', 'gradient_boost']

for m_name in available_models:
    m_path = os.path.join(MODEL_SAVE_PATH, f"{m_name}.joblib")
    if os.path.exists(m_path):
        try:
            models[m_name] = load(m_path)
            print(f"Successfully loaded model: {m_name}")
        except Exception as e:
            print(f"Error loading model {m_name}: {e}")
    else:
        print(f"Model path {m_path} does not exist. Please train the models first.")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/symptoms', methods=['GET'])
def get_symptoms():
    symptoms_data = []
    for s in SYMPTOMS_LIST:
        s_clean = s.replace('.1', '') # clean internal key labels if needed
        s_friendly = get_friendly_name(s)
        s_category = "General"
        # Rough grouping for tags/categories
        if s in ['itching', 'skin_rash', 'nodal_skin_eruptions', 'red_spots_over_body', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling', 'silver_like_dusting', 'blister', 'red_sore_around_nose', 'yellow_crust_ooze', 'dischromic _patches']:
            s_category = "Skin & Nails"
        elif s in ['continuous_sneezing', 'shivering', 'chills', 'cough', 'high_fever', 'mild_fever', 'runny_nose', 'congestion', 'throat_irritation', 'phlegm']:
            s_category = "Respiratory / Cold"
        elif s in ['joint_pain', 'muscle_wasting', 'back_pain', 'weakness_in_limbs', 'neck_pain', 'cramps', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness', 'muscle_pain']:
            s_category = "Muscular & Joint"
        elif s in ['stomach_pain', 'acidity', 'ulcers_on_tongue', 'vomiting', 'indigestion', 'nausea', 'loss_of_appetite', 'constipation', 'abdominal_pain', 'diarrhoea', 'swelling_of_stomach', 'belly_pain', 'stomach_bleeding', 'distention_of_abdomen']:
            s_category = "Gastrointestinal"
        elif s in ['burning_micturition', 'spotting_ urination', 'yellow_urine', 'dark_urine', 'bladder_discomfort', 'foul_smell_of urine', 'continuous_feel_of_urine']:
            s_category = "Urinary System"
        elif s in ['fatigue', 'weight_gain', 'weight_loss', 'lethargy', 'increased_appetite', 'polyuria', 'obesity', 'excessive_hunger']:
            s_category = "Metabolic & Systemic"
        elif s in ['anxiety', 'mood_swings', 'restlessness', 'depression', 'irritability', 'lack_of_concentration']:
            s_category = "Neurological & Mood"
        elif s in ['headache', 'dizziness', 'spinning_movements', 'loss_of_balance', 'unsteadiness', 'altered_sensorium', 'visual_disturbances', 'blurred_and_distorted_vision', 'slurred_speech', 'weakness_of_one_body_side', 'loss_of_smell', 'coma']:
            s_category = "Brain & Senses"
        elif s in ['chest_pain', 'fast_heart_rate', 'palpitations', 'breathlessness']:
            s_category = "Cardiovascular"
        elif s in ['yellowish_skin', 'yellowing_of_eyes', 'acute_liver_failure', 'swelled_lymph_nodes', 'malaise']:
            s_category = "Liver & Lymphatic"
        
        symptoms_data.append({
            'id': s,
            'name': s_friendly,
            'category': s_category
        })
    return jsonify({
        'symptoms': symptoms_data,
        'categories': list(set(s['category'] for s in symptoms_data))
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json() or {}
    selected_symptoms = data.get('symptoms', [])
    model_name = data.get('model', 'random_forest')
    
    if model_name not in models:
        # Fallback to any loaded model
        if models:
            model_name = list(models.keys())[0]
        else:
            return jsonify({'error': 'No trained models available. Run main.py to train them first.'}), 400
            
    clf = models[model_name]
    
    # Construct input vector matching the exact SYMPTOMS_LIST
    input_vector = {}
    for s in SYMPTOMS_LIST:
        input_vector[s] = 1 if s in selected_symptoms else 0
        
    df_test = pd.DataFrame(columns=SYMPTOMS_LIST)
    df_test.loc[0] = np.array([input_vector[s] for s in SYMPTOMS_LIST])
    
    try:
        prediction = clf.predict(df_test)
        predicted_disease = prediction[0]
        
        # Calculate approximate model probabilities if supported
        prob_percent = None
        if hasattr(clf, "predict_proba"):
            probs = clf.predict_proba(df_test)
            max_prob_idx = np.argmax(probs[0])
            prob_val = probs[0][max_prob_idx]
            prob_percent = round(float(prob_val) * 100, 1)
            
        return jsonify({
            'success': True,
            'disease': predicted_disease,
            'probability': prob_percent,
            'model_used': model_name,
            'symptoms_count': len(selected_symptoms)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    # Ensure templates and static folders are present
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    app.run(debug=True, port=5000)
