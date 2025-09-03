# Image Processing Lab 1: Image Scaling and Rotation

This repository contains implementations of fundamental image processing techniques for scaling and rotation using two different interpolation methods: **Nearest Neighbor** and **Bilinear Interpolation**.

## Overview

The lab demonstrates how to implement image transformations from scratch without relying on built-in OpenCV functions for interpolation. We compare the quality and characteristics of two interpolation methods when applied to scaling and rotation operations.

## Approach

### 1. Image Loading and Setup

We start by loading a test image (`cameraman.bmp`) using OpenCV and setting up the necessary libraries:
- OpenCV for image I/O operations
- NumPy for numerical computations
- Matplotlib for visualization
- Math library for trigonometric functions

### 2. Scaling Implementations

#### Nearest Neighbor Scaling
```python
def nearest_neighbor_scaling(image, scale_x, scale_y):
    height, width = image.shape[:2]
    new_height, new_width = int(height * scale_y), int(width * scale_x)
    scaled_image = np.zeros((new_height, new_width, 3), dtype=np.uint8)
    
    for i in range(new_height):
        for j in range(new_width):
            x = min(int(j / scale_x), width - 1)
            y = min(int(i / scale_y), height - 1)
            scaled_image[i, j] = image[y, x]
    
    return scaled_image
```

**Key characteristics:**
- Simple and fast implementation
- Maps each pixel in the output image to the nearest pixel in the input image
- Results in blocky, pixelated appearance when upscaling
- Preserves sharp edges but introduces aliasing artifacts

#### Bilinear Interpolation Scaling
```python
def bilinear_scaling(image, scale_x, scale_y):
    height, width = image.shape[:2]
    new_height, new_width = int(height * scale_y), int(width * scale_x)
    scaled_image = np.zeros((new_height, new_width, image.shape[2]), dtype=np.uint8)

    for i in range(new_height):
        for j in range(new_width):
            x = j / scale_x
            y = i / scale_y

            x_floor = int(np.floor(x))
            y_floor = int(np.floor(y))
            x_ceil = min(x_floor + 1, width - 1)
            y_ceil = min(y_floor + 1, height - 1)

            dx = x - x_floor
            dy = y - y_floor

            v1 = image[y_floor, x_floor, :]
            v2 = image[y_floor, x_ceil, :]
            v3 = image[y_ceil, x_floor, :]
            v4 = image[y_ceil, x_ceil, :]


            q1 = v1 * (x_ceil - x) + v2 * (x - x_floor)
            q2 = v3 * (x_ceil - x) + v4 * (x - x_floor)
            q = q1 * (y_ceil - y) + q2 * (y - y_floor)

            scaled_image[i,j,:] = q

    return scaled_image
```

**Key characteristics:**
- More computationally intensive but produces smoother results
- Interpolates between four neighboring pixels using weighted averages
- Reduces aliasing artifacts and produces more natural-looking scaled images
- Better preserves gradual intensity transitions

### 3. Rotation Implementations

#### Nearest Neighbor Rotation
```python
def nearest_neighbor_rotation(image, angle):
    theta = np.deg2rad(angle)

    height, width = image.shape[:2]
    angle_rad=math.radians(angle)

    new_height = int(abs(height * math.cos(angle_rad)) + abs(width * math.sin(angle_rad)))
    new_width = int(abs(width * math.cos(angle_rad)) + abs(height * math.sin(angle_rad)))
    rotated_image = np.zeros((new_height, new_width, image.shape[2]), dtype=np.uint8)

    if image.ndim == 3:
        new_image = np.zeros((new_height, new_width, 3), dtype=image.dtype)
    else:
        new_image = np.zeros((new_height, new_width), dtype=image.dtype)

    orig_cx, orig_cy = width / 2, height / 2
    new_cx, new_cy = new_width / 2, new_height / 2

    for i in range(new_height):
        for j in range(new_width):
            y = i - new_cy
            x = j - new_cx

            src_x = x * np.cos(-theta) - y * np.sin(-theta) + orig_cx
            src_y = x * np.sin(-theta) + y * np.cos(-theta) + orig_cy

            src_x = int(round(src_x))
            src_y = int(round(src_y))

            if 0 <= src_x < width and 0 <= src_y < height:
                new_image[i, j] = image[src_y, src_x]

    return new_image

```

