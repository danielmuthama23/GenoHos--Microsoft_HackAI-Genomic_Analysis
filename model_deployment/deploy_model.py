from azureml.core import Workspace, Model
from azureml.core.webservice import AciWebservice
from azureml.core.model import InferenceConfig

def deploy_model(model):
    """
    Deploy the trained model using Azure Machine Learning.
    """
    ws = Workspace.from_config()
    model.register(workspace=ws, model_name="Disease_Recovery_Model")
    
    # Deploy as a web service
    inference_config = InferenceConfig(entry_script="score.py")
    deployment_config = AciWebservice.deploy_configuration(cpu_cores=1, memory_gb=1)
    
    service = Model.deploy(ws, "disease-recovery-service", [model], inference_config, deployment_config)
    service.wait_for_deployment(show_output=True)
    print(f"Service deployed at: {service.scoring_uri}")

# Example usage
deploy_model(model)