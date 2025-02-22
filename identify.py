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


# New code (OCR, cleaning, and dynamic operations)
def evaluate_operation(array, operation):
    try:
        numbers = []
        for item in array:
            if '/' in item:
                numerator, denominator = item.split('/')
                numbers.append(float(numerator) / float(denominator))
            else:
                numbers.append(float(item))
        
        if operation == 'add':
            result = sum(numbers)
        elif operation == 'subtract':
            result = numbers[0] - sum(numbers[1:])
        elif operation == 'multiply':
            result = 1
            for num in numbers:
                result *= num
        elif operation == 'divide':
            result = numbers[0]
            for num in numbers[1:]:
                if num == 0:
                    raise ZeroDivisionError("Division by zero is not allowed.")
                result /= num
        else:
            raise ValueError("Invalid operation.")
        
        return result
    except Exception as e:
        return f"Error: {e}"

# Ask the user for the operation
operation = input("Enter the operation (add, subtract, multiply, divide): ").strip().lower()

# Perform the operation and display the result
result = evaluate_operation(numbers_array, operation)
print(f"Result of {operation}: {result}")
