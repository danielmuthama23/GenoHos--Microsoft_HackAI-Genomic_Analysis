### AI-Powered Genomic Analysis with Molecular Phenotyping and RAG Chat Interface

#### Overview
This project is an AI-powered platform for analyzing genomic data with proteomic, and metabolomic properties to predict disease recovery and provide personalized treatment recommendations. It leverages Microsoft Fabric for data orchestration, Azure AI Search for retrieval, and Azure OpenAI for natural language generation. It will also summarize findings from genomic data analysis, focusing on detecting disease associations through mutation patterns in breast cancer samples.

### Project Flow


	Data Ingestion: Load genomic, proteomic, and metabolomic data into OneLake.

	Data Preprocessing: Clean, normalize, and transform data using Synapse Data Engineering.

	Model Training: Train AI models (e.g., Random Forest) to predict disease recovery.

	Molecular Phenotyping: Identify biomarkers for disease recovery.

	RAG Chat Interface: Allow users to query the system and retrieve insights.

	Visualization: Create interactive dashboards using Power BI.

### Project Structure

	GenomicAnalysisWorkspace/
	│
	├── BioEventHouse/                     # Eventhouse and KQL Database for genomic events
	│   ├── (Eventhouse data)
	│   └── (KQL Database)
	│
	├── BioEventHouse_queryset/            # KQL Queryset for querying genomic events
	│
	├── Biospecimen_RAG_System/            # Notebook for biospecimen RAG (Retrieval-Augmented Generation) system
	│
	├── Biospecimen_Report_Generator/      # Notebook for generating biospecimen reports
	│
	├── BiospecimenClassifier/             # Machine learning model for biospecimen classification
	│
	├── Data_Engineering/                  # Notebook for data engineering tasks
	│
	├── Genomel_H/                         # Lakehouse for genomic data
	│   ├── (Lakehouse data)
	│   ├── Semantic model
	│   └── SQL analytics endpoint
	│
	├── GenomicAnalysisPipeline/           # Notebook and experiment for genomic analysis
	│   ├── (Notebook)
	│   └── (Experiment)
	│
	├── GenomicDataProcessing/             # Notebook for genomic data processing
	│
	└── model_deployment/                  # Notebook and experiment for model deployment
	    ├── (Notebook)
	    └── (Experiment)


## Key Components

### Data Storage
- **BioEventHouse**: Eventhouse and KQL Database for genomic event data  
- **Genomel_H**: Lakehouse for genomic data with semantic model and SQL analytics  

### Analysis Tools
- Multiple Jupyter notebooks for various genomic analysis tasks  
- Experiments tracking for machine learning workflows  

### Machine Learning
- **BiospecimenClassifier**: ML model for biospecimen classification  
- Model deployment experiments  

### Reporting
- **Biospecimen_RAG_System**: Retrieval-Augmented Generation system  
- **Biospecimen_Report_Generator**: Automated report generation  

### Setup Instructions

#### 1. Prerequisites
- **Azure Account**: Access to Microsoft Fabric, Azure AI Search, and Azure OpenAI.
- **Python 3.8+**: Install Python and required libraries.
- **Power BI Desktop**: For creating visualizations.
- **Microsoft Fabric Workspace**: With contributor permissions.
- **Genomic Datasets**: Access to required genomic data sources.

#### 2. Install Dependencies
Install the required Python libraries:

### 3. Configure Azure Resources
#### Microsoft Fabric:

Create a Fabric workspace and set up OneLake.

#### Azure AI Search:

Create an index for storing research papers and genomic data.

#### Azure OpenAI:

Set up an OpenAI resource and deploy a GPT-4 model.

### 4. Update Configuration
Replace placeholders (e.g., <api_key>, <connection_string>) in the code with your Azure resource details.

### Visualization
Use Power BI to create interactive dashboards for visualizing:

Molecular phenotyping profiles.

Top biomarkers for disease recovery.

Trends in gene expression.

### Contributing
Contributions are welcome! Please follow these steps:

### Fork the repository.

