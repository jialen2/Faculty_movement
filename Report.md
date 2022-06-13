# The Problem
The project aims at discovering professor moving trends between different academic institutions, and find useful information for institutions based on faculty movement statistics.

# Approaches
The project can be summarized into 3 steps: scraping, analyzing and ranking. I will discuss each step in detail later.
## Scraping  
In the scraping step, we collect information about professors from different institutions from LinkedIn. Collected information includes their education history and work history. Sample result files can be found in directory "Faculty_Movement/scrape/Computer_Science", which contains information about faculties in the top 100 Computer Science Department in the U.S.

How to scrape:
1. Sign up for linkedin accounts. DON'T use personal email to sign up. Register fake accounts in Outlook or Gmail should work.
2. Place faculty lists that needs to scrape on in the directory "Faculty_Movement/scrape/faculty_list/[Major]/", where "Major" is the major those faculty work on. 
3. Place signed linkedin accounts into "scrape/linkedin_account.txt", which stores all linkedin accounts used in the scraping process, with one email per line.
4. (Only do when using a linkedin account for the first time) In the directory "Faculty_Movement/scrape", run "python3 get_faculty_data.py --test" and complete the LinkedIn user authentification process in the pop up window. When you see the main page of linkedIn, you can Ctrl-C to quit the window. Please repeat the process for several times until no authentification popped up.
5. run "python3 get_faculty_data.py" in the "Faculty_Movement/scrape" directory, and start the scraping process.

Final Result:
Done scraping for faculty in the top 100 Computer Science Departments in the U.S, stored in the directory "Faculty_Movement/scrape/Computer_Science".

## Analyzing
In the analyzing step, we transform the faculty data we collected from the last step into csv files that store faculty movements between institutions. 4 types files are provided:  
i. edu_to_edu.csv represents faculty graduating from one institution and join another instituion for further study.   
ii. work_from_edu.csv represents faculty graduating from one institution and join another instituion for work.  
iii. work_to_work.csv represents faculty quit working from one institution and join another instituion for continuous work.  
iv. general.csv represents all movements in the 3 categories mentioned above.  

How to analyze:
1. Make sure all files from scraping process are stored in directory in the step 5 of the scraping process.
2. Run "python3 parse_data.py" in "Faculty_Movement/analyze" directory. The code may take some time to finish.

Final Result:
Get all 4 kinds of files in the directory "Faculty_Movement/analyze/result/normal" about faculty information in the top 100 CS Departments.

## Ranking
We provide ranking on institutions mainly in two methods: Page Rank algorithm and Minimum Violation Ranking algorithm.

### Page Rank algorithm
We use the Page Rank algorithm to analyze the incoming node quality for each institution. 

How to run the algorithm:
We built Python Library Networkx to build graph for faculty movement data stored in csv files. You can run the "run_page_rank" method in the "Faculty_Movement/analyze/movement.py" to the page rank ranking the top 100 CS department.

### Minimum Violation Ranking algorithm
The idea was originally from the paper:  
https://www.science.org/doi/10.1126/sciadv.1400005  
More details can be found at:  
https://www.science.org/action/downloadSupplement?doi=10.1126%2Fsciadv.1400005&file=1400005_sm.pdf  
The algorithm is implemented at file "Faculty_Movement/analyze/minimum_violation_ranking.py", which used MCMC method to congressively find the ranking with fewer violations. However, we could not guarentee that the ranking we found using this method is the ranking with the minimum violation.  
In fact, we found that the ranking provided in the paper may not be the ranking with minimum violation. We can find ranking with fewer violations.  

## Data Storage
Faculty movement data are stored in the csv files. Those shoule be able to be imported into all kinds of databases. We use Neo4j for online data storage. Some useful Neo4j commands can be found in "Faculty_Movement/analyze/cypher_command" (Command used for importing csv data into database, selecting columns, deleting tables, etc.)  

# Results
We improved and finalized the Linkedin scrping methods and was able to get faculty information for the top 100 Computer Science Department in the U.S.  
We also analyzed the data and tried some methods including Page Rank and Minimum Violation algorithm to provide ranking for institutions on the aspect of faculty movement.

# Assessment
For this project, we achieved the goals of being able to retrieve information about faculty movement, and also trying some approaches for analyzing the data. But we haven't tried enough approaches to be able to compare the result for each approach. We should try more analytical approaches to provide more useful information about institutions hierarchy in the future.

# Reflection
We learned a lot of techniques and tools in the field of data processing, analytics and storage. It's a very good hands-on experience to learn and practice these techniques. The project also provides me insights about how a research work should be done like what kind of academic problems are interesting and meaningful to approach and how should we approach it. Thanks for the mentoring of Professor Kevin Chang and help of other group members in the reserach lab, I'm able to make some progress on the research work :)

# Future Plan
People who work on the project in the future can start the project in tow ways:
1. Keep researching on looking for more optimal ways to find the minimum violation ranking for the data, and possibly validate the ranking in the paper mentioned above or find out why the ranking is not optimal.
2. Try other ways on analyzing the faculty movement data to retrieve more useful information. Some thoughts include using Community Detection Algorithm, and analyzing data points in multi-dimensional space.





