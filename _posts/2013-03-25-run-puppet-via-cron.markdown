---
layout: post
title: "Run Puppet via Cron"
date: 2013-03-25 13:37
comments: true
categories: Puppet
published: true
---

While deploying [Puppet](http://puppetlabs.com) on several Ubuntu machines, everything was fine until Nagios started sending out warnings about high memory and high CPU usage, caused by the Puppet agent process. Related Bug-reports are:

  * [Bug #1395](https://projects.puppetlabs.com/issues/1395#change-55821) puppet memory usage
  * [Bug #12310](http://projects.puppetlabs.com/issues/12310#note-16) Significant slow down in 2.7.10 apply
  * [Bug #995719](https://bugs.launchpad.net/ubuntu/+source/puppet/+bug/995719) process_name.rb removed in 2.7.11 but still provided by puppet-common
  
A common workaround is to run the Puppet agent via Cron. Take a look at the [Cron Patterns](http://projects.puppetlabs.com/projects/1/wiki/Cron_Patterns) Wiki page, but don't get too confused. Until Puppet 2.6, simply run: 

``` bash
/usr/sbin/puppetd --no-daemonize --onetime
```

With Puppet 2.7 it slightly changed to:
    
``` bash
/usr/bin/puppet agent --no-daemonize --onetime
```
    
Furthermore you won't run all the agents at the same time. So the next step is to plan the execution time. To run Puppet every 30 minutes, use ``fqdn_rand(30)`` to generate a value between 0 and 29 for the first, and add 30 more to get the second point of time:

``` puppet
$min1 = fqdn_rand(30)
$min2 = $min1 + 30
```
    
The ``fqdn_rand`` function will generate the same value each time you call it, dependent on the FQDN of the actual host.
Finally, the file resource will look like this: 

``` puppet
file { '/etc/cron.d/puppet-cron':
  ensure  => 'present',
  content => "$min1,$min2 * * * * root /usr/bin/puppet agent --no-daemonize --onetime\n",
  mode    => '0644',
  owner   => 'root',
  group   => 'root',
} 
```

As a side effect, this will solve another problem for you.
Have you ever tried to reconfigure Puppet via Puppet?
Currently there is no way telling Puppet to stop, re-read it's configuration and start again (e.g. via sending the SIGHUP signal). This related Bug-report was added two years ago:

 * [Bug #7273](http://projects.puppetlabs.com/issues/7273) - Add additional signals for restarting Puppet agent runs
