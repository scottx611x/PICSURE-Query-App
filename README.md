# PICSURE Query App
Web app that allows for querying the [BD2K PICSURE API](http://bd2k-picsure.hms.harvard.edu/) using [AFL query strings](http://paradigm4.com/HTMLmanual/13.3/scidb_ug/ch14.html), JSON Strings, and dynamically based on genes of interest.

Can currently output results to:
- a [plotly](https://plot.ly/) table
- ???

# Pre-reqs:
- A valid `BD2K PICSURE API Key`
- 🐍`python`
- `pip`
- `virtualenv-wrapper` (optional but reccomended)

# Installation:
- `mkvirtualenv picsure-querier && workon picsure-querier` (optional)
- `pip install -r requirements.txt`
- tweak values in `constants.py` to fit your needs
- `python app.py`
You should be able to view the site @ http://localhost:5000

# TODOs:
- [ ] Dockerize w/ Apache
- [ ] Fix coding sins from hacakthon
- [ ] Backend with async support/ Python 3+: [sanic](https://github.com/channelcat/sanic)
- [ ] Celery + DB for long running queries
- [ ] Auth 0
- [ ] Add NHANES support
- [ ] More dynamic query interface for users. See [Jason's dynamic dropdowns](https://github.com/hms-dbmi/hackathon-Sept2017/blob/835140a43efc7962645ba9a4d8cbcf5877ea8d2c/hackathon_examples/pic-sure-api-driven-ui/src/main/webapp/js/dropdownBuilder.js)

---

# Query
<img width="1679" alt="screen shot 2017-09-15 at 3 36 09 pm" src="https://user-images.githubusercontent.com/5629547/30500377-0454165a-9a2c-11e7-9c42-e88e38a9d0dd.png">

# Wait
<img width="1680" alt="screen shot 2017-09-15 at 3 36 21 pm" src="https://user-images.githubusercontent.com/5629547/30500378-04553a44-9a2c-11e7-91ec-cc37f930e32b.png">

# Viola!
<img width="1679" alt="screen shot 2017-09-15 at 3 37 02 pm" src="https://user-images.githubusercontent.com/5629547/30500379-0458b822-9a2c-11e7-8c4e-52ee92e990a0.png">
