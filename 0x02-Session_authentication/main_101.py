#!/usr/bin/env python3
import time
from api.v1.auth.session_exp_auth import SessionExpAuth

# Initialize the session auth with a short duration (e.g., 3 seconds for testing)
session_auth = SessionExpAuth()
session_auth.session_duration = 3  # Set session duration to 3 seconds

# Step 1: Create a session for a user
user_id = "user_123"
session_id = session_auth.create_session(user_id)
print(f"Session ID: {session_id}")

# Step 2: Immediately check if the session is valid
retrieved_user_id = session_auth.user_id_for_session_id(session_id)
print(f"User ID right after session creation: {retrieved_user_id}")

# Step 3: Wait for the session to expire (e.g., 4 seconds)
time.sleep(4)

# Step 4: Check if the session is still valid after expiration
retrieved_user_id_after_expiration = session_auth.user_id_for_session_id(
    session_id)
print(
    f"User ID after session expiration: {retrieved_user_id_after_expiration}")

# Expected output:
# Session ID: <some_session_id>
# User ID right after session creation: user_123
# User ID after session expiration: None
