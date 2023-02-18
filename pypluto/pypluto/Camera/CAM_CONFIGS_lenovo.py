import numpy as np

CAMERA_HEIGHT = 1.8 #m

#matrix_coefficients - Intrinsic matrix of the calibrated camera
MATRIX_COEFFICIENTS = np.array([
        [
            289.1084845919912,
            0.0,
            309.4435568215443
        ],
        [
            0.0,
            293.8920476148095,
            242.59815032382136
        ],
        [
            0.0,
            0.0,
            1.0
        ]
    ])

#distortion_coefficients - Distortion coefficients associated with our camera
DISTORTION_COEFFICIENTS = np.array([
            -0.2868759826260511,
            0.20730330782367065,
            0.016643787447130097,
            -0.02460910630108414,
            -0.06969337867772066
        ])