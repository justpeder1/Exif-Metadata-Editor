from PIL import Image, ExifTags
from PIL.ExifTags import TAGS, GPSTAGS
import os
import json
import datetime

def get_labeled_exif(exif):
    labeled = {}
    for (key, val) in exif.items():
        # Get the tag name instead of the numeric key
        tag_name = TAGS.get(key, key)
        
        # Process GPS tags separately
        if tag_name == 'GPSInfo':
            labeled[tag_name] = {}
            for gps_key in val:
                sub_tag_name = GPSTAGS.get(gps_key, gps_key)
                labeled[tag_name][sub_tag_name] = val[gps_key]
        else:
            # Convert bytes to string if needed
            if isinstance(val, bytes):
                try:
                    val = val.decode('utf-8')
                except UnicodeDecodeError:
                    val = val.hex()
            
            # Convert tuples to lists for JSON serialization
            if isinstance(val, tuple):
                val = list(val)
                
            labeled[tag_name] = val
    
    return labeled

def get_exif_data(image_path):
    try:
        # Get file stats
        file_stats = os.stat(image_path)
        file_size = file_stats.st_size
        
        # Open the image
        image = Image.open(image_path)
        
        # Get basic image info
        width, height = image.size
        format_type = image.format
        mode = image.mode
        
        # Initialize exif_data with basic image info
        exif_data = {
            'FileSize': file_size,
            'ImageWidth': width,
            'ImageLength': height,  # EXIF uses ImageLength for height
            'Format': format_type,
            'Mode': mode,
            'MIMEType': f'image/{format_type.lower()}' if format_type else 'image/unknown'
        }
        
        # Check if image has EXIF data
        if hasattr(image, '_getexif') and image._getexif():
            exif = image._getexif()
            if exif:
                # Merge labeled EXIF data with basic image info
                labeled_exif = get_labeled_exif(exif)
                exif_data.update(labeled_exif)
                
                # Format date fields if they exist
                for date_field in ['DateTimeOriginal', 'DateTimeDigitized', 'DateTime']:
                    if date_field in exif_data:
                        # Keep the date format as is for now
                        exif_data[date_field] = exif_data[date_field]
                
                # Calculate more accurate dimensions if they exist in EXIF
                if 'PixelXDimension' in exif_data and exif_data['PixelXDimension']:
                    exif_data['ImageWidth'] = exif_data['PixelXDimension']
                if 'PixelYDimension' in exif_data and exif_data['PixelYDimension']:
                    exif_data['ImageLength'] = exif_data['PixelYDimension']
        
        # Handle potential errors with ColorSpace
        if 'ColorSpace' in exif_data:
            if exif_data['ColorSpace'] == 1:
                exif_data['ColorSpace'] = 'sRGB'
            elif exif_data['ColorSpace'] == 2:
                exif_data['ColorSpace'] = 'Adobe RGB'
        
        # Add creation time if available (for Windows files without EXIF)
        if 'DateTime' not in exif_data and hasattr(file_stats, 'st_ctime'):
            creation_time = datetime.datetime.fromtimestamp(file_stats.st_ctime)
            exif_data['DateTime'] = creation_time.strftime('%Y:%m:%d %H:%M:%S')
            
        # If no EXIF message field was added, remove it
        if 'message' in exif_data:
            del exif_data['message']
            
        # Debug log
        print(f"EXIF data extracted from {image_path}: {json.dumps(exif_data, indent=2)}")
            
        return exif_data
    
    except Exception as e:
        print(f"Error extracting EXIF data: {e}")
        return {'error': str(e), 'FileSize': os.path.getsize(image_path) if os.path.exists(image_path) else 0}

def update_exif_data(image_path, updated_exif):
    try:
        # Open the image and get existing EXIF data
        with Image.open(image_path) as img:
            # Check if image format supports EXIF
            if img.format not in ['JPEG', 'TIFF']:
                return False
            
            # Get existing EXIF data
            exif_dict = img._getexif() or {}
            
            # Create a new dictionary with numeric keys for EXIF
            new_exif = {}
            
            # Map from tag names to numeric keys
            tag_to_key = {v: k for k, v in TAGS.items()}
            
            # Apply updates to relevant fields
            for tag_name, value in updated_exif.items():
                if tag_name == 'GPSInfo' and isinstance(value, dict):
                    gps_tag_key = tag_to_key.get('GPSInfo')
                    if gps_tag_key:
                        # Map from GPS tag names to numeric keys
                        gps_to_key = {v: k for k, v in GPSTAGS.items()}
                        gps_data = {}
                        
                        for gps_tag, gps_value in value.items():
                            gps_key = gps_to_key.get(gps_tag)
                            if gps_key:
                                gps_data[gps_key] = gps_value
                        
                        if gps_data:
                            new_exif[gps_tag_key] = gps_data
                else:
                    key = tag_to_key.get(tag_name)
                    if key:
                        new_exif[key] = value
            
            # Save with updated EXIF
            if new_exif:
                # Create new image with updated EXIF (Pillow doesn't allow direct modification)
                output_img = img.copy()
                # Save to a temporary file first
                temp_path = image_path + '.temp'
                output_img.save(temp_path, exif=new_exif)
                
                # Replace original with the temp file
                os.replace(temp_path, image_path)
                
                return True
            
            return False
            
    except Exception as e:
        print(f"Error updating EXIF data: {e}")
        return False 