# Optical-flow-racing

![Video GIF](Optical_Flow_racing.gif)

This project is an implementation of Lucas Kanade algorithm for extracting optical flow using OpenCV directly from a webcam to play a fun racing game.


Optical flow is a very popular feature used in modern tracking devices which involve exposure to visual stimulus along with pure deep learning methods.

Here, The same Task could be achieved by a Deep Learning approach or by masking a specific color(Somewhat similiar to Green-screens in media) but using a fully Deep Learning approach would be an overkill to a task of this complexity and the masking method will require a label to be worn by the subject which is restricting the degree of freedom.

The optical flow appears to be the optimal given the complexity of implementation.

# Requirements
- python-opencv v4.2
- PyGame v1.9
- numpy v1.19
- OpenCV intergrable webcam
