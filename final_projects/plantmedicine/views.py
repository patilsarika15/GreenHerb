from django.shortcuts import render
from .forms import ImageUploadForm
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
import os
import json
import numpy as np
import tensorflow as tf

import json
from .forms import PlantSearchForm

# Define the path to the saved model and JSON file
MODEL_PATH = r'model/plant_medicine/my_model.h5'
JSON_PATH = r'model/plant_medicine/medicine_qualities.json'
Images_leaf = r'static/Images_leaf'
# Load class names
CLASS_NAMES = [
    "Aloevera", "Amla", "Amruta_Balli", "Arali", "Ashoka", "Ashwagandha", "Avacado", "Bamboo", "Basale", 
    "Betel", "Betel_Nut", "Brahmi", "Castor", "Curry_Leaf", "Doddapatre", "Ekka", "Ganike", "Gauva", 
    "Geranium", "Henna", "Hibiscus", "Honge", "Insulin", "Jasmine", "Lemon", "Lemon_grass", "Mango", 
    "Mint", "Nagadali", "Neem", "Nithyapushpa", "Nooni", "Pappaya", "Pepper", "Pomegranate", "Raktachandini", 
    "Rose", "Sapota", "Tulasi", "Wood_sorel"
]

# Load medicinal information from JSON file
with open(JSON_PATH) as json_file:
    MEDICINAL_INFO = json.load(json_file)

@csrf_exempt
def predict_plant(request):
    if request.method == 'POST' and 'image' in request.FILES:
        # Handle uploaded image
        uploaded_image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_image.name, uploaded_image)
        uploaded_file_path = fs.path(filename)

        static_folder = Images_leaf 
        
        # Delete all other images in the static folder
        for file_name in os.listdir(static_folder):
            file_path = os.path.join(static_folder, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        
        # Save the uploaded image with a unique name in the static folder
        unique_filename = os.path.join(static_folder, 'uploaded_image.jpg')
        with open(unique_filename, 'wb') as f:
            for chunk in uploaded_image.chunks():
                f.write(chunk)


        # Load the saved model
        try:
            model = tf.keras.models.load_model(MODEL_PATH)
        except Exception as e:
            return JsonResponse({"error": f"Error loading the model: {str(e)}"}, status=500)

        # Load and preprocess the image
        try:
            img = tf.keras.preprocessing.image.load_img(uploaded_file_path, target_size=(224, 224))
            img_array = tf.keras.preprocessing.image.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0)
        except Exception as e:
            return JsonResponse({"error": f"Error loading or preprocessing the image: {str(e)}"}, status=400)

        # Make predictions
        predictions = model.predict(img_array)

        # Get the predicted class index
        predicted_index = np.argmax(predictions[0])

        # Get the predicted class name
        predicted_class = CLASS_NAMES[predicted_index]

        response_data = {"predicted_class": predicted_class}

        # Include medicinal qualities if available for the predicted class
        if predicted_class in MEDICINAL_INFO:
            response_data["medicinal_qualities"] = MEDICINAL_INFO[predicted_class]["medicinal_qualities"]
            response_data["cures"] = MEDICINAL_INFO[predicted_class]["cures"]

        return render(request, 'plant/result.html', {'response_data': response_data,'uploaded_file_path':uploaded_file_path})
    else:
        form = ImageUploadForm()
        return render(request, 'plant/predict.html', {'form': form})


import json
from django.shortcuts import render
from .forms import PlantSearchForm

def search_plant(request):
    if request.method == 'POST':
        form = PlantSearchForm(request.POST)
        if form.is_valid():
            plant_name = form.cleaned_data['plant_name']
            plant_name_text = request.POST.get("plant_name_text")

            # Read the JSON data from the file
            with open(JSON_PATH, 'r') as file:
                plant_data = json.load(file)

            # Check if the plant exists in the JSON data
            if plant_name or plant_name_text in plant_data:
                # Retrieve the details of the plant
                plant_details = plant_data[plant_name]
                medicinal_qualities = plant_details.get('medicinal_qualities', [])
                cures = plant_details.get('cures', [])
                recommended_consumption = plant_details.get('recommended_consumption', '')
                bt = plant_details.get('bt', '')
                img_address = plant_details.get('img_address', '')

                # Prepare context to pass to the template
                context = {
                    'plant_name': plant_name,
                    'medicinal_qualities': medicinal_qualities,
                    'cures': cures,
                    'recommended_consumption': recommended_consumption,
                    "bt" : bt,
                    'img_address':img_address
                }

                # Render the template with the context data
                return render(request, 'plant/plant_details.html', context)
            else:
                # If plant is not found, render a template indicating so
                return render(request, 'plant/search_plant.html', {'plant_choices': CLASS_NAMES})

    # If request method is not POST, render the search plant template with plant choices
    return render(request, 'plant/search_plant.html', {'plant_choices': CLASS_NAMES})


# Import necessary libraries
from django.shortcuts import render
import json

# Assuming you have defined CLASS_NAMES and JSON_PATH somewhere in your code

def text(request):
    if request.method == 'POST':
        # Get the plant name submitted by the user
        plant_name_text = request.POST.get("plant_name_text")

        # Read the JSON data from the file
        with open(JSON_PATH, 'r') as file:
            plant_data = json.load(file)

        # Check if the plant exists in the JSON data
        if plant_name_text in plant_data:
            # Retrieve the details of the plant
            plant_details = plant_data[plant_name_text]
            medicinal_qualities = plant_details.get('medicinal_qualities', [])
            cures = plant_details.get('cures', [])
            recommended_consumption = plant_details.get('recommended_consumption', '')
            bt = plant_details.get('bt', '')
            img_address = plant_details.get('img_address', '')

            # Prepare context to pass to the template
            context = {
                'plant_name': plant_name_text,
                'medicinal_qualities': medicinal_qualities,
                'cures': cures,
                'recommended_consumption': recommended_consumption,
                'bt': bt,
                'img_address': img_address
            }

            # Render the template with the context data
            return render(request, 'plant/plant_details.html', context)
        else:
            # If plant is not found, render a template indicating so
            return render(request, 'plant/plant_not_found.html', {'plant_name': plant_name_text})

    # If request method is not POST or if there's no input, render the form template
    return render(request, 'plant/text.html')

def imagePlant(request):
    return render(request, 'plant/imgleaf.html')