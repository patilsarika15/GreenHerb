import numpy as np
import tensorflow as tf
import json

# Load the saved model
model = tf.keras.models.load_model("my_model.h5")

# Load class names
class_names = [
    "Aloevera", "Amla", "Amruta_Balli", "Arali", "Ashoka", "Ashwagandha", "Avacado", "Bamboo", "Basale", 
    "Betel", "Betel_Nut", "Brahmi", "Castor", "Curry_Leaf", "Doddapatre", "Ekka", "Ganike", "Gauva", 
    "Geranium", "Henna", "Hibiscus", "Honge", "Insulin", "Jasmine", "Lemon", "Lemon_grass", "Mango", 
    "Mint", "Nagadali", "Neem", "Nithyapushpa", "Nooni", "Pappaya", "Pepper", "Pomegranate", "Raktachandini", 
    "Rose", "Sapota", "Tulasi", "Wood_sorel"
]

# Get user input for the image path
image_path = 'a.jpg'

# Load and preprocess the image
img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
img_array = tf.keras.preprocessing.image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)

# Make predictions
predictions = model.predict(img_array)

# Get the predicted class index
predicted_index = np.argmax(predictions[0])

# Load medicinal information from JSON file
with open('medicine_qualities.json') as json_file:
    medicinal_info = json.load(json_file)

# Get the predicted class name
predicted_class = class_names[predicted_index]

# Display the predicted class name
print("Predicted class name:", predicted_class)

# Display medicinal qualities if available for the predicted class
if predicted_class in medicinal_info:
    print("Medicinal Qualities:")
    for quality in medicinal_info[predicted_class]["medicinal_qualities"]:
        print("- ", quality)
else:
    print("No medicinal information available for this plant.")
