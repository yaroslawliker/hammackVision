## Topic
Machine learning and computer vision.

## About repositroy
This repository stores files for the first of my third course coursework.
It contains experiments, examples, calculations and python code.

## New distance detecting method
This work introduces a new distance measurement method without using stereovision, depth sensors or object's size.

Let say, the floor is a flat surface. The method calculates 3D coordinates of an object (where y = 0) staying on this surface (taking camera coords are (0, y, 0), using camera angles and y.

Shortly: using pixel coordinates of the object's lowest point on the photo, camera y and camera angles we back-project the pixel point to 3D, by finding a line coming from the pixel trough the camera pinhole to the 3D world, and then finding the intersection point between this line and the floor plane. The intersection point is our object's point.

## The Android App
The seconds part, which is an Android app that uses camera, neurol networks and some code from this repo, is located on another repo: https://github.com/yaroslawliker/hammackVisionAndroid

## Paper
The paper with coursework is available on [this link](https://docs.google.com/document/d/1Dc-XodYoyybPe4YkiPFXeac6KoiGOq_3TwD8k0fiPYs/edit?usp=sharing) (in Ukrainian). 

## Objective
Develop a security machine vision mobile app.

Scenario: The user is hanging-out on a hammak, scared for his things (probably backpack, bicycle ect) to be stolen. He mounts his smartphone with a camera pointing to his things. Camera have to detect any person, approaching closer than M meters to camera/bags, and play an alarm sound.
