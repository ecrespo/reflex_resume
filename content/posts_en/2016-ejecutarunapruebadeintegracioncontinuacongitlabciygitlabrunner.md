Title: Running a continuous integration test with gitlab-ci and gitlab-runner. 
Date: 2016-06-16 09:00 
Category: Tutorial de integración continua
Tags: CI/CD,Gitlab-ci, Gitlab-runner,Docker
lang: en  
translation: true  


In previous articles I explained how to use [gitlab-ce (broken link)](/blog/instalargitlabpormediodedocker) and [gitlab-runner (broken link)](/blog/instalargitlabrunnerdegitlabcipormediodedocker) through containers and connect them for continuous integration.

For docker to work through gitlab-runner you need to modify the runner's configuration, adding the name and the ip of the machine as shown below (file `/etc/gitlab-runner/config.toml`):
```
concurrent = 1

[[runners]]
  name = "Sample gitlab-ci cpp project"
  url = "http://12.168.0.60:9080t/ci"
  token = "5faac16d0aaf8f97fd66f5f586ed9f5f"
  executor = "docker"
  [runners.docker]
    tls_verify = false
    image = "debian"
    privileged = false
    disable_cache = false
    volumes = ["/cache"]
    extra_hosts = ["culata.dst:192.168.0.60"]
  [runners.cache]
    Insecure = false

```

After modifying the file, run:
```
gitlab-runner restart
```
In the runner article a project called `sample-gitlabci-cpp-project` is registered, taken from [github](https://github.com/olindata/sample-gitlabci-cpp-project).

It contains the following:
```
sample-gitlabci-cpp-project
├── helloworld.cpp
├── README.md
└── verify.sh
```

The `helloworld.cpp` file has the following:
```
// 'Hello World!' program 
 
#include <iostream>
 
int main()
{
  std::cout << "Hello World!" << std::endl;
  return 0;
}

```
The `verify.sh` file is the one that drives the build:
```
#!/bin/bash

echo "Starting sample CI verification script"

echo "Trying to execute ./helloworld"

OUTPUT=`./helloworld`
RETVAL=$?

if [ $RETVAL -eq 0 ]; then
  echo "Retval is 0, OK"
else
  echo "Retval is not 0, FAIL"
  exit 1
fi

if [ "$OUTPUT" == "Hello World!" ]; then
  echo "Output is correct, OK"
else
  echo "Output is not right, FAIL"
  exit 1
fi
```

There is another hidden file named `.gitlab-ci.yml`, which contains the docker container build process with the execution of `verify.sh`:
```
# Specify the docker image to use (only used if using docker runners)
# See: http://doc.gitlab.com/ee/ci/docker/using_docker_images.html
image: debian      

# Define commands that run before each job's script
before_script:
  - apt-get update
  - apt-get install -y gcc g++

# Try to compile our sample hello world app
compile:
  script:
  # Compile our app
  - g++ helloworld.cpp -o helloworld
  # Verify that our compiled app works properly with a custom "test" script
  - ./verify.sh
  # Save the compiled output from the above for downloading via GitLab and in Gitlab 8.6 to use in future build steps
  artifacts:
    paths:
    - helloworld
```

Now all that is left is to go to the build section of the project and run a build; the following figure shows the build running:

![](./images/ejecutarunapruebadeintegracioncontinuacongitlabciygitlabrunner-1.png)

As the figure shows, the build went through without problems.

In upcoming articles its use with node.js and Django will be shown.

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
