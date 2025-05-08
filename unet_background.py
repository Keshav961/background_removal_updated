import streamlit as st
from rembg import remove
from PIL import Image, ImageOps
import io
import zipfile
import os

st.title("🧼 U²-Net Background Remover for Car Parts")
st.markdown("Upload multiple images. Background will be removed using **U²-Net**, and replaced with **white background**.")

uploaded_files = st.file_uploader("Upload Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

def transparent_to_white(pil_img):
    if pil_img.mode in ("RGBA", "LA"):
        bg = Image.new("RGB", pil_img.size, (255, 255, 255))
        bg.paste(pil_img, mask=pil_img.split()[3])
        return bg
    return pil_img.convert("RGB")

if uploaded_files:
    zip_buffer = io.BytesIO()
    zip_file = zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED)

    st.subheader("🖼️ Preview (First 3 Only)")
    
    for idx, file in enumerate(uploaded_files):
        original = Image.open(file).convert("RGBA")
        removed = remove(original)
        white_bg = transparent_to_white(removed)

        # Save all to zip
        buffer = io.BytesIO()
        white_bg.save(buffer, format="JPEG", quality=95)
        out_filename = file.name.replace(".png", "_white.jpg").replace(".jpeg", "_white.jpg").replace(".jpg", "_white.jpg")
        zip_file.writestr(out_filename, buffer.getvalue())

        # Show preview for first 3 only
        if idx < 3:
            st.markdown(f"**{file.name}**")
            col1, col2 = st.columns(2)
            col1.image(original, caption="Original", use_container_width=True)
            col2.image(white_bg, caption="White Background", use_container_width=True)

            st.download_button(
                label=f"📥 Download {file.name}",
                data=buffer.getvalue(),
                file_name=out_filename,
                mime="image/jpeg"
            )

    zip_file.close()

    st.success(f"✅ Processed {len(uploaded_files)} images.")
    st.download_button(
        label="📦 Download All as ZIP",
        data=zip_buffer.getvalue(),
        file_name="white_background_parts.zip",
        mime="application/zip"
    )
