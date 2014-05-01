---
layout: post
title: "Pros and cons using Puppet's $::osfamily instead of $::operatingsystem Fact"
date: 2013-03-27 11:36
comments: true
categories: Puppet
published: true
---

Once you read the [Puppet Style Guide](http://docs.puppetlabs.com/guides/style_guide.html), you should know how to write well structured manifests, with the modest indentation, spacing, arrow alignment, quoting and so on.
Well, I think there are lots of other things you <del>better</del> should care. 
For this time, it's about when to use ``$::osfamily`` and when better to stay with the ``$::operatingsystem`` fact.

#### Pros

The key benefit of using ``$::osfamily`` is that you don't end up forking your favorite Puppet module on GitHub to add the eleventh RedHat derivate: 

``` puppet
case $::operatingsystem {
   'RedHat', 'CentOS', 'Scientific', . . . , 'OracleLinux', 'OEL': {
     # do something RHEL specific
   }
   'ubuntu', 'debian': {
     # do something Debian specific 
   }
   default: {
     # ...
   }
}
```

Instead you would use:

``` puppet
case $::osfamily {
   'redhat': {
     # do something RHEL specific
   }
   'debian': {
     # do something Debian specific 
   }
   default: {
     # ...
   }
}
```
    
It allows you to write cleaner manifests and works well for common tasks. 
You still have the choice to handle details via ``$::operatingsystem`` the more complex your classes become.

#### Cons
    
There are disadvantages of course: You claim tosupport an Operating-System you might haven't even heard of.
But my experience is that most people are using the EPEL repositories anyway. So wouldn't it be enough to test your modules against EPEL? And yes: you really should test your manifests!

#### Support for Facter < 1.6.1

The ``$::osfamily`` fact was introduced with Facter 1.6.1. There is a simple workaround for older versions. I found this solution in the description of the [puppetlabs-mysql Module](https://github.com/puppetlabs/puppetlabs-mysql/). Just put this into your ``site.pp`` (before any node definition):


``` puppet
if ! $::osfamily {
  case $::operatingsystem {
    'RedHat', 'Fedora', 'CentOS', 'Scientific', 'SLC', 'Ascendos', 'CloudLinux', 'PSBM', 'OracleLinux', 'OVS', 'OEL': {
      $osfamily = 'RedHat'
    }
    'ubuntu', 'debian': {
      $osfamily = 'Debian'
    }
    'SLES', 'SLED', 'OpenSuSE', 'SuSE': {
      $osfamily = 'Suse'
    }
    'Solaris', 'Nexenta': {
      $osfamily = 'Solaris'
    }
    default: {
      $osfamily = $::operatingsystem  
    }
  }
}
```

It defines ``$::osfamily`` if not available.
