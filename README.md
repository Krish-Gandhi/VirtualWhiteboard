# VirtualWhiteboard

This project was created using OpenCV, Google's MediaPipe and numpy libraries. 

The idea for this project came to me when I attempted to use a dry erase whiteboard to teach my friend (who was chatting with me via video call) how to do a Fourier transform. I realized it was difficult for her to read the whiteboard for a few reasons such as lighting in the room, distance from the camera, camera quality, etc.

For optimal hand detection, when trying to perform a gesture, try to have your entire hand in frame with your palm directly facing the camera.

As of May 16, 2024 4:22 PM CST, this is version v1.0 of this whiteboard. 

It has the following features/functionality:

Draw: 
    Gesture: Touching your pointer finger to your thumb
    Indicator: Thumb landmark will turn blue 
    Effect: A blue spot will be left where the thumb landmark currently is
            Note: This feature is limited by your device's performance because this program runs frame by frame. As a result, lines may not appear continuous if you move your hands too fast. For optimal results, move your hand slowly to match your device's FPS.

Erase:
    Gesture: Touching your pinky finger to your thumb
    Indicator: Thumb landmark will turn green 
    Effect: Clears all drawing from entire board

Close:
    Gesture: Touching your ring finger to your thumb
    Indicator: Thumb landmark will turn red
    Effect: Closes window and exits program

Possible future features:

-Undo
-Partial Erase
-Change Draw Color