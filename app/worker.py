from app.celery_app import celery_app

from app.database import SessionLocal

from app.models.schema import (
    VideoRecord,
    EventRecord,
)

from app.pipeline.frame_sampler import (
    FrameSampler,
)

from app.cv.perception import (
    VideoPerception,
)

from app.pipeline.event_engine import (
    EventEngine,
)

from app.cv.attribute_extractor import (
    AttributeExtractor,
)

from app.ai.llm_service import (
    LLMService,
)
from app.ai.scene_understanding import (
    SceneUnderstanding,
)
from app.ai.event_indexer import EventIndexer
@celery_app.task(
    bind=True,
    name="app.worker.process_video_task",
)
def process_video_task(
    self,
    video_id: str,
    video_path: str,
):

    db = SessionLocal()

    video = None

    try:

        # ========================================
        # FETCH VIDEO
        # ========================================

        video = (
            db.query(VideoRecord)
            .filter(
                VideoRecord.id == video_id
            )
            .first()
        )

        if not video:

            return {
                "status": "failed",
                "reason":
                    "Video record not found",
            }


        # ========================================
        # UPDATE STATUS
        # ========================================

        video.status = "PROCESSING"

        db.commit()


        print("=" * 70)
        print("SENTINELAI AI PIPELINE STARTED")
        print(f"Video: {video.filename}")
        print(f"Video ID: {video_id}")
        print("=" * 70)


        # ========================================
        # INITIALIZE PIPELINE
        # ========================================

        sampler = FrameSampler(
            target_fps=2.0
        )

        perception = VideoPerception(
            model_name="yolo26n.pt",
            confidence_threshold=0.35,
        )

        attribute_extractor = (
            AttributeExtractor()
        )

        event_engine = EventEngine(
            exit_threshold=4.0,
            movement_threshold=8.0,
            stop_threshold=2.0,
        )
        scene_understanding = SceneUnderstanding()

        sampled_frames = 0
        detected_objects = 0
        generated_events = 0

        scene_detections = []


        # ========================================
        # SAVE EVENT HELPER
        # ========================================

        def save_event(event):

            nonlocal generated_events

            record = EventRecord(

                video_id=video_id,

                start_timestamp=(
                    event[
                        "start_timestamp"
                    ]
                ),

                end_timestamp=(
                    event[
                        "end_timestamp"
                    ]
                ),

                event_type=(
                    event[
                        "event_type"
                    ]
                ),

                entity_id=(
                    event[
                        "entity_id"
                    ]
                ),

                object_class=(
                    event[
                        "object_class"
                    ]
                ),

                confidence=(
                    event[
                        "confidence"
                    ]
                ),

                anomaly_score=None,

                description=(
                    event[
                        "description"
                    ]
                ),

                metadata_json=(
                    event[
                        "metadata"
                    ]
                ),

                embedding=None,
            )

            db.add(record)

            generated_events += 1


        # ========================================
        # PROCESS VIDEO
        # ========================================

        for sample in sampler.sample(
            video_path
        ):

            timestamp = (
                sample["timestamp"]
            )

            frame = (
                sample["frame"]
            )

            change_score = (
                sample["change_score"]
            )

            sampled_frames += 1


            print(
                f"[{timestamp:.2f}s] "
                f"Change Score: "
                f"{change_score:.6f}"
            )


            # ====================================
            # ADAPTIVE COMPUTE
            # ====================================

            CHANGE_THRESHOLD = 0.015


            # ------------------------------------
            # LOW CHANGE
            # ------------------------------------

            if (
                change_score
                < CHANGE_THRESHOLD
            ):

                print(
                    f"[{timestamp:.2f}s] "
                    "Low change → skipping YOLO"
                )

                skipped_events = (
                    event_engine.update_time(
                        timestamp
                    )
                )

                for event in skipped_events:

                    print(
                        f"[{timestamp:.2f}s] "
                        f"EVENT → "
                        f"{event['description']}"
                    )

                    save_event(event)

                continue


            # ------------------------------------
            # MEANINGFUL CHANGE
            # ------------------------------------

            print(
                f"[{timestamp:.2f}s] "
                "Meaningful change → running YOLO"
            )


            # ====================================
            # YOLO + BYTE TRACK
            # ====================================

            detections = (
                perception.track_frame(
                    frame
                )
            )


            # ====================================
            # ATTRIBUTE EXTRACTION
            # ====================================

            for detection in detections:
            
                # ====================================
                # EXTRACT OBJECT ATTRIBUTES
                # ====================================
                attributes = (
                    attribute_extractor.extract(
                        frame=frame,
                        detection=detection,
                    )
                )
            
                detection["attributes"] = attributes
            
                # ====================================
                # COLLECT SCENE INFORMATION
                # ====================================
                scene_detections.append({
                    "class_name": detection.get(
                        "class_name",
                        "unknown"
                    ),
            
                    "track_id": detection.get(
                        "track_id"
                    ),
            
                    "attributes": detection.get(
                        "attributes",
                        {}
                    ),
                })
            
            
            detected_objects += len(detections)


            print(
                f"[{timestamp:.2f}s] "
                f"Detected "
                f"{len(detections)} "
                f"tracked objects"
            )


            # ====================================
            # EVENT ENGINE
            # ====================================

            height, width = frame.shape[:2]

            events = (
                event_engine.process(

                    timestamp=timestamp,

                    detections=detections,

                    frame_width=width,

                    frame_height=height,
                )
            )


            # ====================================
            # SAVE EVENTS
            # ====================================

            for event in events:

                print(
                    f"[{timestamp:.2f}s] "
                    f"EVENT → "
                    f"{event['description']}"
                )

                save_event(event)


            # ====================================
            # PERIODIC COMMIT
            # ====================================

            if (
                sampled_frames % 20 == 0
            ):

                db.commit()


        # ========================================
        # FINAL EVENT COMMIT
        # ========================================

        db.commit()


        # ========================================
        # SCENE UNDERSTANDING
        # ========================================
        
        print("=" * 70)
        print("ANALYZING VIDEO SCENE")
        print("=" * 70)
        
        
        scene_info = (
            scene_understanding.analyze_scene(
                detections=scene_detections
            )
        )
        
        
        print(
            "SCENE TYPE:",
            scene_info["scene_type"]
        )
        
        print(
            "SCENE DESCRIPTION:",
            scene_info["scene_description"]
        )
        
        print(
            "OBJECT COUNTS:",
            scene_info["object_counts"]
        )

        all_events = (
            db.query(EventRecord)
           .filter(EventRecord.video_id == video_id)
           .order_by(EventRecord.start_timestamp)
           .all()
        )
        
        # ---------------------------------------------------------
        # GENERATE AI VIDEO SUMMARY
        # ---------------------------------------------------------
        
        llm_service = LLMService()
        
        summary = llm_service.summarize_events(
           video_duration=video.duration,
           events=all_events
        )
        
        video.summary = summary
        
        # ---------------------------------------------------------
        # INDEX EVENTS FOR VIDEO RAG / Q&A
        # ---------------------------------------------------------
        
        print("=" * 70)
        print("INDEXING EVENTS FOR VIDEO Q&A")
        print("=" * 70)
        
        indexer = EventIndexer()
        
        index_result = indexer.index_video(video_id)
        
        print("EVENT INDEXING COMPLETED:")
        print(index_result)
        
        # ---------------------------------------------------------
        # MARK VIDEO AS COMPLETED
        # ---------------------------------------------------------
        
        video.status = "COMPLETED"
        db.commit()


        print("=" * 70)
        print(
            "SENTINELAI AI PIPELINE COMPLETED"
        )

        print(
            f"Sampled Frames: "
            f"{sampled_frames}"
        )

        print(
            f"Tracked Detections: "
            f"{detected_objects}"
        )

        print(
            f"Generated Events: "
            f"{generated_events}"
        )

        print("=" * 70)


        return {

            "status":
                "completed",

            "video_id":
                video_id,

            "sampled_frames":
                sampled_frames,

            "detections":
                detected_objects,

            "events":
                generated_events,

            "indexed_events": index_result["indexed_events"],
            
            "summary":
                summary,
        }


    except Exception as error:

        print(
            "SENTINELAI PIPELINE FAILED:"
        )

        print(error)

        db.rollback()


        if video:

            try:

                video.status = "FAILED"

                db.commit()

            except Exception:

                db.rollback()


        raise


    finally:

        db.close()