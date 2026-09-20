import math


class EventEngine:

    def __init__(
        self,
        exit_threshold=4.0,
        movement_threshold=8.0,
        stop_threshold=2.0,
        edge_margin=80,
    ):

        # Currently active objects
        self.active_tracks = {}

        # Number of sessions for reused YOLO IDs
        self.track_sessions = {}

        self.exit_threshold = exit_threshold
        self.movement_threshold = movement_threshold
        self.stop_threshold = stop_threshold
        self.edge_margin = edge_margin


    # =============================================
    # UNIQUE ENTITY ID
    # =============================================

    def create_entity_id(
        self,
        object_class,
        track_id,
    ):

        key = (
            object_class,
            track_id,
        )

        if key not in self.track_sessions:

            self.track_sessions[key] = 1

        else:

            self.track_sessions[key] += 1

        session = self.track_sessions[key]

        return (
            f"{object_class}_"
            f"{track_id}_"
            f"session_{session}"
        )


    # =============================================
    # EDGE CHECK
    # =============================================

    def is_near_edge(
        self,
        bbox,
        frame_width,
        frame_height,
    ):

        if (
            bbox is None
            or frame_width is None
            or frame_height is None
        ):
            return False

        x1 = bbox["x1"]
        y1 = bbox["y1"]

        x2 = bbox["x2"]
        y2 = bbox["y2"]

        margin = self.edge_margin

        return (
            x1 <= margin
            or y1 <= margin
            or x2 >= frame_width - margin
            or y2 >= frame_height - margin
        )


    # =============================================
    # EVENT HELPER
    # =============================================

    def build_event(
        self,
        event_type,
        entity_id,
        track_data,
        start_timestamp,
        end_timestamp,
        description,
        metadata=None,
    ):

        if metadata is None:
            metadata = {}

        metadata["track_id"] = track_data["track_id"]

        if track_data.get("attributes"):
            metadata["attributes"] = (
                track_data["attributes"]
            )

        return {

            "start_timestamp": start_timestamp,

            "end_timestamp": end_timestamp,

            "event_type": event_type,

            "entity_id": entity_id,

            "object_class":
                track_data["object_class"],

            "confidence":
                track_data["confidence"],

            "description": description,

            "metadata": metadata,
        }


    # =============================================
    # UPDATE TIME WHEN YOLO IS SKIPPED
    # =============================================

    def update_time(
        self,
        timestamp,
    ):

        events = []

        for entity_id, track_data in self.active_tracks.items():

            if (
                track_data["motion_state"]
                != "stationary"
            ):
                continue

            stationary_since = (
                track_data["stationary_since"]
            )

            if stationary_since is None:
                continue

            stationary_duration = (
                timestamp
                - stationary_since
            )

            if (
                stationary_duration
                >= self.stop_threshold
            ):

                track_data[
                    "motion_state"
                ] = "stopped"

                events.append(
                    self.build_event(

                        event_type="stopped",

                        entity_id=entity_id,

                        track_data=track_data,

                        start_timestamp=stationary_since,

                        end_timestamp=timestamp,

                        description=(
                            f"{track_data['object_class'].capitalize()} "
                            f"#{track_data['track_id']} "
                            f"stopped moving."
                        ),

                        metadata={
                            "stationary_duration":
                                stationary_duration,
                        },
                    )
                )

        return events


    # =============================================
    # MAIN DETECTION PROCESSING
    # =============================================

    def process(
        self,
        timestamp,
        detections,
        frame_width=None,
        frame_height=None,
    ):

        events = []

        current_entities = set()

        current_track_lookup = {}

        # -----------------------------------------
        # Build lookup of active tracks
        # -----------------------------------------

        for entity_id, track_data in (
            self.active_tracks.items()
        ):

            key = (
                track_data["object_class"],
                track_data["track_id"],
            )

            current_track_lookup[key] = entity_id


        # =========================================
        # 1. PROCESS DETECTIONS
        # =========================================

        for detection in detections:

            track_id = detection["track_id"]

            object_class = (
                detection["class_name"]
            )

            confidence = (
                detection["confidence"]
            )

            center = detection.get(
                "center"
            )

            bbox = detection.get(
                "bbox"
            )

            attributes = detection.get(
                "attributes",
                {}
            )

            track_key = (
                object_class,
                track_id,
            )


            # -------------------------------------
            # FIND ENTITY
            # -------------------------------------

            if (
                track_key
                in current_track_lookup
            ):

                entity_id = (
                    current_track_lookup[
                        track_key
                    ]
                )

            else:

                entity_id = (
                    self.create_entity_id(
                        object_class,
                        track_id,
                    )
                )

            current_entities.add(
                entity_id
            )


            # =====================================
            # NEW OBJECT
            # =====================================

            if (
                entity_id
                not in self.active_tracks
            ):

                track_data = {

                    "object_class":
                        object_class,

                    "track_id":
                        track_id,

                    "start_timestamp":
                        timestamp,

                    "last_seen":
                        timestamp,

                    "confidence":
                        confidence,

                    "attributes":
                        attributes,

                    "last_x":
                        (
                            center["x"]
                            if center
                            else None
                        ),

                    "last_y":
                        (
                            center["y"]
                            if center
                            else None
                        ),

                    "last_bbox":
                        bbox,

                    "motion_state":
                        "unknown",

                    "stationary_since":
                        timestamp,

                    "missing_since":
                        None,
                }

                self.active_tracks[
                    entity_id
                ] = track_data

                events.append(
                    self.build_event(

                        event_type="entered",

                        entity_id=entity_id,

                        track_data=track_data,

                        start_timestamp=timestamp,

                        end_timestamp=timestamp,

                        description=(
                            f"{object_class.capitalize()} "
                            f"#{track_id} entered "
                            f"the monitored scene."
                        ),

                        metadata={
                            "center": center,
                            "bbox": bbox,
                        },
                    )
                )

                continue


            # =====================================
            # EXISTING OBJECT
            # =====================================

            track_data = (
                self.active_tracks[
                    entity_id
                ]
            )

            previous_state = (
                track_data["motion_state"]
            )

            previous_x = (
                track_data["last_x"]
            )

            previous_y = (
                track_data["last_y"]
            )


            # -------------------------------------
            # UPDATE TRACK
            # -------------------------------------

            track_data[
                "missing_since"
            ] = None

            track_data[
                "last_seen"
            ] = timestamp

            track_data[
                "confidence"
            ] = confidence

            track_data[
                "last_bbox"
            ] = bbox

            # Update attributes only if available
            if attributes:
                track_data[
                    "attributes"
                ] = attributes


            # =====================================
            # MOVEMENT ANALYSIS
            # =====================================

            if (
                center is not None
                and previous_x is not None
                and previous_y is not None
            ):

                movement_distance = math.sqrt(

                    (
                        center["x"]
                        - previous_x
                    ) ** 2

                    +

                    (
                        center["y"]
                        - previous_y
                    ) ** 2
                )


                # =================================
                # OBJECT IS MOVING
                # =================================

                if (
                    movement_distance
                    >= self.movement_threshold
                ):

                    if previous_state in (
                        "stationary",
                        "stopped",
                        "unknown",
                    ):

                        events.append(
                            self.build_event(

                                event_type=
                                    "started_moving",

                                entity_id=
                                    entity_id,

                                track_data=
                                    track_data,

                                start_timestamp=
                                    timestamp,

                                end_timestamp=
                                    timestamp,

                                description=(
                                    f"{object_class.capitalize()} "
                                    f"#{track_id} "
                                    f"started moving."
                                ),

                                metadata={
                                    "movement_distance":
                                        movement_distance,

                                    "previous_center": {
                                        "x":
                                            previous_x,

                                        "y":
                                            previous_y,
                                    },

                                    "current_center":
                                        center,
                                },
                            )
                        )

                    track_data[
                        "motion_state"
                    ] = "moving"

                    track_data[
                        "stationary_since"
                    ] = None


                # =================================
                # OBJECT IS STATIONARY
                # =================================

                else:

                    if previous_state in (
                        "moving",
                        "unknown",
                    ):

                        track_data[
                            "motion_state"
                        ] = "stationary"

                        track_data[
                            "stationary_since"
                        ] = timestamp


            # -------------------------------------
            # UPDATE POSITION
            # -------------------------------------

            if center is not None:

                track_data[
                    "last_x"
                ] = center["x"]

                track_data[
                    "last_y"
                ] = center["y"]


        # =========================================
        # 2. CHECK MISSING OBJECTS
        # =========================================

        exited_entities = []

        for entity_id, track_data in list(
            self.active_tracks.items()
        ):

            if entity_id in current_entities:
                continue


            if (
                track_data[
                    "missing_since"
                ]
                is None
            ):

                track_data[
                    "missing_since"
                ] = timestamp


            missing_duration = (

                timestamp

                -

                track_data[
                    "last_seen"
                ]
            )


            # =====================================
            # GRACE PERIOD
            # =====================================

            if (
                missing_duration
                < self.exit_threshold
            ):
                continue


            bbox = (
                track_data[
                    "last_bbox"
                ]
            )

            near_edge = self.is_near_edge(

                bbox,

                frame_width,

                frame_height,
            )


            object_class = (
                track_data[
                    "object_class"
                ]
            )

            track_id = (
                track_data[
                    "track_id"
                ]
            )


            # =====================================
            # EXIT EVENT
            # =====================================

            events.append(
                self.build_event(

                    event_type="exited",

                    entity_id=entity_id,

                    track_data=track_data,

                    start_timestamp=(
                        track_data[
                            "last_seen"
                        ]
                    ),

                    end_timestamp=timestamp,

                    description=(
                        f"{object_class.capitalize()} "
                        f"#{track_id} left "
                        f"the monitored scene."
                    ),

                    metadata={

                        "last_seen":
                            track_data[
                                "last_seen"
                            ],

                        "missing_duration":
                            missing_duration,

                        "near_frame_edge":
                            near_edge,

                        "exit_reason": (
                            "disappeared_near_edge"
                            if near_edge
                            else
                            "tracking_lost"
                        ),
                    },
                )
            )

            exited_entities.append(
                entity_id
            )


        # =========================================
        # 3. REMOVE EXITED TRACKS
        # =========================================

        for entity_id in exited_entities:

            del self.active_tracks[
                entity_id
            ]


        return events