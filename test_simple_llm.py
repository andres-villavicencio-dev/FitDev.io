#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple LLM mock test for FitDev.io
"""

import os
import sys
import logging
from unittest.mock import patch, MagicMock

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import from fitdev
from fitdev.utils.llm_integration import OpenAIProvider, OllamaProvider
from fitdev.agents.development.frontend import FrontendDeveloperAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_with_mocked_llm():
    """Test the LLM integration with a mocked provider."""
    logger.info("Testing with mocked LLM provider...")
    
    # Create a mock for the LLM provider
    mock_llm = MagicMock()
    mock_llm.generate_text.return_value = """
{
    "component": {
        "code": "import React, { useState } from 'react';\\n\\nexport const UserProfile = ({ user }) => {\\n  const [isEditing, setIsEditing] = useState(false);\\n  const [userData, setUserData] = useState(user);\\n\\n  const handleEdit = () => {\\n    setIsEditing(true);\\n  };\\n\\n  const handleSave = () => {\\n    setIsEditing(false);\\n    // Call API to save user data\\n  };\\n\\n  return (\\n    <div className=\\"user-profile\\">\\n      <div className=\\"profile-header\\">\\n        <img src={userData.avatar || 'default-avatar.png'} alt=\\"User avatar\\" />\\n        <h2>{userData.name}</h2>\\n      </div>\\n      <div className=\\"profile-content\\">\\n        {isEditing ? (\\n          <>\\n            <input\\n              value={userData.name}\\n              onChange={(e) => setUserData({...userData, name: e.target.value})}\\n            />\\n            <button onClick={handleSave}>Save</button>\\n          </>\\n        ) : (\\n          <>\\n            <p>Email: {userData.email}</p>\\n            <p>Role: {userData.role}</p>\\n            <button onClick={handleEdit}>Edit Profile</button>\\n          </>\\n        )}\\n      </div>\\n    </div>\\n  );\\n};",
        "framework": "React",
        "component_type": "profile",
        "test_coverage": true,
        "responsive": true
    }
}
"""
    
    # Enable LLM
    os.environ["ENABLE_LLM"] = "true"
    os.environ["ENABLE_BROWSER"] = "false"
    
    # Create a frontend developer agent
    frontend_dev = FrontendDeveloperAgent()
    
    # Override the execute_task_with_llm method to use our mock
    frontend_dev.execute_task_with_llm = mock_llm.generate_task_response
    mock_llm.generate_task_response.return_value = {
        "status": "completed",
        "agent": frontend_dev.name,
        "component": {
            "code": "import React, { useState } from 'react';\n\nexport const UserProfile = ({ user }) => {\n  const [isEditing, setIsEditing] = useState(false);\n  const [userData, setUserData] = useState(user);\n\n  const handleEdit = () => {\n    setIsEditing(true);\n  };\n\n  const handleSave = () => {\n    setIsEditing(false);\n    // Call API to save user data\n  };\n\n  return (\n    <div className=\"user-profile\">\n      <div className=\"profile-header\">\n        <img src={userData.avatar || 'default-avatar.png'} alt=\"User avatar\" />\n        <h2>{userData.name}</h2>\n      </div>\n      <div className=\"profile-content\">\n        {isEditing ? (\n          <>\n            <input\n              value={userData.name}\n              onChange={(e) => setUserData({...userData, name: e.target.value})}\n            />\n            <button onClick={handleSave}>Save</button>\n          </>\n        ) : (\n          <>\n            <p>Email: {userData.email}</p>\n            <p>Role: {userData.role}</p>\n            <button onClick={handleEdit}>Edit Profile</button>\n          </>\n        )}\n      </div>\n    </div>\n  );\n};",
            "framework": "React",
            "component_type": "profile",
            "test_coverage": True,
            "responsive": True
        }
    }
    
    # Create a task
    task = {
        "id": "task-123",
        "title": "Create User Profile Component",
        "description": "Implement a responsive user profile component with avatar, user details, and edit functionality",
        "type": "component_implementation",
        "component_type": "profile",
        "framework": "React"
    }
    
    # Execute the task
    logger.info(f"Executing task: {task['title']}...")
    
    try:
        result = frontend_dev.execute_task(task)
        logger.info(f"Task execution result status: {result.get('status', 'unknown')}")
        
        # Check if component was generated
        if "component" in result:
            component = result["component"]
            code = component.get("code", "")
            logger.info(f"Generated component code length: {len(code)} characters")
            
            # Show a snippet of the code
            if code:
                logger.info(f"Code snippet: {code[:100]}...")
                
        logger.info("Mock LLM test completed successfully")
    except Exception as e:
        logger.error(f"Error executing task: {str(e)}")
        raise

if __name__ == "__main__":
    logger.info("Starting simple LLM test with mocking")
    test_with_mocked_llm()
    logger.info("Test completed")