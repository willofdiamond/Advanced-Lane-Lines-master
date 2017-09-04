## Writeup Template

### You can use this file as a template for your writeup if you want to submit it as a markdown file, but feel free to use some other method and submit a pdf if you prefer.

---

**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Code References)
[lane detection code]:(https://github.com/willofdiamond/Advanced-Lane-Lines-master/blob/master/lane_detection.ipynb).

[//]: # (Image References)

[image1]: (Advanced-Lane-Lines-master/Unknown.png) "Undistorted"
[image2]: (https://github.com/willofdiamond/Advanced-Lane-Lines-master/blob/master/undistortLane.png) "Road undistorted"
[image3]: (https://github.com/willofdiamond/Advanced-Lane-Lines-master/blob/master/binaryImages.png) "Binary Example"
[image4]: (https://github.com/willofdiamond/Advanced-Lane-Lines-master/blob/master/wrapmask.jpg) "Warp Example"
[image5]: .https://github.com/willofdiamond/Advanced-Lane-Lines-master/blob/master/color_fit_lines.png "Fit Visual"
[image6]: (https://github.com/willofdiamond/Advanced-Lane-Lines-master/blob/master/example_output.png) "Output"
[video1]: (https://github.com/willofdiamond/Advanced-Lane-Lines-master/blob/master/project_video1.mp4) "Video"


---


### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is contained in the twelfth code cell of the IPython notebook located in [lane detection code].  

I start by preparing "object points", which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.  

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result:

![alt text][image1]

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

To demonstrate this step, I will describe how I apply the distortion correction to one of the test images like this one:
![alt text][image2]

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.
Initially RGB image is converted in to HSL, S channel image seems to reflect the lanes well in different lighting conditions. I had applied Sobel edge detector mask in x direction which preserve the highlight the edges in the y direction (Lanes are vertical edges). I used a combination of color and gradient thresholds to generate a binary image. Here's an example of my output for this step.

![alt text][image3]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for my perspective transform includes a function called `wrap_image()`, which appears in cell 50 of [lane detection code]. Function takes a image as input while source (`src`) and destination (`dst`) points are hard coded in to the function in the following manner:

```python
x_len = image.shape[1]
y_len = image.shape[0]
source_points = np.float32([[x_len/7*6-50,y_len-50],
             [x_len/2+70,y_len/2+100],
             [(x_len/2)-60,y_len/2+100],
             [x_len/6+50,y_len-50]
            ])
destination_point = np.float32([[x_len/7*6-50,y_len],
                 [x_len/7*6-50,0],
                 [x_len/8+100,0],
                 [x_len/8+100,y_len]
                ])
```

This resulted in the following source and destination points:

| Source        | Destination   |
|:-------------:|:-------------:|
| 1047, 670     | 1047, 720     |
| 710, 460      | 1047, 0       |
| 580, 460      | 260, 0        |
| 263, 670      | 260, 720      |

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a  warped mask image.

![alt text][image4]

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?
process_image_multiframe function defined in the cell 55 has the code to detect lane lines. frame_update_var and average_update_var are used to define when I am updating the measuring parameters of the lane images and how many parameters from frame_update_var intervals are  average to get references parameters. lines_ROC  and lines_ROC2 functions defined in cell 28 and 29 both use histogram of an image to find lanes. Once the left and right lane positions are determined they are fitted with a polynomial function.

![alt text][image5]

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

I am calculating the radius of curvature in both ines_ROC  and lines_ROC2 functions defined in cell 28 and 29. Left and right lanes in the image are found. They are fitted to a second order polynomial. Using the fitted parameters new lanes lines are generated this lanes are then converted to real world units and then radius of curvature is calculated by using the following formula

```python
 left_curverad = ((1 + (2*left_fit_cr[0]*y_eval*ym_per_pix + left_fit_cr[1])**2)**1.5) / np.absolute(2*left_fit_cr[0])
    right_curverad = ((1 + (2*right_fit_cr[0]*y_eval*ym_per_pix + right_fit_cr[1])**2)**1.5) / np.absolute(2*right_fit_cr[0])

```

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I implemented this step in function process_image_multiframe defined in cell 55  of my code an example of result on a test image:

![alt text][image6]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video] [video1]

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

When I initially implemented the algorithm by calculating lanes in each frame independently noise is causing false lanes. This is avoided by changing the threshold of the Sobel operator and using the curve fit parameters from the average of the average_update_var number of previous frames at frame_update_var intervals.
