import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# ===== Page Setup =====
st.set_page_config(page_title="Certificate Generator", page_icon="🎓", layout="wide")

st.title("🎓 Generate Your Certificate Instantly")
st.write("Enter your name below and download your personalized certificate as a PDF.")

# ===== Admin Section (for you to upload the template) =====
with st.sidebar:
    st.header("⚙️ Admin Settings")
    st.write("Upload your certificate template and set text properties.")
    template_file = st.file_uploader("Upload Certificate Template (JPG/PNG)", type=["jpg", "jpeg", "png"])
    font_size = st.slider("Font Size", 20, 200, 60)
    font_color = st.color_picker("Font Color", "#000000")
    x_pos = st.number_input("X Position", 0, 5000, 850)
    y_pos = st.number_input("Y Position", 0, 5000, 650)
    font_file = st.file_uploader("Upload Font (.ttf)", type=["ttf"])
    st.markdown("---")
    st.write("👨‍💻 Developed by **Tanvir Even**")

# ===== User Section =====
if template_file:
    # Load certificate template
    template = Image.open(template_file)

    st.subheader("✏️ Enter Your Name")
    user_name = st.text_input("Full Name")

    if user_name:
        # Load font
        if font_file:
            font = ImageFont.truetype(font_file, font_size)
        else:
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()

        # Make a copy of template
        cert = template.copy()
        draw = ImageDraw.Draw(cert)

        # Draw the name
        draw.text((x_pos, y_pos), user_name, font=font, fill=font_color)

        # Show preview
        st.image(cert, caption=f"Preview for {user_name}", use_container_width=True)

        # Save as PDF in memory
        pdf_bytes = io.BytesIO()
        cert_rgb = cert.convert("RGB")
        cert_rgb.save(pdf_bytes, format="PDF")
        pdf_bytes.seek(0)

        # Download button
        st.download_button(
            label="📥 Download Certificate (PDF)",
            data=pdf_bytes,
            file_name=f"{user_name}_certificate.pdf",
            mime="application/pdf"
        )
else:
    st.warning("Please upload a certificate template from the sidebar.")
