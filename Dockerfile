FROM ubuntu
RUN mkdir -p /var/lib/rss
COPY test2.py /var/lib/rss/test2.py
COPY rssKeysList.txt /var/lib/rss/rssKeysList.txt
COPY rssWebSites.txt /var/lib/rss/rssWebSites.txt
COPY rssWebSites2.txt /var/lib/rss/rssWebSites2.txt
COPY requirements.txt /var/lib/rss/requirements.txt
RUN apt-get update
RUN apt-get install --yes python-pip python-dev build-essential
RUN pip install --upgrade pip
RUN apt-get install --reinstall libpython2.7-stdlib
RUN pip install -r /var/lib/rss/requirements.txt
ENTRYPOINT ["python", "/var/lib/rss/test2.py", "--feeds-from-file", "/var/lib/rss/rssWebSites.txt"]
