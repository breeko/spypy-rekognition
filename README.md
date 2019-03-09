# spypy-rekognition

Object detection using [aws rekognition](https://aws.amazon.com/rekognition/) and [aws lambda](https://aws.amazon.com/lambda/)

To use aws services, a credentials must exist in `~/.aws/credentials` with an `aws_access_key_id` and `aws_secret_access_key`


To setup run `./setup-server.sh`

To rest run `./test.sh`

To package for lambda run `make build-lambda-package`

To detect objects from a url:

```
from detect import detect_images_from_urls

url='https://cdn1.autoexpress.co.uk/sites/autoexpressuk/files/2/22/dsc112-733_0.jpg' 
out = detect_images_from_urls(url)

print(out)


{
    "Labels": [
        {
            "Name": "Car",
            "Confidence": 99.79230499267578,
            "Instances": [
                {
                    "BoundingBox": {
                        "Width": 0.3765823245048523,
                        "Height": 0.3229130208492279,
                        "Left": 0.5312161445617676,
                        "Top": 0.5803122520446777
                    },
                    "Confidence": 99.79230499267578
                }
            ],
            "Parents": [
                {
                    "Name": "Vehicle"
                },
                {
                    "Name": "Transportation"
                }
            ]
        },
        {
            "Name": "Vehicle",
            "Confidence": 99.79230499267578,
            "Instances": [],
            "Parents": [
                {
                    "Name": "Transportation"
                }
            ]
        },
        {
            "Name": "Transportation",
            "Confidence": 99.79230499267578,
            "Instances": [],
            "Parents": []
        },
        {
            "Name": "Road",
            "Confidence": 99.0093994140625,
            "Instances": [],
            "Parents": []
        },
        {
            "Name": "Tarmac",
            "Confidence": 97.38719177246094,
            "Instances": [],
            "Parents": []
        },
        {
            "Name": "Freeway",
            "Confidence": 92.62093353271484,
            "Instances": [],
            "Parents": [
                {
                    "Name": "Road"
                }
            ]
        },
        {
            "Name": "Highway",
            "Confidence": 92.62093353271484,
            "Instances": [],
            "Parents": [
                {
                    "Name": "Road"
                },
                {
                    "Name": "Freeway"
                }
            ]
        },
        {
            "Name": "Spoke",
            "Confidence": 80.92488098144531,
            "Instances": [],
            "Parents": []
        },
        {
            "Name": "Tire",
            "Confidence": 80.87281799316406,
            "Instances": [],
            "Parents": []
        },
        {
            "Name": "Wheel",
            "Confidence": 76.86325073242188,
            "Instances": [],
            "Parents": []
        }
    ],
    "LabelModelVersion": "2.0",
    "ResponseMetadata": {
        "RequestId": "fcf34897-4280-11e9-ad41-cdf4c9733e98",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "content-type": "application/x-amz-json-1.1",
            "date": "Sat, 09 Mar 2019 15:35:38 GMT",
            "x-amzn-requestid": "fcf34897-4280-11e9-ad41-cdf4c9733e98",
            "content-length": "1081",
            "connection": "keep-alive"
        },
        "RetryAttempts": 0
    }
}
```