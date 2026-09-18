# Movie preparation

## Generate voice track

```sh
export $(cat .env | xargs)

for file in slide*.txt; do
    python3 "tts_demo.py" "$file" --voice ash
done

# python3 "tts_demo.py" slide13.txt --voice ash
```

## Combine voice tracks

```sh
rm full_demo.mp3
python3 merge_mp3.py *.mp3 -o full_demo.mp3
```

## Recorded scenes

### Publishing an API service

(Slide 13) Janis: Go through tooling. Go through the restish commands.

### Requesting access - Common SSO

Harley: Login to Common SSO, select the API.

### Access Control

Mark: Fake email, navigating to Connection Requests

### Calling the service

Harley: Fake email, calling the API
