# Surround-View-System-using-4-Fisheye-Cameras-in-Raspberry-Pi-3

By using 4 cameras installed in front, back, right and left of the car, we can see the surroundings in our car in just one screen. These 4 cameras are connected to a multi camera adapter module that the functions is to turn on which camera will be active (this process is sequential).

- Hardware: Raspberry Pi 3, Multi Camera Adapter V2.2, Fisheye Camera OV05646
- Tools: Python (OpenCV), I2C Protocol (SDA/SCL), SPI (MISO/MOSI/CLK)
- Step:
1. Take Image
2. Calibrate Fish Eye
3. Convert Bird’s Eye View
4. Stitch Image

- Result: FPS = 0.5 with resolution each camera is 640x480
- This project is collaboration with Foreign Student (Pakistan)

