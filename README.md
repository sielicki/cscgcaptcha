# cscg2020: captcha

This is some of the scripts I used to get the flag for the CSCG2020 challenge Captcha.

The idea of the challenge is that the service requests you to solve 4 stages:

Stage 1: 1 captcha,   30 seconds
Stage 2: 3 captchas,  30 seconds
Stage 3: 10 captchas, 30 seconds
Stage 4: 100 captchas, 30 seconds

Pretty clever -- the captchas are flawwed enough that machines can solve them
with a bit of work, so you basically have the opposite of a captcha: one that
only a machine can solve given the time constraints.

Scripts:
* `get_training_data.py` scrapes tagged images
* `train.py` trains on the images
* `runner.py` runs the trained model against the website

Credit where credit is due:

* keras-ocr project
