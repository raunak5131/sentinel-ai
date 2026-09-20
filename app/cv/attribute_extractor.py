import cv2
import numpy as np


class AttributeExtractor:
    """
    Extract visual attributes from detected objects.

    Current:
    - Dominant color

    Future:
    - Vehicle type
    - Person clothing color
    - Scene attributes
    """

    def extract(self, frame, detection):

        bbox = detection.get("bbox")

        if bbox is None:
            return {}

        color = self.extract_color(
            frame=frame,
            bbox=bbox,
        )

        attributes = {}

        if color is not None:
            attributes["color"] = color

        return attributes


    # =========================================
    # COLOR EXTRACTION
    # =========================================

    def extract_color(self, frame, bbox):

        height, width = frame.shape[:2]

        x1 = max(0, int(bbox["x1"]))
        y1 = max(0, int(bbox["y1"]))

        x2 = min(width, int(bbox["x2"]))
        y2 = min(height, int(bbox["y2"]))

        if x2 <= x1 or y2 <= y1:
            return None

        crop = frame[y1:y2, x1:x2]

        if crop.size == 0:
            return None

        # Ignore very small detections
        if crop.shape[0] < 5 or crop.shape[1] < 5:
            return None

        crop = cv2.resize(
            crop,
            (100, 100),
            interpolation=cv2.INTER_AREA,
        )

        hsv = cv2.cvtColor(
            crop,
            cv2.COLOR_BGR2HSV,
        )

        # Flatten pixels
        pixels = hsv.reshape(-1, 3)

        # Remove extremely dark pixels
        pixels = pixels[pixels[:, 2] > 40]

        if len(pixels) == 0:
            return None

        # Median is more robust than simple average
        h, s, v = np.median(
            pixels,
            axis=0,
        )

        return self.hsv_to_color_name(
            h=h,
            s=s,
            v=v,
        )


    # =========================================
    # HSV TO HUMAN COLOR
    # =========================================

    def hsv_to_color_name(
        self,
        h,
        s,
        v,
    ):

        # Black
        if v < 50:
            return "black"

        # White / gray
        if s < 35:

            if v > 200:
                return "white"

            if v > 100:
                return "gray"

            return "dark gray"

        # OpenCV Hue = 0 to 179

        if h < 10 or h >= 170:
            return "red"

        if h < 25:
            return "orange"

        if h < 35:
            return "yellow"

        if h < 85:
            return "green"

        if h < 100:
            return "cyan"

        if h < 130:
            return "blue"

        if h < 160:
            return "purple"

        return "red"