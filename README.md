# Unofficial CollegeScoreCard data visualization

This is the codebase of [CollegeScoreCard.io](https://collegescorecard.io/), which is built with [Dash by Plotly](https://dash.plot.ly/), and powered (mostly) by the [official CollegeScoreCard dataset](https://collegescorecard.ed.gov/data/). This is a work-in-progress, but may be useful to others.

### Notes

1. The "requirements.txt" file is embarrassingly long. I plan to fix it later.

2. The official dataset is stored into two MySQL databases (or, two SQLite databases) following some processing steps. [Here](https://github.com/royanin/collegescorecard_db) is the codebase to generate the databases.

3. I plan to publish the processing steps, once the related jupyter notebooks are clean enough! For now, you can find a short description of the processes and the variables [here](https://collegescorecard.io/explainer).

4. Most of the impotant data in [CollegeScoreCard.io](https://collegescorecard.io/) comes from the official sources, but errors might have crept in during my processing. Please do not make important life/financial decisions based on CollegeScoreCard.io or this codebase, at least for now.

5. I highly appreciate your feedback -- please do let me know if you catch mistakes in the data analysis, or catch bugs, or the general usability of the website.

### References

1. [Dash user guide](https://dash.plot.ly/)
2. [Dash/Plotly community forum](https://community.plot.ly/)
3. [Flask -- a Python-based web framework](http://flask.pocoo.org/)
4. [The Flask Mega-Tutorial by Miguel Grinberg](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
5. [Official CollegeScoreCard dataset](https://collegescorecard.ed.gov/data/)

### Background

At [collegescorecard.ed.gov](https://collegescorecard.ed.gov/), run by the US Department of Education, we can see how the US higher ed institutions fare on a variety of metrics. For example, one can find quantities such as the median debt of the graduates, the standardized test scores required to get in and so on. The goal of the official scorecard website is to help the higher ed stakeholders (e.g., students, parents, teachers, counselors etc.) make a quantitative understanding of the institutions. This is a fantastic goal, especially so, since the dataset that powers the website is [publicly available!](https://collegescorecard.ed.gov/data/)

While the official CollegeScoreCard website is a good starting point for viewing the dataset, I wanted better ways to analyze and compare different schools, and visualize the results more interactively. Having come across [Dash by Plotly](https://dash.plot.ly/) recently, I decided to build [CollegeScoreCard.io](https://collegescorecard.io/) to incorporate some of these ideas.

A special shoutout to the Plotly team for creating the amazing Dash library that makes [CollegeScoreCard.io](https://collegescorecard.io/) possible!