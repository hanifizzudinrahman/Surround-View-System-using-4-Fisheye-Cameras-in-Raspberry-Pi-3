# Surround-View-System-using-4-Fisheye-Cameras-in-Raspberry-Pi-3

By using 4 cameras installed in front, back, right and left of the car, we can see the surroundings in our car in just one screen. These 4 cameras are connected to a multi camera adapter module that the functions is to turn on which camera will be active (this process is sequential).

- Hardware: Raspberry Pi 3, Multi Camera Adapter V2.2, Fisheye Camera OV05646
- Tools: Python (OpenCV), I2C Protocol (SDA/SCL), SPI (MISO/MOSI/CLK)
- Step:
![1  Real Hardware _ Chess Board](https://user-images.githubusercontent.com/47806867/135233957-3edf0cfa-24a2-4561-b386-0d2138bff45f.jpg)
1. Take Image
2. Calibrate Fish Eye
![9](https://user-images.githubusercontent.com/47806867/135234710-a5ad9c38-85ee-4b58-bc2d-b60ab0e94da7.jpg)
![9](https://user-images.githubusercontent.com/47806867/135234732-78f536e8-f752-43e6-b799-afbb7dda2f8f.jpg)

3. Convert Bird’s Eye View
![3 BEV-Remove-Camera_A_1](https://user-images.githubusercontent.com/47806867/135234304-710c9d27-014e-4a04-a78f-a0659e92c37b.jpg)
![3 BEV-Remove-Camera_B_1](https://user-images.githubusercontent.com/47806867/135234312-3d2acd7e-6cfb-46bf-a9c3-e0e140ec342a.jpg)
![3 BEV-Remove-Camera_C_1](https://user-images.githubusercontent.com/47806867/135234315-c3b54ea1-997e-494e-ac92-5faa1ebdc4fb.jpg)
![3 BEV-Remove-Camera_D_1](https://user-images.githubusercontent.com/47806867/135234318-3db8d490-f30a-4bbe-8470-322e27d0886a.jpg)

4. Stitch Image
![1 1 STITCHING-BEV-OR-6 1 BEV-FINAL-SameSize-Camera_A_1](https://user-images.githubusercontent.com/47806867/135234127-25779ef5-9fc2-4ff9-81a6-af2754c4d1b0.jpg)

![1 STITCHING-BEV-CAR-FINAL-6 1 BEV-FINAL-SameSize-Camera_A_1](https://user-images.githubusercontent.com/47806867/135234061-3c8c2d46-6a83-4072-b7cf-3acdb372bc78.jpg)

- Result: FPS = 0.5 with resolution each camera is 640x480
- This project is collaboration with Foreign Student (Pakistan)



