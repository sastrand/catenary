# Catenary
#### A command-line tool for teams to communicate in channels within workspaces.

The group collaboration platform Slack was launched in August of 2013. Originally part of a gaming platform, it had a minimal feature set
and '90s color scheme. Its popularity rapidly grew. By 2015 the [*Financial Times*](http://www.ft.com/cms/s/0/bd7dbf46-d24c-11e4-9c25-00144feab7de.html) remarked that Slack was the first piece of business technology to cross from business
to person use since Microsoft Office and the Blackberry.
By 2017 [it claimed](https://www.forbes.com/sites/alexkonrad/2017/09/12/slack-passes-6-million-daily-users-and-opens-up-channels-to-multi-company-use/#33e8d917fdb2)
over six million active daily users and garnered open-source competition from [two significant projects](https://en.wikipedia.org/wiki/Slack_(software)#Alternatives).

Slack changed the way people talk about their work by bringing a technology that already existed back into the mainstream, and I want to explore what that involved.

Based on IRC, this project is a mock of Slack's basic functionality with a description of the protocols used to implement it.

### Running Catenary

* Server.py can be run with `python3 server.py`. It calls methods in msg_processing.py.
* Client.py can be run in a different process or on a different machine also with `python3 client.py`.
* The dependencies are minimal and all part of the python3 standard library.
