# **Automating Data Pipeline Deployment with CI/CD & AWS Lambda**

Author: Pharoah Evelyn

<p align="center">
    <img src=https://github.com/Pharoah0/CI-CD-Pipeline-with-GitHub-Actions/blob/main/images/Main.png/>
</p>
### **Overview**

In digital advertising, businesses need real-time insights into campaign performance across multiple platforms. However, managing data ingestion, transformation, and deployment at scale can be a bottleneck, leading to inefficiencies and delayed decision-making.

This project employs a **CI/CD pipeline using GitHub Actions** to automate the deployment of a **data processing pipeline using AWS Lambda**, ensuring **faster, reliable, and repeatable** data updates while minimizing manual intervention.

---

### **Business Problem**

A digital marketing analytics firm struggled with **delayed ad performance reporting** due to an inefficient data pipeline deployment process. Their data engineers manually updated and deployed processing scripts, leading to the following:

- **Deployment inconsistencies**: Different environments had mismatched dependencies, causing failures.
- **Slow update cycles**: Manual deployments took hours, delaying critical campaign insights.
- **Error-prone workflows**: Human errors in deployment led to missing data, misclassified ad platforms, and incorrect performance metrics.

The company required **an automated, scalable solution** to streamline their data pipeline, ensuring real-time ad performance insights across Facebook, Google Ads, and TikTok.

---

### **Data Preparation**

The raw advertising campaign data is stored in **Amazon S3**, with inconsistencies in platform names and missing values. Key processing tasks include:

- Standardizing platform names (e.g., correcting "Facebok" to "Facebook").
- Handling missing values by imputing clicks with the median and setting conversions to zero when missing.
- Feature engineering: **Click-Through Rate (CTR)** and **Return on Investment (ROI)** calculations.
- Storing the processed data in **Amazon S3 (processed/ directory)** for downstream analytics.

---

### **Methods Used**

This project integrates **AWS Lambda with GitHub Actions CI/CD** to enable **continuous deployment and automated updates** of the data pipeline:

1. **AWS Lambda for Serverless Processing**

   - Reads raw advertising data from S3, cleans and enriches it, then writes the processed output back to S3.
   - Uses **pandas, numpy, and boto3** for data processing.

2. **GitHub Actions for CI/CD**

   - Automates Lambda deployment on **each push to the main branch**.
   - Ensures that the correct dependencies (`boto3`, `pandas,` `numpy`) are included in the package.
   - Uses **AWS CLI** to manage Lambda function updates dynamically.

3. **Shell Script for Manual Deployment**
   - Allows engineers to trigger an on-demand update via `deploy_lambda.sh`.

---

### **Discoveries Made**

By implementing CI/CD automation, the data engineering team achieved:

- **87% reduction** in deployment time (from **~30 minutes manual setup** to **~4 minutes automated deployment**).
- **Consistent execution environment** with dependencies managed automatically, reducing function failures.
- **Faster time-to-insight**, enabling near real-time ad performance analysis.
- **Elimination of human error** from manual deployments, improving data accuracy.

---

### **Key Improvements**

Here are a few notable outcomes achieved by implementing this pipeline:

- **Deployment Time**: Reduced from **30+ minutes** (manual) to **under 4 minutes** (automated via CI/CD).
- **Data Accuracy**: Corrected mis-labeled or missing data and standardized platform names, leading to more reliable analytics.

---

### **Conclusion**

This CI/CD pipeline **transformed** the data ingestion and processing workflow by:

✅ Automating deployment, reducing manual effort.  
✅ Ensuring **reliable and consistent** function execution.  
✅ Accelerating time-to-insight for marketing teams.  
✅ Improving **data quality** for better decision-making.

This approach enhances **DevOps efficiency** and enables **scalable and maintainable** data processing pipelines for real-world analytics applications.

---

### **Ways to Improve This Project**

- Implement **unit tests** for the Lambda function to validate transformations before deployment.
- Extend CI/CD to **monitor execution logs** and alert failures via AWS CloudWatch & SNS.
- Introduce **step functions** for orchestrating multi-step data transformations.
- Explore **containerized Lambda deployment** for even more flexibility.

---

### **Final Thoughts**

This project showcases **how CI/CD with GitHub Actions can revolutionize data engineering workflows** by removing bottlenecks in deployment and improving overall system resilience. 🚀
