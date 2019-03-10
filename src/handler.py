from detect import detect_from_urls

def handler(event, context):
    urls = event.get("urls") or event["multiValueQueryStringParameters"]["urls"]
    out = detect_from_urls(urls)

    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": { },
        "body": str(out)
    }