#### Bilinear Interpolation Rotation
```python
def bilinear_rotation(image, angle):
    angle_rad = math.radians(angle)
    height, width = image.shape[:2]

    new_height = int(abs(height * math.cos(angle_rad)) + abs(width * math.sin(angle_rad)))
    new_width = int(abs(width * math.cos(angle_rad)) + abs(height * math.sin(angle_rad)))
    rotated_image = np.zeros((new_height, new_width, image.shape[2]), dtype=np.uint8)

    ox, oy = width // 2, height // 2
    nx, ny = new_width // 2, new_height // 2

    for i in range(new_height):
        for j in range(new_width):
            x = (j - nx) * math.cos(-angle_rad) - (i - ny) * math.sin(-angle_rad) + ox
            y = (j - nx) * math.sin(-angle_rad) + (i - ny) * math.cos(-angle_rad) + oy

            if 0 <= x < width - 1 and 0 <= y < height - 1:
                x1, y1 = int(np.floor(x)), int(np.floor(y))
                x2, y2 = min(x1 + 1, width - 1), min(y1 + 1, height - 1)
                dx, dy = x - x1, y - y1

                for c in range(image.shape[2]):
                    value = (1 - dx) * (1 - dy) * image[y1, x1, c] + \
                            dx * (1 - dy) * image[y1, x2, c] + \
                            (1 - dx) * dy * image[y2, x1, c] + \
                            dx * dy * image[y2, x2, c]
                    rotated_image[i, j, c] = int(value)

    return rotated_image
```

### 4. Experimental Results

The lab includes practical demonstrations with:
- **Scaling factor**: 3x enlargement of the original 256x256 image
- **Rotation angle**: Various angles to demonstrate rotation capabilities
- **Visual comparison**: Side-by-side comparison of nearest neighbor vs. bilinear results

## Key Findings

### Quality Comparison
1. **Nearest Neighbor**:
   - Produces sharp, blocky results
   - Faster computation
   - Suitable for pixel art or when preserving exact pixel values is important
   - More prone to aliasing artifacts

2. **Bilinear Interpolation**:
   - Produces smoother, more natural-looking results
   - Higher computational cost
   - Better for photographic images
   - Reduces aliasing but may introduce slight blurring


## Files in Repository

- `IVPR_LAB_1.ipynb`: Complete Jupyter notebook with implementations and experiments
- `cameraman.bmp`: Original test image (256x256 pixels)
- `nn_scaled.jpg`: Result of nearest neighbor scaling
- `bilinear_scaled.jpg`: Result of bilinear interpolation scaling
- `nn_rotated.jpg`: Result of nearest neighbor rotation
- `bilinear_rotated.jpg`: Result of bilinear interpolation rotation

## Usage

1. Load the Jupyter notebook in Google Colab or local Jupyter environment
2. Run all cells to see the implementations and results
3. Modify scaling factors or rotation angles to experiment with different parameters
4. Compare the visual quality of different interpolation methods

## Technical Implementation Details

### Coordinate System
- Uses standard image coordinate system (origin at top-left)
- Handles boundary conditions to prevent out-of-bounds access
- Implements proper inverse transformation for rotation

### Optimization Considerations
- Uses NumPy arrays for efficient memory access
- Implements bounds checking to prevent segmentation errors
- Could be further optimized using vectorized operations or GPU acceleration

## Conclusion

This lab demonstrates the fundamental trade-offs in image processing between computational efficiency and output quality. While nearest neighbor interpolation is faster and simpler, bilinear interpolation provides significantly better visual quality for most applications, especially when dealing with natural images.
