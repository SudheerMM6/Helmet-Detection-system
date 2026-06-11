
import os
import sys
import tempfile
from functools import lru_cache


def get_confidence_threshold():
    return float(os.getenv("DETECTION_CONFIDENCE", "0.92"))


def get_model_path():
    return os.getenv("MODEL_PATH", "best_motorcycle_final.pt")


def validate_model_path(model_path):
    if not model_path:
        raise ValueError("MODEL_PATH cannot be empty")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")

    return model_path


@lru_cache(maxsize=1)
def load_model(model_path):
    import torch

    return torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)


def run_smoke_test():
    threshold = get_confidence_threshold()
    if not 0 <= threshold <= 1:
        raise ValueError("DETECTION_CONFIDENCE must be between 0 and 1")

    model_path = get_model_path()
    if not model_path:
        raise ValueError("MODEL_PATH cannot be empty")

    print("Smoke test passed: configuration helpers load without the YOLO model.")


def main():
    import cv2
    import streamlit as st

    confidence_threshold = get_confidence_threshold()
    model_path = get_model_path()

    st.title("Helmet Violation Detection")
    st.sidebar.title("Options")

    try:
        validate_model_path(model_path)
        model = load_model(model_path)
    except Exception as exc:
        st.error(f"Could not load the detection model: {exc}")
        st.stop()

    # Upload video file
    video_file = st.sidebar.file_uploader("Upload a video file", type=["mp4", "avi"])

    if video_file is not None:
        # Save the uploaded video file
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(video_file.read())
        temp_file.close()

        # Open the temporary video file
        video_cap = cv2.VideoCapture(temp_file.name)

        # Create a placeholder to display the video
        video_placeholder = st.empty()

        # Create a new folder to store the extracted frames
        output_folder = "helmet_data"
        os.makedirs(output_folder, exist_ok=True)
        temp_output_folder = "temp_helmet_data"
        os.makedirs(temp_output_folder, exist_ok=True)

        extracted_frames = os.listdir(output_folder)
        extracted_frames.sort()

        temp_extracted_frames = os.listdir(temp_output_folder)
        temp_extracted_frames.sort()

        for frame_name in temp_extracted_frames:
            frame_path = os.path.join(temp_output_folder, frame_name)
            os.remove(frame_path)

        for frame_name in extracted_frames:
            frame_path = os.path.join(output_folder, frame_name)
            os.remove(frame_path)

        frame_count = 0

        while True:
            # Read a frame from the video
            ret, frame = video_cap.read()

            if not ret:
                break

            frame_count += 1

            # Perform motorcycle detection
            results = model(frame)

            # Get the predicted bounding boxes and confidence scores
            boxes = results.xyxy[0]
            confidence = boxes[:, 4]
            class_ids = boxes[:, 5].int()

            # Iterate over the detected objects and save frames with motorcycles
            for box, conf, class_id in zip(boxes, confidence, class_ids):
                if class_id == 0 and conf > confidence_threshold:
                    xmin, ymin, xmax, ymax = box[:4].int()
                    output_filename = f"frame_{frame_count}_motorcycle.jpg"

                    output_path = os.path.join(output_folder, output_filename)
                    cv2.imwrite(output_path, frame[ymin:ymax, xmin:xmax])

                    output_path = os.path.join(temp_output_folder, output_filename)
                    cv2.imwrite(output_path, frame[ymin:ymax, xmin:xmax])

                    print(f"Frame {frame_count} saved")

                    extracted_frames = os.listdir(output_folder)
                    extracted_frames.sort()

                    temp_extracted_frames = os.listdir(temp_output_folder)
                    temp_extracted_frames.sort()

                    for frame_name in temp_extracted_frames:
                        frame_path = os.path.join(output_folder, frame_name)
                        frame = cv2.imread(frame_path)
                        st.image(frame, channels="BGR", caption=frame_name)

                    for frame_name in temp_extracted_frames:
                        frame_path = os.path.join(temp_output_folder, frame_name)
                        os.remove(frame_path)

            # Display the frame on the interface
            video_placeholder.image(frame, channels="BGR")

            # Delay between frames to match the video's frame rate
            fps = video_cap.get(cv2.CAP_PROP_FPS)
            delay = int(100 / fps)

            # Wait for the next frame
            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break

        # Remove the temporary video file
        os.remove(temp_file.name)

        # Display the extracted frames on the interface
        # st.header("Extracted Frames")

    else:
        st.info("Please upload a video file.")


if __name__ == "__main__":
    if "--smoke-test" in sys.argv:
        run_smoke_test()
    else:
        main()