**Repository:** [https://github.com/danielmuthama23/Genomic_Analysis.git](#)  


# SUMMARY

## 1. Genomic Analysis Report: Mutation-Disease Association Detection
This report summarizes findings from genomic data analysis, focusing on detecting disease associations through mutation patterns in breast cancer samples.  

**Analysis Methods:**  
- Mutation frequency analysis of key cancer genes  
- Protein-protein interaction networks to identify functional clusters  
- Metabolic pathway mapping to detect dysregulated processes  

**Key Datasets:**  
- `PDC_biospecimen_manifest_03272025_214257.csv`  
- Embedded mock genomic data for test and validation  

---

## 2. Key Findings  

### 2.1 Mutation-Disease Associations  
![Mutation Counts](mutation_disease_counts.png)  

**Top Pathogenic Mutations:**  
| Gene    | Mutation Count | Disease-Associated | Percentage |  
|---------|---------------|--------------------|------------|  
| TP53    | 8             | 8                  | 100%       |  
| PIK3CA  | 5             | 5                  | 100%       |  
| BRCA1   | 4             | 4                  | 100%       |  

**Insights:**  
- **TP53 mutations** were ubiquitous (100% disease-linked), indicating its role as a primary driver.  
- **PIK3CA** and **BRCA1/2** mutations showed strong disease associations.  

---

### 2.2 Protein Interaction Network  
![Protein Network](protein_network.png)  

**Critical Hubs (High Connectivity):**  
1. **TP53** (4 interactions)  
2. **BRCA1** (3 interactions)  
3. **PIK3CA** (3 interactions)  

**Key Observations:**  
- Red nodes (PDC-identified proteins) formed central hubs.  
- Green edges (activation) dominated oncogenic pathways (e.g., PIK3CA→AKT1).  

---

### 2.3 Metabolic Pathway Dysregulation  
![Metabolic Pathways](metabolic_pathways.png)  

**Most Dysregulated Pathways:**  
1. **Glycolysis** (↑ Glucose-6-P, Fructose-1,6-BP)  
2. **TCA Cycle** (↓ Succinyl-CoA, ↑ Acetyl-CoA)  
3. **Fatty Acid Synthesis** (↑ Malonyl-CoA)  

**Top Dysregulated Metabolite:**  
- **Acetyl-CoA** (2.1-fold change, linked to PTEN mutations).  

---

## 3. Disease Detection Methodology  

### 3.1 Mutation-Based Detection  
- **Thresholds:** Genes with >70% disease-associated mutations flagged as high-risk.  
- **Validation:** Cross-referenced with COSMIC database.  

### 3.2 Network Analysis  
- Prioritized **hub genes** (e.g., TP53) as biomarkers.  
- **Inhibition edges** (red) highlighted drug targets (e.g., PTEN→AKT1).  

### 3.3 Metabolic Insights  
- Glycolysis/TCA cycle disruptions correlated with TP53/PIK3CA mutations.  
- High Acetyl-CoA suggests vulnerability to metabolic inhibitors.  

---

## 4. Conclusions & Recommendations  
  From the analysis we conclude:-

**Diagnostic Markers:**  
- **TP53 mutations** as universal biomarkers.  
- **PIK3CA activation** signals aggressive subtypes.  

**Therapeutic Targets:**  
- Target **PIK3CA-AKT1 interactions**.  
- Explore **metabolic inhibitors** for Acetyl-CoA-overproducing tumors.  

**Future Works:**  
- Validate with clinical outcomes data.  
- Expand analysis to RNA-seq.  

---

## 5. Files Generated  

| File                          | Description                                  |  
|-------------------------------|----------------------------------------------|  
| `mutation_disease_counts.png` | Top mutated genes with disease associations. |  
| `protein_network.png`         | Protein interaction network with PDC hubs.   |  
| `metabolic_pathways.png`      | Dysregulated metabolic pathways.             |  


---

**Prepared by:** Daniel Muthama 
**Date:** April 2, 2025  

---

### How to Use This Report  
- **Clinicians:** Focus on TP53/PIK3CA status for patient stratification.  
- **Researchers:** Explore metabolic pathways for novel drug combinations.  
- **Data Teams:** Replicate pipeline using `DataEngineering.tex`.  

**Contact:** (mailto:danielmuthama23@gmail.com)  

### License
This project is licensed under the MIT License. See the LICENSE file for details.

### Contact
For questions or feedback, please contact:

#### Acknowledgments
Microsoft Fabric for data orchestration.

Azure AI Search for retrieval.

Azure OpenAI for natural language generation.