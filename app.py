import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Football Media Bot", page_icon="⚽")

st.title("⚽ Match Day Video Stitcher")
st.info("Upload the interview. We'll attach the 1080p Intro & Outro automatically.")

# Static filenames
INTRO_FILE = "intro.mp4"
OUTRO_FILE = "outro.mp4"
TEMP_INTERVIEW = "temp_interview.mp4"
FINAL_OUTPUT = "final_match_video.mp4"
LIST_FILE = "inputs.txt"

# Check if branding files exist in the repo
if not os.path.exists(INTRO_FILE) or not os.path.exists(OUTRO_FILE):
    st.error("⚠️ Error: 'intro.mp4' or 'outro.mp4' not found in repository.")
else:
    uploaded_file = st.file_uploader("Choose Interview Clip", type=["mp4"])

    if uploaded_file:
        # Save upload to disk
        with open(TEMP_INTERVIEW, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        if st.button("🚀 Generate Final Video"):
            with st.spinner("Stitching 1080p streams..."):
                
                # Create the manifest for FFmpeg
                with open(LIST_FILE, "w") as f:
                    f.write(f"file '{INTRO_FILE}'\n")
                    f.write(f"file '{TEMP_INTERVIEW}'\n")
                    f.write(f"file '{OUTRO_FILE}'\n")

                # The 'Concat Demuxer' command - fast and lossless
                cmd = [
                    "ffmpeg", "-y", "-f", "concat", "-safe", "0",
                    "-i", LIST_FILE, "-c", "copy", FINAL_OUTPUT
                ]

                process = subprocess.run(cmd, capture_output=True, text=True)

                if process.returncode == 0:
                    st.success("Video ready for download!")
                    with open(FINAL_OUTPUT, "rb") as vid:
                        st.download_button(
                            label="⬇️ Download Edited Video",
                            data=vid,
                            file_name="team_edit_1080p.mp4",
                            mime="video/mp4"
                        )
                else:
                    st.error("Processing failed.")
                    st.code(process.stderr)
                
                # Cleanup temporary files
                if os.path.exists(TEMP_INTERVIEW): os.remove(TEMP_INTERVIEW)
                if os.path.exists(LIST_FILE): os.remove(LIST_FILE)
