import os
from PIL import Image, ImageEnhance, ImageFilter

def convert_to_max_color_16x16(input_file, output_profile):
    if not os.path.exists(input_file):
        print(f"Error: The file '{input_file}' was not found.")
        return

    # 1. Open the image and convert it to RGB mode
    img = Image.open(input_file)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # 2. Automatically center-crop the image into a square
    width, height = img.size
    min_dim = min(width, height)
    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    img = img.crop((left, top, left + min_dim, top + min_dim))
    
    # 3. Boost color, contrast, and sharpness for vivid details at 16x16
    img = ImageEnhance.Color(img).enhance(1.4)
    img = ImageEnhance.Contrast(img).enhance(1.3)
    img = img.filter(ImageFilter.DETAIL)
    img = ImageEnhance.Sharpness(img).enhance(2.5)
    
    # 4. Resize down to 16x16 pixels without limiting the color palette
    img_small = img.resize((16, 16), resample=Image.Resampling.BICUBIC)
    
    # 5. Upscale back to 512x512 with crisp, sharp pixel blocks
    final_preview = img_small.resize((512, 512), resample=Image.Resampling.NEAREST)
    final_preview.save(output_profile)
    
    # Count unique colors using get_flattened_data() to avoid deprecation warnings
    unique_colors = len(set(img_small.get_flattened_data()))
    print(f"Done! Saved as: {output_profile} (Contains {unique_colors} unique colors at 16x16!)")

if __name__ == "__main__":
    input_file = "my_picture.png" 
    output_profile = "wplace_max_color_16x16.png"
    
    print("Calculating maximum color depth at 16x16...")
    convert_to_max_color_16x16(input_file, output_profile)
