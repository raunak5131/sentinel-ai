import json

from groq import Groq

from app.config import settings


class LLMService:
    """
    SentinelAI LLM Intelligence Layer.

    Converts structured temporal video events into
    a natural-language video summary using Groq.
    """

    def __init__(self):

        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

        self.model = "openai/gpt-oss-20b"


    def prepare_events_context(
        self,
        events: list,
    ) -> list:
        """
        Convert SQLAlchemy EventRecord objects into
        compact structured data for the LLM.
        """

        formatted_events = []

        for event in events:

            formatted_events.append({
                "time": round(
                    float(event.start_timestamp),
                    1,
                ),

                "type": event.event_type,

                "object": event.object_class,

                "id": event.entity_id,

                "description": event.description,
            })

        return formatted_events


    def build_summary_prompt(
        self,
        video_duration: float,
        events: list,
    ) -> str:

        events_context = (
            self.prepare_events_context(events)
        )

        # Compact JSON saves tokens
        events_json = json.dumps(
            events_context,
            separators=(",", ":"),
        )

        prompt = f"""
Summarize this video using ONLY the event data below.

Video duration: {video_duration:.1f} seconds

Events:
{events_json}

Rules:
- Write only the final summary.
- Do not explain your reasoning.
- Do not analyze the data step by step.
- Do not mention every individual event.
- Combine related events into a natural chronological description.
- Mention only important entries, exits, movement, and stationary behavior.
- Ignore redundant tracking events.
- Do not invent actions, objects, locations, colors, sports, or intentions.
- Keep the summary between 60 and 150 words.
- Be concise and professional.

Final summary:
"""

        return prompt.strip()


    def summarize_events(
        self,
        video_duration: float,
        events: list,
    ) -> str:

        if not events:

            return (
                "No significant tracked activity "
                "was detected in the video."
            )


        prompt = self.build_summary_prompt(
            video_duration=video_duration,
            events=events,
        )


        try:

            response = (
                self.client.chat.completions.create(

                    model=self.model,

                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You summarize structured video "
                                "events accurately. Produce the "
                                "final answer directly and do not "
                                "include reasoning."
                            ),
                        },

                        {
                            "role": "user",
                            "content": prompt,
                        },
                    ],

                    temperature=0.2,

                    # Increased because GPT-OSS may use
                    # hidden reasoning tokens.
                    max_completion_tokens=3000,
                )
            )


            print("=" * 70)
            print("RAW LLM RESPONSE:")
            print(response)
            print("=" * 70)


            if not response.choices:

                raise RuntimeError(
                    "LLM returned no choices."
                )


            choice = response.choices[0]

            message = choice.message

            summary = getattr(
                message,
                "content",
                None,
            )


            print(
                "FINISH REASON:",
                choice.finish_reason,
            )


            # Successful summary
            if summary and summary.strip():

                return summary.strip()


            # Important debugging information
            reasoning = getattr(
                message,
                "reasoning",
                None,
            )


            if reasoning:

                print("=" * 70)
                print("MODEL REASONING WAS PRESENT")
                print(reasoning[:1000])
                print("=" * 70)


            print(
                "WARNING: LLM returned empty content."
            )


            # Do not return an ugly technical message
            # to the user.
            return (
                self.generate_fallback_summary(
                    video_duration,
                    events,
                )
            )


        except Exception as error:

            print(
                "LLM SUMMARY GENERATION FAILED:"
            )

            print(error)


            return (
                self.generate_fallback_summary(
                    video_duration,
                    events,
                )
            )


    def generate_fallback_summary(
        self,
        video_duration: float,
        events: list,
    ) -> str:
        """
        Basic fallback summary if the LLM fails.
        """

        object_types = set()

        for event in events:

            if event.object_class:

                object_types.add(
                    event.object_class
                )


        if object_types:

            objects = ", ".join(
                sorted(object_types)
            )

            return (
                f"The {video_duration:.1f}-second video "
                f"contains tracked activity involving "
                f"{objects}. Multiple objects enter, move "
                f"through, or leave the monitored scene."
            )


        return (
            f"The {video_duration:.1f}-second video "
            f"contains multiple tracked events involving "
            f"object movement within the monitored scene."
        )