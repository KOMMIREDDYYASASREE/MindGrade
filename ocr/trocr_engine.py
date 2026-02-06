from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import torch

processor = TrOCRProcessor.from_pretrained(
    "microsoft/trocr-base-handwritten"
)
model = VisionEncoderDecoderModel.from_pretrained(
    "microsoft/trocr-base-handwritten"
)

def extract_text(image):
    pixel_values = processor(image, return_tensors="pt").pixel_values
    ids = model.generate(pixel_values)
    return processor.batch_decode(
        ids, skip_special_tokens=True
    )[0]
