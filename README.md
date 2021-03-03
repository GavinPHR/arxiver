# arxiver
Practical Group Coursework for Text Technologies for Data Science


| Meeting     | Description |
| ----------- | ----------- |
| 20 Jan      | Set out initial plan, each team member will look into their respective areas. These include fron-end, back-end (database, hosting), main information retrieval algorithm, and data collection. |
| 20 Jan      | Andrew and Ben will look into different aspects of the main algorithm, Jie will continue with the data, Gavin will start implement some web stuff       |
| 03 Feb      | Andrew and Ben will get the coursework code adapted to this project, Jie will continue with data cleaning, Gavin will implement the rest of the web functionalities. In the next meeting, we should have individual parts almost ready and be able to fit them together.        |
| 10 Feb      | Same as last meeting.   |
| 17 Feb      | 1. There is currently no way to rank the papers (besides according to dates), Jie will be working on getting citation counts so it would be easier to rank. For now, Gavin will assign some random citation counts to do some experiments with ranking. 2. As discussed last week, there is indeed no need to host the full dataset on the server. We should be only hosting the index, and for every paper, we will need to host its title, authors, abstract, link to pdf. 3. The queries seem to be not stemmed, which results in keyerros in the alphabet, and the search does not return any results. Andrew will try to fix that. 4. With 1220000 papers, the currently time for building the index is prohibitively long. Maybe Ben can look into methods where stemming is not required (if stemming is indeed taking the most time)? |
| 24 Feb      | Not Recorded |
| 03 Mar      | Some memory issues, trying either to remove docs with 1 word occurance, or save an index for each high-frequency word. Jie will get the citations. More front-end and ranking should be done before next week. |
