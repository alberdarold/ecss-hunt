/**
 * Authentication utilities for 1sub.io integration
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://ecss-hunt.onrender.com';

export interface SessionInfo {
  authenticated: boolean;
  user_id?: string;
  tool_id?: string;
  expires_at?: string;
  message?: string;
}

export interface VerifyResponse {
  success: boolean;
  user_id: string;
  tool_id?: string;
  expires_at?: string;
  error?: string;
  message?: string;
}

/**
 * Verify a JWT token from 1sub.io and create a session
 */
export async function verifyToken(token: string): Promise<VerifyResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/auth/verify`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include', // Important for session cookies
      body: JSON.stringify({ token }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      return {
        success: false,
        user_id: '',
        error: errorData.error || 'Verification failed',
        message: errorData.message || 'Failed to verify token',
      };
    }

    const data = await response.json();
    
    // Store minimal session info in localStorage for UI state
    if (data.success) {
      localStorage.setItem('auth_user_id', data.user_id);
      localStorage.setItem('auth_tool_id', data.tool_id || '');
      localStorage.setItem('auth_expires_at', data.expires_at || '');
    }
    
    return data;
  } catch (error) {
    console.error('Token verification error:', error);
    return {
      success: false,
      user_id: '',
      error: 'network_error',
      message: error instanceof Error ? error.message : 'Network error during verification',
    };
  }
}

/**
 * Get current session information from backend
 */
export async function getSession(): Promise<SessionInfo> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/auth/session`, {
      method: 'GET',
      credentials: 'include', // Important for session cookies
    });

    if (!response.ok) {
      // Clear local storage if session check fails
      clearLocalAuth();
      return {
        authenticated: false,
        message: 'Session check failed',
      };
    }

    const data = await response.json();
    
    // Update localStorage if authenticated
    if (data.authenticated) {
      localStorage.setItem('auth_user_id', data.user_id || '');
      localStorage.setItem('auth_tool_id', data.tool_id || '');
      localStorage.setItem('auth_expires_at', data.expires_at || '');
    } else {
      clearLocalAuth();
    }
    
    return data;
  } catch (error) {
    console.error('Get session error:', error);
    clearLocalAuth();
    return {
      authenticated: false,
      message: 'Failed to check session',
    };
  }
}

/**
 * Logout and clear session
 */
export async function logout(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/auth/logout`, {
      method: 'POST',
      credentials: 'include', // Important for session cookies
    });

    // Clear local storage regardless of response
    clearLocalAuth();
    
    return response.ok;
  } catch (error) {
    console.error('Logout error:', error);
    // Still clear local storage even if request fails
    clearLocalAuth();
    return false;
  }
}

/**
 * Clear authentication data from localStorage
 */
function clearLocalAuth(): void {
  localStorage.removeItem('auth_user_id');
  localStorage.removeItem('auth_tool_id');
  localStorage.removeItem('auth_expires_at');
}

/**
 * Get authentication info from localStorage (for UI state only)
 * Note: This is not authoritative - always verify with backend
 */
export function getLocalAuthInfo(): {
  user_id: string | null;
  tool_id: string | null;
  expires_at: string | null;
  isAuthenticated: boolean;
} {
  const user_id = localStorage.getItem('auth_user_id');
  const tool_id = localStorage.getItem('auth_tool_id');
  const expires_at = localStorage.getItem('auth_expires_at');
  
  return {
    user_id,
    tool_id,
    expires_at,
    isAuthenticated: !!user_id,
  };
}

/**
 * Extract token from URL query parameters
 */
export function extractTokenFromURL(): string | null {
  if (typeof window === 'undefined') return null;
  
  const params = new URLSearchParams(window.location.search);
  return params.get('token');
}

/**
 * Clear token from URL without reloading page
 */
export function clearTokenFromURL(): void {
  if (typeof window === 'undefined') return;
  
  const url = new URL(window.location.href);
  url.searchParams.delete('token');
  window.history.replaceState({}, '', url.toString());
}

/**
 * Get tool_id from backend configuration
 */
export async function getToolId(): Promise<string> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/config/tool-id`, {
      method: 'GET',
      credentials: 'include',
    });

    if (!response.ok) {
      throw new Error('Failed to get tool ID');
    }

    const data = await response.json();
    return data.tool_id;
  } catch (error) {
    console.error('Get tool ID error:', error);
    throw error;
  }
}

/**
 * Check if user is authenticated with 1sub.io
 * Attempts to call 1sub API to verify authentication status
 */
export async function check1SubAuth(): Promise<boolean> {
  try {
    // Try to access a protected 1sub endpoint to check auth status
    // This is a lightweight check - if user has valid cookies, it will succeed
    const response = await fetch('https://1sub.vercel.app/api/user/me', {
      method: 'GET',
      credentials: 'include', // Include 1sub cookies
    });

    return response.ok;
  } catch (error) {
    console.error('1sub auth check error:', error);
    return false;
  }
}

/**
 * Create a checkout for purchasing credits/tool access
 * Calls 1sub.io API directly from frontend
 */
export async function createCheckout(toolId: string): Promise<{ checkout_id: string; checkout_url: string }> {
  try {
    const response = await fetch('https://1sub.vercel.app/api/checkout/create', {
      method: 'POST',
      credentials: 'include', // Include cookies for 1sub authentication
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ tool_id: toolId }),
    });

    if (response.ok) {
      const data = await response.json();
      const checkout_id = data.checkout_id;
      const checkout_url = `https://1sub.vercel.app/credit_checkout/${checkout_id}`;
      return {
        checkout_id,
        checkout_url,
      };
    } else if (response.status === 401) {
      // Not authenticated with 1sub - throw specific error
      const error: any = new Error('Not authenticated with 1sub.io');
      error.status = 401;
      error.needsLogin = true;
      throw error;
    } else {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || 'Failed to create checkout');
    }
  } catch (error) {
    console.error('Checkout creation error:', error);
    throw error;
  }
}

