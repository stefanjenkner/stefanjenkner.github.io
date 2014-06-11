---
layout: post
title:  "Fabric, duplicity, AWS credentials and System Keyring"
date:   2014-06-11 00:38:28
categories: fabric python keyring amazon aws s3 secrets keychain
---

I still use [Fabric][fabric] for some deployment and systems administration tasks.
Passing secrets or credentials is commonly part of those tasks and it brings up some issues that has been on my mind for quite a long time:

* Fabric's configuration file `fabfile.py` is under version control
* credentials must be kept out of version control
* credentials must not be stored in plain text on any computer

Setting environment variables is commonly required when dealing with [AWS][aws].
[Duplicity][duplicity] (my backup tool of choice) makes use of them, especially when using the Amazon S3 backend.
The affected variables are `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` and `PASSPHRASE` (for symmetric encryption via GPG).
So the goal was to keep those credentials out of version control, retrieve them from the system keyring service and set the environment variables before command execution.

#### A simple backup task

This simple task creates a backup with [duplicity][duplicity] using it's S3 backend:

{% highlight python %}
@task
@hosts('admin@host1.local')
def backup_host1():
    """
    Backup host1.local to S3 via duplicity.
    """
    base_url = 's3://s3-eu-west-1.amazonaws.com/duplicity-host1.local'
    with duplicity_env('host1.local'):
        for local_dir in ['/etc', '/home', '/var/www']:
            remote_url = base_url + '/' + local_dir.replace('/','_')
            sudo("duplicity remove-older-than 60D -v3 --force %s" % (remote_url))
            sudo("duplicity --full-if-older-than 30D -v3 %s %s" % (local_dir, remote_url))
{% endhighlight %}

The task makes use of a custom [Context Manager][cm] `duplicity_env` which will be explained below.

#### Context Managers to the Rescue!

[Context Managers][cm] for use with Python's `with` statement are one of my favorite Fabric-features.
The `with` statement ensures the execution of a specific setup and teardown block, regardless of whether the intended block fails or not. Classes only need to implement `__enter__()` and `__exit__()`.
As Fabric already comes along with it's own context manager for setting environment variables (called `shell_env`), I decided to wrap the (internal) `_setenv` method, instead of starting to implement the context manager as a class.
The [python keyring library][keyring] enables easy access to the system keyring service.
It works pretty well with OS X Keychain and GNOME Keyring, but should also work with the Windows Credential Vault (untestet by me).

{% highlight python %}
def duplicity_env(hostname):
    """
    Set shell environment variables for duplicity.
    """
    from fabric.context_managers import _setenv
    import keyring, sys
    kw = {}
    to_env = {
        'Duplicity': 'PASSPHRASE',
        'Access Key Id': 'AWS_ACCESS_KEY_ID',
        'Secret Access Key': 'AWS_SECRET_ACCESS_KEY',
    }
    for key,var in to_env.items():
        secret = keyring.get_password(hostname, key)
        if secret is None:
            print """Run: python -c \"import keyring;
            keyring.set_password('%s', '%s', 'PASSWORD')\"""" % (hostname, key)
            sys.exit(1)
        else:
            kw[var] = secret
    return _setenv({'shell_env': kw})
{% endhighlight %}

The code above defines a dictionary `to_env` that maps keychain identifiers to environment variables.
If the keyring does not contain the entry, it give some hints on how to add it.

#### OS X Keychain

The [keyring library][keyring] wraps OS X keychain entries like this:

 * Field _Name_ is the display name and can be changed
 * Field _Account_ matches `username`, the second argument of `keyring.get_password(...)`
 * Field _Where_ matches `servicename`, the first argument of `keyring.get_password(...)`

OS X may also bring up a popup to ask for keychain access.

[duplicity]: http://duplicity.nongu.org/
[aws]: http://aws.amazon.com/
[fabric]: http://www.fabfile.org/
[cm]: http://docs.fabfile.org/en/latest/api/core/context_managers.html
[keyring]: https://pypi.python.org/pypi/keyring
