# duty cycle and pulse width

duty cycle is the percentage the signal is high. digital simulating an analog value with a square-ish wave.

in an haptic motor context, this is the "strength of vibration". rather than percentage, it's [0, 255]. (rescale that)

pulse width is how long to buzz in ms.


so a rhythm notation would be a list of durations and strengths
[(500, 0.2), (250, 0.9), (250, 0.9), (250, 0.0)] etc.



# big questions

multiple sensors streaming accelerometer data