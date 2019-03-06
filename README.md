# Python API

A Python API to access Google forms
and process their results for Enactive Robot Assisted Didactics (ERAD) research project.

## Basic setup for a non-tech person

### Git gut
This repository is better to be used with basic git commands. There are some tools that can make the experience more user friendly, but you can also just use git. There are many tutorials around the net, but here just to get you started:
* [Cheatsheet with main commands](https://devhints.io/git-branch)
* [Interactive tutorial](https://learngitbranching.js.org/)

In order to **setup** the repository in the desired location, just use:
```
git clone git@github.com:svarnypetr/pepper_google_form.git
```

Then it is best to follow this **workflow** in the repository:
1. Check the state of the repository to make sure you are on the right branch:

`git status`

2. Make your own branch on which you will do development:
`git checkout -b 'branch_name'`

3. Do your work in the feature branch and commit atomic changes.

  * If you work atomically on simple changes, you can commit all by one command:
  `git commit -am 'description of the new feature added'`

  * If you have changed multiple files, you need to add just the files relevant to the current commit and then commit:
  `git add FILES`
  `git commit -m 'description of the new feature added'`
  
4. Once in a while push your changes to the remote repository so that you have them also on here:
`git push`

5. If you have your main feature that the branch was intended for finished, then prepare the branch for merging into master. That means you need to be up-to-date with the master and then pushing to it:
`git checkout master`
`git pull`
`git checkout 'branch_name'`
`git rebase master`
`git push -f`

6. There might be some merge conflicts, these have to be resolved in the files that are indicated as merge conflicts.
 You will see there marks for the conflicting parts of the file.

### Python virtualenv
It is good practice to use *virtual environments* for Python development as it allows to keep packages separate from the host system Python. 
I am using `virtualenv` as the environment here, but there are also others.

**Basic Virtualenv**
* in folder of project - create a new virtualenv named env using python 
at given path: `virtualenv --python=/path/to/python/bin env`
* activate the virtualenv: `source venv/bin/activate`
* install requirements: `pip install -r requirements`
* deactivate the virtualenv once inside: `deactivate`

**How to SCP to Pepper**
In order to upload the image to Pepper, we can use `scp`. Example guide is [here](http://www.hypexr.org/linux_scp_help.php).
* `scp image.png your_username@PEPPER_IP:/home/nao/.local/share/PackageManager/apps/connectgoogleforms-00573d/html/image.jpg`


### Prelaunch Checklist

* [ ] Are the Ports the same on the server and in the Python box?
* [ ] Is the IP address on the Python box correct, i.e. address of the server PC?