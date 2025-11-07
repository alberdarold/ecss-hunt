"""
1sub.io API Client

This module provides a client for interacting with the 1sub.io API
for user verification and credit consumption.
"""
import os
import time
import hashlib
import logging
from typing import Dict, Optional, Any
from datetime import datetime
import requests

logger = logging.getLogger(__name__)


class OneSubAPIError(Exception):
    """Custom exception for 1sub API errors."""
    pass


class OneSubClient:
    """
    Client for interacting with 1sub.io API.
    
    Handles:
    - User token verification
    - Credit consumption
    - Error handling and retries
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://1sub.vercel.app"):
        """
        Initialize the 1sub API client.
        
        Args:
            api_key: 1sub API key (defaults to ONESUB_API_KEY env var)
            base_url: Base URL for 1sub API (defaults to https://1sub.vercel.app)
        """
        self.api_key = api_key or os.getenv("ONESUB_API_KEY")
        self.base_url = base_url.rstrip("/")
        
        if not self.api_key:
            raise ValueError("ONESUB_API_KEY environment variable not set")
        
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
        })
    
    def verify_user_token(self, token: str) -> Dict[str, Any]:
        """
        Verify a JWT token from 1sub.io and get user information.
        
        Args:
            token: JWT token from 1sub.io redirect
            
        Returns:
            Dictionary containing:
            - valid: bool
            - user_id: str (UUID)
            - tool_id: str (UUID)
            - checkout_id: str (UUID)
            - expires_at: str (ISO datetime)
            
        Raises:
            OneSubAPIError: If verification fails
        """
        url = f"{self.base_url}/api/v1/verify-user"
        
        payload = {"token": token}
        
        try:
            response = self.session.post(
                url,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("valid"):
                    logger.info(f"Token verified for user: {data.get('user_id')}")
                    return data
                else:
                    raise OneSubAPIError("Token is invalid")
            
            elif response.status_code == 401:
                error_data = response.json()
                error_msg = error_data.get("message", "Token verification failed")
                logger.warning(f"Token verification failed: {error_msg}")
                raise OneSubAPIError(error_msg)
            
            elif response.status_code == 429:
                logger.warning("Rate limit exceeded for token verification")
                raise OneSubAPIError("Rate limit exceeded. Please try again later.")
            
            else:
                error_msg = f"Unexpected status code: {response.status_code}"
                logger.error(f"{error_msg}: {response.text}")
                raise OneSubAPIError(error_msg)
                
        except requests.exceptions.Timeout:
            logger.error("Timeout while verifying token")
            raise OneSubAPIError("Request timeout. Please try again.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error while verifying token: {e}")
            raise OneSubAPIError(f"Network error: {str(e)}")
    
    def consume_credits(
        self,
        user_id: str,
        amount: float,
        reason: str,
        idempotency_key: str
    ) -> Dict[str, Any]:
        """
        Consume credits from a user's account.
        
        Args:
            user_id: User UUID from verify_user_token
            amount: Amount of credits to consume (positive number)
            reason: Description of the usage (1-500 characters)
            idempotency_key: Unique key to prevent duplicate charges
            
        Returns:
            Dictionary containing:
            - success: bool
            - new_balance: float
            - transaction_id: str (UUID)
            
        Raises:
            OneSubAPIError: If consumption fails
        """
        url = f"{self.base_url}/api/v1/credits/consume"
        
        payload = {
            "user_id": user_id,
            "amount": amount,
            "reason": reason,
            "idempotency_key": idempotency_key
        }
        
        # Validate inputs
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > 1000000:
            raise ValueError("Amount exceeds maximum (1,000,000)")
        if len(reason) < 1 or len(reason) > 500:
            raise ValueError("Reason must be 1-500 characters")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        
        # Retry logic with exponential backoff
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.session.post(
                    url,
                    json=payload,
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        logger.info(
                            f"Credits consumed: {amount} for user {user_id}. "
                            f"New balance: {data.get('new_balance')}"
                        )
                        return data
                    else:
                        raise OneSubAPIError("Credit consumption failed")
                
                elif response.status_code == 400:
                    error_data = response.json()
                    error_code = error_data.get("error", "")
                    
                    if error_code == "Insufficient credits":
                        # Return this as a special case so caller can handle it
                        return {
                            "success": False,
                            "error": "insufficient_credits",
                            "message": error_data.get("message", "Insufficient credits"),
                            "current_balance": error_data.get("current_balance", 0),
                            "required": error_data.get("required", amount),
                            "shortfall": error_data.get("shortfall", 0)
                        }
                    else:
                        error_msg = error_data.get("message", "Invalid request")
                        logger.warning(f"Credit consumption failed: {error_msg}")
                        raise OneSubAPIError(error_msg)
                
                elif response.status_code == 401:
                    error_data = response.json()
                    error_msg = error_data.get("message", "Invalid API key")
                    logger.error(f"Authentication failed: {error_msg}")
                    raise OneSubAPIError("Invalid API key")
                
                elif response.status_code == 409:
                    error_data = response.json()
                    error_msg = error_data.get("message", "Duplicate request")
                    logger.warning(f"Duplicate request detected: {idempotency_key}")
                    raise OneSubAPIError("Duplicate request detected")
                
                elif response.status_code == 429:
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt  # Exponential backoff
                        logger.warning(f"Rate limited. Retrying in {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise OneSubAPIError("Rate limit exceeded. Please try again later.")
                
                elif response.status_code >= 500:
                    # Server error - retry
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt
                        logger.warning(f"Server error {response.status_code}. Retrying in {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                    else:
                        error_msg = f"Server error: {response.status_code}"
                        logger.error(f"{error_msg}: {response.text}")
                        raise OneSubAPIError(error_msg)
                
                else:
                    error_msg = f"Unexpected status code: {response.status_code}"
                    logger.error(f"{error_msg}: {response.text}")
                    raise OneSubAPIError(error_msg)
                    
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(f"Timeout. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    logger.error("Timeout while consuming credits")
                    raise OneSubAPIError("Request timeout. Please try again.")
            
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(f"Network error. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    logger.error(f"Network error while consuming credits: {e}")
                    raise OneSubAPIError(f"Network error: {str(e)}")
        
        # Should never reach here, but just in case
        raise OneSubAPIError("Failed to consume credits after retries")
    
    def generate_idempotency_key(self, user_id: str, operation: str, query: str = "") -> str:
        """
        Generate a unique idempotency key for a credit operation.
        
        Args:
            user_id: User UUID
            operation: Operation type (e.g., "search")
            query: Optional query string for additional uniqueness
            
        Returns:
            Unique idempotency key string
        """
        timestamp = int(time.time() * 1000)  # Milliseconds
        query_hash = hashlib.md5(query.encode()).hexdigest()[:8] if query else ""
        return f"{user_id}-{operation}-{timestamp}-{query_hash}"
    
    def create_checkout(self, tool_id: str) -> Dict[str, Any]:
        """
        Create a checkout for purchasing credits/tool access.
        
        Args:
            tool_id: Tool UUID from verify_user_token response
            
        Returns:
            Dictionary containing:
            - checkout_id: str (UUID)
            - checkout_url: str (full URL to checkout page)
            
        Raises:
            OneSubAPIError: If checkout creation fails
        """
        url = f"{self.base_url}/api/checkout/create"
        
        payload = {
            "tool_id": tool_id
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        
        try:
            response = self.session.post(
                url,
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                checkout_id = data.get("checkout_id")
                if checkout_id:
                    # Construct full checkout URL
                    checkout_url = f"{self.base_url}/credit_checkout/{checkout_id}"
                    logger.info(f"Checkout created: {checkout_id}")
                    return {
                        "checkout_id": checkout_id,
                        "checkout_url": checkout_url
                    }
                else:
                    raise OneSubAPIError("Invalid response: missing checkout_id")
            
            elif response.status_code == 401:
                error_data = response.json()
                error_msg = error_data.get("message", "Invalid API key")
                logger.error(f"Authentication failed: {error_msg}")
                raise OneSubAPIError("Invalid API key")
            
            elif response.status_code == 400:
                error_data = response.json()
                error_msg = error_data.get("message", "Invalid request")
                logger.warning(f"Checkout creation failed: {error_msg}")
                raise OneSubAPIError(error_msg)
            
            else:
                error_msg = f"Unexpected status code: {response.status_code}"
                logger.error(f"{error_msg}: {response.text}")
                raise OneSubAPIError(error_msg)
                
        except requests.exceptions.Timeout:
            logger.error("Timeout while creating checkout")
            raise OneSubAPIError("Request timeout. Please try again.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error while creating checkout: {e}")
            raise OneSubAPIError(f"Network error: {str(e)}")

