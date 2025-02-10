import logging
from datetime import datetime

# Configure logging to write audit logs to 'audit.log'
logging.basicConfig(filename="audit.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

def log_audit(request):
    """
    Log key details of incoming requests for auditing purposes.
    """
    ip = request.remote_addr
    endpoint = request.path
    method = request.method
    user_agent = request.headers.get("User-Agent")
    logging.info(f"Request from {ip} - {method} {endpoint} - User-Agent: {user_agent}")
