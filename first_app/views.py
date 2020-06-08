from django.shortcuts import render, HttpResponse
from tensorflow import keras  
from django.core.files.storage import FileSystemStorage
import numpy as np
# Create your views here.

def home(request):
    if request.method == 'POST':
        #Do our prediction
        #image is come from request
        image = request.FILES.get('image_name')
        print(image)
        fs = FileSystemStorage()
        filename = fs.save("static/{}".format(image.name), image)
        url = image.name
        print(url)
        uploaded_file_url = fs.url(filename)
        image = keras.preprocessing.image.load_img(uploaded_file_url, target_size=(224,224))
        image = keras.preprocessing.image.img_to_array(image)
        image = np.reshape(image, (1, 224, 224, 3))
        model = keras.models.load_model('C:\\Users\\Wilson Akyeampong\\model.h5')
        prediction = model.predict(image)
        print("prediction {}".format(prediction))
        if prediction[0][0] > 0.5:
            label = "Safe"
            accuracy = prediction[0][0] * 100
        else:
            label = "Explicit"
            accuracy = (1-prediction[0][0]) * 100
        return render(
            request,
            "index.html",
            {
                "label": label,
                "url": url,
                "accuracy": accuracy
            }
        )
    return render(request, "index.html")