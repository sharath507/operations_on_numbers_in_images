import cv2
import easyocr
import re

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Load the image
image = cv2.imread('demo-4-hw.jpg')  # Replace with your image path

# Detect and recognize text
results = reader.readtext(image)

# Function to clean text
def clean_text(text):
    # Remove all non-numeric characters except digits, fractions, and decimals
    cleaned = re.sub(r'[^0-9./-]', '', text)  # Keep digits, '.', '/', and '-'
    # Remove any remaining spaces
    cleaned = cleaned.replace(" ", "")
    return cleaned

# Initialize a list to store recognized numbers
numbers_array = []

# Loop through the results and clean the text
for (bbox, text, confidence) in results:
    print(f"Raw OCR Output: '{text}'")  # Debug: Print raw OCR output
    
    # Clean the text
    cleaned_text = clean_text(text)
    numbers_array.append(cleaned_text)

    # Extract bounding box coordinates
    (top_left, top_right, bottom_right, bottom_left) = bbox
    top_left = tuple(map(int, top_left))
    bottom_right = tuple(map(int, bottom_right))

    # Draw bounding box on the image
    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

# Display the image with bounding boxes
cv2.imshow('Detected Numbers', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Print the recognized numbers in array format
print("Recognized Numbers in Array Format:")
print(numbers_array)