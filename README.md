# PreCog Recruitment Tasks

Directory structure of the submission is as follows:

```
- task-1/
    - Task 1.pdf
- task-2/
    - dump.txt
    - Report.pdf
    - Task 2.ipynb
- task-3/
    - task-a/
        -  dump/
        -  Rec_task/
        -  code.py
        -  paths
    - task-b/
        -  copy_stackoverflow.com_directory_here
        -  dump_link
        -  Report.pdf
        -  Task 3b.ipynb
```

Dependencies:

- Python 3.6+
- Anaconda
  - matplotlib
  - wordcloud
  - pandas
- pymongo
- tweepy
- pytz
- tabula
- hashlib
- xmltodict
- datetime
- json

Note: In order to use tabula, java development kit should also be installed.

## Task 1

Summary of 502 words is written in Task 1.pdf<br>
Topic: Signals Matter: Understanding Popularity and Impact of Users on Stack Overflow

## Task 2

To run this jupyter notebook

```
cd task-2
jupyter-notebook
```

Now choose Task 2.ipynb from the jupyter notebook landing page.<br>
To start executing: `Cell > Run All`<br>
Report of this jupyter-notebook is present in Report.pdf<br>
dump.txt consists of all the tweets collected by the program in the form of a list.<br>
paths file contains relative path to pdfs for testing purposes.

## Task 3

### Subtask A

To run this code.py

```
cd task-3/task-a
python code.py
```

Now enter path relative to the pdf in the prompt.<br>
The tables present in pdf are parsed and gets stored in task3a database.<br>
Tables follow a specific format: tbl\_{1}\_{2} where {1} is the table number and {2} is the md5 hash of pdf file.

To dump the tables from Mongo Database:

```
mongodump --db task3a
```

### Subtask B

Note: Because of its huge size, I haven't uploaded the stackoverflow.com folder. To download: [Click here](https://drive.google.com/file/d/1QTVwoZReZudfKkapWTUBvi0T9YCaLXX9/view)<br>
Extract and copy stackoverflow.com folder inside task-3/task-b folder such that directory structure looks like:

```
- task-3/
    - task-b/
            -  stackoverflow.com/
                - Badges.xml
                - Posts.xml
                - Tags.xml
                - Users.xml
                - Votes.xml
            -  dump_link
            -  Report.pdf
            -  Task 3b.ipynb
```

To run this code.py

```
cd task-3/task-b
jupyter-notebook
```

Now choose Task 3b.ipynb from the jupyter notebook landing page.<br>
To start executing: `Cell > Run All`<br>
Report of this jupyter-notebook is present in Report.pdf<br>
The parsed data is stored in task3b database in following collections: badges, tags, users, votes, posts<br>
dump can be downloaded by the link present in dump_link file.

To dump the tables from Mongo Database:

```
mongodump --db task3b
```

# Machine Specifications

Details of the machine on which the programs were tested:

- Operating System: Elementary OS 5.1 (Hera)
- Terminal: Bash
- Processor: Intel Core i7-8750H CPU @ 2.20 GHz 2.21 GHz
- RAM: 16 GB

# Developed by

- Shlok Pandey
- Email: shlok.pandey@research.iiit.ac.in
- Roll Number: 2020121008
