import streamlit as st
import requests
from PIL import Image
import io

UPLOAD_URL = "http://localhost:8000/api/upload/dermato/"
REPORT_URL = "http://localhost:8000/api/report/dermato/"

CATEGORIES = {
    "Total Body Mapping": "total_body",
    "Head & Neck": "head_neck",
    "Torso": "torso",
    "Upper Extremities": "upper_ext",
    "Lower Extremities": "lower_ext",
    "Global View": "global",
    "Regional View": "regional",
    "Close-up Dermoscopy": "closeup"
}

st.title("Medscope Image Uploader & Report Generator")
tab1, tab2 = st.tabs(["Upload Images", "Generate Report"])

with tab1:
    st.subheader("Upload Dermatoscopic Images")

    category_label = st.selectbox("Select Category", list(CATEGORIES.keys()))
    uploaded_files = st.file_uploader("Choose image files", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

    if uploaded_files:
        st.markdown("### Image Preview")
        for f in uploaded_files:
            img = Image.open(f)
            st.image(img, caption=f.name, width=200)

    if st.button("Upload"):
        if uploaded_files:
            for f in uploaded_files:
                f.seek(0)
            files = [("images", (f.name, f, "image/jpeg")) for f in uploaded_files]
            data = {"category": CATEGORIES[category_label]}

            with st.spinner("Uploading..."):
                res = requests.post(UPLOAD_URL, files=files, data=data)

            if res.status_code == 201:
                st.success("Images uploaded successfully!")
                st.json(res.json())
            else:
                st.error(f"Upload failed: {res.status_code}")
        else:
            st.warning("Please select images to upload.")

with tab2:
    st.subheader("Generate Diagnostic PDF Report")

    if st.button("Generate & Download Report"):
        with st.spinner("Generating report..."):
            res = requests.get(REPORT_URL)

        if res.status_code == 200:
            st.success("Report generated successfully!")
            st.download_button(
                label="Download Report",
                data=res.content,
                file_name="its_ya_boi.pdf",
                mime="application/pdf"
            )
        else:
            st.error("Failed to generate report. Make sure images are uploaded.")
