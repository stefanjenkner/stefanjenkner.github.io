---
layout: post
title:  "Backup to Amazon Glacier with Duplicity and Duply"
date:   2015-11-11 07:38:31
categories: backup duplicity s3 storage duply amazon glacier
---

This is kind of a cheat sheet on how to create a fully encrypted backup on
[Amazon Glacier][glacier] with [Duplicity][duplicity] and [Duply][duply] (a
frontend/wrapper for Duplicity) for as little as EUR 0,01 per gigabyte (plus
transfer fees). 

 1. Get Duplicity version 0.6.26+, Duply version 1.9.1+, GnuPG and python-keyring
 2. Create a Bucket, setup permissions and create lifecycle rules
 3. Create a Duply profile
 4. Store the passwords in the keyring

Additionally, an [AWS][aws] account is needed.

#### Step 1: Get Duplicity version 0.6.26+, Duply version 1.9.1+, GnuPG and python-keyring

On Mac OS X with Homebrew:

{% highlight bash %}
brew install gnupg duplicity duply python
pip install keyring
{% endhighlight %}

On Debian/Ubuntu:

{% highlight bash %}
sudo apt-get install gnupg duplicity duply python-keyring
{% endhighlight %}

Package names may differ depending on the version of your distributions. Please
try `gnupg2` and `python3-keyring` if one of these packages cannot be found.


#### Step 2: Create a Bucket, setup permissions and create lifecycle rules

Don't forget to remember the region when creating a new Bucket on the S3 Management Console.
This time I chose Ireland (eu-west-1).

When attach a lifecycle rule to the bucket. 

 * Target: Objects with the prefix `_my_folder_to_backup/archive_`
 * Configuration: Archive to the Glacier Storage Class 1 days after the object's creation date.

Following this, create a new user and attach this custom policy:

{% highlight json %}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:ListBucket" ],
      "Resource": "arn:aws:s3:::my_bucket"
    },
    {
      "Effect": "Allow",
      "Action": [ "s3:PutObject", "s3:GetObject", "s3:DeleteObject"],
      "Resource": "arn:aws:s3:::my_bucket/*"
    }
  ]
}
{% endhighlight %}

There is one thing missing here. Once the archived files (not the index files,
not the signatures) moved to Glacier class storage via lifecyle rules, this user is
not (yet) able to move them back to standard class storage for restore.



#### Step 3: Create a Duply profile

Create the Duply profile with `duply my_profile create` and adjust the configuration
in profile in `~/.duply/my_profile/conf`.

{% highlight bash %}
SOURCE=/my/folder/to/backup

TARGET='s3://s3-eu-west-1.amazonaws.com/my_bucket/_my_folder_to_backup'
TARGET_USER=`keyring get 'duplicity my_profile' AWS_ACCESS_KEY_ID`
TARGET_PASS=`keyring get 'duplicity my_profile' AWS_SECRET_ACCESS_KEY`

# Uncomment if you prefere the more secure public/private key encryption
GPG_PW=`keyring get 'duplicity my_profile' PASSPHRASE`

DUPL_PARAMS="$DUPL_PARAMS --volsize 25 "

DUPL_PARAMS="$DUPL_PARAMS --file-prefix-manifest manifest_ "
DUPL_PARAMS="$DUPL_PARAMS --file-prefix-archive archive_ "
DUPL_PARAMS="$DUPL_PARAMS --file-prefix-signature signature_"
{% endhighlight %}

Please check the permissions of the created profile in `~/.duply/my_profile/`.


#### Step 4: Store the passwords in the keyring

The [keyring][keyring] commandline utility supports multiple backends: the
Mac OS X Keychain, the Linux Secret Service and the Windows Credential Vault.
There are defaults for each platform, but you can also [define which backend to
use](https://pypi.python.org/pypi/keyring#configure-your-keyring-lib) (or even
write your own).

To store the AWS Access Key from Step 2:

{% highlight bash %}
keyring set 'duplicity my_profile' AWS_ACCESS_KEY_ID
{% endhighlight %}

To store the AWS Access Secret from Step 2:

{% highlight bash %}
keyring set 'duplicity my_profile' AWS_SECRET_ACCESS_KEY
{% endhighlight %}

To store the key for symmetric GPG encryption:

{% highlight bash %}
keyring set 'duplicity my_profile' PASSPHRASE
{% endhighlight %}

These secrets will be retrieved via `keyring get ...` during the backup/restore
process.


#### Test

Test the backup process via:

{% highlight bash %}
duply my_profile backup
{% endhighlight %}

To restore a file or folder from backup:

{% highlight bash %}
duply my_profile restore Makefile
{% endhighlight %}

To fetch a single file or folder from backup:

{% highlight bash %}
duply my_profile fetch Makefile /tmp/Makefile
{% endhighlight %}

Also check out `duply --help` for a brief overview.


#### Résumé

I'm pretty happy with this backup solution, but there are some annoying parts as well:

 * Lifecyle rule needs to be created for each backup folder.
 * The user policy is missing an action for moving Glacier class storage items back to standard class storage.

In summary, it can be stated that this backup solution isn't perfect yet,
but it's built upon Open-Source tools and it's easy to customize. 


[aws]: https://aws.amazon.com/
[glacier]: https://aws.amazon.com/glacier/
[duplicity]: http://duplicity.nongu.org/
[duply]: http://duply.net/
[keyring]: https://pypi.python.org/pypi/keyring
