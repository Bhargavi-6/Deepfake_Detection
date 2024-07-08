import tensorflow as tf
import os
from tensorflow.keras.preprocessing import image

# Load the pre-trained model
image_model = tf.keras.models.load_model('model/cnn_deepfake_image.h5')

# Configure upload folder and allowed file extensions
IMAGE_UPLOAD_FOLDER = 'uploads/images'
IMAGE_ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(IMAGE_UPLOAD_FOLDER, exist_ok=True)


def image_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in IMAGE_ALLOWED_EXTENSIONS


def predict_image(filepath):
    img = image.load_img(filepath, target_size=(256, 256))
    img_tensor = image.img_to_array(img)
    img_tensor = tf.expand_dims(img_tensor, axis=0)

    # Indicate classifying before prediction

    predicted = image_model.predict(img_tensor)
    predicted_class = tf.argmax(predicted, axis=1).numpy()[0]

    # Determine prediction label and class for CSS
    prediction_label = 'Fake' if predicted_class == 1 else 'Real'
    prediction_class = 'fake' if predicted_class == 1 else 'real'

    return f'The image is predicted as {prediction_label}.'