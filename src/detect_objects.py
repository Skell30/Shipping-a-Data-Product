from ultralytics import YOLO
import os
import json
from pathlib import Path

# Load YOLOv8 model (you can also use yolov8n.pt or yolov8x.pt for different sizes)
model = YOLO("yolov8m.pt")

# Define path to images
image_dir = Path(r"data\raw\images\2025-07-13")  # or wherever your scraped images are
output_file = Path("data/processed/yolo_detections.json")

results = []

for img_path in image_dir.glob("*.jpg"):
    detections = model(img_path)
    for r in detections:
        for box in r.boxes:
            result = {
                "image_path": str(img_path),
                "detected_object_class": model.names[int(box.cls)],
                "confidence_score": float(box.conf[0])
            }
            results.append(result)

# Save results
output_file.parent.mkdir(parents=True, exist_ok=True)
with open(output_file, "w") as f:
    json.dump(results, f, indent=2)

print(f"✅ Saved detections to {output_file}")
