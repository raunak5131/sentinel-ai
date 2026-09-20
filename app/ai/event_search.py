import re

from app.database import SessionLocal
from app.models.schema import EventRecord
from app.ai.event_embedder import EventEmbedder
from app.ai.query_understanding import QueryUnderstanding


class EventSearch:

    def __init__(self):
        self.embedder = EventEmbedder()
        self.query_understanding = QueryUnderstanding()

    def extract_time_range(self, query):
        """
        Detect simple time references from the user's query.

        Examples:
            "around 20 seconds" -> (18, 22)
            "at 20 seconds"     -> (19, 21)
            "between 15 and 25 seconds" -> (15, 25)
        """

        query_lower = query.lower()

        # between X and Y seconds
        match = re.search(
            r"between\s+(\d+(?:\.\d+)?)\s+and\s+(\d+(?:\.\d+)?)\s*seconds?",
            query_lower,
        )

        if match:
            start = float(match.group(1))
            end = float(match.group(2))
            return start, end

        # around X seconds
        match = re.search(
            r"around\s+(\d+(?:\.\d+)?)\s*seconds?",
            query_lower,
        )

        if match:
            center = float(match.group(1))
            return max(0, center - 2), center + 2

        # at X seconds
        match = re.search(
            r"at\s+(\d+(?:\.\d+)?)\s*seconds?",
            query_lower,
        )

        if match:
            center = float(match.group(1))
            return max(0, center - 1), center + 1

        return None

    def get_available_object_classes(self, db, video_id):
        rows = (
            db.query(EventRecord.object_class)
            .filter(EventRecord.video_id == video_id)
            .filter(EventRecord.object_class.is_not(None))
            .distinct()
            .all()
        )

        return [row[0] for row in rows]

    def search(self, video_id, query, limit=5):
        db = SessionLocal()

        try:
            # Get objects actually present in this video
            available_objects = self.get_available_object_classes(
                db=db,
                video_id=video_id,
            )

            # Understand the user's question
            query_info = self.query_understanding.understand(
                question=query,
                available_objects=available_objects,
            )

            print("=" * 60)
            print("QUERY UNDERSTANDING")
            print("=" * 60)
            print(f"Question: {query}")
            print(f"Available objects: {available_objects}")
            print(f"Parsed query: {query_info}")
            print("=" * 60)

            query_embedding = self.embedder.embed(query)

            time_range = self.extract_time_range(query)

            query_obj = (
                db.query(EventRecord)
                .filter(EventRecord.video_id == video_id)
                .filter(EventRecord.embedding.is_not(None))
            )
            # ----------------------------------------
            # STRUCTURED FILTERS
            # ----------------------------------------

            if query_info["object_class"]:
                query_obj = query_obj.filter(
                    EventRecord.object_class == query_info["object_class"]
                )

            if query_info["event_type"]:
                query_obj = query_obj.filter(
                    EventRecord.event_type == query_info["event_type"]
                )

            # Apply temporal filtering when a time range exists
            if time_range:

                start_time, end_time = time_range

                query_obj = query_obj.filter(
                    EventRecord.start_timestamp >= start_time,
                    EventRecord.start_timestamp <= end_time,
                )

            if query_info["intent"] == "count":
                events = (
                    query_obj
                    .order_by(EventRecord.start_timestamp)
                    .all()
                )

                results = []

                for event in events:
                    results.append({
                        "event_id": str(event.id),
                        "timestamp": event.start_timestamp,
                        "event_type": event.event_type,
                        "entity_id": event.entity_id,
                        "object_class": event.object_class,
                        "confidence": event.confidence,
                        "description": event.description,
                        "metadata": event.metadata_json,
                    })

                return results

            events = query_obj.order_by(EventRecord.start_timestamp).limit(limit).all()

            results = []

            for event in events:

                results.append(
                    {
                        "event_id": str(event.id),
                        "timestamp": event.start_timestamp,
                        "event_type": event.event_type,
                        "entity_id": event.entity_id,
                        "object_class": event.object_class,
                        "confidence": event.confidence,
                        "description": event.description,
                        "metadata": event.metadata_json,
                    }
                )

            return results

        finally:
            db.close()
