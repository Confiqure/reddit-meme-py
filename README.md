# reddit-meme-py

Our goal is to use Reddit’s API to download trending memes while using basic image recognition to classify memes.

## How it works

The algorithm works by comparing any given image to one of many pre-labeled memes in the `comparisons/` directory. The comparsion algorithm first resizes the comparison images to the input image and then basically compares the individual RGB values for each pixel. This strategy is loosely the Euclidean distance classifier since we only compare against one sample per class.

## Dependencies

Both [numpy](https://www.numpy.org/) and [opencv](https://pypi.org/project/opencv-python/) are dependencies for this project. Installing:
```sh
$ sudo pip install opencv
$ sudo pip install numpy
```

## Usage

To classify an image on your local machine:
```sh
$ python classify.py /path/to/image
```

To classify an online image resource, add the `--url` flag:
```sh
$ python classify.py http://image.url/path/to/image --url
```

For verbose output, add the `--verbose` flag:
```sh
$ python classify.py /path/to/image --verbose
```

Set a different comparison meme directory via the `--comparisons_dir`:
```sh
$ python classify.py /path/to/image --comparisons_dir /path/to/comparisons
```

## Future Work

- Build a meme rating system
- Build a recommending system based on user ratings
- Extend computer vision to extract text from memes
- Further classify and recommend memes using text as well as the meme type
