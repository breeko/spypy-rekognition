# s3_bucket = "spypy-images"

max_labels = 10

# After uploading a file into the unprocessed, it triggers a lambda function to process
# Below represents the number of attempts and the wait between attempts when trying to access a processed image
max_num_attempts = 5
sleep_after_attempt = 1

date_format = "%Y-%m-%d-%H-%M-%S-%f"
date_format_printable = "%Y-%m-%d %H:%M:%S"

min_confidence = 0.8

s3_unprocessed_bucket = "spypy-1"
s3_processed_bucket = "spypy-1-objects-processed"

valid_image_types = (".png", ".jpg")

alpha = 20