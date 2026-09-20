from openai import OpenAI

from app.config import settings


class SceneUnderstanding:

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1",
        )

        self.model = "openai/gpt-oss-20b"


    # =========================================
    # MAIN SCENE ANALYSIS
    # =========================================

    def analyze_scene(self, detections):

        if not detections:

            return {
                "scene_description":
                    "No significant objects were detected.",

                "scene_type":
                    "unknown",

                "object_counts":
                    {},
            }


        object_counts = {}

        for detection in detections:

            object_class = detection.get(
                "class_name",
                "unknown"
            )

            object_counts[object_class] = (
                object_counts.get(object_class, 0) + 1
            )


        object_text = "\n".join(
            [
                f"- {name}: {count}"
                for name, count in object_counts.items()
            ]
        )


        prompt = f"""
You are analyzing a surveillance video.

The object detector found the following objects:

{object_text}

Based ONLY on this information:

1. Describe the overall scene in one concise sentence.
2. Classify the scene.

Allowed scene types:

road
parking_area
indoor
outdoor
crowd
industrial
unknown

Do not invent objects or activities that were not provided.

Return EXACTLY:

SCENE_DESCRIPTION: <one sentence>
SCENE_TYPE: <one allowed type>
"""


        response = self.client.chat.completions.create(

            model=self.model,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a visual surveillance "
                        "scene analysis system."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],

            temperature=0.1,
        )


        raw_response = (
            response
            .choices[0]
            .message
            .content
        )


        result = self.parse_response(
            raw_response
        )


        result["object_counts"] = object_counts

        return result


    # =========================================
    # PARSE RESPONSE
    # =========================================

    def parse_response(self, response):

        scene_description = (
            "Scene analysis unavailable."
        )

        scene_type = "unknown"


        for line in response.splitlines():

            line = line.strip()


            if line.startswith(
                "SCENE_DESCRIPTION:"
            ):

                scene_description = (
                    line[
                        len("SCENE_DESCRIPTION:"):
                    ]
                    .strip()
                )


            elif line.startswith(
                "SCENE_TYPE:"
            ):

                scene_type = (
                    line[
                        len("SCENE_TYPE:"):
                    ]
                    .strip()
                    .lower()
                )


        allowed_types = {
            "road",
            "parking_area",
            "indoor",
            "outdoor",
            "crowd",
            "industrial",
            "unknown",
        }


        if scene_type not in allowed_types:

            scene_type = "unknown"


        return {
            "scene_description":
                scene_description,

            "scene_type":
                scene_type,
        }