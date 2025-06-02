# 📐 Window Offset Guidelines for Application Tiling

This document defines window offset adjustments to create visually balanced, tiled window layouts across different screen resolutions.

## 🖥️ Base Resolution: 1920x1080 (1080p)

These offsets were tested and refined to make each window align perfectly into quarters of the screen:

| Window Region     | Original Position        | Adjusted Position           | Offsets Applied              |
|-------------------|--------------------------|------------------------------|-------------------------------|
| Top-left (Word)   | (0, 0, 960, 540)         | (0, 0, 960, 540)             | No offset                    |
| Top-right (XAMPP) | (960, 0, 960, 540)       | (950, 0, 980, 547)           | x: -10, width: +20, height: +7 |
| Bottom-left (Paint 1) | (0, 540, 960, 540)  | (-8, 538, 973, 547)          | x: -8, y: -2, width: +13, height: +7 |
| Bottom-right (Zoom) | (960, 540, 960, 540)   | (950, 538, 980, 547)         | x: -10, y: -2, width: +20, height: +7 |

---

## 📏 Scaled Offsets for Other Resolutions

The following table linearly scales offsets proportionally to other standard resolutions.  
_(Assumes same DPI scaling across resolutions.)_

