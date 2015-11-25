---
layout: post
title:  "Getting started with Docker Machine on Amazon EC2"
date:   2015-11-24 23:13:23
categories: docker docker-machine amazon aws ec2 iam policy
---

[Docker Machine][docker-machine] is one part of the Docker Toolbox which
helps you to manage and setup [Docker][docker] environments.
There are drivers for various cloud platforms and virtualization products.

Getting started with [Docker Machine][docker-machine] on [EC2][ec2] is
straight forward: a [brief section](https://docs.docker.com/machine/drivers/aws/)
of the official documentation covers all command line options and environment
variables which are relevant to `docker-machine --driver amazonec2 create ...`.

The required steps are:

1. Create an new IAM user and attach a *Custom Policy* to the user
2. Find out the VPC ID
3. Create your first instance with [Docker Machine][docker-machine]

This guide applies to [Docker Machine][docker-machine] version 0.5.0 on OS X.

#### Create an new IAM user and attach a Custom Policy to the user

Login to the AWS console and navigate to Services / IAM / Users.

Create a new user (e.g. docker-machine), note the access key and secret and
populate the environment variables:

{% highlight bash %}
export AWS_ACCESS_KEY_ID=AKI...
export AWS_SECRET_ACCESS_KEY=...
{% endhighlight %}

Then select the user, switch to the *Permissions* tab and add new
*Custom Policy* (expand Inline Policy to do so).
The following policy was shared by
[Brandon Mangold](https://github.com/bmangold) on
[docker-machine Issue 1655 (Minimal IAM policy)](https://github.com/docker/machine/issues/1655#issuecomment-128872611).

A slightly extended it with permissions for creating security groups:

{% highlight json %}
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "TheseActionsDontSupportResourceLevelPermissions",
            "Effect": "Allow",
            "Action": [
                "ec2:CreateKeyPair",
                "ec2:DeleteKeyPair",
                "ec2:ImportKeyPair",
                "ec2:Describe*",
                "ec2:CreateTags",
                "ec2:CreateSecurityGroup",
                "ec2:AuthorizeSecurityGroupIngress"
            ],
            "Resource": "*"
        },
        {
            "Sid": "ThisActionsSupportResourceLevelPermissions",
            "Effect": "Allow",
            "Action": ["ec2:RunInstances"],
            "Resource": [
                "arn:aws:ec2:eu-west-1::image/ami-*",
                "arn:aws:ec2:eu-west-1:%AWS_ACCOUNT_ID%:instance/*",
                "arn:aws:ec2:eu-west-1:%AWS_ACCOUNT_ID%:key-pair/*",
                "arn:aws:ec2:eu-west-1:%AWS_ACCOUNT_ID%:network-interface/*",
                "arn:aws:ec2:eu-west-1:%AWS_ACCOUNT_ID%:placement-group/*",
                "arn:aws:ec2:eu-west-1:%AWS_ACCOUNT_ID%:security-group/*",
                "arn:aws:ec2:eu-west-1:%AWS_ACCOUNT_ID%:subnet/*",
                "arn:aws:ec2:eu-west-1:%AWS_ACCOUNT_ID%:volume/*"
                ]
        },
        {
            "Sid": "TheseActionsSupportResourceLevelPermissions",
            "Effect": "Allow",
            "Action": [
                "ec2:TerminateInstances",
                "ec2:StopInstances",
                "ec2:StartInstances",
                "ec2:RebootInstances"
            ],
            "Resource": [
                "arn:aws:ec2:eu-west-1:%AWS_ACCOUNT_ID%:instance/*"
            ]
        }
    ]
}
{% endhighlight %}

Replace `%AWS_ACCOUNT_ID%` with your account ID. Get it from: AWS console / My Account.
I also changed the region to `eu-west-1`.

#### Find out the VPC ID

This step is also covered in the official drivers documentation.
Login to the AWS console and navigate to Services / VPC / Your VPCs.
Get the VPC ID from the VPC column and set the environment variable like this:

{% highlight bash %}
export AWS_VPC_ID=vpc-....
{% endhighlight %}


#### Create your first instance with

Four environment variables have been populated:

{% highlight bash %}
export AWS_ACCESS_KEY_ID=AKI... # first step
export AWS_SECRET_ACCESS_KEY=... # first step
export AWS_VPC_ID=vpc-.... # second step
{% endhighlight %}

As mentioned in the previous step, I changed to region to `eu-west-1`.
It must match the region in the IAM policy:

{% highlight bash %}
export AWS_DEFAULT_REGION=eu-west-1 # Ireland
{% endhighlight %}


Create the *aws01* machine with `-D` option for debugging:

{% highlight bash %}
docker-machine -D create --driver amazonec2 aws01
{% endhighlight %}

Everything is fine, if the command above completes with the message:
*"To see how to connect Docker to this machine, run: docker-machine env aws01"*
If not so, check out the troubleshooting section below.

As the new docker machine on EC2 is ready now, it's time to verfy the setup:

{% highlight bash %}
eval "$(docker-machine env aws01)" # setup DOCKER_* environment variables
docker ps                          # list running containers
docker images                      # list images
docker-machine ls                  # list docker machines
docker-machine ssh aws01           # ssh into instance aws01
{% endhighlight %}

Use the docker-machine command to interact with the newly created EC2 instance.

#### Troubleshooting

If the creation of instances via `docker create` fails:

 * Check the IAM policy: region matches / AWS ID matches?
 * Go to AWS console / Services / EC2 / Security Groups and check if the group already exists.
 * You may have to remove the *aws01* key pair if the first run of `docker-machine create` fails: Go to AWS console / Services / EC2 / Key paris.

[aws]: https://aws.amazon.com/
[ec2]: https://aws.amazon.com/ec2/
[docker-machine]: https://docs.docker.com/machine/
[docker]: https://www.docker.com/
[ec2driver]: https://docs.docker.com/machine/drivers/aws/
