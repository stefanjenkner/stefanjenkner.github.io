---
layout: post
title:  "Time tracking with the Pomodoro.app"
date:   2014-05-02 07:11:11
categories: pomodoro timetracking sqlite
---

I'm a huge fan of the [Pomodoro.app][pomodoro.app]. 
It helps me to focus on my work and it controlls my messenger status (Adium) to tell my colleagues when I'm busy.
Now I even use it to log my activies and put them into a SQLite database for reporting. 

#### Clue code

The [Pomodoro.app][pomodoro.app] can invoke AppleScripts on certain events. 
I'm not a big fan of the AppleScript-Language but I know how to make it run external programs. 
For that reason I wrote a [few lines of Python][gist] to insert the activities into the database. 

Frist put the [Python-Script][gist] somewhere.
Then launch _Pomodoro_ , go to _Preferences_ / _Scripts_, check _End_ and put this script into the field:

{% highlight applescript %}
-- Applescript:
do shell script "/Users/stefan/timesheet_add.py -t \"$pomodoroName\" -m \"$duration\""
{% endhighlight %}

Just replace the path to ``timesheet_add.py``. The parameters ``$pomodoroName`` (name of the activity) and ``$duration`` (time in minutes) will be passed to the script.

#### Database

The table structure is as simple as:

{% highlight sql %}
CREATE TABLE activities (
  day text,
  activity text,
  minutes text,
  added timestamp
);
{% endhighlight %}

This ``timesheet`` view groups all activities with the same name on a certain day and shows the time ``HH:MM`` formated:

{% highlight sql %}
CREATE VIEW timesheet AS
   select day, activity , (sum(minutes)/60) || ':' || (sum(minutes)%60) as hours 
   from activities
   group by day,activity
{% endhighlight %}

The next one only selects activities of the current week:

{% highlight sql %}
CREATE VIEW timesheet_current_week AS
   select day,activity, (sum(minutes)/60) || ':' || (sum(minutes)%60) as hours 
   from activities 
   where strftime('%YW%W', day) = strftime('%YW%W', date('now')) 
   group by day,activity
{% endhighlight %}

With a slightly altered ``WHERE`` condition to select last weeks activities:

{% highlight sql %}
CREATE VIEW timesheet_last_week AS
  select day,activity, (sum(minutes)/60) || ':' || (sum(minutes)%60) as hours
  from activities
  where strftime('%YW%W', day) = strftime('%YW%W', date('now', '-7 days')) 
  group by day,activity
{% endhighlight %}

There is even a view that indicates if you worked too much (100% = 480 minutes = 8 hours):

{% highlight sql %}
CREATE VIEW completeness_current_week AS
  select
   day,
   (sum(minutes)/60) || ':' || (sum(minutes)%60) as hours,
   round(((100.0/480.0)*sum(minutes)), 2) as percent
  from activities 
  where strftime('%YW%W', day) = strftime('%YW%W', date('now'))
  group by day
{% endhighlight %}

I use [SQLite Professional][sqlitepro] (at that time it was free) to display the views.
It automatically detects changes on the database file and refreshes the current view.


[pomodoro.app]: https://github.com/ugol/pomodoro
[gist]:         https://gist.github.com/sedden/19391359f6c0e4baf8ed
[sqlitepro]:    https://www.sqlitepro.com/