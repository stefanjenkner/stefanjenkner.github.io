---
layout: post
title:  "Automated builds for ARM Docker containers on Intel hosts"
date:   2016-04-11 23:11:01
categories: docker arm qemu build-automation arm travis-ci integration
---

In order to enable automated builds for ARM [Docker][docker] containers on Intel
hosts, the Docker images must contain the `qemu-arm-static` binary.
For that reason, the base image `sedden/rpi-raspbian-qemu` exists:

*   <https://github.com/sedden/docker-rpi-raspbian-qemu>
*   <https://hub.docker.com/r/sedden/rpi-raspbian-qemu/>

### Enable automated builds for ARM containers on Travis CI

Automated builds can easily be enabled on [Travis CI][travis-ci].
[binfmt-support](http://www.nongnu.org/binfmt-support/) is used to register
ARM binaries to be executed by `/usr/bin/qemu-arm-static`.

The `.travis.yml` must contain this part:

    before_script:
      - sudo apt-get --yes --no-install-recommends install binfmt-support qemu-user-static
      - echo ':arm:M::\x7fELF\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x28\x00:\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff\xff:/usr/bin/qemu-arm-static:' | sudo tee -a /proc/sys/fs/binfmt_misc/register

[docker]: https://www.docker.com/
[travis-ci]: https://www.travis-ci.org/
