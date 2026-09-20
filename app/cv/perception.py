from ultralytics import YOLO


class VideoPerception:
    """
    SentinelAI visual perception layer.

    Performs:
        1. Object detection
        2. ByteTrack multi-object tracking
        3. Bounding-box extraction
        4. Persistent track IDs
    """

    def __init__(
        self,
        model_name: str = "yolo26n.pt",
        confidence_threshold: float = 0.35,
    ):

        print(
            f"Loading YOLO model: {model_name}"
        )

        self.model = YOLO(model_name)

        self.confidence_threshold = (
            confidence_threshold
        )

    def track_frame(self, frame):

        results = self.model.track(
            source=frame,
            persist=True,
            tracker="bytetrack.yaml",
            conf=self.confidence_threshold,
            verbose=False,
        )

        detections = []

        if not results:
            return detections

        result = results[0]

        if result.boxes is None:
            return detections

        boxes = result.boxes

        # If tracking ID doesn't exist,
        # ByteTrack did not produce a tracked object
        if boxes.id is None:
            return detections

        track_ids = (
            boxes.id
            .int()
            .cpu()
            .tolist()
        )

        class_ids = (
            boxes.cls
            .int()
            .cpu()
            .tolist()
        )

        confidences = (
            boxes.conf
            .cpu()
            .tolist()
        )

        xyxy_boxes = (
            boxes.xyxy
            .cpu()
            .tolist()
        )

        names = self.model.names

        for (
            track_id,
            class_id,
            confidence,
            bbox,
        ) in zip(
            track_ids,
            class_ids,
            confidences,
            xyxy_boxes,
        ):

            x1, y1, x2, y2 = bbox

            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2

            width = x2 - x1
            height = y2 - y1

            detection = {

                "track_id": int(track_id),

                "class_id": int(class_id),

                "class_name": names[
                    int(class_id)
                ],

                "confidence": float(
                    confidence
                ),

                "bbox": {
                    "x1": float(x1),
                    "y1": float(y1),
                    "x2": float(x2),
                    "y2": float(y2),
                },

                "center": {
                    "x": float(center_x),
                    "y": float(center_y),
                },

                "width": float(width),

                "height": float(height),
            }

            detections.append(
                detection
            )

        return detections