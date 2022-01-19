# juefei-chen-faculty-info-frontend

This is the frontend for visualizing faculty information already collected and controlling the distributed crawler.

## Setup

Please setup and start this frontend on your own computer

To run the backend, please refer to https://github.com/Forward-UIUC-2021F/juefei-chen-education-today

```bash
npm i
```

## Start

```bash
npm start
```

## Error Handling

```bash
# try this command
nvm install v14.3.0
```

## Usage

This UI contains 3 separated tabs, overview, data, and tasks

**Overview**

![1](https://github.com/Forward-UIUC-2021F/juefei-chen-faculty-info-frontend/blob/main/readme_img/1.png)

On the top of the overview tab, there are four charts displaying the general information and statistics of the faculty data already collected.

Below them, there is a table, and you can see the tasks (for scraping faculty info) that will be executed next. You can prioritize task(s) by clicking the checkboxes and then clicking the button "PRIORITIZE". If you want to prioritize tasks for a whole University, select the university in the search box above, then click "PRIORITIZE ALL", and finally click "REFRESH TASK TABLE".

**Data**

![1](https://github.com/Forward-UIUC-2021F/juefei-chen-faculty-info-frontend/blob/main/readme_img/2.png)

You can visualize facutly info of a department with the search box at the top. If you only select a university without specifying department, the department of this university will be listed.

If you have seen errors in some fields, you can directly modify each cell and then click "CHANGE". All changes will be saved to the database.

**Tasks**

![1](https://github.com/Forward-UIUC-2021F/juefei-chen-faculty-info-frontend/blob/main/readme_img/3.png)

You can visualize the statistics of all tasks that has been exectued for each university in the tab.

