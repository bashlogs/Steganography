import streamlit as st

# Import steganography functions (from separate file or within app.py)
from Steganography1 import (
    encode_txt_data,
    decode_txt_data,
    encode_aud_data,
    decode_aud_data,
    encode_vid_data,
    decode_vid_data,
    encode_img_data,
    decode_img_data
)

global a
a = None
# Title and Introduction
st.title("Steganography App")
st.write("A user-friendly tool for encoding and decoding secret messages.")

# Sidebar for Mode Selection
selected_mode = st.sidebar.selectbox("Select Mode", ("Text Encoding/Decoding", "Audio Encoding", "Video Encoding", "Image Encoding"))

# Text Encoding/Decoding Functionality
if selected_mode == "Text Encoding/Decoding":
    st.header("Text Steganography")

    # Encoding Section
    st.subheader("Encode Text Data")
    cover_text_file_encode = st.file_uploader("Upload Cover Text File (TXT)", type="txt")
    data_to_encode = st.text_input("Enter Data to Encode")
    encode_submit_button = st.button("Encode Data")

    # Decoding Section
    st.subheader("Decode Stego Text")
    decode_stego_file = st.file_uploader("Upload Stego File to Decode (TXT)", type="txt")
    decode_submit_button = st.button("Decode Data")

    if encode_submit_button and cover_text_file_encode is not None and data_to_encode:
        encode_txt_data(cover_text_file_encode.name, data_to_encode)
        st.success("Data successfully encoded in the new_file.txt!")

    if decode_submit_button and decode_stego_file is not None:
        decoded_message = decode_txt_data(decode_stego_file.name)  # Call your function
        if decoded_message:
            st.write("Decoded Message:", decoded_message)
        else:
            st.warning("No message found in the stego file.")


# Implement placeholders for Audio, Video, and Image Encoding Functionality (similar to Text)
elif selected_mode == "Audio Encoding":
    st.header("Audio Steganography")
    st.subheader("Encode Audio Data")
    cover_audio_file_encode = st.file_uploader("Upload Cover Audio File (WAV, MP3, etc.)", type=["wav", "mp3"])
    data_to_encode_audio = st.text_input("Enter Data to Encode")
    encode_submit_button_audio = st.button("Encode Data")

    # Decoding Section
    st.subheader("Decode Audio Data")
    st.info("To decode, upload the audio file with hidden data.")
    decode_audio_file = st.file_uploader("Upload Stego Audio File to Decode", type=["wav", "mp3"])
    decode_submit_button_audio = st.button("Decode Data")

    if encode_submit_button_audio and cover_audio_file_encode is not None and data_to_encode_audio:
        # Call your encode audio function here
        encode_aud_data(cover_audio_file_encode.name, data_to_encode_audio)
        st.success("Data successfully encoded in the audio file!")

    if decode_submit_button_audio and decode_audio_file is not None:
        # Call your decode audio function here
        decoded_message_audio = decode_aud_data(decode_audio_file.name)
        st.write("Decoded Message:", decoded_message_audio)

elif selected_mode == "Video Encoding":
    
    st.header("Video Steganography")
    # Encoding Section
    st.subheader("Encode Video Data")
    cover_video_file_encode = st.file_uploader("Upload Cover Video File (MP4, AVI, etc.)", type=["mp4", "avi"])
    frame_number_encode = st.number_input("Enter Frame Number to Encode", min_value=1)
    data_to_encode_video = st.text_input("Enter Data to Encode")
    encode_key = st.text_input("Enter the key to encrypt: ")
    encode_submit_button_video = st.button("Encode Data")

    # Decoding Section
    st.subheader("Decode Video Data")
    st.info("To decode, upload the video file with hidden data.")
    decode_video_file = st.file_uploader("Upload Stego Video File to Decode", type=["mp4", "avi"])
    frame_number_decode = st.number_input("Enter Frame Number to Decode", min_value=1)
    decode_key = st.text_input("Enter the key to decrypt: ")
    decode_submit_button_video = st.button("Decode Data")
    
    a = encode_vid_data(cover_video_file_encode.name, frame_number_encode, data_to_encode_video, encode_key)
    st.success("Data successfully encoded in the video file!")

    
    if decode_submit_button_video and decode_video_file is not None:
        print(decode_submit_button_video)
        print(decode_video_file)
        print("Inside decode")
        print(a)
        if a is not None:
            decoded_message_video = decode_vid_data(a, frame_number_decode, decode_video_file.name, decode_key)
            st.write("Decoded Message:", decoded_message_video)
        else:
            st.error("No data to decode. Please encode data first.")

    


elif selected_mode == "Image Encoding":
    st.header("Image Steganography")

    # Encoding Section
    st.subheader("Encode Image Data")
    cover_image_file_encode = st.file_uploader("Upload Cover Image File", type=["jpg", "jpeg", "png"])
    data_to_encode_image = st.text_input("Enter Data to Encode")
    encode_submit_button_image = st.button("Encode Data")

    # Decoding Section
    st.subheader("Decode Image Data")
    st.info("To decode, upload the image file with hidden data.")
    decode_image_file = st.file_uploader("Upload Stego Image File to Decode", type=["jpg", "jpeg", "png"])
    decode_submit_button_image = st.button("Decode Data")

    if encode_submit_button_image and cover_image_file_encode is not None and data_to_encode_image:
        # Call your encode image function here
        encode_img_data(cover_image_file_encode.name, data_to_encode_image)
        st.success("Data successfully encoded in the image file!")

    if decode_submit_button_image and decode_image_file is not None:
        # Call your decode image function here
        decoded_message_image = decode_img_data(decode_image_file.name)
        st.write("Decoded Message:", decoded_message_image)


else:
    st.warning("Invalid mode selection. Please choose a valid option.")
