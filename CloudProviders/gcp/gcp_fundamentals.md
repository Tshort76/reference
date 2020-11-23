<div align="center">**GCP**</div>
===

<img src="./images/infrastructure_domains.png" alt="GCP" width="75%">

# Overview
### GCP Resource organization
Organizations and Folders only exist within a GSuite account.

<img src="./images/GCP_resource_org.jpeg" alt="GCP" width="50%">


# Compute 
<dl>
  <dt>Google App Engine</dt>
  <dd>*Serverless*, container-based compute platform (~ AWS Fargate)</dd>
  <dt>Google Compute Engine</dt>
  <dd>VM-based compute (~ AWS EC2)</dd>
  <dt>Google Kubernetes Engine</dt>
  <dd>Managed Kubernetes cluster (~ AWS EKS)</dd>
  <dt>Google Cloud Functions</dt>
  <dd>Serverless execution environment (~ AWS Lambda)</dd>
</dl>

# Storage 
<dl>
  <dt>Google Cloud Storage</dt>
  <dd>Basic object store (~ AWS S3), with different storage classes depending on required access frequency</dd>
  <dt>Persistent Disk</dt>
  <dd>Block storage for VMs (~ AWS EBS).  This offering is unique in allowing multiple reader access to a single disk</dd>
  <dt>Google Cloud Filestore</dt>
  <dd>Managed NFS file system (~ AWS EFS) that allows legacy (file system based) software to run in the cloud</dd>
</dl>



# Sources
1. <a name="src1">[Official GCP Documentation](https://cloud.google.com/docs)</a>
2. <a name="src2">[Udemy Google Cloud Platform (GCP) Fundamentals for Beginners](https://www.udemy.com/course/google-cloud-platform-gcp-fundamentals-for-beginners/)</a>
3. <a name="src3">[Cloud Comparison chart](http://comparecloud.in/)</a>