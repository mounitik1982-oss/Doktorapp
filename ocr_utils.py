import easyocr

# initialize the OCR reader once
reader = easyocr.Reader(['en'], gpu=False)

def extract_text(image_path):
    """
    Extracts text from the given image using EasyOCR.
    Returns the raw text as a string.
    """
    try:
        results = reader.readtext(image_path, detail=0)
        return "\n".join(results)
    except Exception as e:
        return f"Error during OCR: {str(e)}"
