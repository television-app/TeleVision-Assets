import os
import sys
from PIL import Image

# Configuration
LOGOS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX_SIZE_KB = 60
MAX_SIZE_BYTES = MAX_SIZE_KB * 1024

def get_file_size(file_path):
    return os.path.getsize(file_path)

def optimize_image(file_path):
    try:
        file_size = get_file_size(file_path)
        if file_size <= MAX_SIZE_BYTES:
            return False

        print(f"Optimizing {os.path.basename(file_path)} ({file_size / 1024:.2f} KB)...")
        
        img = Image.open(file_path)
        img_format = img.format
        
        # If it's not a common image format, verify
        if img_format not in ['PNG', 'JPEG', 'JPG']:
            return False

        # Attempt to optimize without resizing first
        temp_path = file_path + ".temp"
        
        # Quality reduction loop (mostly for JPEGs, but resize for PNGs)
        # For PNGs, we can't really change "quality" in same way, so we rely on resize
        # For JPEGs, we can lower quality.
        
        quality = 90
        scale = 1.0
        
        while True:
            # Resize if scale < 1.0
            if scale < 1.0:
                 new_width = int(img.width * scale)
                 new_height = int(img.height * scale)
                 # Use LANCZOS for best quality resizing
                 resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            else:
                resized_img = img

            # Save to temp
            if img_format == 'PNG':
                # PNG optimization
                resized_img.save(temp_path, format='PNG', optimize=True)
            else:
                # JPEG optimization
                resized_img.save(temp_path, format='JPEG', quality=quality, optimize=True)

            # Check size
            new_size = get_file_size(temp_path)
            
            if new_size <= MAX_SIZE_BYTES:
                print(f"  -> Reduced to {new_size / 1024:.2f} KB")
                break
            
            # Adjust parameters for next iteration
            if img_format == 'JPEG':
                if quality > 30:
                    quality -= 10
                else:
                    scale *= 0.9 # Start resizing if quality is too low
            else:
                # For PNG, just reduce size immediately as quality param doesn't exist/work same way
                scale *= 0.9
            
            if scale < 0.1:
                print(f"  -> Could not optimize {os.path.basename(file_path)} within reasonable limits.")
                os.remove(temp_path)
                return False

        # Replace original
        os.replace(temp_path, file_path)
        return True

    except Exception as e:
        print(f"Error optimizing {file_path}: {e}")
        if os.path.exists(file_path + ".temp"):
            os.remove(file_path + ".temp")
        return False

def main():
    if not os.path.exists(LOGOS_DIR):
        print(f"Directory not found: {LOGOS_DIR}")
        sys.exit(1)

    print(f"Scanning {LOGOS_DIR} for images > {MAX_SIZE_KB}KB...")
    
    optimized_count = 0
    extensions = ('.png', '.jpg', '.jpeg')
    
    for filename in os.listdir(LOGOS_DIR):
        if filename.lower().endswith(extensions):
            file_path = os.path.join(LOGOS_DIR, filename)
            if optimize_image(file_path):
                optimized_count += 1
                
    print(f"Done. Optimized {optimized_count} images.")

if __name__ == "__main__":
    main()
