import logging
import requests
import configparser
import os
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PowerBIAuthenticator:
    """Handles authentication for Power BI API."""

    def __init__(self, config_path='config.ini'):
        """
        Initialize the authenticator with configurations.
        
        :param config_path: Path to the configuration file.
        """
        self.config = configparser.ConfigParser()
        if not os.path.exists(config_path):
            logger.error(f"Configuration file not found: {config_path}")
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        self.config.read(config_path)
        logger.info(f"Loaded configuration from {config_path}")

    def get_access_token(self, connection_name='powerbi'):
        """
        Retrieve an access token using client credentials.
        
        :param connection_name: Section name in config.ini.
        :return: Access token string.
        """
        try:
            tenant_id = self.config.get(connection_name, 'tenant')
            client_id = self.config.get(connection_name, 'appid')
            client_secret = self.config.get(connection_name, 'clientsecret')
            
            url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
            
            payload = {
                'grant_type': 'client_credentials',
                'client_id': f"{client_id}@{tenant_id}",
                'client_secret': client_secret,
                'scope': 'https://analysis.windows.net/powerbi/api/.default',
                'resource': 'https://analysis.windows.net/powerbi/api'
            }
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            logger.info("Requesting access token...")
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            
            token = response.json().get('access_token')
            if not token:
                logger.error("Access token not found in response.")
                raise ValueError("Access token not found in response.")
                
            logger.info("Access token retrieved successfully.")
            return token
        except Exception as e:
            logger.error(f"Error retrieving access token: {e}")
            raise

class PowerBIManager:
    """Handles Power BI dataset operations."""

    def __init__(self, access_token):
        """
        Initialize the manager with an access token.
        
        :param access_token: Valid Power BI access token.
        """
        self.access_token = access_token
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

    def refresh_dataset(self, workspace_id, dataset_id):
        """
        Trigger a refresh for a specific dataset.
        
        :param workspace_id: ID of the workspace.
        :param dataset_id: ID of the dataset.
        :return: Response from the API.
        """
        # If workspace_id is provided, use the group endpoint, else use myorg
        if workspace_id and workspace_id.lower() != 'me':
            url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets/{dataset_id}/refreshes"
        else:
            url = f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes"
            
        logger.info(f"Triggering refresh for dataset: {dataset_id}")
        response = requests.post(url, headers=self.headers)
        
        if response.status_code == 202:
            logger.info("Refresh request accepted.")
            return True
        else:
            logger.error(f"Failed to trigger refresh: {response.status_code} - {response.text}")
            return False

    def get_refresh_status(self, workspace_id, dataset_id):
        """
        Retrieve the latest refresh status for a dataset.
        
        :param workspace_id: ID of the workspace.
        :param dataset_id: ID of the dataset.
        :return: Status string or None.
        """
        if workspace_id and workspace_id.lower() != 'me':
            url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets/{dataset_id}/refreshes?$top=1"
        else:
            url = f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes?$top=1"
            
        logger.info(f"Checking refresh status for dataset: {dataset_id}")
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            data = response.json()
            refreshes = data.get('value', [])
            if refreshes:
                status = refreshes[0].get('status')
                logger.info(f"Current status: {status}")
                return status
            else:
                logger.info("No refresh history found.")
                return "No history found"
        else:
            logger.error(f"Failed to get refresh status: {response.status_code} - {response.text}")
            return None
