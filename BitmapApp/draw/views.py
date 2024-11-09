import random
import numpy as np  # Make sure numpy is installed
from django.shortcuts import render
from django.http import JsonResponse
from PIL import Image
import base64
import io
from django.views.decorators.csrf import csrf_exempt
import os
import json



def draw_view(request):
    # Randomly select a target letter from A to Z
    target_letter = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return render(request, 'draw/draw.html', {'target_letter': target_letter})

def calculate_accuracy(user_drawing, target_bitmap):
    # Resize both images to a standard size (28x28) and convert to grayscale
    user_drawing = user_drawing.resize((28, 28)).convert('L')
    target_bitmap = target_bitmap.resize((28, 28)).convert('L')

    # Convert images to binary based on a threshold
    threshold = 128
    user_binary = np.array(user_drawing).astype(np.uint8) > threshold
    target_binary = np.array(target_bitmap).astype(np.uint8) > threshold

    # Calculate similarity as the percentage of matching pixels
    matching_pixels = np.sum(user_binary == target_binary)
    total_pixels = user_binary.size
    accuracy = (matching_pixels / total_pixels) * 100

    return accuracy


@csrf_exempt
def process_drawing(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_data = data.get('image')
            target_letter = data.get('target_letter')
            
            if not image_data or not target_letter:
                return JsonResponse({'error': 'Image or target letter missing.'}, status=400)
            
            # Decode the base64 image data
            image_data = image_data.split(',')[1]  # Remove base64 prefix
            image_bytes = base64.b64decode(image_data)
            user_drawing = Image.open(io.BytesIO(image_bytes))

            # Load the target bitmap of the letter
            target_path = os.path.join('draw', 'alphabet_images', f"{target_letter}.png")
            if not os.path.exists(target_path):
                return JsonResponse({'error': f"Target image for letter '{target_letter}' not found."}, status=404)

            target_bitmap = Image.open(target_path)

            # Calculate accuracy
            accuracy = calculate_accuracy(user_drawing, target_bitmap)

            # Return the calculated accuracy as JSON response
            return JsonResponse({'message': 'Image processed!', 'accuracy': accuracy})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)