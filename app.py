import streamlit as st
import os
from moviepy.editor import VideoFileClip

# Set path FFMPEG
ffmpeg_path = "/path/to/your/ffmpeg"
os.environ["FFMPEG_BINARY"] = ffmpeg_path

# Function to compress video
def compress_video(input_file, bitrate='500k', lossless=False):
    video = VideoFileClip(input_file.name)
    output_buffer = io.BytesIO()
    
    if lossless:
        video.write_videofile(output_buffer, codec='libx264', preset='ultrafast', ffmpeg_params=['-crf', '0'])
    else:
        video.write_videofile(output_buffer, codec='libx264', preset='slow', bitrate=bitrate)
    
    output_buffer.seek(0)
    return output_buffer.read()

# Main application
def main():
    st.title("Video Compression")

    # File upload - video
    video_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov", "mkv"])

    if video_file is not None:
        st.video(video_file)
        st.write("Uploaded Video File Details:")
        video_details = {"Filename": video_file.name, "FileType": video_file.type, "FileSize": video_file.size}
        st.write(video_details)

        # Compress video button
        if st.button("Compress Video"):
            st.write("Compressing video...")
            compressed_video = compress_video(video_file, bitrate='500k', lossless=False)
            st.success("Video compression successful!")

            # Download button for compressed video
            st.write("### Download Compressed Video")
            video_download_button_str = f"Download Compressed Video File ({os.path.splitext(video_file.name)[0]}_compressed.mp4)"
            st.download_button(label=video_download_button_str, data=compressed_video, file_name=f"{os.path.splitext(video_file.name)[0]}_compressed.mp4", mime="video/mp4")

if __name__ == "__main__":
    main()
