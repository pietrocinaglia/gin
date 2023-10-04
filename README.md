## GIN: a web-based tool for generating synthetic interconnected network datasets for bioinformatics.

'Generator of synthetic Interconnected Networks' (GIN) is a user-friendly and effective tool which allows generating synthetic dataset, particularly suitable for bioinformatics applications that need evaluating the performance of their methodology based on comparison and successive computations. Briefly, it is able to generate synthetic interconnected networks, by also providing noising counterparts, useful, e.g., in network alignment tasks.


### Testing

GIN has been tested by using Gunicorn 'Green Unicorn' (gunicorn), as Python WSGI HTTP Server for UNIX. Note that index.html is a redirect to the ready-to-use web-application.


### Requirements

#### Front-end
jQuery, Bootstrap, and template are already imported, as well. You don't need to do anything.

#### Back-end
GIN needs Python3 >= 3.9, and the dependencies listed in 'requirements.txt'.

The packages listed into 'requirements.txt' can be installed via [Python Package Installer (pip)](https://pip.pypa.io/en/stable/):

```
pip install -r requirements.txt
```

(or its alias 'pip3', if any).
- Flask
- networkx
- gunicorn


### License

MIT License - Copyright (c) 2023 Pietro Cinaglia

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

