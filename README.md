# Face Detection and Blurring Tool 🎭

A Python application that provides a user-friendly interface for detecting and blurring faces in images. Built with CustomTkinter and OpenCV, this tool offers both single and batch processing capabilities with a modern, dark-themed interface.

## ✨ Features

- 🎨 **Modern UI**: Clean and intuitive interface with dark mode theme
- 📸 **Multiple Image Support**: Process multiple images in one session
- 👤 **Face Detection**: Automatic face detection using OpenCV's Haar Cascade
- 🔒 **Privacy Protection**: Apply Gaussian blur to detected faces
- 🔄 **Batch Processing**: Process and save multiple images at once
- 👀 **Preview**: Side-by-side comparison of original and processed images
- 📁 **File Management**: Easy image addition, removal, and navigation

## 📸 Screenshots

### Main Interface

![Main Interface](<Screenshot%20(10).png>)
_Main application window showing the dark theme interface with image preview_

### Batch Processing

![Batch Processing](<Screenshot%20(11).png>)
_Batch processing interface with multiple images loaded_

## 🔧 Requirements

```bash
python >= 3.6
opencv-python
customtkinter
Pillow
```

## 🚀 Installation

1. Clone the repository or download the source code
2. Install the required packages:
   ```bash
   pip install opencv-python customtkinter pillow
   ```
3. Run the application:
   ```bash
   python face_blur_app.py
   ```

## 📖 Usage

### 🔍 Single Image Processing

1. Click "Add Images" to select one or more images
2. Use "Previous" and "Next" buttons to navigate through images
3. Click "Blur Current" to process the displayed image
4. Click "Save Current" to save the processed image

### 📦 Batch Processing

1. Add multiple images using the "Add Images" button
2. Click "Process All" to detect and blur faces in all images
3. Use "Save All" to save all processed images to a selected directory

### 🎛️ Additional Controls

- **Remove Selected**: Remove the current image from the list
- **Navigation**: Use Previous/Next buttons to browse through images
- **Preview**: View original and processed images side by side

## 🔍 Features in Detail

### 📸 Image Management

- Support for multiple image formats (JPG, JPEG, PNG, BMP, GIF)
- Maintain a list of loaded images with file names
- Easy navigation between images

### 👤 Face Detection and Blurring

- Automatic face detection using Haar Cascade Classifier
- Gaussian blur effect for privacy protection
- Adjustable blur intensity

### 🔄 Batch Operations

- Process multiple images at once
- Batch save with automatic file naming
- Progress feedback for batch operations

### 🎨 User Interface

- Dark mode theme for reduced eye strain
- Responsive layout that adapts to content
- Clear status messages and operation feedback

## 📝 File Naming Convention

When saving processed images, the application automatically:

- Adds "\_blurred" suffix to the original filename
- Preserves the original file extension
- Example: `image.jpg` → `image_blurred.jpg`

## ⚠️ Error Handling

The application includes comprehensive error handling for:

- Image loading failures
- Processing errors
- File saving issues
- Invalid file formats

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the [MIT License](LICENSE) - see the [LICENSE](LICENSE) file for details.
