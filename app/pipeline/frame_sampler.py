import cv2
import numpy as np


class FrameSampler:
    """
    SentinelAI adaptive frame sampler.

    Pipeline:

        Video
          ↓
        Uniform sampling
          ↓
        OpenCV frame comparison
          ↓
        Change score
          ↓
        Important / Static decision
    """

    def __init__(
        self,
        target_fps: float = 2.0,
        resize_width: int = 320,
    ):
        self.target_fps = target_fps
        self.resize_width = resize_width

    def _prepare_for_comparison(self, frame):

        height, width = frame.shape[:2]

        if width > self.resize_width:

            scale = (
                self.resize_width / width
            )

            new_height = int(
                height * scale
            )

            frame = cv2.resize(
                frame,
                (
                    self.resize_width,
                    new_height,
                ),
            )

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY,
        )

        gray = cv2.GaussianBlur(
            gray,
            (5, 5),
            0,
        )

        return gray

    def _calculate_change_score(
        self,
        previous_frame,
        current_frame,
    ):

        if previous_frame is None:
            return 1.0

        difference = cv2.absdiff(
            previous_frame,
            current_frame,
        )

        # Average normalized pixel difference
        change_score = (
            float(np.mean(difference))
            / 255.0
        )

        return round(
            change_score,
            6,
        )

    def sample(
        self,
        video_path: str,
    ):

        cap = cv2.VideoCapture(
            video_path
        )

        if not cap.isOpened():

            raise ValueError(
                f"Could not open video: "
                f"{video_path}"
            )

        native_fps = cap.get(
            cv2.CAP_PROP_FPS
        )

        if (
            not native_fps
            or native_fps <= 0
        ):
            native_fps = 30.0

        total_frames = int(
            cap.get(
                cv2.CAP_PROP_FRAME_COUNT
            )
        )

        frame_interval = max(
            1,
            int(
                round(
                    native_fps
                    / self.target_fps
                )
            ),
        )

        previous_comparison_frame = None

        frame_index = 0
        sampled_count = 0

        try:

            while True:

                success, frame = cap.read()

                if not success:
                    break

                if (
                    frame_index
                    % frame_interval
                    == 0
                ):

                    timestamp = (
                        frame_index
                        / native_fps
                    )

                    comparison_frame = (
                        self
                        ._prepare_for_comparison(
                            frame
                        )
                    )

                    change_score = (
                        self
                        ._calculate_change_score(
                            previous_comparison_frame,
                            comparison_frame,
                        )
                    )

                    previous_comparison_frame = (
                        comparison_frame
                    )

                    sampled_count += 1

                    yield {

                        "timestamp":
                            round(
                                timestamp,
                                3,
                            ),

                        "frame_index":
                            frame_index,

                        "frame":
                            frame,

                        "change_score":
                            change_score,
                    }

                frame_index += 1

        finally:

            cap.release()

        print(
            f"FrameSampler finished. "
            f"Original frames={total_frames}, "
            f"Sampled frames={sampled_count}"
        )