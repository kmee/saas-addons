===========================
Saas Operator Remote Deploy
===========================

Automate remote operator deployment with Gitlab and Rancher Fleet Stack

Configuration
=============

To configure this module, you need to:

#. Go to the SaaS module settings and fill in all configuration parameters in the 'Operator Remote Deployment' section.

 - GitLab URL: GitLab instance URL
 - GitLab Private Token: Private token for GitLab access
 - GitLab Deplyment Repo: Namespace e reposítorio de deployment do Fleet. i.e: namespace/reponame
 - Deployment Repo Branch: Branch of the repository where the changes will be committed
 - Deployment Folder Prefix: Folder name prefix in repo for new operator
 - Deployment Committer Name: Change commit author name
 - Deployment Committer E-mail: Change commit author e-mail

Usage
=====

To use this module, you need to:

#. Go to the form view of a remote type versioned operator that has not yet been implemented.
#. Click the "Deploy Operator" button.


Changelog
=========
