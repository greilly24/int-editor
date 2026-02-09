import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Football Media Bot", page_icon="⚽")

st.title("⚽ Match Day Video Stitcher")
st.info("Stitching Intro + Interview + Outro (1080p Optimized)")

INTRO_FILE = "intro.mp4"
OUTRO_FILE = "outro.mp4"
TEMP_INTERVIEW = "temp_interview.mp4"
FINAL_OUTPUT = "final_match_video.mp4"

if not os.path.exists(INTRO_FILE) or not os.path.exists(OUTRO_FILE):
    st.error("⚠️ Branding files (intro/outro) missing from GitHub!")
else:
    uploaded_file = st.file_uploader("Upload Interview Clip", type=["mp4"])

    if uploaded_file:
        with open(TEMP_INTERVIEW, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        if st.button("🚀 Generate Final Video"):
            with st.spinner("Processing... usually takes 30-60 seconds."):
                
                # This command re-syncs all timestamps to fix the '35 hour' bug
                cmd = [
                    "ffmpeg", "-y",
                    "-i", INTRO_FILE,
                    "-i", TEMP_INTERVIEW,
                    "-i", OUTRO_FILE,
                    "-filter_complex", "[0:v][0:a][1:v][1:a][2:v][2:a]concat=n=3:v=1:a=1[v][a]",
                    "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", 
                    "-preset", "ultrafast",  # This is the fastest possible setting
                    "-crf", "23",            # Maintains high visual quality
                    "-pix_fmt", "yuv420p", 
                    FINAL_OUTPUT
                ]

                process = subprocess.run(cmd, capture_output=True, text=True)

                if process.returncode == 0:
                    st.success("✅ Done!")
                    with open(FINAL_OUTPUT, "rb") as vid:
                        st.download_button(
                            label="⬇️ Download Edited Video",
                            data=vid,
                            file_name="team_edit_fixed.mp4",
                            mime="video/mp4"
                        )
                else:
                    st.error("Error during processing.")
                    st.code(process.stderr)
