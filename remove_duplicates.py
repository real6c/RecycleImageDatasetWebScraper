"""
Quick script to check for and remove duplicate images in the original dataset
"""

import hashlib
import argparse
from pathlib import Path
from collections import defaultdict

def get_file_hash(file_path):
    """Calculate MD5 hash of a file"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def main():
    parser = argparse.ArgumentParser(description='Check for and remove duplicate images')
    parser.add_argument('--dataset_dir', type=str, default='../images',
                       help='Directory containing images to check (default: ../images)')
    
    args = parser.parse_args()
    
    # Define path to original images
    images_dir = Path(args.dataset_dir)
    
    if not images_dir.exists():
        print(f"Error: Images directory {images_dir} does not exist")
        return
    
    print(f"Scanning for duplicates in: {images_dir}")
    
    # Find all image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(images_dir.rglob(f'*{ext}'))
        image_files.extend(images_dir.rglob(f'*{ext.upper()}'))
    
    print(f"Found {len(image_files)} image files")
    
    # Calculate hashes and find duplicates
    hash_dict = defaultdict(list)
    
    for i, image_file in enumerate(image_files):
        if i % 100 == 0:
            print(f"Processing {i}/{len(image_files)} files...")
        
        try:
            file_hash = get_file_hash(image_file)
            hash_dict[file_hash].append(str(image_file))
        except Exception as e:
            print(f"Error processing {image_file}: {e}")
    
    # Find duplicates
    duplicates = {hash_val: files for hash_val, files in hash_dict.items() if len(files) > 1}
    
    # Report results
    print(f"\n{'='*50}")
    print("DUPLICATE CHECK RESULTS")
    print(f"{'='*50}")
    
    if duplicates:
        print(f"Found {len(duplicates)} sets of duplicate images:")
        print()
        
        total_duplicates = 0
        files_to_remove = []
        
        for hash_val, files in duplicates.items():
            print(f"Duplicate set {len(files)} files:")
            # Keep the first file, remove the rest
            keep_file = files[0]
            remove_files = files[1:]
            files_to_remove.extend(remove_files)
            
            print(f"  KEEP: {keep_file}")
            for file_path in remove_files:
                print(f"  REMOVE: {file_path}")
            print()
            total_duplicates += len(files) - 1  # Count extra copies
        
        print(f"Total duplicate files: {total_duplicates}")
        print(f"Unique images: {len(image_files) - total_duplicates}")
        print(f"Files to remove: {len(files_to_remove)}")
        
        # Ask for confirmation
        print(f"\n{'='*50}")
        print("REMOVAL SUMMARY")
        print(f"{'='*50}")
        print(f"• Total images scanned: {len(image_files)}")
        print(f"• Duplicate sets found: {len(duplicates)}")
        print(f"• Files to remove: {len(files_to_remove)}")
        print(f"• Unique images after removal: {len(image_files) - len(files_to_remove)}")
        print(f"• Space saved: ~{len(files_to_remove)} files")
        
        response = input(f"\nDo you want to remove {len(files_to_remove)} duplicate files? (y/n): ").lower().strip()
        
        if response in ['y', 'yes']:
            print("\nRemoving duplicate files...")
            removed_count = 0
            for file_path in files_to_remove:
                try:
                    Path(file_path).unlink()
                    removed_count += 1
                    if removed_count % 10 == 0:
                        print(f"Removed {removed_count}/{len(files_to_remove)} files...")
                except Exception as e:
                    print(f"Error removing {file_path}: {e}")
            
            print(f"\n✅ Successfully removed {removed_count} duplicate files!")
            print(f"Remaining unique images: {len(image_files) - removed_count}")
        else:
            print("No files were removed.")
    else:
        print("No duplicate images found! ✅")
    
    print(f"Total images scanned: {len(image_files)}")

if __name__ == "__main__":
    main() 
