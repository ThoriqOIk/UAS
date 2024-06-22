import streamlit as st
import os
from pydub import AudioSegment
from PIL import Image
from moviepy.editor import VideoFileClip
import io

# Function to compress audio
def compress_audio(input_file, bitrate='64k', lossless=False):
    audio = AudioSegment.from_file(input_file)
    compressed_audio = audio.set_frame_rate(48000).set_channels(1)
    output_buffer = io.BytesIO()
    
    if lossless:
        compressed_audio.export(output_buffer, format='opus', codec='libopus')
    else:
        compressed_audio.export(output_buffer, format='mp3', bitrate=bitrate)
    
    return output_buffer.getvalue()

# Function to compress image
def compress_image(input_file, quality=50, lossless=False):
    img = Image.open(input_file)
    output_buffer = io.BytesIO()
    img_format = input_file.name.split(".")[-1].lower()
    
    if lossless:
        img.save(output_buffer, format='WebP', lossless=True)
    else:
        if img_format not in ["jpg", "jpeg"]:
            st.warning("Only JPEG format is supported for lossy compression. Converting the image to JPEG...")
            img = img.convert("RGB")
        img.save(output_buffer, format='JPEG', quality=quality)
    
    return output_buffer.getvalue()

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

# Define page for audio compression
def audio_compression():
    st.title("Audio Compression")
    
    # Sidebar
    st.sidebar.title("Settings")
    compression_type = st.sidebar.radio("Compression Type", ["Lossy", "Lossless"])
    
    if compression_type == "Lossy":
        audio_bitrate = st.sidebar.selectbox("Select audio bitrate", ["64k", "128k", "192k", "256k", "320k"])
    else:
        audio_bitrate = None
    
    # Main content
    st.write("""
    ## Upload your audio file and compress it!
    """)
    
    # File upload - audio
    audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "flac", "ogg"])
    
    if audio_file is not None:
        st.audio(audio_file, format='audio/mp3', start_time=0)
        st.write("Uploaded Audio File Details:")
        audio_details = {"Filename": audio_file.name, "FileType": audio_file.type, "FileSize": audio_file.size}
        st.write(audio_details)
        
        # Compress audio button
        if st.button("Compress Audio"):
            st.write("Compressing audio...")
            compressed_audio = compress_audio(audio_file, bitrate=audio_bitrate, lossless=(compression_type == "Lossless"))
            st.success("Audio compression successful!")
            
            # Download button for compressed audio
            st.write("### Download Compressed Audio")
            audio_download_button_str = f"Download Compressed Audio File ({os.path.splitext(audio_file.name)[0]}_compressed.{('opus' if compression_type == 'Lossless' else 'mp3')})"
            st.download_button(label=audio_download_button_str, data=compressed_audio, file_name=f"{os.path.splitext(audio_file.name)[0]}_compressed.{('opus' if compression_type == 'Lossless' else 'mp3')}", mime="audio/opus" if compression_type == "Lossless" else "audio/mpeg")

# Define page for image compression
def image_compression():
    st.title("Image Compression")
    
    # Sidebar
    st.sidebar.title("Settings")
    compression_type = st.sidebar.radio("Compression Type", ["Lossy", "Lossless"])
    
    if compression_type == "Lossy":
        image_quality = st.sidebar.slider("Select image quality", min_value=1, max_value=100, value=50)
    else:
        image_quality = None
    
    # Main content
    st.write("""
    ## Upload your image file and compress it!
    """)
    
    # File upload - image
    image_file = st.file_uploader("Upload an image file", type=["jpg", "jpeg", "png"])
    
    if image_file is not None:
        st.image(image_file, caption="Uploaded Image", use_column_width=True)
        st.write("Uploaded Image File Details:")
        image_details = {"Filename": image_file.name, "FileType": image_file.type, "FileSize": image_file.size}
        st.write(image_details)
        
        # Compress image button
        if st.button("Compress Image"):
            st.write("Compressing image...")
            compressed_image = compress_image(image_file, quality=image_quality, lossless=(compression_type == "Lossless"))
            st.success("Image compression successful!")
            
            # Download button for compressed image
            st.write("### Download Compressed Image")
            image_download_button_str = f"Download Compressed Image File"
            st.download_button(label=image_download_button_str, data=compressed_image, file_name=f"{os.path.splitext(image_file.name)[0]}_compressed.{('webp' if compression_type == 'Lossless' else 'jpg')}", mime="image/webp" if compression_type == "Lossless" else "image/jpeg")

# Define page for video compression
def video_compression():
    st.title("Video Compression")
    
    # Sidebar
    st.sidebar.title("Settings")
    compression_type = st.sidebar.radio("Compression Type", ["Lossy", "Lossless"])
    
    if compression_type == "Lossy":
        video_bitrate = st.sidebar.selectbox("Select video bitrate", ["500k", "1000k", "1500k", "2000k", "2500k"])
    else:
        video_bitrate = None
    
    # Main content
    st.write("""
    ## Upload your video file and compress it!
    """)
    
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
            compressed_video = compress_video(video_file, bitrate=video_bitrate, lossless=(compression_type == "Lossless"))
            st.success("Video compression successful!")
            
            # Download button for compressed video
            st.write("### Download Compressed Video")
            video_download_button_str = f"Download Compressed Video File ({os.path.splitext(video_file.name)[0]}_compressed.mp4)"
            st.download_button(label=video_download_button_str, data=compressed_video, file_name=f"{os.path.splitext(video_file.name)[0]}_compressed.mp4", mime="video/mp4")

# Multipage function
def multipage():
    pages = {
        "Audio Compression": audio_compression,
        "Image Compression": image_compression,
        "Video Compression": video_compression
    }
    
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    
    page = pages[selection]
    page()

# Run the app
if __name__ == '__main__':
    multipage()
