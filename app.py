import argparse
import time
import sys
import logging
from assembly import PowerBIAuthenticator, PowerBIManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def monitor_refresh(workspace_id, dataset_id):
    """
    Triggers refresh and polls for status until success or failure.
    
    :param workspace_id: ID of the workspace.
    :param dataset_id: ID of the dataset.
    """
    try:
        # 1. Authentication
        auth = PowerBIAuthenticator()
        token = auth.get_access_token()
        
        # 2. Trigger Refresh
        pbi = PowerBIManager(token)
        success = pbi.refresh_dataset(workspace_id, dataset_id)
        
        if not success:
            logger.error("Failed to trigger refresh. Exiting.")
            sys.exit(1)
            
        # 3. Poll Status
        logger.info("Starting status polling every 30 seconds...")
        while True:
            status = pbi.get_refresh_status(workspace_id, dataset_id)
            
            if status == "Completed":
                logger.info("Refresh completed successfully!")
                break
            elif status == "Failed":
                logger.error("Refresh failed!")
                sys.exit(1)
            elif status == "No history found":
                logger.warning("No Refresh history found.")
                sys.exit(1)
            elif status == "Unknown":
                logger.warning("Refresh in Progress, continuing to get updates...")
            
            time.sleep(30)
            
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Power BI Dataset Refresh Utility')
    parser.add_argument('workspace_id', help='The ID of the Power BI Workspace')
    parser.add_argument('dataset_id', help='The ID of the Power BI Dataset')
    
    args = parser.parse_args()
    
    monitor_refresh(args.workspace_id, args.dataset_id)